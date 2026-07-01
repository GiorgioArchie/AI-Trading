---
title: "ICT Copilot v2 — Changes (WIP working copy)"
type: changelog
status: wip
phase: forward-test
topic: ict-copilot-app
updated: 2026-06-29
summary: "Isolated working copy of the ICT Copilot (port 8081) with six research-driven improvements. NOT yet ported to the live (C) ICT Copilot — test here first, then merge."
related:
  - "[[(C) Research Synthesis — Does the Edge Survive Scrutiny (2026-06-29)]]"
  - "[[(C) Validation Harness Spec — Costs & OHLC-Path Null (2026-06-29)]]"
  - "[[(C) 00 HTF Bias — Liquidity & Order Flow]]"
---

# ICT Copilot v2 — Changes

> **Isolated working copy.** Lives beside the live app; runs on **:8081** (live stays on :8080), reuses the same `.env`. Nothing here touches the live `(C) ICT Copilot` until we're satisfied and port the diffs over. Double-click `(C) launch.command` to run.

Six improvements, all driven by the 2026-06-29 research synthesis + the cost findings. All pure-logic changes were unit-tested in-sandbox against the real `bias_state.json` and `feedback.jsonl`; live behaviour (TV read + Claude call) still needs Zion's eye on :8081.

## 1. Timeframe stack: 1D → 4H (matches the validated bias gate)
`ict_copilot.py` `ANALYSIS_TIMEFRAMES` and the prompt now read **4H (240) → 1H → 15m → 5m → 1m**, not the daily. The Live Engine retired the daily read in **D18**; the Copilot was still leading HTF bias off it. Now the discretionary front-end and the gate look at the same frames.

## 2. Grounded on Gate-0 (the deterministic bias), with reconciliation
New `gate0_context_block(symbol)` reads `(C) Live Engine/bias_state.json` and injects the classifier's bias (direction, model, alignment bin, draw) into the prompt. Claude must **agree or explicitly flag disagreement** via a new schema field `gate0_agreement` (AGREE / DISAGREE / NO_GATE) + `gate0_note`. Turns the Copilot into the discretionary half of a two-engine check instead of a blind parallel guess. *(Note: bias_state.json is only as fresh as the last loop run — the block surfaces its `as of` timestamp.)*

## 3. Abstention is now allowed — and encouraged
The old prompt **forbade** standing aside on weak setups ("a weak/low-conviction setup is C or C- — NOT NO TRADE"). The research (Mann, Stasiak, ECMP) says the opposite: edge comes from taking only high-conviction setups and **passing on coin-flips**. Rewrote the stand-aside policy: a **C-tier read is a STAND ASIDE** (model = "NO TRADE" with the specific missing condition), a coin-flip is a pass, and "most setups are stand-asides — that is correct." A/B grades are the only takes.

## 4. The 1.3R floor is now NET of realistic cost
`risk_gate.py` adds the confirmed **Apex** round-turn commissions (MNQ/MES $1.04, MCL/MGC $1.34) + tick sizes + a `COST_MODE` (`funded` default / `sim`) + slippage knob. The R_BLOCK veto now checks **net** R = gross − cost-in-R. Verified: a 1.4R-gross setup on a tight 8-pt MNQ stop is **1.27R net → blocked in funded mode, passes in sim**. Set `COST_MODE=sim` on commission-free TopstepX; `funded` is the truth for the $50k goal.

## 5. Feedback → aggregate calibration (not raw recency)
`build_feedback_block` no longer dumps the raw last-50 outcomes into the prompt (which invites recency-overfitting and literally told the model to *avoid* NO TRADE). It now computes **hit-rate by grade tier** (A/B/C/NO TRADE) with a min-sample guard. Tested against the real log: with only 7 resolved trades it correctly returns "insufficient sample — don't over-weight recent results" instead of a misleading table.

## 6. (Carried, not yet built) instrument tick/spread regime + IV-rank lens
Flagged for the next pass: tag contracts by tick/spread regime (deweight small-tick SI per Briola + D20), and wire the **IV-rank lens** (the existing `conviction_score.py` TODO — `uw_data` doesn't parse `iv_rank` yet). Both noted so they aren't re-discovered as missing.

## 7. R floor → 0.85R on the FIRST DOL (revises D14) — Zion, 2026-06-29
The `MIN_R` floor dropped from **1.3R to 0.85R, measured to the first DOL (PT1)**, with the runner to **PT2 judged separately by the day-type ceiling**. Also fixed a latent bug: the old floor was computed against PT2 but *labeled* "first draw." Now `rr_ratio` = first-DOL R (the floor metric), and a new `rr_to_pt2` = the runner. Rationale: setups that open with a near first target often run much further, so a 1.3R-to-first-DOL floor was killing good runners — but the runner must still justify the trade (0.85R first DOL with no PT2 beyond ~2R is still weak C-tier). Verified net-of-cost: 0.9R first-DOL → 0.77R net → still blocked; 1.0R → 0.87R net → passes. **Caveat (logged in D22):** this revises Zion's own D14 ruling and is a hypothesis — dropping to 0.85R raises the first-DOL breakeven win rate (~low-40s% → ~mid-50s%), so track first-DOL-R vs realized final-R to confirm runners materialize.

## What's tested vs not
- **Unit-tested in sandbox (pass):** net-of-cost R floor (funded vs sim), gate0 block from live state, calibration aggregation + guard, grade-tier mapping, all modules compile.
- **Needs live verification on :8081 (Zion):** the full Analyze round-trip (TV 4H read, Claude returning `gate0_agreement`, more frequent NO TRADE calls, the cost-net R reason showing in the UI).
- **Follow-up (cosmetic):** `dashboard.html` doesn't yet render the new fields specially (`gate0_agreement`, gross-vs-net R) — the data is in the JSON payload, but the panel styling is a small follow-up.

## Port-to-live checklist (once satisfied)
Copy the diffs in `ict_copilot.py` (timeframe stack, gate0 block + injection, abstention prompt, calibration fn) and `risk_gate.py` (cost block + net R floor) into `(C) ICT Copilot/`, keep its port 8080, then update its `(C) README.md`. Log a D22 decision entry referencing this changelog.
