import os
import json
try:
    import urllib.request as urlreq
except ImportError:
    urlreq = None

from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

UW_KEY = os.environ.get("UNUSUAL_WHALES_API_KEY", os.environ.get("UW_KEY", "your-uw-key-here"))

_BASE = "https://api.unusualwhales.com"


def _get(path):
    headers = {
        "Authorization": f"Bearer {UW_KEY}",
        "Content-Type": "application/json",
    }
    req = urlreq.Request(f"{_BASE}{path}", headers=headers)
    with urlreq.urlopen(req, timeout=10) as r:
        return json.loads(r.read())


def fetch_context():
    ctx = {}
    try:
        ctx["tide"]   = _get("/api/market/tide")
    except Exception as e:
        ctx["tide_error"] = str(e)
    try:
        ctx["flow"]   = _get("/api/options/flow/summary")
    except Exception as e:
        ctx["flow_error"] = str(e)
    try:
        ctx["regime"] = _get("/api/market/regime")
    except Exception as e:
        ctx["regime_error"] = str(e)
    return ctx


def summarize(ctx):
    if not ctx or all(k.endswith("_error") for k in ctx):
        return "", {}

    lines  = []
    parsed = {}

    tide = ctx.get("tide") or {}
    if tide:
        bias = (tide.get("data") or {}).get("bias") or tide.get("bias") or ""
        parsed["tide"] = {"bias": bias.upper() if bias else "NEUTRAL"}
        lines.append(f"Tide: {bias or 'N/A'}")

    flow = ctx.get("flow") or {}
    if flow:
        dom = (flow.get("data") or {}).get("dominance") or flow.get("dominance") or ""
        parsed["flow"] = {"dominance": dom.upper() if dom else "NEUTRAL"}
        lines.append(f"Flow dominance: {dom or 'N/A'}")

    regime = ctx.get("regime") or {}
    if regime:
        r = (regime.get("data") or {}).get("regime") or regime.get("regime") or "NEUTRAL"
        parsed["regime_estimate"] = r.upper()
        lines.append(f"Regime: {r}")

    summary = "UW Options Flow:\n" + "\n".join(lines) if lines else ""
    return summary, parsed
