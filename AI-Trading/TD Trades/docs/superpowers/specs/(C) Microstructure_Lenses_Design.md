# (C) Microstructure & Positioning Lenses — Design Spec

**Date:** 2026-05-22
**Owner:** Zion (with Claude as synthesis partner)
**Status:** Draft — awaiting user review before transition to writing-plans
**Source idea:** `00 Inputs/Research/Concepts to Expand and Integrate.md`

---

## 1. Overview

Absorb 11 market-analysis concepts (Bookmap, CFTC COT, Goldman PB, dealer gamma, net gamma exposure, open interest, options flow, vanna flow, 0DTE, IV surface, mean reversion) into the TD Trades knowledge base so they function as **active analytical lenses** Claude carries into every market discussion — not just a glossary.

The deliverables are externalized artifacts (markdown + later code), not Claude internal memory. Files are durable, inspectable, owned by Zion, and survive model upgrades.

### Locked profile (from brainstorming)

| | |
|---|---|
| **Asset** | ES / NQ index futures (US prop firms) |
| **Style** | Scalper — 1m / 5s execution, 5–30 min holds |
| **Data access** | Free (CFTC.gov, CME public, Yahoo) + paid options-flow / dealer-gamma service class (UW / SpotGamma / Tradytics — specific vendor TBD) |
| **No Bookmap subscription (yet)** | Microstructure lens stays theoretical-until-subscribed |
| **Existing methodology** | ICT / Smart Money Concepts — liquidity-hunting, "draw of the day," 10-layer Knowledge Graph |

### Goals

- Build a **single synthesis doc** that mirrors the proven `(C) ICT_Concepts_Synthesis.md` pattern — same shape, same validation-question flow, same graduation path to `02 Playbook/`.
- Build a **daily pre-market card** that operationalises the synthesis as a 5-minute morning ritual.
- Sketch a **Phase 3 code integration** into TradingAgents as forward-looking work, without speccing it in detail here.

### Non-goals

- Modifying existing vault files (`(C) Knowledge_Graph_Master.md`, `(C) ICT_Concepts_Synthesis.md`, etc.). Cross-links into them are a separate ask.
- Writing TradingAgents code now — that is Phase 3, separate spec.
- Subscribing to or implementing Bookmap-dependent microstructure tooling.
- Researching macro / news / Fed integration. Out of scope for this list.

### Honest caveats baked into the synthesis

1. **"Goldman PB data" is not accessible.** The substitute is BofA Hartnett Flow Show + public Goldman commentary (Hatzius / Kostin) + flow-aggregator Twitter. Documented as such.
2. **Microstructure lens is theoretical-only** until a Bookmap (or equivalent L2 feed) subscription exists.
3. **Mean reversion is reframed** — not a separate strategy. It's the *positive-gamma-regime tactic* layered onto existing liquidity-sweep playbook. Negative-gamma days become the chase / momentum tactic.

---

## 2. Architecture & file layout

```
03 Projects/TD Trades/
├── 01 Refinement/
│   ├── (C) ICT_Concepts_Synthesis.md          ← existing, untouched
│   ├── (C) Knowledge_Graph_Master.md          ← existing, untouched
│   ├── (C) Microstructure_Lenses_Synthesis.md ← NEW (Phase 1)
│   └── (C) YouTube_Playlist_Study_Tracker.md  ← existing, untouched
├── 02 Playbook/
│   └── [empty — lenses graduate here once gates pass]
└── 07 Outputs/
    ├── (C) Desk_Reference_Card.md             ← existing, untouched
    ├── (C) Intelligence_Summary.md            ← existing, untouched
    ├── (C) Model_Selection_Decision_Tree.md   ← existing, untouched
    ├── (C) Playbook_Mapping_Guide.md          ← existing, untouched
    └── (C) Pre_Market_Lens_Card.md            ← NEW (Phase 2, template)
```

**Two new files only.** No edits to existing vault files in Phase 1 / Phase 2.

**Knowledge Graph integration:** The synthesis file will be linked from `(C) Knowledge_Graph_Master.md` at an L2 (State) or L3 (Context) node — exact insertion point is a separate user approval before any edit to the KG file.

---

## 3. Phase 1 — Master synthesis document structure

**File:** `01 Refinement/(C) Microstructure_Lenses_Synthesis.md`

### Document skeleton

