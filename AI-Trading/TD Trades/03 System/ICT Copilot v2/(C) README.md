---
status: canonical
type: readme
phase: forward-test
topic: ict-copilot-app
updated: 2026-06-12
summary: "Flask ICT Copilot — live TradingView + Unusual Whales → Claude trade call, now wired to the vault's current doctrine (D13 2-model spine, risk gate, conviction score, Live Engine panel). Integrated into 03 System 2026-06-12."
---

# (C) ICT Copilot

A small Flask app that turns a live TradingView chart into a structured, graded
ICT trade call. It reads the chart through the `tv` CLI, pulls Unusual Whales
options-flow context, loads the **current canonical playbook** from this vault,
asks Claude (`claude-sonnet-4-6`, with prompt caching) for a JSON trade call, runs
a **risk gate** and **conviction score** over the result, logs everything to
Supabase, and serves a dark-themed dashboard with a feedback loop.

This is the vault-resident copy. The original lived in a partner repo
(`Ai Trading/AI-Trading/TD Trades/03 System`); this copy is upgraded to the
vault's newer doctrine — see *What changed* below.

## Architecture (text diagram)

```
  TradingView desktop ──(tv CLI :9222)──┐
  Unusual Whales API ───────────────────┤
                                        ▼
  Browser ──HTTP──▶  app.py (Flask)  ──▶ ict_copilot.analyze()
   dashboard.html      │                   │  · load_playbook()  → 02 Playbook/*.md (00–05)
   (vanilla JS/CSS)    │                   │                     + Knowledge Graph + Confluence Map
                       │                   │  · build prompt (cached static + playbook blocks)
                       │                   └─▶ Claude claude-sonnet-4-6 → JSON trade call
                       │
                       ├─▶ conviction_score.compute()   (Gate 1 selection, long & short)
                       ├─▶ risk_gate.compute()          (sizing + R_BLOCK/DEADZONE_BLOCK/RISK_BLOCK)
                       ├─▶ db.log_trade()               → Supabase  (call JSONB)
                       └─▶ /api/vault_state             → (C) Live Engine/bias_state.json + setups.json
```

Endpoints: `POST /api/analyze`, `POST /api/feedback`, `GET /api/history`,
`GET /api/trade/<id>`, `GET /api/vault_state`.

## Prerequisites
- **TradingView desktop** launched with remote debugging:
  `/Applications/TradingView.app/Contents/MacOS/TradingView --remote-debugging-port=9222`
- **`tv` CLI** at `~/.npm-global/bin/tv` (the TradingView MCP bridge in
  `03 System/tradingview-mcp/`).
- **Supabase** project with the `trades` table created from `setup_db.sql`.
- **`ANTHROPIC_API_KEY`** (required).
- **`UNUSUAL_WHALES_API_KEY`** (optional — without it, flow context and the
  conviction score are skipped; structure-only analysis still works).

## Setup
```bash
cd "03 System/(C) ICT Copilot"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# create .env (see env vars below); never commit it
# run setup_db.sql once in the Supabase SQL editor
```

## Run
```bash
python3 app.py
# → http://localhost:8080
```

## Environment variables (names only — keep values in `.env`, never commit)
- `ANTHROPIC_API_KEY`
- `UNUSUAL_WHALES_API_KEY` (optional)
- `SUPABASE_URL`
- `SUPABASE_SERVICE_KEY`
- `SUPABASE_KEY` (present in `.env` but currently unused — anon key reserved for future client-side use)
- `ACCOUNT_SIZE` (optional, default 50000 — drives risk-gate sizing)
- `TD_TRADES_ROOT` (optional fallback if the self-locating path search fails)

## What changed vs the partner-repo version
- **Current playbook set.** Loads the 6 canonical `02 Playbook/` docs (00–05) +
  the Knowledge Graph + the Concept Confluence Map. **Stops** loading the retired
  `(C) Model_Selection_Decision_Tree.md`.
- **D13 2-model ruling.** `model` is now `REV` / `CONT` / `NO TRADE` (was
  Rev/Continuation/IFVG/MFD). **IFVG** and **MFD** became boolean overlay fields
  (`ifvg_confirmation`, `mfd_overlay`), not models.
- **5-step A+ checklist** (from `(C) 05 Discipline`) is part of the schema and UI.
- **Risk gate** (`risk_gate.py`): 0.5% sizing in micros, the 1.3R floor
  (`R_BLOCK`), the 11:30–13:30 ET dead zone (`DEADZONE_BLOCK`), and an advisory
  daily-stop (`RISK_BLOCK`). Flag names match the Live Engine's `eval_setups.py`.
- **Conviction score** (`conviction_score.py`): Gate-1 selection score from the
  live UW read, TAKE/HALF/SKIP, both directions, STRUCTURE_ONLY for commodities.
- **Live Engine panel.** Reads `(C) Live Engine/bias_state.json` + `setups.json`
  read-only and shows Gate-0 bias, open setups, and recent lessons.
- **Self-locating paths.** Walks up to find the `02 Playbook` folder instead of
  hardcoding `SCRIPT_DIR.parent`, so the app is relocatable (Reorg Plan convention).

## Where vault data feeds in
- `ict_copilot.load_playbook()` reads `02 Playbook/`, `01 Refinement/`, `07 Outputs/`.
- `app.read_vault_state()` reads `03 System/(C) Live Engine/bias_state.json` and
  `setups.json` (read-only — the Copilot never writes to the Live Engine).
- Doctrine sources: `(C) 02 Selection` (conviction), `(C) 04 Risk Management` +
  `(C) 05 Discipline` (risk gate), `(C) 03 Models` (2-model spine).

## Files
| File | Role |
|---|---|
| `app.py` | Flask server + endpoints + vault-state reader |
| `ict_copilot.py` | TV read, self-locating playbook loader, Claude prompt/schema, logging |
| `uw_data.py` | Unusual Whales fetch + summarize (Layer C) |
| `risk_gate.py` | sizing + R_BLOCK / DEADZONE_BLOCK / RISK_BLOCK |
| `conviction_score.py` | Gate-1 selection score (long & short) |
| `db.py` | Supabase trade storage |
| `dashboard.html` | dark-theme UI (vanilla JS/CSS) |
| `setup_db.sql` | one-time Supabase schema |
| `requirements.txt` / `.gitignore` | deps + ignore rules |
