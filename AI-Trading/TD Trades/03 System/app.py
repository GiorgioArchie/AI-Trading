#!/usr/bin/env python3
"""
ICT Co-pilot Web Server
Run: python3 app.py
Open: http://localhost:5000
"""

from flask import Flask, jsonify, request, send_from_directory
from pathlib import Path
import json

import uw_data
from ict_copilot import (
    get_market_data,
    load_playbook,
    load_recent_feedback,
    analyze,
    log_call,
    mark_feedback,
    FEEDBACK_LOG,
)

SCRIPT_DIR = Path(__file__).parent
app = Flask(__name__)


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
        playbook    = load_playbook()
        feedback    = load_recent_feedback(50)
        call        = analyze(market_data, playbook, news_context, feedback, uw_summary, gamma_override)
        call_id     = log_call(call, market_data)

        return jsonify({
            "success":    True,
            "call_id":    call_id,
            "call":       call,
            "symbol":     market_data["status"].get("chart_symbol"),
            "timeframe":  market_data["status"].get("chart_resolution"),
            "uw":         uw_parsed,
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


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
    entries = load_recent_feedback(200)
    result = []
    for e in reversed(entries):
        call = e.get("call", {})
        result.append({
            "id":         e["id"],
            "timestamp":  e["timestamp"][:16].replace("T", " "),
            "symbol":     e.get("symbol", "?"),
            "timeframe":  e.get("timeframe", "?"),
            "model":      call.get("model", "?"),
            "direction":  call.get("direction", "?"),
            "confidence": call.get("confidence", "?"),
            "outcome":    e.get("outcome", "pending"),
            "notes":      e.get("notes", ""),
            "call":       call,
        })
    return jsonify(result)


@app.route("/api/trade/<call_id>", methods=["GET"])
def api_trade(call_id):
    entries = load_recent_feedback(500)
    for e in entries:
        if e["id"] == call_id:
            return jsonify({
                "success":   True,
                "call_id":   e["id"],
                "call":      e.get("call", {}),
                "symbol":    e.get("symbol"),
                "timeframe": e.get("timeframe"),
                "timestamp": e["timestamp"][:16].replace("T", " "),
                "outcome":   e.get("outcome", "pending"),
                "notes":     e.get("notes", ""),
            })
    return jsonify({"success": False, "error": "Trade not found"}), 404


if __name__ == "__main__":
    print("\n  ICT Co-pilot Dashboard")
    print("  ─────────────────────────")
    print("  Open: http://localhost:5000\n")
    app.run(debug=False, port=5000, host="127.0.0.1")
