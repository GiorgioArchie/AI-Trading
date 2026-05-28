# Unusual Whales MCP Connector — Setup Guide

## What this gives you

Once installed, Claude can answer questions like:
- "Show me the latest unusual options flow"
- "What dark pool prints happened on NVDA today?"
- "What stocks has Nancy Pelosi been trading?"
- "Any unusual insider buying this week?"
- "What's the market tide showing right now?"
- "Give me AAPL's IV rank and recent flow"

---

## 1 — Install Python dependencies

Open Terminal and run:

```bash
pip install mcp httpx pydantic
```

If you use Python 3 explicitly:
```bash
pip3 install mcp httpx pydantic
```

---

## 2 — Note your Python path

```bash
which python3
# e.g. /usr/local/bin/python3  or  /opt/homebrew/bin/python3
```

You'll need this path in the next step.

---

## 3 — Add the connector to Claude Desktop

Open (or create) this file:
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

Add the `unusual_whales` block inside `mcpServers`:

```json
{
  "mcpServers": {
    "unusual_whales": {
      "command": "/usr/local/bin/python3",
      "args": ["/path/to/unusual_whales_mcp.py"],
      "env": {
        "UNUSUAL_WHALES_API_KEY": "YOUR_API_KEY_HERE"
      }
    }
  }
}
```

**Replace:**
- `/usr/local/bin/python3` → your actual Python path from step 2
- `/path/to/unusual_whales_mcp.py` → the full path to where you saved the file
- `YOUR_API_KEY_HERE` → your Unusual Whales API key

---

## 4 — Restart Claude Desktop

Fully quit and reopen Claude Desktop. The connector will load automatically.

---

## Available Tools

| Tool | What it does |
|------|-------------|
| `uw_flow_alerts` | Unusual options flow alerts (global or by ticker) |
| `uw_flow_recent` | Recent options flow for a specific ticker |
| `uw_flow_full_tape` | Complete options tape for a date |
| `uw_flow_per_expiry` | Options flow broken down by expiration |
| `uw_iv_rank` | IV Rank for a ticker |
| `uw_darkpool_recent` | Latest dark pool prints across all stocks |
| `uw_darkpool_ticker` | Dark pool trades for a specific ticker |
| `uw_congress_recent_trades` | Latest congressional trade disclosures |
| `uw_congress_politician_trades` | Trades for a specific politician |
| `uw_congress_politicians` | List all politicians with trade data |
| `uw_congress_unusual_trades` | Flagged unusual congressional trades |
| `uw_insider_transactions` | Recent SEC Form 4 insider filings |
| `uw_insider_ticker` | Insider activity for a specific stock |
| `uw_stock_info` | Stock metadata and fundamentals |
| `uw_stock_state` | Live price quote / stock state |
| `uw_stock_ohlc` | OHLC price candles (1m to weekly) |
| `uw_market_movers` | Top gainers and losers |
| `uw_market_tide` | Market Tide net options premium indicator |
| `uw_options_volume` | Options volume and call/put ratio |
| `uw_stock_screener` | Stock screener for unusual activity |
| `uw_news_headlines` | Latest market news |
| `uw_company_profile` | Detailed company profile |

---

## Troubleshooting

**"UNUSUAL_WHALES_API_KEY is not set"** — Check that your key is in `claude_desktop_config.json` under `env`.

**"Error 403: Access denied"** — Some endpoints require a paid plan tier. Check your subscription at unusualwhales.com.

**"Error 401: Invalid API key"** — Double-check the key in your config file.

**Tools don't appear in Claude** — Make sure you fully quit Claude Desktop (Cmd+Q, not just close the window) and reopen it.
