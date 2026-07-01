#!/usr/bin/env python3
"""
ICT Co-pilot — Real-time NQ trading analysis
Reads live TradingView chart data, applies Zion's ICT framework via Claude API,
and outputs a structured trade call with feedback loop.

Usage:
    python3 ict_copilot.py                          # Analyze current chart
    python3 ict_copilot.py feedback <id> correct    # Mark call correct
    python3 ict_copilot.py feedback <id> incorrect "missed the ERL sweep"
"""

import subprocess
import json
import os
import sys
import time
import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
from dotenv import load_dotenv
import anthropic
import uw_data
import db

# ── Paths (self-locating, per the Reorg Plan convention) ──────────────────────
SCRIPT_DIR = Path(__file__).resolve().parent


def _find_project_root(start: Path) -> Path:
    """Walk up from `start` until a directory containing `02 Playbook` is found.

    That directory is the TD Trades project root. Falls back to the
    TD_TRADES_ROOT env var, then errors clearly. This keeps every vault file
    reference relocatable instead of hardcoding `SCRIPT_DIR.parent` (which only
    worked when the script lived directly in `03 System/`).
    """
    for candidate in (start, *start.parents):
        if (candidate / "02 Playbook").is_dir():
            return candidate
    env_root = os.environ.get("TD_TRADES_ROOT")
    if env_root and (Path(env_root) / "02 Playbook").is_dir():
        return Path(env_root)
    raise RuntimeError(
        "Could not locate the TD Trades project root.\n"
        f"  Walked up from: {start}\n"
        "  No ancestor directory contains a '02 Playbook' folder.\n"
        "  Set TD_TRADES_ROOT to the project root "
        "(the folder that contains '02 Playbook')."
    )


PROJECT_ROOT = _find_project_root(SCRIPT_DIR)          # TD Trades root
PLAYBOOK_DIR = PROJECT_ROOT                            # back-compat alias
FEEDBACK_LOG = SCRIPT_DIR / "feedback.jsonl"
TV_CLI       = Path.home() / ".npm-global" / "bin" / "tv"

# ── Load env ──────────────────────────────────────────────────────────────────
load_dotenv(SCRIPT_DIR / ".env")
API_KEY = os.environ.get("ANTHROPIC_API_KEY")



# ── Session context ───────────────────────────────────────────────────────────

ET = ZoneInfo("America/New_York")

MACRO_WINDOWS = [
    (9*60+50,  10*60+10, "09:50–10:10 ET (Silver Bullet — most important)"),
    (10*60+50, 11*60+10, "10:50–11:10 ET"),
    (11*60+50, 12*60+10, "11:50–12:10 ET (lunch macro)"),
    (13*60+10, 13*60+50, "13:10–13:50 ET"),
    (14*60+50, 15*60+10, "14:50–15:10 ET"),
    (15*60+15, 15*60+45, "15:15–15:45 ET"),
]


def get_session_context():
    """Return current ET time, session phase, and active macro window."""
    now    = datetime.datetime.now(ET)
    mins   = now.hour * 60 + now.minute

    if mins < 9*60+30:
        phase     = "Pre-market — NY session has NOT opened. DO NOT TRADE."
        tradeable = False
    elif mins < 10*60:
        phase     = "NY Open (09:30–10:00 ET) — first 30 min, elevated volatility"
        tradeable = True
    elif mins < 12*60:
        phase     = "NY AM session (10:00–12:00 ET) — prime trading window"
        tradeable = True
    elif mins < 13*60+30:
        phase     = "Lunch (12:00–13:30 ET) — low liquidity, high noise, avoid"
        tradeable = False
    elif mins < 16*60:
        phase     = "NY PM session (13:30–16:00 ET) — tradeable"
        tradeable = True
    else:
        phase     = "After hours — NY session CLOSED. DO NOT TRADE."
        tradeable = False

    active_macro = next(
        (label for start, end, label in MACRO_WINDOWS if start <= mins <= end),
        None,
    )

    # Next upcoming macro window
    next_macro = next(
        (label for start, end, label in MACRO_WINDOWS if start > mins),
        None,
    )

    return {
        "current_time":        now.strftime("%Y-%m-%d %H:%M ET (%A)"),
        "session_phase":       phase,
        "tradeable":           tradeable,
        "active_macro_window": active_macro or "none — between windows",
        "next_macro_window":   next_macro   or "none remaining today",
    }


