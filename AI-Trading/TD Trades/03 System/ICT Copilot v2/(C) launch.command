#!/bin/bash
# (C) ICT Copilot v2 (WIP) launcher — double-click to start the app on :8081.
# Isolated working copy; the live Copilot stays on :8080.
# Self-locating: works no matter where the vault lives.
cd "$(dirname "$0")"

# First run: create venv + install deps
if [ ! -d .venv ]; then
  echo "First run — setting up Python environment..."
  python3 -m venv .venv
  .venv/bin/pip install -r requirements.txt
fi

# Start TradingView with remote debugging if nothing is listening on 9222
if ! lsof -i :9222 >/dev/null 2>&1; then
  if [ -d "/Applications/TradingView.app" ]; then
    echo "Starting TradingView with --remote-debugging-port=9222..."
    open -a TradingView --args --remote-debugging-port=9222
    sleep 3
  else
    echo "WARNING: TradingView.app not found — /api/analyze will fail without it."
  fi
fi

# Open the dashboard once the server is up
( sleep 2; open "http://localhost:8081" ) &

echo "Starting ICT Copilot on http://localhost:8081 (Ctrl+C to stop)..."
.venv/bin/python app.py
