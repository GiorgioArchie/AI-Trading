"""
Risk Gate — encodes the canonical risk doctrine from
`02 Playbook/(C) 04 Risk Management.md` + `(C) 05 Discipline`.

Computes, for a Claude trade call:
  · position sizing (micros only, 0.5% floor)
  · the 0.85R first-DOL floor veto  → flag "R_BLOCK"
  · the 11:30–13:30 ET dead zone    → flag "DEADZONE_BLOCK"
  · the daily 2-loss stop (advisory)→ flag "RISK_BLOCK"
  · day-type R ceilings (advisory text)

Flag names intentionally match the Live Engine's eval_setups.py conventions
(RISK_BLOCK, R_BLOCK, DEADZONE_BLOCK) so the two systems speak the same language.

NOTE on RISK_BLOCK: realized R is NOT tracked in the Copilot's trade log, so the
daily-stop check is an ADVISORY count of resolved-incorrect calls today, not a
true −2R breach. The UI labels it as advisory.
"""

import os
import re
import datetime
from zoneinfo import ZoneInfo

ET = ZoneInfo("America/New_York")

RISK_PCT = 0.005                       # 0.5% of account per trade (04 Risk floor)
MIN_R    = 0.85                        # 0.85R floor to the FIRST DOL (Zion 2026-06-29; revises D14's 1.3R)
DAILY_LOSS_COUNT = 2                   # 2 losses (or −2R) → daily stop (D2)

# Dead zone: no NEW entries 11:30–13:30 ET (D16 / 05 Discipline)
DEADZONE_START = datetime.time(11, 30)
DEADZONE_END   = datetime.time(13, 30)

# $/point map — MICROS only on a $50k account (04 Risk).
DOLLARS_PER_POINT = {
    "MNQ": 2,    # micro NQ
    "MES": 5,    # micro ES
    "MCL": 100,  # micro crude
    "MGC": 10,   # micro gold
}

# Symbol root → micro contract. App symbols look like "CME_MINI:NQ1!".
ROOT_TO_MICRO = {
    "NQ": "MNQ",
    "ES": "MES",
    "CL": "MCL",
    "GC": "MGC",
}

# ── Cost realism (the R floor must be NET of cost, not gross) ─────────────────
# COST_MODE: "funded" (real Apex/Topstep cost) or "sim" (0 — today's eval P&L, the
# optimistic baseline). Default funded — the $50k goal is funded money.
COST_MODE = os.environ.get("COST_MODE", "funded").lower()
# Total entry+exit slippage in ticks (sim fills are optimistic; live you cross the spread).
try:
    SLIPPAGE_TICKS = float(os.environ.get("SLIPPAGE_TICKS", "2"))
except (TypeError, ValueError):
    SLIPPAGE_TICKS = 2.0
# Confirmed Apex Tradovate round-turn commissions (2026-06-29). TopstepX is
# commission-free (exchange fees only ≈ $0.70 RT MES) — set COST_MODE=sim there,
# or override these via env if you scale on Topstep.
APEX_RT_COMMISSION = {"MNQ": 1.04, "MES": 1.04, "MCL": 1.34, "MGC": 1.34}
TICK_SIZE          = {"MNQ": 0.25, "MES": 0.25, "MCL": 0.01, "MGC": 0.10}


def cost_in_R(micro, dpp, stop_distance_pts):
    """Round-trip cost expressed in R (commission + slippage ÷ the trade's risk).
    Returns 0.0 in sim mode or when inputs are missing."""
    if COST_MODE == "sim" or not micro or not dpp or not stop_distance_pts:
        return 0.0
    commission  = APEX_RT_COMMISSION.get(micro, 0.0)
    tick_value  = TICK_SIZE.get(micro, 0.0) * dpp
    cost_usd    = commission + SLIPPAGE_TICKS * tick_value
    risk_usd    = stop_distance_pts * dpp
    if risk_usd <= 0:
        return 0.0
    return round(cost_usd / risk_usd, 3)

# Day-type R ceilings (advisory text only — 04 Risk / D15).
DAY_TYPE_CEILINGS = {
    "overnight_displaced":           "~2–3R (move already delivered pre-NY)",
    "rebalanced_then_continuation":  "~4–7R (NY rebalances, then delivers)",
}


def account_size():
    """Account size from env ACCOUNT_SIZE (default 50000)."""
    try:
        return float(os.environ.get("ACCOUNT_SIZE", "50000"))
    except (TypeError, ValueError):
        return 50000.0


def symbol_to_micro(symbol):
    """Map an app symbol ('CME_MINI:NQ1!') to its micro contract ('MNQ').

    Returns (micro_code, dollars_per_point) or (None, None) if unmapped.
    """
    if not symbol:
        return None, None
    # strip exchange prefix, trailing '1!' / digits / '!'
    root = symbol.split(":")[-1].upper()
    root = re.sub(r"[0-9!].*$", "", root)        # NQ1! -> NQ
    micro = ROOT_TO_MICRO.get(root)
    if not micro:
        return None, None
    return micro, DOLLARS_PER_POINT.get(micro)


def _first_number(text):
    """Parse the first numeric value out of a free-text level string.

    entry_zone / stop are free text (e.g. "30,676.2 (1m FVG)"). Returns a float
    or None. Strips thousands-separator commas inside numbers.
    """
    if text is None:
        return None
    if isinstance(text, (int, float)):
        return float(text)
    # grab a number that may contain commas / a decimal
    m = re.search(r"-?\d[\d,]*\.?\d*", str(text))
    if not m:
        return None
    try:
        return float(m.group(0).replace(",", ""))
    except ValueError:
        return None