# ── TradingView helpers ───────────────────────────────────────────────────────

# Timeframes read on every analysis, in order. Format: (label, tv_code, bar_count, purpose)
ANALYSIS_TIMEFRAMES = [
    ("4H",  "240", 90,  "4H — HTF bias CONTEXT & draw frame (the anchor; daily read retired per D18)"),
    ("1H",  "60",  120, "1H — intermediate structure, order-flow phase, MSS"),
    ("15m", "15",  120, "15m — faster MSS confirmer + IRL (nearest unmitigated FVG)"),
    ("5m",  "5",   120, "5m — model confirmation, ERL sweep, neckline, FVG entry"),
    ("1m",  "1",   100, "1m — execution precision, flip candle, MSS confirmation"),
]


def tv(*args, timeout=30):
    """Run a tv CLI command and return parsed JSON output."""
    result = subprocess.run(
        [str(TV_CLI)] + list(args),
        capture_output=True, text=True, timeout=timeout
    )
    if result.returncode != 0:
        raise RuntimeError(f"tv {' '.join(args)} failed: {result.stderr.strip()}")
    return json.loads(result.stdout)


def get_market_data(status_callback=None):
    """Fetch status, quote, and OHLCV bars across 4 timeframes (auto-switches chart)."""
    status = tv("status")
    if not status.get("success"):
        raise RuntimeError(
            "TradingView not connected.\n"
            "Launch with: /Applications/TradingView.app/Contents/MacOS/TradingView --remote-debugging-port=9222"
        )

    quote       = tv("quote")
    original_tf = status.get("chart_resolution", "5")
    ohlcv       = {}

    for label, tf_code, bar_count, purpose in ANALYSIS_TIMEFRAMES:
        if status_callback:
            status_callback(f"Reading {label}…")
        try:
            tv("timeframe", tf_code)
            time.sleep(0.8)                              # wait for chart to load
            bars = tv("ohlcv", "-n", str(bar_count))
            ohlcv[label] = {"purpose": purpose, "bars": bars}
        except Exception as e:
            ohlcv[label] = {"purpose": purpose, "error": str(e)}

    # Restore the user's original timeframe
    try:
        tv("timeframe", original_tf)
    except Exception:
        pass

    return {"status": status, "quote": quote, "ohlcv": ohlcv}


# ── Playbook loader ───────────────────────────────────────────────────────────

def load_playbook():
    """Load the current canonical playbook (D13 2-model spine).

    Order:
      1. All 6 docs in `02 Playbook/` (00–05), sorted by filename.
      2. `01 Refinement/(C) Knowledge_Graph_Master.md` (master framework).
      3. `07 Outputs/(C) Concept Confluence Map (2026-06-10).md` (reasoning layer).

    The retired `(C) Model_Selection_Decision_Tree.md` is NO LONGER loaded
    (partially superseded by the 2-model spine — Decisions Log D13).
    Returns a list of (label, text) sections in load order so prompt caching
    sees a stable concatenation.
    """
    sections = []

    # 1. The 6 numbered playbook docs (00–05), globbed + sorted so a renamed or
    #    re-ordered file is picked up automatically. Filenames use em-dashes (—).
    playbook_dir = PROJECT_ROOT / "02 Playbook"
    for path in sorted(playbook_dir.glob("*.md")):
        sections.append((f"Playbook — {path.stem}", path.read_text()))

    # 2. Knowledge Graph master framework.
    kg = PROJECT_ROOT / "01 Refinement" / "(C) Knowledge_Graph_Master.md"
    if kg.exists():
        sections.append(("Knowledge Graph (Master Framework)", kg.read_text()))

    # 3. Concept Confluence Map (concept → gate → lens/UW confluence).
    ccm = PROJECT_ROOT / "07 Outputs" / "(C) Concept Confluence Map (2026-06-10).md"
    if ccm.exists():
        sections.append(("Concept Confluence Map", ccm.read_text()))

    return sections


# ── Gate 0 — deterministic bias (read the validated classifier's bias_state.json) ──

