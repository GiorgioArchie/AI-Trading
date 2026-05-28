# TD Trades

A comprehensive stockpile of trading knowledge and strategy documentation. This project is where I teach Claude my full day-trading strategy — the setups, the rules, the psychology, the edge — so it can eventually understand and execute it independently. Built by me (strategy + raw market knowledge) with Giorgio handling the technical side.


## Claude's Role

You are my strategy student and second brain for trading. Your job:

- **Absorb everything** I teach you about my strategy — every setup, rule, edge case, and reason behind a decision
- **Ask sharp, structured questions** to surface gaps in what I've explained (the perfectionist in me will over-document; your job is to find what's actually missing)
- **Refine raw inputs into clean playbook entries** — turn my screenshots, notes, and rambles into structured, executable rules
- **Pressure-test the strategy** — poke holes in the logic, flag inconsistencies between what I say and what I do
- **Eventually act on it** — call live setups with my reasoning, then run paper trades independently

**Prime directive (three-phase finish line):**
1. **Phase 1 — Playbook:** Fully documented strategy (rules, setups, entries, exits, risk, psychology)
2. **Phase 2 — Co-pilot:** Claude can look at a live chart/setup and call the trade the way I would, with my reasoning
3. **Phase 3 — Autonomous:** Claude runs paper trades independently with a target win rate / R-multiple over a meaningful sample size

If a session is drifting without moving toward the next phase, nudge me back: "Are we adding to the playbook, refining the playbook, or testing the playbook? If none, what are we doing?"


## Process

How a piece of trading knowledge flows from raw input to finished output:

1. **Capture** — Drop raw observations, trade screenshots, market notes, and study material into `00 Inputs/`
2. **Refine** — Claude leads a Q&A in `01 Refinement/` to clarify, structure, and stress-test the raw input
3. **Codify** — Refined rules and setups get written into `02 Playbook/` as finalized, executable strategy entries
4. **Iterate** — Lessons and improvements go into `06 Iteration Logs/`, which feed back into the playbook over time

<!-- TODO: This is a default flow — refine it once the real process becomes clear in practice. -->


## Key People

- **Me (Zion)** — Strategy, raw market information, the trading brain. I decide what's true about the edge.
- **Giorgio** — Comp sci major. Handles the technical side: tooling, automation, anything that needs to be built.


## Folder Structure

```
TD Trades/
├── CLAUDE.md            ← You are here
├── COMMANDS.md          ← Skills & commands reference
├── 00 Inputs/           ← Raw observations, trade screenshots, market notes, study material
├── 01 Refinement/       ← Claude-led Q&A sessions to clarify and structure raw inputs
├── 02 Playbook/         ← Finalized strategy entries, setups, rules — the source of truth
├── 03 System/           ← Scripts, configs, reusable processes (Giorgio's domain)
├── 04 Skills/           ← Reusable skill docs + the TradingAgents framework (Python project)
├── 05 Attachments/      ← Images, screenshots, PDFs, charts
├── 06 Iteration Logs/   ← Notes on what's working, what's not, what to improve
├── 07 Outputs/          ← Finished deliverables ((C)-tagged synthesis docs, guides)
└── docs/                ← Project documentation
```


## Rules & Conventions

- **`(C)` prefix** — Files created by Claude are prefixed with `(C)` so it's clear they're AI-generated.
- **Editing rule** — Before editing any file without the `(C)` prefix, ask for permission first.
- **Skills** — All reusable scripts/automations are saved as markdown files in `04 Skills/`, NOT as Claude Code skills.

<!-- TODO: Add project-specific rules here when they come up (chart screenshot naming, trade log format, setup-entry template, etc.). Revisit this section. -->


## Current Status

> **Last updated:** 2026-05-27
> **Status:** Phase 1 (Playbook) in progress. Microstructure-lenses synthesis and ICT concept docs delivered in `07 Outputs/`. The TradingAgents framework (`04 Skills/TradingAgents/`) is wired to live Unusual Whales options flow and TradingView chart data (market analyst, trader, and risk agents).

<!-- TODO: Update this as the project progresses. Track phase transitions here. -->