def _rr_ratio(call):
    """Numeric rr_ratio from the call, or None."""
    val = call.get("rr_ratio")
    if isinstance(val, (int, float)):
        return float(val)
    return _first_number(val)


def in_dead_zone(now_et=None):
    """True during the 11:30–13:30 ET mid-day no-new-entry window."""
    now_et = now_et or datetime.datetime.now(ET)
    return DEADZONE_START <= now_et.time() <= DEADZONE_END


def count_losses_today(get_history_fn):
    """Advisory daily-loss count: resolved-incorrect calls with created_at today (ET).

    `get_history_fn` is a callable returning the trade rows (db.get_history). On
    any failure returns 0 (gate stays advisory and non-fatal).
    """
    try:
        rows = get_history_fn(200)
    except Exception:
        return 0
    today_et = datetime.datetime.now(ET).date()
    n = 0
    for r in rows or []:
        if (r.get("outcome") or "") != "incorrect":
            continue
        created = r.get("created_at") or ""
        if not created:
            continue
        try:
            dt = datetime.datetime.fromisoformat(created.replace("Z", "+00:00"))
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=datetime.timezone.utc)
            if dt.astimezone(ET).date() == today_et:
                n += 1
        except (ValueError, TypeError):
            continue
    return n


def compute(call, symbol, get_history_fn=None, now_et=None):
    """Compute the risk gate for a Claude call.

    Returns a dict:
      {
        flags: [...],                # RISK_BLOCK / R_BLOCK / DEADZONE_BLOCK
        contracts: int | None,
        stop_distance_pts: float | None,
        dollars_per_point: float | None,
        account: float,
        risk_dollars: float,
        sizing_reason: str,          # why sizing is null, if it is
        advisory: { day_type_ceilings, daily_loss_count, daily_loss_advisory, ... }
      }
    """
    now_et   = now_et or datetime.datetime.now(ET)
    account  = account_size()
    risk_dollars = round(RISK_PCT * account, 2)
    flags    = []

    micro, dpp = symbol_to_micro(symbol)

    entry = _first_number(call.get("entry_zone"))
    stop  = _first_number(call.get("stop"))
    stop_distance = None
    contracts = None
    sizing_reason = ""

    if entry is not None and stop is not None:
        stop_distance = round(abs(entry - stop), 6)
    if stop_distance in (None, 0):
        sizing_reason = ("Could not parse a numeric entry & stop "
                         "(levels are free-text) — sizing unavailable.")
    elif dpp is None:
        sizing_reason = (f"No micro $/point mapping for symbol '{symbol}'. "
                         "Micros only on a $50k account.")
    else:
        contracts = int((risk_dollars) // (stop_distance * dpp))
        if contracts < 1:
            sizing_reason = ("Stop too wide for the 0.5% floor at micro size — "
                             "skip (never size up to make it worth it).")

    # ── R floor (0.85R to the FIRST DOL) — NET of realistic cost (revises D14, 2026-06-29) ──
    # rr_ratio is the R to the first DOL (PT1); the runner to PT2 is judged by the day-type
    # ceiling, not this floor. So a near first target with a far runner still qualifies.
    rr = _rr_ratio(call)                              # gross R:R to the first DOL
    crt = cost_in_R(micro, dpp, stop_distance)        # round-trip cost in R
    net_rr = round(rr - crt, 3) if rr is not None else None
    if net_rr is not None and net_rr < MIN_R:
        flags.append("R_BLOCK")

    # ── Dead zone ───────────────────────────────────────────────
    deadzone = in_dead_zone(now_et)
    if deadzone:
        flags.append("DEADZONE_BLOCK")

    # ── Daily stop (advisory) ───────────────────────────────────
    daily_loss_count = 0
    if get_history_fn is not None:
        daily_loss_count = count_losses_today(get_history_fn)
        if daily_loss_count >= DAILY_LOSS_COUNT:
            flags.append("RISK_BLOCK")

    advisory = {
        "day_type_ceilings": DAY_TYPE_CEILINGS,
        "daily_loss_count": daily_loss_count,
        "daily_loss_threshold": DAILY_LOSS_COUNT,
        "daily_loss_advisory": (
            "ADVISORY: realized R is not tracked in this log, so the daily stop "
            "is counted from resolved-incorrect calls today (ET), not a true −2R."
        ),
        "dead_zone_window": "11:30–13:30 ET",
        "in_dead_zone": deadzone,
        "min_r": MIN_R,
        "rr_ratio_gross": rr,
        "cost_R": crt,
        "rr_ratio_net": net_rr,
        "cost_mode": COST_MODE,
        "slippage_ticks": SLIPPAGE_TICKS,
        "r_floor_note": (f"{MIN_R}R first-DOL floor checked NET of cost: gross {rr} − {crt}R cost "
                         f"= {net_rr}R ({COST_MODE} mode)." if rr is not None
                         else "no numeric R:R parsed."),
        "risk_pct": RISK_PCT,
        "micro": micro,
    }

    return {
        "flags": flags,
        "contracts": contracts,
        "stop_distance_pts": stop_distance,
        "dollars_per_point": dpp,
        "account": account,
        "risk_dollars": risk_dollars,
        "sizing_reason": sizing_reason,
        "advisory": advisory,
    }
