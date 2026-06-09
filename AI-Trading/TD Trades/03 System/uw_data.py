"""
Unusual Whales live data fetcher.
Provides Layer C (gamma/vol regime) and options flow context for ICT analysis.
"""

import json
import os
from datetime import date
from dotenv import load_dotenv
import requests

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

UW_BASE   = "https://api.unusualwhales.com/api"
UW_KEY    = os.environ.get("UNUSUAL_WHALES_API_KEY", "")
TIMEOUT   = 8
MIN_SWEEP = 75_000   # $75k minimum premium for flow alerts


def _headers():
    return {"Authorization": f"Bearer {UW_KEY}", "Accept": "application/json"}


def _get(path, params=None):
    """GET wrapper — returns parsed JSON or an error dict."""
    try:
        r = requests.get(f"{UW_BASE}{path}", headers=_headers(),
                         params=params, timeout=TIMEOUT)
        if r.ok:
            return r.json()
        return {"_error": f"HTTP {r.status_code}: {r.text[:120]}"}
    except Exception as e:
        return {"_error": str(e)}


def fetch_context():
    """
    Fetch all UW data needed for ICT Layer C analysis.
    Returns a dict with raw responses for each data source.
    """
    today = date.today().isoformat()
    return {
        "market_tide":    _get("/market/market-tide"),
        "flow_alerts":    _get("/option-trades/flow-alerts", {"limit": 50}),
        "qqq_flow":       _get("/lit-flow/QQQ"),
        "spy_flow":       _get("/lit-flow/SPY"),
        "total_oi_vol":   _get("/market/total-options-volume"),
        "qqq_darkpool":   _get("/darkpool/QQQ", {"date": today}),
    }


# ── Summariser ────────────────────────────────────────────────────────────────

def _safe_float(val, default=0.0):
    try:
        return float(val)
    except (TypeError, ValueError):
        return default


def _extract_list(data):
    """Pull a list out of whatever shape the API returns."""
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for key in ("data", "alerts", "results", "tides", "trades"):
            if isinstance(data.get(key), list):
                return data[key]
    return []


