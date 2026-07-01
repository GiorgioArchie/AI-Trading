#!/usr/bin/env python3
"""
ICT Co-pilot Web Server
Run: python3 app.py
Open: http://localhost:5000
"""

from flask import Flask, jsonify, request, send_from_directory
from pathlib import Path
import json
import traceback

import uw_data
import db
import risk_gate
import conviction_score
from ict_copilot import (
    get_market_data,
    load_playbook,
    load_recent_feedback,
    analyze,
    log_call,
    mark_feedback,
    PROJECT_ROOT,
)

SCRIPT_DIR  = Path(__file__).parent
LIVE_ENGINE = PROJECT_ROOT / "03 System" / "(C) Live Engine"
app = Flask(__name__)


# ── Vault Live Engine tie-in ──────────────────────────────────────────────────

def _read_json(path):
    """Read a JSON file → dict; graceful {} on missing/corrupt."""
    try:
        if path.exists():
            return json.loads(path.read_text())
    except Exception as e:
        print(f"  [VAULT] {path.name} read failed: {e}", flush=True)
    return {}


def read_vault_state():
    """Read bias_state.json + setups.json from the Live Engine.

    Returns {bias, open_setups, recent_lessons} with lists capped at 10.
    """
    bias_raw   = _read_json(LIVE_ENGINE / "bias_state.json")
    setups_raw = _read_json(LIVE_ENGINE / "setups.json")

    # Gate 0 HTF bias per symbol (bias_scan.py output).
    bias = {
        "generated_utc": bias_raw.get("generated_utc"),
        "symbols":       bias_raw.get("symbols", {}),
    }

    # Open setups = anything not closed/cancelled (cap 10, small payload).
    open_setups = []
    for s in (setups_raw.get("setups") or []):
        if s.get("status") in ("closed", "cancelled"):
            continue
        open_setups.append({
            "id":         s.get("id"),
            "symbol":     s.get("symbol"),
            "direction":  s.get("direction"),
            "type":       s.get("type"),
            "status":     s.get("status"),
            "entry_zone": s.get("entry_zone"),
            "stop":       s.get("stop"),
            "targets":    s.get("targets"),
        })
        if len(open_setups) >= 10:
            break

    # Recent lessons (most recent last in the file → take the tail, cap 10).
    lessons = setups_raw.get("lessons") or []
    recent_lessons = []
    for l in lessons[-10:]:
        recent_lessons.append({
            "ts":          l.get("ts"),
            "symbol":      l.get("symbol"),
            "direction":   l.get("direction"),
            "outcome":     l.get("outcome"),
            "targets_hit": l.get("targets_hit"),
            "auto_note":   l.get("auto_note"),
            "thesis":      l.get("thesis"),
        })
    recent_lessons.reverse()  # newest first

    return {
        "bias":           bias,
        "open_setups":    open_setups,
        "recent_lessons": recent_lessons,
    }


@app.route("/")
def index():
    return send_from_directory(str(SCRIPT_DIR), "dashboard.html")


@app.route("/api/analyze", methods=["POST"])
def api_analyze():
    try:
        data           = request.json or {}
        news_context   = data.get("news_context", "none")
        gamma_override = data.get("gamma_override", "")

        # Fetch live UW data
        uw_summary  = ""
        uw_parsed   = {}
        if uw_data.UW_KEY and uw_data.UW_KEY != "your-uw-key-here":
            try:
                ctx = uw_data.fetch_context()
                uw_summary, uw_parsed = uw_data.summarize(ctx)
                print("  [UW] data loaded", flush=True)
            except Exception as uw_err:
                print(f"  [UW] fetch failed: {uw_err}", flush=True)

        market_data = get_market_data(status_callback=lambda msg: print(f"  [TV] {msg}", flush=True))
        symbol      = market_data["status"].get("chart_symbol")

        # ── Gate 1 (Selection) — compute BOTH long & short conviction pre-analysis
        conviction = conviction_score.compute(uw_parsed, symbol)
        conviction_ctx = conviction_score.context_block(conviction, symbol)

        playbook    = load_playbook()
        feedback    = load_recent_feedback(50)
        call        = analyze(
            market_data, playbook, news_context, feedback,
            uw_summary, gamma_override, conviction_context=conviction_ctx,
        )
        call_id     = log_call(call, market_data)

        # ── Attach the conviction matching the returned direction
        direction = call.get("direction")
        conviction_out = conviction_score.for_direction(conviction, direction)

        # ── Risk Gate — compute from the call's parsed stop/entry numbers
        try:
            risk = risk_gate.compute(call, symbol, get_history_fn=db.get_history)
        except Exception as risk_err:
            print(f"  [RISK] gate failed: {risk_err}", flush=True)
            risk = {"flags": [], "error": str(risk_err)}

        return jsonify({
            "success":    True,
            "call_id":    call_id,
            "call":       call,
            "symbol":     symbol,
            "timeframe":  market_data["status"].get("chart_resolution"),
            "uw":         uw_parsed,
            "risk":       risk,
            "conviction": conviction_out,
        })
    except Exception as e:
        tb = traceback.format_exc()
        print(f"\n[ERROR IN ANALYZE]\n{tb}", flush=True)
        return jsonify({"success": False, "error": f"{type(e).__name__}: {e}", "traceback": tb}), 500


@app.route("/api/feedback", methods=["POST"])
def api_feedback():
    try:
        data = request.json or {}
        mark_feedback(
            data["call_id"],
            data["outcome"],
            data.get("notes", ""),
        )
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/history", methods=["GET"])
def api_history():
    try:
        rows = db.get_history(200)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    result = []
    for r in rows:
        call = r.get("call") or {}
        ts   = (r.get("created_at") or "")[:16].replace("T", " ")
        result.append({
            "id":         r["id"],
            "timestamp":  ts,
            "symbol":     r.get("symbol", "?"),
            "timeframe":  r.get("timeframe", "?"),
            "model":      r.get("model") or call.get("model", "?"),
            "direction":  r.get("direction") or call.get("direction", "?"),
            "confidence": r.get("confidence") or call.get("confidence", "?"),
            "rr_ratio":   r.get("rr_ratio"),
            "outcome":    r.get("outcome", "pending"),
            "notes":      r.get("notes", ""),
            "call":       call,
        })
    return jsonify(result)


@app.route("/api/trade/<call_id>", methods=["GET"])
def api_trade(call_id):
    try:
        row = db.get_trade(call_id)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    if not row:
        return jsonify({"success": False, "error": "Trade not found"}), 404
    ts   = (row.get("created_at") or "")[:16].replace("T", " ")
    call = row.get("call") or {}
    return jsonify({
        "success":   True,
        "call_id":   row["id"],
        "call":      call,
        "symbol":    row.get("symbol"),
        "timeframe": row.get("timeframe"),
        "timestamp": ts,
        "outcome":   row.get("outcome", "pending"),
        "notes":     row.get("notes", ""),
    })


@app.route("/api/vault_state", methods=["GET"])
def api_vault_state():
    """Read-only Live Engine tie-in: Gate 0 bias + open setups + recent lessons."""
    try:
        return jsonify(read_vault_state())
    except Exception as e:
        # Never break the page on a vault read; return empty graceful payload.
        print(f"  [VAULT] state read failed: {e}", flush=True)
        return jsonify({"bias": {"symbols": {}}, "open_setups": [], "recent_lessons": []})


if __name__ == "__main__":
    print("\n  ICT Co-pilot Dashboard — v2 (WIP)")
    print("  ─────────────────────────────────")
    print("  Open: http://localhost:8081\n")
    app.run(debug=False, port=8081, host="127.0.0.1")