def gate0_context_block(symbol):
    """Read the Live Engine's deterministic Gate-0 bias for `symbol` and format it
    as context so Claude reconciles its discretionary read against the validated
    classifier instead of guessing blind. Empty string if unavailable.
    """
    try:
        path = PROJECT_ROOT / "03 System" / "(C) Live Engine" / "bias_state.json"
        if not path.exists():
            return ""
        st = json.loads(path.read_text())
        syms = st.get("symbols", {}) or {}
        root = (symbol or "").split(":")[-1].upper()          # CME_MINI:NQ1! -> NQ1!
        entry = syms.get(root)
        if entry is None:                                      # fallback: match on bare root
            bare = root.rstrip("!").rstrip("0123456789")
            entry = next((v for k, v in syms.items()
                          if k.upper().startswith(bare)), None)
        if not entry:
            return ""
        d = entry.get("direction")
        gen = st.get("generated_utc", "?")
        if not d:
            return ("## GATE 0 — DETERMINISTIC BIAS (validated classifier, read independently)\n"
                    f"No active bias this session ({entry.get('reason', '—')}; as of {gen}). "
                    "The gate does NOT confirm an HTF bias right now — lean on structure, keep "
                    "conviction low, and set gate0_agreement = \"NO_GATE\".")
        return ("## GATE 0 — DETERMINISTIC BIAS (validated classifier, read INDEPENDENTLY of you)\n"
                f"direction: {d.upper()}  |  model: {entry.get('model')}  |  "
                f"alignment: {entry.get('bin')} {entry.get('alignment')}  |  "
                f"draw: {entry.get('target_name')} {entry.get('target')}  |  "
                f"flip_tf: {entry.get('flip_tf')}  |  as of {gen}\n"
                "Your HTF read SHOULD agree with this. If you disagree, set gate0_agreement = "
                "\"DISAGREE\" and justify why a discretionary read should override a validated gate; "
                "if you agree, set \"AGREE\". A LOW-alignment gate is weak confirmation — size down.")
    except Exception:
        return ""


# ── Feedback helpers ──────────────────────────────────────────────────────────

def load_recent_feedback(n=50):
    """Return last n resolved trades from Supabase for model learning context."""
    try:
        return db.get_resolved_feedback(n)
    except Exception as e:
        print(f"  [DB] feedback load failed: {e}", flush=True)
        return []


