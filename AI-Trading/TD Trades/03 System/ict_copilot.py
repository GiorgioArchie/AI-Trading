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

# ── Paths ─────────────────────────────────────────────────────────────────────
SCRIPT_DIR   = Path(__file__).parent
PLAYBOOK_DIR = SCRIPT_DIR.parent
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

ANALYSIS_TIMEFRAMES = [
    ("1D",  "1D", 50,  "Daily — HTF bias, DOL, ERL (Asia/London highs/lows)"),
    ("1H",  "60", 80,  "1H — intermediate structure, order flow phase"),
    ("15m", "15", 80,  "15m — IRL (nearest FVG), model forming"),
    ("5m",  "5",  100, "5m — model confirmation, neckline, FVG entry"),
    ("1m",  "1",  100, "1m — execution precision, flip candle, MSS confirmation"),
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
            time.sleep(0.8)
            bars = tv("ohlcv", "-n", str(bar_count))
            ohlcv[label] = {"purpose": purpose, "bars": bars}
        except Exception as e:
            ohlcv[label] = {"purpose": purpose, "error": str(e)}

    try:
        tv("timeframe", original_tf)
    except Exception:
        pass

    return {"status": status, "quote": quote, "ohlcv": ohlcv}


# ── Playbook loader ───────────────────────────────────────────────────────────

def load_playbook():
    """Load the two most critical playbook documents."""
    files = {
        "knowledge_graph":  PLAYBOOK_DIR / "01 Refinement" / "(C) Knowledge_Graph_Master.md",
        "decision_tree":    PLAYBOOK_DIR / "07 Outputs"    / "(C) Model_Selection_Decision_Tree.md",
    }
    result = {}
    for k, p in files.items():
        if not p.exists():
            continue
        try:
            result[k] = p.read_text()
        except Exception as e:
            print(f"  [Playbook] skipping {p.name}: {e}", flush=True)
    return result


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


# ── Claude API ────────────────────────────────────────────────────────────────

SYSTEM_STATIC = """\
You are an ICT (Inner Circle Trader) co-pilot for NQ/ES futures scalping.
You apply Zion's specific trading strategy to live TradingView chart data and
produce a structured trade call.

## HTF DIRECTION FILTER (hard rule — no exceptions)
You must determine the larger timeframe (Daily / 1H) order flow bias FIRST before calling any trade.
  · Bullish HTF order flow  → ONLY Long trades are valid. A Short setup = NO TRADE.
  · Bearish HTF order flow  → ONLY Short trades are valid. A Long setup = NO TRADE.
This filter overrides everything. Even an A+ Short setup in bullish HTF flow is NO TRADE.
State the HTF bias clearly in reasoning.htf_bias and enforce the filter before evaluating any model.

## WHEN TO SAY NO TRADE (strict — only these 4 cases)
NO TRADE is reserved for hard rule violations only. Do NOT use it for uncertainty or weak setups.
  1. DOL was taken BEFORE any model formed — the daily objective is gone
  2. Current time is outside NY session hours (before 09:30 ET or after 16:00 ET)
  3. There is literally zero discernible structure — no swing points, no ERL, no IRL at all
  4. Proposed trade direction conflicts with HTF order flow bias (see HTF DIRECTION FILTER above)

Everything else gets a letter grade. A weak, messy, or low-conviction setup is C or C- — NOT NO TRADE.
Lunch hours (12:00–13:30) are low-quality but NOT a hard NO TRADE rule — grade them C or C-.

## THREE-LAYER DECISION HIERARCHY (C → B → A)
Layer C — Gamma regime (user-provided)
  · Below influence threshold → sizing modifier only, all setups available
  · Above threshold → structural filter, may reduce grade but does NOT force NO TRADE

Layer B — News / MFD filter
  · Major red-folder news in next 1-2 hours → identify as MFD model, not NO TRADE

Layer A — ICT order flow (actual model selection)
  · Order flow flipped (ERL swept + neckline shift) → Rev Model
  · Order flow strong and aligned → Continuation Model
  · Inverted FVG retesting in structured environment → IFVG Model
  · Structure unclear or confluences weak → assign a low letter grade (C+/C/C-), NOT NO TRADE
  · Only if all 3 hard NO TRADE conditions above are met → NO TRADE

## CORE STRATEGY — FVG RETRACEMENT
The primary entry model is a retracement into an unmitigated Fair Value Gap (FVG), trading in the
OPPOSITE direction of the retracement (i.e., with the original impulsive move that created the FVG).

A Fair Value Gap forms in a 3-candle sequence:
  · Candle 1: the candle immediately before the impulse
  · Candle 2: the strong impulse candle (creates the gap)
  · Candle 3: the candle immediately after the impulse
  · Bullish FVG: gap between high of candle 1 and low of candle 3 (price gapped up)
  · Bearish FVG: gap between low of candle 1 and high of candle 3 (price gapped down)

Entry: price retraces back into the FVG → enter in the direction of the original impulse.

## STOP LOSS PLACEMENT (hard rule)
The stop loss is the extreme of the 3-candle sequence that created the FVG being traded:
  · Long  (bullish FVG): stop = the LOW of candle 1 in the sequence (the low that preceded the up-impulse)
  · Short (bearish FVG): stop = the HIGH of candle 1 in the sequence (the high that preceded the down-impulse)
This is NOT a generic swing low/high — it is specifically the extreme of the sequence that formed the FVG.
Reference the 1m or 5m chart for this level. State the exact price in the "stop" field.

## EXECUTION TIMEFRAMES
- Entry is executed on the 1m or 5m chart
- Use 5m for model and neckline confirmation
- Use 1m for the flip candle / MSS confirmation and precise entry timing

## EXIT RULES
- PT1: Scale 50% at the next IRL (nearest unmitigated FVG in the direction of trade). Move SL to BE.
- PT2: Run remaining position to ERL (previous Asia/London session high/low)

## RISK/REWARD RULE (hard gate — no exceptions)
- Calculate PT1 R:R as: (PT1 price − entry price) ÷ (entry price − stop price) for longs, reversed for shorts
- If PT1 R:R < 0.85 → output NO TRADE with no_trade_reason "R:R below minimum (0.85 required at PT1)"
- Always include the calculated PT1 R:R in the output field "rr_ratio" (numeric, e.g. 1.2)
- If levels are not precise enough to calculate R:R, assume worst case and apply the rule conservatively

## CONFIDENCE GRADING SCALE
Grade on how many ICT conditions are confirmed and how cleanly. Be honest but not overly harsh.
  A+ — Perfect: DOL clear, model fully confirmed, 3+ confluences stacking, clean 5m/1m structure
  A  — Strong: most conditions met, 2-3 confluences, one minor ambiguity
  A- — Good: solid setup, DOL valid, model forming, 2 confluences, one gap
  B+ — Decent: model visible, ERL/IRL identifiable, only 1-2 confluences
  B  — Average: setup qualifies, structure slightly messy, low confluence count
  B- — Weak: model technically present but real concerns (messy structure, ambiguous IRL)
  C+ — Marginal: setup barely qualifies, significant doubts about one core condition
  C  — Very weak: model speculative, most experienced traders would pass
  C- — Extremely low conviction: only one condition met or counter-evidence present
  NO TRADE — ONLY for the 3 hard violations listed above

## OUTPUT FORMAT — respond ONLY with this JSON, no extra text
{
  "model":          "Rev | Continuation | IFVG | MFD | NO TRADE",
  "direction":      "Long | Short | N/A",
  "entry_zone":     "price or level description",
  "stop":           "price of candle 1 low (long) or candle 1 high (short) of the FVG sequence",
  "pt1":            "IRL target (FVG level)",
  "pt2":            "ERL target (session high/low)",
  "confidence":     "A+ | A | A- | B+ | B | B- | C+ | C | C- | NO TRADE",
  "confidence_reason": "one sentence explaining exactly why this grade was given",
  "rr_ratio":       2.5,
  "risk": {
    "stop_pts":    18.5,
    "dollar_risk": 370,
    "fits_budget": true,
    "note":        "18.5 pts stop → $370 risk at 1 contract (budget: $500)"
  },
  "no_trade_reason": "only if NO TRADE",
  "reasoning": {
    "layer_c_gamma":   "regime read",
    "layer_b_news":    "news check",
    "htf_bias":        "direction + structural evidence",
    "dol":             "current DOL + still valid?",
    "erl":             "ERL levels (Asia/London session H/L)",
    "irl":             "nearest unmitigated FVG",
    "model_forming":   "what is forming + confirmation status",
    "confluences":     ["list each stacked confluence"]
  }
}
"""


def build_playbook_block(playbook):
    parts = ["## YOUR PLAYBOOK\n"]
    if "knowledge_graph" in playbook:
        parts.append("### Knowledge Graph (Master Framework)\n" + playbook["knowledge_graph"])
    if "decision_tree" in playbook:
        parts.append("\n### Model Selection Decision Tree\n" + playbook["decision_tree"])
    return "\n".join(parts)


def build_feedback_block(feedback):
    if not feedback:
        return ""
    lines = ["\n## RECENT FEEDBACK — learn from these patterns\n"]
    resolved = [e for e in feedback if e.get("outcome") not in ("pending", "")]
    if not resolved:
        return ""
    for e in resolved:
        outcome = e.get("outcome", "pending")
        call    = e.get("call", {})
        r       = call.get("reasoning", {})
        conf    = call.get("confidence", "?")
        ts = (e.get("created_at") or e.get("timestamp") or "")[:16]
        lines.append(
            f"[{ts}] {outcome.upper()} — "
            f"{call.get('model','?')} {call.get('direction','?')} [{conf}] "
            f"| {r.get('model_forming','?')}"
        )
        if e.get("notes"):
            lines.append(f"  Notes: {e['notes']}")
    lines.append(
        "\nPattern guidance: if a past call was marked INCORRECT and said NO TRADE, "
        "there was likely a valid setup you missed — grade it next time instead of defaulting to NO TRADE."
    )
    return "\n".join(lines)


_POINT_VALUES = {
    "NQ": 20, "MNQ": 2,
    "ES": 50, "MES": 5,
    "YM": 5,  "MYM": 0.5,
    "RTY": 50, "M2K": 5,
}

def _point_value(symbol: str) -> tuple[float, str]:
    """Return ($/point, instrument_name) for the chart symbol."""
    s = symbol.upper()
    for ticker, pv in _POINT_VALUES.items():
        if ticker in s:
            return pv, ticker
    return 20.0, "NQ"  # default to NQ


def analyze(market_data, playbook, news_context, feedback, uw_summary="", gamma_override="", contracts=1):
    """Call Claude API and return the trade call dict."""
    if not API_KEY:
        raise RuntimeError(
            "ANTHROPIC_API_KEY not set.\n"
            "Add it to: 03 System/.env\n"
            "  ANTHROPIC_API_KEY=sk-ant-..."
        )

    client = anthropic.Anthropic(api_key=API_KEY)

    playbook_block  = build_playbook_block(playbook)
    feedback_block  = build_feedback_block(feedback)

    symbol   = market_data["status"].get("chart_symbol", "NQ1!")
    pv, instr = _point_value(symbol)
    max_pts  = 500 / (contracts * pv)

    session = get_session_context()

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

## MULTI-TIMEFRAME OHLCV
- Daily: HTF bias, DOL identification, ERL (Asia/London session highs/lows)
- 1H: intermediate structure, order flow phase (distribution vs rebalancing)
- 15m: IRL identification (nearest unmitigated FVG), model forming
- 5m: model confirmation, neckline structure, FVG entry zone
- 1m: execution precision — flip candle, MSS confirmation, exact entry timing
Trades are executed on the 1m or 5m timeframe.

{tf_block}

## POSITION SIZING & RISK CONSTRAINT
Contracts:         {contracts}
Max loss:          $500 per trade
Point value:       ${pv}/point ({instr})
Max stop distance: {max_pts:.1f} points from entry

You MUST always calculate the structural stop distance in points and include the "risk" block in your output.
If the structural stop distance exceeds {max_pts:.1f} points:
  - Lower the confidence grade by one full letter (A+ → A, A → A-, A- → B+, B+ → B, B → B-, etc.)
  - Set risk.fits_budget = false
  - Do NOT call NO TRADE for this reason alone — still call the trade

## USER CONTEXT
News / events next 2 hours: {news_context}
Gamma override (manual):    {gamma_override if gamma_override else "none — use UW data above"}

{uw_summary if uw_summary else "UW data unavailable — use manual gamma override if provided."}

{feedback_block}

Apply the C→B→A hierarchy across all timeframes and return your trade call as JSON."""

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

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass

    match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", raw, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass

    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass

    if stop_reason == "max_tokens" or raw.startswith("{"):
        candidate = raw
        candidate = re.sub(r',?\s*"[^"]*"\s*:\s*"[^"]*$', '', candidate)
        candidate = re.sub(r',?\s*"[^"]*"\s*:\s*$',        '', candidate)
        candidate = re.sub(r',\s*$',                        '', candidate)
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

    bar = "=" * 62
    print(f"\n{bar}")
    print(f"  {model:20} {direction:6}  [{confidence}]")
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

    print(bar)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) >= 4 and sys.argv[1] == "feedback":
        notes = " ".join(sys.argv[4:]) if len(sys.argv) > 4 else ""
        mark_feedback(sys.argv[2], sys.argv[3], notes)
        return

    print("ICT Co-pilot — fetching live market data...")

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

    print("\n[Context — press Enter to skip]")
    news_context    = input("News in next 2 hours (e.g. 'CPI 8:30am' or 'none'): ").strip() or "none"
    gamma_override  = input("Gamma override (leave blank to use UW live data): ").strip()

    playbook = load_playbook()
    feedback = load_recent_feedback()
    if feedback:
        resolved = [e for e in feedback if e.get("outcome") != "pending"]
        print(f"Loaded {len(resolved)} resolved feedback entries.")

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

    print("\nAnalyzing with Claude...")
    try:
        call = analyze(market_data, playbook, news_context, feedback, uw_summary, gamma_override)
    except Exception as e:
        print(f"\n✗ {e}")
        return

    display(call)
    call_id = log_call(call, market_data)

    print(f"\n  Call ID: {call_id}")
    print(f"  Mark correct:   python3 ict_copilot.py feedback {call_id} correct")
    print(f"  Mark incorrect: python3 ict_copilot.py feedback {call_id} incorrect 'reason'\n")


if __name__ == "__main__":
    main()