def summarize(ctx):
    """
    Convert raw UW context into a structured summary for Claude (Layer C).
    Returns (markdown_string, parsed_dict).
    """
    sections = []
    parsed   = {}

    # ── Market Tide ────────────────────────────────────────────
    tide_raw  = ctx.get("market_tide", {})
    tide_list = _extract_list(tide_raw)
    entry     = tide_list[-1] if tide_list else {}

    net_call = _safe_float(entry.get("net_call_premium"))
    net_put  = _safe_float(entry.get("net_put_premium"))
    net_vol  = _safe_float(entry.get("net_volume"))

    if net_call or net_put:
        # net_put is typically positive even when bearish; compare magnitudes
        if net_call > abs(net_put) * 1.3:
            tide_bias = "BULLISH — net call premium dominates"
        elif abs(net_put) > abs(net_call) * 1.3:
            tide_bias = "BEARISH — net put premium dominates"
        else:
            tide_bias = "NEUTRAL — balanced call/put premium"

        parsed["tide"] = {"net_call": net_call, "net_put": net_put, "bias": tide_bias}
        sections.append(
            f"### Market Tide (as of {(entry.get('timestamp') or entry.get('date') or 'now')[:16]})\n"
            f"Net call premium : ${net_call:>12,.0f}\n"
            f"Net put premium  : ${net_put:>12,.0f}\n"
            f"Net volume       : {net_vol:>12,.0f}\n"
            f"Bias             : {tide_bias}"
        )
    elif "_error" in tide_raw:
        sections.append(f"### Market Tide\nUnavailable — {tide_raw['_error']}")
    else:
        sections.append("### Market Tide\nNo data returned.")

    # ── Flow Alerts (aggressor-side aware) ─────────────────────
    alerts_raw  = ctx.get("flow_alerts", {})
    all_alerts  = _extract_list(alerts_raw)

    calls, puts = [], []
    for a in all_alerts[:20]:
        typ        = str(a.get("type", "")).lower()
        ticker     = a.get("ticker", "?")
        ask_prem   = _safe_float(a.get("total_ask_side_prem", 0))  # aggressor buyers
        bid_prem   = _safe_float(a.get("total_bid_side_prem", 0))  # sellers/closers
        total_prem = _safe_float(a.get("total_premium", 0))
        strike     = a.get("strike", "?")
        expiry     = str(a.get("expiry", "?"))[:10]
        rule       = a.get("alert_rule", "")
        has_sweep  = a.get("has_sweep", False)
        sweep_tag  = " SWEEP" if has_sweep else ""
        aggressor  = "AT-ASK" if ask_prem > bid_prem else "AT-BID"
        line = (f"  {ticker:6} {typ.upper():4}  ${total_prem:>9,.0f}  "
                f"ask${ask_prem:>7,.0f}  strike {strike}  exp {expiry}  "
                f"[{rule}{sweep_tag}] {aggressor}")
        if "call" in typ:
            calls.append((ask_prem, line))
        elif "put" in typ:
            puts.append((ask_prem, line))

    calls.sort(key=lambda x: -x[0])
    puts.sort(key=lambda x: -x[0])

    # Aggressive at-ask premium (directional conviction)
    call_ask = sum(p for p, _ in calls)
    put_ask  = sum(p for p, _ in puts)

    if calls or puts:
        n_c, n_p = len(calls), len(puts)
        if call_ask > put_ask * 1.5:
            flow_dom = f"CALL-DOMINATED — ${call_ask:,.0f} aggressive call buying vs ${put_ask:,.0f} puts (bullish pressure)"
        elif put_ask > call_ask * 1.5:
            flow_dom = f"PUT-DOMINATED — ${put_ask:,.0f} aggressive put buying vs ${call_ask:,.0f} calls (bearish pressure)"
        else:
            flow_dom = f"BALANCED — calls ${call_ask:,.0f} / puts ${put_ask:,.0f} at-ask premium"

        parsed["flow"] = {"calls": n_c, "puts": n_p,
                          "call_ask_prem": call_ask, "put_ask_prem": put_ask,
                          "dominance": flow_dom}
        sections.append(
            f"### Options Flow Alerts (aggressor-side)\n"
            f"Dominance: {flow_dom}\n\n"
            f"Top CALL sweeps (at-ask = bullish aggressor):\n"
            + ("\n".join(l for _, l in calls[:3]) or "  none") +
            f"\n\nTop PUT sweeps (at-ask = bearish aggressor):\n"
            + ("\n".join(l for _, l in puts[:3]) or "  none")
        )
    elif "_error" in alerts_raw:
        sections.append(f"### Flow Alerts\nUnavailable — {alerts_raw['_error']}")
    else:
        sections.append("### Flow Alerts\nNo alerts in current window.")

    # ── QQQ Dark Pool ─────────────────────────────────────────
    dp_raw  = ctx.get("qqq_darkpool", {})
    dp_list = _extract_list(dp_raw)
    if dp_list and "_error" not in dp_raw:
        total_dp_vol = sum(_safe_float(t.get("size", 0)) for t in dp_list)
        total_dp_val = sum(_safe_float(t.get("premium", 0)) for t in dp_list)
        parsed["darkpool"] = {"trades": len(dp_list), "volume": total_dp_vol, "premium": total_dp_val}
        sections.append(
            f"### QQQ Dark Pool\n"
            f"{len(dp_list)} trades  {total_dp_vol:,.0f} shares  ${total_dp_val:,.0f} premium"
        )

    # ── Regime Estimate for Layer C ───────────────────────────
    tide_bias = parsed.get("tide", {}).get("bias", "")
    flow_dom  = parsed.get("flow", {}).get("dominance", "")
    c_ask     = parsed.get("flow", {}).get("call_ask_prem", 0)
    p_ask     = parsed.get("flow", {}).get("put_ask_prem", 0)

    if "BULLISH" in tide_bias and c_ask >= p_ask:
        regime = "BULLISH FLOW — bullish tide + call-side aggressor buying. Favor long setups."
    elif "BEARISH" in tide_bias and p_ask >= c_ask:
        regime = "BEARISH FLOW — bearish tide + put-side aggressor buying. Favor short setups."
    elif "NEUTRAL" in tide_bias:
        regime = "NEUTRAL FLOW — balanced tide. Mean-reversion context; grade setups by structure quality."
    elif "CALL" in flow_dom:
        regime = "CALL-HEAVY FLOW — call aggressor buying despite neutral tide. Mild upside bias."
    elif "PUT" in flow_dom:
        regime = "PUT-HEAVY FLOW — put aggressor buying despite neutral tide. Mild downside bias."
    else:
        regime = "MIXED — no clear directional signal. Let price structure lead."

    parsed["regime_estimate"] = regime
    sections.append(f"### Layer C — Regime Estimate\n{regime}")

    return "\n\n".join(sections), parsed