def log_call(call, market_data):
    """Write a trade call to Supabase. Returns the call_id."""
    call_id  = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    symbol   = market_data["status"].get("chart_symbol", "?")
    timeframe = market_data["status"].get("chart_resolution", "?")
    try:
        db.log_trade(call_id, call, symbol, timeframe)
        print(f"  [DB] trade {call_id} saved", flush=True)
    except Exception as e:
        print(f"  [DB] save failed: {e} — falling back to JSONL", flush=True)
        entry = {
            "id": call_id, "timestamp": datetime.datetime.now().isoformat(),
            "symbol": symbol, "timeframe": timeframe,
            "call": call, "outcome": "pending", "notes": "",
        }
        with open(FEEDBACK_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    return call_id


def mark_feedback(call_id, outcome, notes=""):
    """Update trade outcome in Supabase."""
    try:
        db.update_outcome(call_id, outcome, notes)
        print(f"✓ Marked {call_id} as {outcome}")
    except Exception as e:
        print(f"  [DB] update failed: {e}")


# ── Feedback context builder ───────────────────────────────────────────────────


# ── Claude API ────────────────────────────────────────────────────────────────

SYSTEM_STATIC = """\
You are an ICT (Inner Circle Trader) co-pilot for NQ/ES futures scalping.
You apply Zion's specific trading strategy to live TradingView chart data and
produce a structured trade call.

## THE 2-MODEL SPINE (Decisions Log D13 — this REPLACES the old 4-model framework)
There are exactly TWO models. The model falls out of the HTF bias state — it is
not a separate detector. After HTF bias is set, ask one question of the lower-
timeframe structure:

  · REV (Reversal) — a FRESH SWEEP of an ERL extreme + an MSS flip that closes
    order flow back the other way. The state machine just flipped against the
    prior bias. Trade the NEW draw — the opposite ERL across the range. Stop sits
    beyond the swept extreme (the wick that grabbed the liquidity).
  · CONT (Continuation) — HTF bias intact, no fresh opposing MSS. Price is in a
    pullback (a discount/premium within the leg), retraces into an FVG (POI),
    displaces out the far edge. Trade the SAME standing ERL the bias already
    points at. Stop sits 1pt beyond the structural swing the displacement leg
    originated from. This is the DEFAULT — most days are continuation.

IFVG and MFD are NOT models — they are OVERLAYS:
  · ifvg_confirmation — the inverse-FVG step is the REVERSAL-CONFIRMATION trigger.
    When the FVG that held the prior trend is violated and inverts polarity, that
    first clean displacement back through it IS the MSS confirmation of the REV.
    Set ifvg_confirmation=true when a REV is confirmed this way.
  · mfd_overlay — a NEWS-DAY overlay. When major red-folder news engineers a
    liquidity pool that becomes the draw, set mfd_overlay=true and treat the day
    with extra caution and the dead-zone/discipline rules. MFD overlays the SAME
    REV/CONT fork onto the news pool; it is never the model itself.

So `model` is one of: "REV", "CONT", or "NO TRADE". Never emit Rev/Continuation/
IFVG/MFD as model values — IFVG and MFD live in the two boolean overlay fields.

## WHEN TO STAND ASIDE (model = "NO TRADE") — abstaining IS the edge
Research consensus (Mann, Stasiak, ECMP) and our own breakeven scorecard say the same thing:
expectancy comes from TAKING ONLY high-conviction setups and STANDING ASIDE on coin-flips.
Forcing a graded trade on a marginal read is exactly how the edge bleeds out. So abstain —
set model = "NO TRADE" — whenever ANY of these hold:
  1. DOL/draw was taken BEFORE any model formed — the objective is gone.
  2. Outside NY session hours (before 09:30 / after 16:00 ET).
  3. No discernible structure — no swing points, no ERL, no IRL.
  4. COIN-FLIP read — the honest probability the setup works is near 50/50: the draw is
     unclear, the timeframes conflict, Gate 0 disagrees with no compelling structural reason
     to override it, OR the best grade you could honestly give is C+/C/C-. A C-tier read is a
     STAND ASIDE, not a trade to take small.
**Most setups are stand-asides — that is correct and expected, not a failure to find a trade.**
When you stand aside, name the SPECIFIC missing condition in no_trade_reason (never a vague
"uncertain"). Only an honest A/B-grade setup is one to actually take; anything weaker is a PASS.
Lunch (12:00–13:30) is low-quality and usually a stand-aside.

## DECISION FLOW
Layer C — Gamma regime (UW / user-provided)
  · Negative gamma / trending → favors CONT (dealers amplify; the draw extends).
  · Positive gamma / mean-reverting → favors REV at extremes (dealers fade).
  · Mixed/divergent → cut size or skip; let structure lead. Sizing modifier only —
    it can reduce grade but does NOT force NO TRADE.

Layer B — News / MFD overlay
  · Major red-folder news in the next 1-2 hours → set mfd_overlay=true, apply extra
    caution, still classify the underlying REV/CONT model. Not an automatic NO TRADE.

Layer A — ICT order flow (the model itself)
  · Fresh sweep at an ERL extreme + MSS flip → REV (set ifvg_confirmation if the
    inverse-FVG confirmed it).
  · Bias intact, pullback into FVG, standing ERL target → CONT.
  · Structure unclear, confluences weak, or only a C-tier read → STAND ASIDE (NO TRADE).
  · Gate 0 (deterministic bias) is your independent check — agree with it, or justify override.

## TIMEFRAME STACK (validated bias gate — D18; the DAILY read is RETIRED)
- HTF bias = **4H context → MSS on 1H / 15m / 5m** (fractal, not 1H-only). 4H is the
  anchor/draw frame. Do NOT treat the daily as the bias timeframe — it is gone.
- Entry is executed on the **1m or 5m** chart.
- Use 5m for model + neckline confirmation and the ERL sweep; 1m for the flip candle /
  MSS confirmation and precise entry timing.
- Entry zone and stop reference 1m/5m structure, not HTF bars.

## EXIT RULES
- PT1: Scale 50% at IRL (nearest unmitigated FVG). Move SL to BE.
- PT2: Run remaining position to ERL (the standing draw for CONT; the opposite ERL across the range for REV)

## RISK/REWARD RULE (floor is on the FIRST DOL; the runner is judged separately)
- `rr_ratio` = R to the **FIRST DOL** (PT1): (PT1 price − entry) ÷ (entry − stop) for longs,
  reversed for shorts. This is the number the floor checks.
- **0.85R FLOOR to the first DOL** (Zion 2026-06-29, revises D14's 1.3R): a setup whose first
  DOL is < ~0.85R from the structural stop is NOT a trade. Rationale: trades that open with a
  near first target often run much further, so judging only the first DOL at 1.3R was killing
  good runners. The floor stays low; the RUNNER must still justify the trade —
- `rr_to_pt2` = R to PT2 (the final draw / ERL): the runner. It must fit the day-type ceiling
  (05 Discipline / D15): overnight-displaced ≈ 2–3R; rebalanced-then-continuation ≈ 4–7R. A
  trade with 0.85R to first DOL but no realistic PT2 beyond ~2R is still a weak C-tier — the
  edge is the runner, not the scalp to first DOL.
- Always output both `rr_ratio` (first DOL) and `rr_to_pt2` (runner), numeric.
- If levels aren't precise enough, assume worst case and apply the rule conservatively.

## THE 5-STEP A+ CHECKLIST (from (C) 05 Discipline — run in order)
Fill the `checklist` object with a {pass, note} for each step:
  1. draw          — what's the liquidity target (which ERL)? No clear draw → fail.
  2. mtf_alignment — do the timeframes agree on that draw? (2 aligned ≈ C+/B, 4–5 ≈ A)
  3. poi           — is price at a valid FVG / order block for the entry?
  4. model         — REV or CONT? (state which, in the note)
  5. rr            — first DOL clears the 0.85R floor AND the runner (PT2) fits the day-type ceiling?
Anything that isn't an A/B grade is a skip. Most setups are skips.

## CONFIDENCE GRADING SCALE
Grade on how many ICT conditions are confirmed and how cleanly. Be honest but not overly harsh.
  A+ — Perfect: draw clear, model fully confirmed, 4–5 TFs aligned, clean 5m/1m structure
  A  — Strong: most conditions met, 3+ aligned, one minor ambiguity
  A- — Good: solid setup, draw valid, model forming, 2 aligned, one gap
  B+ — Decent: model visible, ERL/IRL identifiable, only 1-2 confluences
  B  — Average: setup qualifies, structure slightly messy, low confluence count
  B- — Weak: model technically present but real concerns (messy structure, ambiguous IRL)
  C+ — Marginal: setup barely qualifies, significant doubts about one core condition
  C  — Very weak: model speculative, most experienced traders would pass
  C- — Extremely low conviction: only one condition met or counter-evidence present
  → A/B grades are TAKES. C-tier grades are STAND-ASIDES — emit model "NO TRADE" with the
    specific missing condition, do not take them small. NO TRADE is the right answer often.

## OUTPUT FORMAT — respond ONLY with this JSON, no extra text
{
  "model":          "REV | CONT | NO TRADE",
  "direction":      "Long | Short | N/A",
  "gate0_agreement": "AGREE | DISAGREE | NO_GATE",
  "gate0_note":     "if DISAGREE: why your discretionary read overrides the validated gate",
  "ifvg_confirmation": true,
  "mfd_overlay":       false,
  "entry_zone":     "price or level description",
  "stop":           "structural level + regime scaling note",
  "pt1":            "IRL target (FVG level)",
  "pt2":            "ERL target (standing draw for CONT / opposite ERL for REV)",
  "confidence":     "A+ | A | A- | B+ | B | B- | C+ | C | C- | NO TRADE",
  "confidence_reason": "one sentence explaining exactly why this grade was given",
  "rr_ratio":       0.9,
  "rr_to_pt2":      3.2,
  "no_trade_reason": "only if NO TRADE",
  "checklist": {
    "draw":          {"pass": true, "note": "which ERL is the target"},
    "mtf_alignment": {"pass": true, "note": "which TFs agree on the draw"},
    "poi":           {"pass": true, "note": "the valid FVG/OB at entry"},
    "model":         {"pass": true, "note": "REV or CONT + why"},
    "rr":            {"pass": true, "note": "first-DOL R vs 0.85 floor; PT2 runner vs day-type ceiling"}
  },
  "reasoning": {
    "layer_c_gamma":   "regime read (favors REV or CONT)",
    "layer_b_news":    "news check (MFD overlay?)",
    "htf_bias":        "direction + structural evidence",
    "dol":             "current draw + still valid?",
    "erl":             "ERL levels (Asia/London session H/L)",
    "irl":             "nearest unmitigated FVG",
    "model_forming":   "REV vs CONT + confirmation status (IFVG?)",
    "confluences":     ["list each stacked confluence"]
  }
}
"""


def build_playbook_block(playbook):
    """Return playbook docs formatted for the system prompt.

    `playbook` is the list of (label, text) sections from load_playbook().
    """
    parts = ["## YOUR PLAYBOOK (current canonical — 2-model spine, D13)\n"]
    for label, text in playbook:
        parts.append(f"### {label}\n{text}")
    return "\n\n".join(parts)


def _grade_tier(conf):
    c = (conf or "").strip().upper()
    if c.startswith("A"):
        return "A-tier"
    if c.startswith("B"):
        return "B-tier"
    if c.startswith("C"):
        return "C-tier"
    if "NO TRADE" in c or c == "NO_TRADE":
        return "NO TRADE"
    return "ungraded"


def build_feedback_block(feedback, min_sample=10):
    """Aggregate CALIBRATION context (hit-rate by grade) — NOT a raw recent-trade dump.

    Why the change: injecting the raw last-N resolved trades as "learn from these
    patterns" invites recency-overfitting (chasing the last few outcomes on a tiny
    sample). The honest signal is aggregate reliability: does an A grade actually win
    more often than a C grade? If not, the grades aren't calibrated. Feedback is for
    measuring calibration, not in-context steering.
    """
    if not feedback:
        return ""
    resolved = [e for e in feedback if e.get("outcome") in ("correct", "incorrect")]
    n = len(resolved)
    if n < min_sample:
        return (f"\n## CALIBRATION\nInsufficient resolved sample (n={n}) to calibrate grades — "
                "do NOT over-weight the few recent results; judge this setup on its own structure.")
    from collections import defaultdict
    tot, win = defaultdict(int), defaultdict(int)
    for e in resolved:
        tier = _grade_tier((e.get("call") or {}).get("confidence"))
        tot[tier] += 1
        if e.get("outcome") == "correct":
            win[tier] += 1
    lines = [f"\n## CALIBRATION — your historical hit-rate by grade (n={n} resolved)"]
    for tier in ("A-tier", "B-tier", "C-tier", "NO TRADE", "ungraded"):
        if tot[tier]:
            lines.append(f"  {tier:9} {win[tier]}/{tot[tier]}  ({100*win[tier]/tot[tier]:.0f}% correct)")
    lines.append(
        "Honesty anchor: if A-tier is NOT clearly beating C-tier, your grades aren't "
        "calibrated — grade more conservatively and stand aside more. Aggregate signal only; "
        "do not chase recent outcomes."
    )
    return "\n".join(lines)


def analyze(market_data, playbook, news_context, feedback, uw_summary="",
            gamma_override="", conviction_context=""):
    """Call Claude API and return the trade call dict.

    `conviction_context` is an optional pre-computed Gate-1 (Selection) summary
    (both long and short conviction scores) injected so Claude can weigh the
    selection edge alongside structure — see conviction_score.py.
    """
    if not API_KEY:
        raise RuntimeError(
            "ANTHROPIC_API_KEY not set.\n"
            "Add it to: 03 System/.env\n"
            "  ANTHROPIC_API_KEY=sk-ant-..."
        )

    client = anthropic.Anthropic(api_key=API_KEY)

    playbook_block  = build_playbook_block(playbook)
    feedback_block  = build_feedback_block(feedback)
    gate0_block     = gate0_context_block(market_data["status"].get("chart_symbol"))

    session = get_session_context()

    # Build multi-timeframe OHLCV section
    tf_sections = []
    for label, data in market_data["ohlcv"].items():
        if "error" in data:
            tf_sections.append(f"### {label} — {data.get('purpose','')}\nERROR: {data['error']}")
        else:
            tf_sections.append(
                f"### {label} — {data.get('purpose','')}\n"
                + json.dumps(data.get("bars", {}), indent=2)
            )
    tf_block = "\n\n".join(tf_sections)

    user_msg = f"""## CURRENT TIME & SESSION
Time:              {session['current_time']}
Session phase:     {session['session_phase']}
Tradeable now:     {'YES' if session['tradeable'] else 'NO — outside NY session hours'}
Active macro window: {session['active_macro_window']}
Next macro window:   {session['next_macro_window']}

## LIVE MARKET DATA

### Chart Status
{json.dumps(market_data['status'], indent=2)}

### Current Quote
{json.dumps(market_data['quote'], indent=2)}

## MULTI-TIMEFRAME OHLCV (validated stack — 4H anchor, no daily)
- 4H: HTF bias CONTEXT + draw frame, ERL (Asia/London/prior-day highs/lows)
- 1H: intermediate structure, order-flow phase (distribution vs rebalancing), MSS
- 15m: faster MSS confirmer + IRL (nearest unmitigated FVG)
- 5m: model confirmation, ERL sweep, neckline structure, FVG entry zone
- 1m: execution precision — flip candle, MSS confirmation, exact entry timing
Trades are executed on the 1m or 5m timeframe.

{tf_block}

## USER CONTEXT
News / events next 2 hours: {news_context}
Gamma override (manual):    {gamma_override if gamma_override else "none — use UW data above"}

{gate0_block if gate0_block else ""}

{uw_summary if uw_summary else "UW data unavailable — use manual gamma override if provided."}

{conviction_context if conviction_context else ""}

{feedback_block}

Apply the C→B→A decision flow across all timeframes and return your trade call as JSON."""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=8192,
        system=[
            {
                "type": "text",
                "text": SYSTEM_STATIC,
                "cache_control": {"type": "ephemeral"},
            },
            {
                "type": "text",
                "text": playbook_block,
                "cache_control": {"type": "ephemeral"},
            },
        ],
        messages=[{"role": "user", "content": user_msg}],
    )

    stop_reason = response.stop_reason
    raw         = response.content[0].text.strip()
    print(f"  [Claude] stop_reason={stop_reason}  output_tokens={response.usage.output_tokens}  raw_len={len(raw)}", flush=True)
    print(f"  [Claude] raw preview: {raw[:120]!r}", flush=True)

    import re

    # Strategy 1: try raw directly
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass

    # Strategy 2: extract from ```json ... ``` fences
    match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", raw, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass

    # Strategy 3: find outermost { ... } block
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass

    # Strategy 4: truncated JSON recovery — close any open braces/brackets
    # Handles max_tokens cutoff mid-response
    if stop_reason == "max_tokens" or raw.startswith("{"):
        candidate = raw
        # Strip trailing incomplete key-value (e.g. `"key":` or `"key": "partial`)
        candidate = re.sub(r',?\s*"[^"]*"\s*:\s*"[^"]*$', '', candidate)
        candidate = re.sub(r',?\s*"[^"]*"\s*:\s*$',        '', candidate)
        candidate = re.sub(r',\s*$',                        '', candidate)
        # Close open arrays and objects
        opens = candidate.count("{") - candidate.count("}")
        candidate += "]" * (candidate.count("[") - candidate.count("]"))
        candidate += "}" * max(opens, 0)
        try:
            parsed = json.loads(candidate)
            parsed["_truncated"] = True
            return parsed
        except json.JSONDecodeError:
            pass

    return {"raw_response": raw}