```
# (C) Microstructure & Positioning Lenses — Synthesis & Playbook Mapping

## Executive Summary
## How These Lenses Plug Into Your Existing Framework
## Part 1 — Dealer / Options Regime         (Tier-1 priority)
## Part 2 — Positioning Intel
## Part 3 — Microstructure                  (theoretical until Bookmap)
## Part 4 — Strategy Frame: Mean Reversion as Regime Tactic
## Part 5 — Validation Questions for Zion (per lens, inline-answer format)
## Part 6 — Playbook Graduation Map
## Part 7 — Forward Look: Phase 3 (TradingAgents Code)
```

### Per-lens template

```markdown
### N.X Lens Name
**What it is:** [one-paragraph plain-English]
**Why it matters for ES/NQ scalp:** [direct tie to scalper timeframe]
**Data source:** [specific endpoint / URL / publication]
**Refresh cadence:** [pre-market / hourly / weekly]
**Signal interpretation:** [what high / low / flipped means in trade terms — discrete enum-shaped when possible, to be Phase-3-friendly]
**Validation questions for Zion:**
- [ ] [question 1]
- [ ] [question 2]
**Playbook mapping target:** `02 Playbook/[entry]`
**Failure modes / when this lens lies:** [honest caveats — at least 2 specific situations]
```

The **Failure Modes** field is new vs the existing ICT synthesis. Positioning data lies in predictable ways (GEX distortion around quad-witching, COT 5-day lag, etc.). Forcing this field prevents over-trusting any single lens.

### Per-cluster content depth

#### Part 1 — Dealer / Options Regime *(highest priority)*

| Lens | Depth | Coverage |
|---|---|---|
| GEX (Net Gamma Exposure) | Deep | Sign interpretation; gamma-flip level; positive-gamma = range compression vs negative-gamma = range expansion; "zero gamma" as the day's regime line; provenance of SpotGamma's "Volatility Trigger" and "Call Wall" |
| Dealer gamma by strike | Deep | Reading the profile chart; identifying magnet strikes; gravity vs repel mechanics; charm decay through the day |
| 0DTE & pin dynamics | Deep | Why SPX 0DTE drives ES at 15:00–15:30; pin levels; OPEX-day vs daily-0DTE differences; the 0DTE volatility-suppression effect on intraday range |
| Vanna windows | Deep | Specific timings (10:00 / 14:00 / 15:30 ET) and the vol-crush + vanna-unwind mechanics behind each; pattern note: vanna flow under low VIX is larger than dealers admit |
| IV surface | Medium | Skew shift as leading indicator (put-skew steepening = hedge demand; call-skew richness = chase / FOMO); term-structure inversion (front-back) = stress signal |
| Options flow tape (UW-style) | Medium | Reading block prints vs sweeps vs dark-pool prints; aggressive-sweep filters (e.g. premium > 100K); telling hedging from directional bets |

#### Part 2 — Positioning Intel

| Lens | Depth | Coverage |
|---|---|---|
| CFTC COT | Deep | ES futures specifically — large specs vs dealers vs leveraged funds; "extreme positioning fade" pattern; 5-day reporting lag; disaggregated COT format; weekly pull from cftc.gov |
| Open Interest by strike | Medium | CME public data; top-strike OI walls as gravity; OI build vs unwind; weekly vs monthly OPEX OI structure |
| "Goldman PB" substitute | Short | Honest documentation of what's accessible: BofA Flow Show PDFs (Sunday-night leaks), public Goldman Hatzius / Kostin notes, aggregator Twitter; practical 30-min Sunday-night ritual |

#### Part 3 — Microstructure *(theoretical until Bookmap subscription)*

| Lens | Depth | Coverage |
|---|---|---|
| Bookmap concepts | Medium-theoretical | Heatmap reading; iceberg detection; absorption vs exhaustion; cumulative volume delta; footprint — framed as "what you'll look for the day you subscribe" |
| Free-substitute order flow | Medium | TradingView CVD indicator; footprint via paid TV; volume profile (TPO) reading for ES |
| What's actually noise without Bookmap | Short | Honest list — iceberg hunting and real-time absorption require Bookmap |

#### Part 4 — Strategy Frame: Mean Reversion as Regime Tactic

| Topic | Depth | Coverage |
|---|---|---|
| Positive gamma = fade days | Deep | Dealer mechanics: short gamma above zero forces sell-rip / buy-dip → range compression. Tactical: sweeps fail faster, FVG-fills high quality, tight stops. |
| Negative gamma = chase days | Deep | Dealer mechanics: long gamma below zero forces chase → range expansion. Tactical: sweeps run further, momentum extension is real, wider stops appropriate. |
| Gamma flip level as regime line | Deep | Daily identification (UW / SpotGamma direct); regime-change behaviour at the flip; VIX-spike pattern when crossing flip. |
| Layering on ICT | Deep | **Connective tissue:** positive-gamma regime increases ICT FVG-fill hit-rate; negative-gamma regime lets liquidity sweeps run further. |