# ── Display ───────────────────────────────────────────────────────────────────

def display(call):
    model      = call.get("model", "UNKNOWN")
    direction  = call.get("direction", "N/A")
    confidence = call.get("confidence", "?")

    overlays = []
    if call.get("ifvg_confirmation"):
        overlays.append("IFVG")
    if call.get("mfd_overlay"):
        overlays.append("MFD")
    overlay_tag = ("  +" + "+".join(overlays)) if overlays else ""

    bar = "=" * 62
    print(f"\n{bar}")
    print(f"  {model:20} {direction:6}  [{confidence}]{overlay_tag}")
    print(bar)

    if model == "NO TRADE":
        print(f"\n  Reason: {call.get('no_trade_reason', 'No valid setup')}\n")
    elif "raw_response" in call:
        print("\n" + call["raw_response"] + "\n")
    else:
        print(f"\n  Entry:  {call.get('entry_zone', '?')}")
        print(f"  Stop:   {call.get('stop', '?')}")
        print(f"  PT1:    {call.get('pt1', '?')}  (scale 50% → move SL to BE)")
        print(f"  PT2:    {call.get('pt2', '?')}  (run remainder)\n")

        r = call.get("reasoning", {})
        print(f"  HTF Bias:  {r.get('htf_bias', '?')}")
        print(f"  DOL:       {r.get('dol', '?')}")
        print(f"  ERL:       {r.get('erl', '?')}")
        print(f"  IRL:       {r.get('irl', '?')}")
        print(f"  Model:     {r.get('model_forming', '?')}")

        confluences = r.get("confluences", [])
        if confluences:
            print(f"\n  Confluences:")
            for c in confluences:
                print(f"    • {c}")

        if r.get("layer_c_gamma"):
            print(f"\n  Gamma:  {r['layer_c_gamma']}")
        if r.get("layer_b_news"):
            print(f"  News:   {r['layer_b_news']}")

        checklist = call.get("checklist", {})
        if checklist:
            print(f"\n  A+ Checklist:")
            for step in ("draw", "mtf_alignment", "poi", "model", "rr"):
                item = checklist.get(step) or {}
                mark = "✓" if item.get("pass") else "✗"
                print(f"    [{mark}] {step:14} {item.get('note', '')}")

    print(bar)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    # ── feedback subcommand ──
    if len(sys.argv) >= 4 and sys.argv[1] == "feedback":
        notes = " ".join(sys.argv[4:]) if len(sys.argv) > 4 else ""
        mark_feedback(sys.argv[2], sys.argv[3], notes)
        return

    print("ICT Co-pilot — fetching live market data...")

    # Market data (with progress output)
    def progress(msg):
        print(f"  {msg}", flush=True)

    try:
        market_data = get_market_data(status_callback=progress)
    except Exception as e:
        print(f"\n✗ {e}")
        return

    symbol     = market_data["status"].get("chart_symbol", "?")
    resolution = market_data["status"].get("chart_resolution", "?")
    print(f"Connected: {symbol} @ {resolution}")

    # Manual inputs
    print("\n[Context — press Enter to skip]")
    news_context    = input("News in next 2 hours (e.g. 'CPI 8:30am' or 'none'): ").strip() or "none"
    gamma_override  = input("Gamma override (leave blank to use UW live data): ").strip()

    # Load playbook + feedback
    playbook = load_playbook()
    feedback = load_recent_feedback()
    if feedback:
        resolved = [e for e in feedback if e.get("outcome") != "pending"]
        print(f"Loaded {len(resolved)} resolved feedback entries.")

    # Fetch live UW data
    uw_summary = ""
    if uw_data.UW_KEY and uw_data.UW_KEY != "your-uw-key-here":
        print("Fetching Unusual Whales data...")
        try:
            ctx        = uw_data.fetch_context()
            uw_summary, _ = uw_data.summarize(ctx)
            print("UW data loaded.")
        except Exception as e:
            print(f"UW fetch failed: {e}")
    else:
        print("UW key not set — skipping options flow.")

    # Analyze
    print("\nAnalyzing with Claude...")
    try:
        call = analyze(market_data, playbook, news_context, feedback, uw_summary, gamma_override)
    except Exception as e:
        print(f"\n✗ {e}")
        return

    # Display + log
    display(call)
    call_id = log_call(call, market_data)

    print(f"\n  Call ID: {call_id}")
    print(f"  Mark correct:   python3 ict_copilot.py feedback {call_id} correct")
    print(f"  Mark incorrect: python3 ict_copilot.py feedback {call_id} incorrect 'reason'\n")


if __name__ == "__main__":
    main()