### Estimated size

~30-40 KB at completion. Comparable to existing ICT synthesis.

---

## 4. Phase 2 — Pre-Market Lens Card

**File:** `07 Outputs/(C) Pre_Market_Lens_Card.md` (template) — daily fills saved as dated copies (`(C) Pre_Market_Lens_Card_YYYY-MM-DD.md`).

### Card skeleton

```
# (C) Pre_Market_Lens_Card — [YYYY-MM-DD]

## TODAY'S READ (one-liner)
> [Regime call + bias + key invalidation level — forced commitment before details.]

## 1 ⋅ Regime (Dealer Gamma)
| Net GEX | Gamma flip level | Call wall | Put wall | Implied 1d range |
|---|---|---|---|---|

## 2 ⋅ 0DTE & Options Flow Yesterday → Overnight
- 0DTE positioning skew
- Largest sweeps overnight (premium > 100K)
- Block prints (institutional, timestamped)
- Dark-pool prints (if relevant)

## 3 ⋅ Positioning Context
| Source | Latest | Read |
|---|---|---|
| COT (last Fri) | … | Stretched / Neutral / Counter |
| OI walls ES | … | Confluence with gamma walls? |
| Hartnett Flow* | (Mon-am if BofA dropped) | Bull / Bear / Mixed |
| Goldman public | (Sun-night Hatzius if available) | Theme |
*Reminder: BofA Flow Show + public Goldman — NOT actual Goldman PB.

## 4 ⋅ Volatility State
- VIX level → vanna-window aggressiveness
- Term structure: contango / backwardation / flat
- Skew direction
- IV-rank ES

## 5 ⋅ Today's Time Map (ET)
- 09:30 — Open (first liquidity sweep — ICT)
- 10:00 — Vanna window #1
- 14:00 — Vanna window #2 (typically highest impact)
- 15:30 — 0DTE pin pressure / closing imbalance
- 16:00 — Close

## 6 ⋅ Today's Plan (ICT × Regime)
- HTF bias (from existing daily / 4H read)
- Draw of the day (liquidity objective)
- Regime modifier (positive → tight stops, fade extremes; negative → wider, chase impulses)
- Invalidation (gamma flip break + close beyond level → switch mode)

## 7 ⋅ Sunday-Night Addendum (Sunday only)
- BofA Flow Show summary
- Week-ahead catalysts (FOMC / NFP / CPI / earnings)
- Cross-asset signals (DXY, yields, oil)
```

### Design rationale

- **TODAY'S READ at top** forces a one-sentence regime call commitment before scanning details. Anti-paralysis.
- **Tables-not-prose** in sections 1, 3, 4 — scannable in 60 seconds.
- **Section 6 explicitly ties to ICT** — regime is a *modifier* on existing draw-of-the-day work, not a replacement.
- **Section 7 is Sunday-only** — separates weekly cadence (COT, BofA, macro) from daily cadence (gamma, OI, flow).
- **Failure-mode reminders embedded** — e.g., COT row reminds of 5-day lag.

### Storage model

Dated copies — historical record builds for retrospective pattern-recall and lens-validation.

### Fill model

- Phase 2 (markdown only): manual fill using data sources documented in synthesis (~15 min morning ritual).
- Phase 3 (later, code): TradingAgents nodes can populate sections 1–4 automatically; sections 5–7 remain manual.

---

## 5. Graduation rules — synthesis → playbook

A lens lives in the synthesis as **research / draft**. It graduates to a `02 Playbook/(C) <Lens_Name>.md` entry only when it's a **rule traded by, not a concept referenced**.

| Gate | Must be true before graduation |
|---|---|
| 1. Conceptual clarity | All validation questions answered inline in synthesis |
| 2. Operational definition | Signal has a number / threshold (e.g. "GEX flips negative" — not "GEX gets low") |
| 3. Tactical mapping | Known trade action it triggers / modifies / vetoes |
| 4. Failure modes documented | At least 2 specific lying scenarios listed |
| 5. ≥5 live observations | Seen in real time across at least 5 sessions and tagged in journal |

Gate 5 is the load-bearing one. Tape time before codification.

**Recommended pacing:** at most 2 lenses per week graduating to playbook. Synthesis can hold all 11 in draft simultaneously; playbook is for what's tradable.

---

## 6. Validation — how we know the lenses work

Three tiers:

1. **Daily lens-attribution.** Every trade in the journal tagged with the lens(es) supporting it: `LENS:gamma+`, `LENS:0DTE-pin`, `LENS:vanna-14`. After 30 days, correlation reveals which lenses produce winning trades vs ornament.
2. **Weekly regime-call accuracy.** TODAY'S READ on the pre-market card is a daily prediction. Scored Friday-close — % correct over 4 weeks shows whether the system is functioning.
3. **Lesson capture.** Anything surprising goes to `00 Notes/(C)lessons.md` per existing AI Brain rule. Patterns stack over time.

---

## 7. Phase 3 — TradingAgents code integration (sketch only)

**Not specced here.** Forward-look so the synthesis writes code-friendly content.

Likely LangGraph analyst nodes to add alongside existing Fundamentals / Sentiment / News / Technical:

| Node | Data source | Decision contribution |
|---|---|---|
| `GammaAnalyst` | Paid service (UW / SpotGamma / Tradytics) API | Regime call; key levels (flip, call/put walls) |
| `OptionsFlowAnalyst` | UW unusual-flow endpoint | Blocks, sweeps, dark-pool prints |
| `FuturesPositioningAnalyst` | CFTC weekly + CME OI | Positioning extreme; OI-wall gravity |
| `IVSurfaceAnalyst` | yfinance + CBOE term-structure data | Skew shift; term inversion |
| `MicrostructureAnalyst` *(deferred)* | Bookmap API (requires subscription) | CVD; absorption; iceberg detection |

### Decisions deferred to Phase 3 spec

- Specific paid-service subscription → defines the API contract.
- Researcher Debate Room integration — own bull/bear voices vs augmenting Technical?
- Backtesting strategy on historical gamma / COT data.
- Caching strategy (paid-API calls expensive).

### What the synthesis must do to be Phase-3-friendly

- Every lens has explicit signal interpretation mapped to a discrete enum (`POSITIVE_GAMMA` / `NEGATIVE_GAMMA` / `FLIP_PENDING`) — code-ready.
- Every lens has explicit data source + refresh cadence — code-ready.
- Validation questions, once answered, become unit-test cases.

---

## 8. Risks flagged

1. **Overload risk.** Going 0 → 11 concepts at once produces surface understanding of all and execution of none. Mitigation: graduation gates (especially Gate 5 = 5 live observations) and the 2-lenses-per-week pacing recommendation. Synthesis holds all 11 in draft simultaneously; playbook fills slowly.
2. **Confirmation bias risk.** Dealer-gamma narratives are story-shaped — every move feels post-hoc explainable. Mitigation: TODAY'S READ scoring (Section 6 validation) forces *predictions* not *explanations*.
3. **Paid-service drift risk.** Without a specific paid service subscribed, the synthesis lens-content is theoretical. Mitigation: recommend Zion picks the service first, then synthesis is written with that vendor's data shapes in mind. If service choice is unresolved at Phase 1 write-time, the synthesis writes generically and a Phase-3 prep task locks the service.

---

## 9. Phase plan

| Phase | Deliverable | Spec status | Blocks on |
|---|---|---|---|
| 1 | `(C) Microstructure_Lenses_Synthesis.md` (synthesis with validation questions; Zion fills inline) | This spec | Spec approval |
| 2 | `(C) Pre_Market_Lens_Card.md` (template + dated daily copies) | This spec | Phase 1 lens definitions stable enough to source from |
| 3 | TradingAgents analyst nodes (Gamma, OptionsFlow, FuturesPositioning, IVSurface, deferred Microstructure) | Separate future spec | Phase 1 filled-in by Zion; paid-service decision made |

---

## 10. Acceptance criteria for this spec

- [ ] Zion approves all five design sections (architecture, synthesis structure, per-cluster depth, pre-market card, graduation+validation+Phase 3 sketch). **All approved 2026-05-22.**
- [ ] This spec written, committed, self-reviewed.
- [ ] Zion reviews the committed spec file and signs off (or requests changes).
- [ ] Spec hands off to `superpowers:writing-plans` for the implementation plan.

---

## 11. Open questions / TBD before implementation plan

- **Paid-service vendor.** UW vs SpotGamma vs Tradytics? Affects synthesis data-source rows. Either pick now or write the synthesis generically and re-pass once chosen.
- **Knowledge Graph insertion point.** L2 (State) or L3 (Context) node for the new synthesis link? Decided before any edit to `(C) Knowledge_Graph_Master.md`.
- **Pre-market card weekday-only vs Sunday-edition split.** Single template with Section 7 conditional, or two templates? Current spec assumes single conditional.
