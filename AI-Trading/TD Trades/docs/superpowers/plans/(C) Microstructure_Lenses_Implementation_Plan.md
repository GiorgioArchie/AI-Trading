# Microstructure & Positioning Lenses Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce two new vault files — a 30-40 KB synthesis covering 11 market-analysis lenses for ES/NQ scalping (Phase 1) and an operational pre-market checklist template (Phase 2) — both following the proven `(C) ICT_Concepts_Synthesis.md` pattern.

**Architecture:** Markdown content drop into Zion's existing Obsidian vault. Synthesis = research/draft (lives in `01 Refinement/`), card = operational ritual (lives in `07 Outputs/`). No edits to existing vault files. No code in this phase. All content is sourced from the design spec at `docs/superpowers/specs/(C) Microstructure_Lenses_Design.md`.

**Tech Stack:** Markdown (Obsidian-flavored), wiki-link syntax `[[...]]`, bash for verification (grep + wc).

**Spec reference:** `docs/superpowers/specs/(C) Microstructure_Lenses_Design.md`

**Execution notes:**
- This is a *content authoring* plan, not a code plan. "Tests" are template-conformance checks (grep) and render checks (open in Obsidian). No TDD red-green.
- Each lens-writing step inlines the **per-lens template** + a **content checklist** + **specific terminology** the author must hit. The author drafts prose at execution time within those rails.
- Zion fills validation-question answers AFTER plan completes — those are not part of execution.
- Per Zion's AI Brain rule "Only create commits when requested," commit steps are included but should be deferred to user-approved commits, not auto-run.

---

## File Structure

**Files created:**
- `01 Refinement/(C) Microstructure_Lenses_Synthesis.md` — single-file synthesis, ~30-40 KB at completion
- `07 Outputs/(C) Pre_Market_Lens_Card.md` — daily-fill template, ~5 KB

**Files NOT modified in this plan:**
- `01 Refinement/(C) Knowledge_Graph_Master.md` — link-in is a separate, explicitly-approved task
- `01 Refinement/(C) ICT_Concepts_Synthesis.md` — referenced, never edited
- Anything else in the vault

---

## Per-lens template (referenced by Tasks 2–6)

Every lens section in the synthesis follows this exact structure. Steps below say "write lens X.Y" — that means populate this template with the lens-specific content listed in the step.

```markdown
### X.Y Lens Name

**What it is:** [one paragraph, plain-English, no jargon-until-defined. 2-4 sentences.]

**Why it matters for ES/NQ scalp:** [concrete tie to 1m/5s execution, 5-30 min holds. 2-3 sentences.]

**Data source:**
- [specific URL or service]
- [refresh endpoint if applicable]
- [free-tier limitations if applicable]

**Refresh cadence:** [pre-market / hourly / daily-close / weekly-Fri-close]

**Signal interpretation:** [discrete-enum-shaped where possible. Example: "POSITIVE_GAMMA = net GEX > 0, NEGATIVE_GAMMA < 0, FLIP_PENDING within 0.5σ of zero." Be Phase-3-friendly.]

**Validation questions for Zion:**
- [ ] [Question 1 — probes Zion's understanding or asks him to commit to specifics]
- [ ] [Question 2]
- [ ] [Question 3 — minimum 3, max 5]

**Playbook mapping target:** `02 Playbook/(C) <Lens_Name_Slug>.md` *(graduates here when all 5 gates pass — see §5 of the synthesis)*

**Failure modes / when this lens lies:**
- [Specific scenario 1 — name the situation, name the symptom]
- [Specific scenario 2 — minimum 2 required per the spec]
```

---

## Verification helpers (used across tasks)

After writing any lens, the verification step runs:

```bash
# All required template fields present?
LENS_SLUG="<lens_anchor>" FILE="01 Refinement/(C) Microstructure_Lenses_Synthesis.md"
cd "$HOME/Desktop/AI Brain/03 Projects/TD Trades"
for field in "What it is" "Why it matters for ES/NQ scalp" "Data source" "Refresh cadence" "Signal interpretation" "Validation questions for Zion" "Playbook mapping target" "Failure modes"; do
  awk "/### $LENS_SLUG/,/^### /" "$FILE" | grep -q "$field" && echo "  ✓ $field" || echo "  ✗ MISSING: $field"
done
```

Expected: all 8 fields print `✓`. Any `✗` = step failed; fix before commit.

---

## Tasks

### Task 1: Scaffold the synthesis file

**Files:**
- Create: `01 Refinement/(C) Microstructure_Lenses_Synthesis.md`

- [ ] **Step 1: Create the file with the full skeleton**

```bash
mkdir -p "$HOME/Desktop/AI Brain/03 Projects/TD Trades/01 Refinement"
```

File content:

````markdown
# (C) Microstructure & Positioning Lenses — Synthesis & Playbook Mapping

> **Status:** Draft — Zion fills validation questions inline as he works through each lens.
> **Source spec:** [[(C) Microstructure_Lenses_Design]]
> **Sister doc:** [[(C) ICT_Concepts_Synthesis]] (the existing methodology this layers onto)

---

## Executive Summary

[~150-250 words. Cover: what this doc is, what it's NOT, how it sits next to the ICT synthesis, reading-order recommendation, the 3 baked-in honest caveats (Goldman PB inaccessible → BofA substitute; Bookmap theoretical-only; mean reversion = regime tactic not separate strategy). Reference the Knowledge Graph (L1-L10) as the parent index.]

---

## How These Lenses Plug Into Your Existing Framework

[~200-300 words. Cover:
- ES/NQ scalper profile (1m/5s execution, 5-30 min holds) → which lens dominates which timeframe
- Mapping into Knowledge Graph layers (L1-L10) — call out which layer each cluster lives at
- The mean-reversion-as-regime-tactic insight — explicit statement that this *modifies* existing liquidity-sweep playbook, not replaces it]

---

## Part 1 — Dealer / Options Regime *(Tier-1 priority for ES/NQ scalp)*

### 1.1 Net Gamma Exposure (GEX) — Daily Framing

[Populated in Task 2.1]

### 1.2 Dealer Gamma Profile by Strike — Magnet & Repel Levels

[Populated in Task 2.2]

### 1.3 0DTE & Pin Dynamics

[Populated in Task 2.3]

### 1.4 Vanna Flow Windows

[Populated in Task 2.4]

### 1.5 Implied Volatility Surface — Skew Shift as Leading Indicator

[Populated in Task 2.5]

### 1.6 Options Flow Tape — Blocks, Sweeps, Dark Pools

[Populated in Task 2.6]

---

## Part 2 — Positioning Intel

### 2.1 CFTC COT — Commitments of Traders

[Populated in Task 3.1]

### 2.2 Open Interest by Strike — Gravity Walls

[Populated in Task 3.2]

### 2.3 "Goldman PB" Realistic Substitute

[Populated in Task 3.3]

---

## Part 3 — Microstructure *(theoretical until Bookmap subscription)*

### 3.1 Bookmap Concepts — Heatmap, Iceberg, Absorption

[Populated in Task 4.1]

### 3.2 Free-Substitute Order Flow

[Populated in Task 4.2]

### 3.3 What's Actually Noise Without Bookmap

[Populated in Task 4.3]

---

## Part 4 — Strategy Frame: Mean Reversion as Regime Tactic

### 4.1 Positive Gamma Days = Fade Extremes

[Populated in Task 5.1]

### 4.2 Negative Gamma Days = Chase Impulses

[Populated in Task 5.2]

### 4.3 The Gamma Flip Level — Regime Line

[Populated in Task 5.3]

### 4.4 Layering Regime onto ICT — The Connective Tissue

[Populated in Task 5.4]

---

## Part 5 — Validation Questions (Consolidated)

[Populated in Task 6. Per the spec, each lens already has its own embedded questions. This part is a flat checklist roll-up so Zion can see at-a-glance how many remain.]

---

## Part 6 — Playbook Graduation Map

[Populated in Task 7. Tabular: lens → playbook target → graduation-gate status]

---

## Part 7 — Forward Look: Phase 3 (TradingAgents Code)

[Populated in Task 8.]
````

- [ ] **Step 2: Verify file created and structure is intact**

```bash
cd "$HOME/Desktop/AI Brain/03 Projects/TD Trades"
test -f "01 Refinement/(C) Microstructure_Lenses_Synthesis.md" && echo "FILE_OK"
grep -c "^## Part " "01 Refinement/(C) Microstructure_Lenses_Synthesis.md"
grep -c "^### " "01 Refinement/(C) Microstructure_Lenses_Synthesis.md"
```

Expected: `FILE_OK`, then `7` (parts), then `16` (lens subsections — 6 + 3 + 3 + 4).

- [ ] **Step 3: Stage commit (do not run unless Zion approves commits)**

```bash
cd "$HOME/Desktop/AI Brain/03 Projects/TD Trades"
git add "01 Refinement/(C) Microstructure_Lenses_Synthesis.md"
git commit -m "feat(synthesis): scaffold microstructure lenses synthesis file"
```

---

### Task 2: Part 1 — Dealer / Options Regime (6 lenses)

**Files:**
- Modify: `01 Refinement/(C) Microstructure_Lenses_Synthesis.md` (replace Part 1 placeholder content)

Each step below populates one lens using the **Per-lens template** at the top of this plan. Author drafts prose per the content checklist provided; verification confirms all 8 template fields are present.

- [ ] **Step 2.1: Write lens 1.1 — Net Gamma Exposure (GEX)**

Content checklist (must cover):
- *What it is:* Net dealer gamma position across all SPX/SPY options, summed by strike, expressed in $ per 1-point spot move. Positive = dealers long gamma; negative = dealers short gamma.
- *Why for ES/NQ scalp:* GEX sign defines the day's regime — positive GEX = mean-revert / range compression, negative GEX = trend / range expansion. Single most important pre-bell read.
- *Data source:* SpotGamma daily "Volatility Trigger" + "Net GEX" / Unusual Whales gamma exposure endpoint / Tradytics GEX dashboard. Free crude approximation: scrape CBOE OI by strike and multiply by ATM gamma estimate.
- *Refresh cadence:* Pre-market daily (data is stale ~30min after close; pre-bell read is best).
- *Signal interpretation:*
  - `POSITIVE_GAMMA`: net GEX > 0. Expect: range compression, sweeps fail faster, dealers sell rips and buy dips → fade-extreme setups favored.
  - `NEGATIVE_GAMMA`: net GEX < 0. Expect: range expansion, sweeps run, dealers chase → momentum setups favored.
  - `FLIP_PENDING`: net GEX within ~10% of zero. Regime is unstable; smaller size, no conviction trades until direction confirms.
- *Validation questions (3-5):* probe Zion on his specific GEX-threshold preferences, how he treats overnight GEX vs intra-day re-pricing, whether he wants to use SpotGamma's "Vol Trigger" or compute his own zero-gamma level, what happens to his ICT setups on flip days.
- *Failure modes:* (1) GEX gets badly distorted around quad-witching (March/June/Sept/Dec 3rd Fri) — values can flip artificially. (2) Late-day GEX moves a lot as 0DTE volume reshapes the profile — pre-bell reading degrades after 14:00 ET.

Verification:

```bash
LENS_SLUG="1.1 Net Gamma Exposure" FILE="01 Refinement/(C) Microstructure_Lenses_Synthesis.md"
cd "$HOME/Desktop/AI Brain/03 Projects/TD Trades"
for field in "What it is" "Why it matters for ES/NQ scalp" "Data source" "Refresh cadence" "Signal interpretation" "Validation questions for Zion" "Playbook mapping target" "Failure modes"; do
  awk "/### $LENS_SLUG/,/^### /" "$FILE" | grep -q "$field" && echo "  ✓ $field" || echo "  ✗ MISSING: $field"
done
```

Expected: 8 ✓ checks.

- [ ] **Step 2.2: Write lens 1.2 — Dealer Gamma Profile by Strike**

Content checklist:
- *What it is:* Gamma exposure distributed across strikes (not the aggregate). Reveals which strikes act as magnets (high positive gamma → dealers must sell as price rises = ceiling) vs repels (high negative gamma → dealers must buy as price falls = floor).
- *Why for ES/NQ scalp:* The profile chart shows the day's intraday gravity. Trading toward a top-magnet strike has higher hit rate than trading away from it. Top magnets work as profit targets; charm decay shifts them through the day.
- *Data source:* SpotGamma daily gamma profile chart / UW gamma exposure by strike / Tradytics gamma chart. Free crude: CBOE OI table → strike-by-strike gamma estimate via Black-Scholes approximation.
- *Refresh cadence:* Pre-market + mid-session re-read (charm decay shifts profile materially by 12:00 ET).
- *Signal interpretation:* Identify top-3 call-side magnets and top-3 put-side magnets. Each gets a label — `MAGNET` (price will gravitate) or `WALL` (price will struggle to penetrate without flow).
- *Validation questions (3-5):* probe Zion on which strikes he'd trust as magnets, whether he distinguishes "magnet" from "wall," how he handles two magnets straddling current price, etc.
- *Failure modes:* (1) Profile lies in overnight when no flow is moving it — early-bell action can dissolve walls fast. (2) Heavy 0DTE volume rebuilds the profile faster than daily snapshots reflect — by 14:00 ET, the morning profile is stale.

Verification: same grep pattern, `LENS_SLUG="1.2 Dealer Gamma Profile"`.

- [ ] **Step 2.3: Write lens 1.3 — 0DTE & Pin Dynamics**

Content checklist:
- *What it is:* Zero-days-to-expiry options. SPX has daily 0DTE. As expiry approaches (every day's 15:00-16:00 ET window), dealers' net delta exposure flips fast → forced hedging → "pin" toward the strike with highest gamma.
- *Why for ES/NQ scalp:* The 15:00-15:30 ET window is the single most predictable scalp setup on positive-gamma days — price pulls toward the pin strike. ES tracks SPX 1:1 here.
- *Data source:* UW 0DTE-specific flow filter / SpotGamma "Hiro" or 0DTE positioning report / Tradytics 0DTE dashboard. Free: CBOE same-day-expiry OI by strike.
- *Refresh cadence:* Pre-market for positioning bias; live during 14:00-16:00 ET window.
- *Signal interpretation:*
  - `PIN_LEVEL`: the strike with highest 0DTE gamma. Used as a 15:00-15:30 ET magnet target.
  - `0DTE_CALL_SKEWED` / `0DTE_PUT_SKEWED`: which side has more open exposure — telegraphs which way the closing imbalance leans.
  - `0DTE_BALANCED`: little net effect; ignore as a signal.
- *Validation questions:* probe Zion on how he times the pin trade, what filter he uses for "high enough gamma to pin," how he treats OPEX days vs daily 0DTE, etc.
- *Failure modes:* (1) OPEX Fridays (3rd Fri monthly + quarterlies) — pin dynamics get overwhelmed by monthly OI roll. (2) High-VIX days — vanna unwind overrides pin attempts. (3) FOMC/CPI days — macro flow drowns out 0DTE positioning.

Verification: same grep, `LENS_SLUG="1.3 0DTE"`.

- [ ] **Step 2.4: Write lens 1.4 — Vanna Flow Windows**

Content checklist:
- *What it is:* Vanna = sensitivity of option delta to changes in IV. When IV falls (common from open through mid-session), dealers' net delta shifts → they buy underlying to hedge. This buying clusters at three predictable windows: ~10:00 ET (post-open IV crush), ~14:00 ET (post-EU close vol drop), ~15:30 ET (closing-rotation vol crush).
- *Why for ES/NQ scalp:* The 10:00 / 14:00 / 15:30 windows are exploitable as known dealer-bid moments. Pattern: low-VIX days have under-appreciated vanna size — bigger moves than dealers admit.
- *Data source:* No direct data — read VIX/VVIX trajectory + IV term-structure shape. UW intraday vol flow if available. SpotGamma "Charm/Vanna model" if subscribed.
- *Refresh cadence:* Live during windows; pre-market for "expected size" estimate via VIX level.
- *Signal interpretation:*
  - `VANNA_AGGRESSIVE`: VIX > 18 → larger vanna unwinds → bigger windowed moves.
  - `VANNA_MODERATE`: VIX 13-18 → meaningful but not headline.
  - `VANNA_LATENT`: VIX < 13 → still meaningful but quieter; easy to miss.
- *Validation questions:* probe Zion on which window he prioritizes, whether he positions for it or just lets it run, how he handles a day where IV rises instead of falls, etc.
- *Failure modes:* (1) IV-rising days (sell-off mornings) reverse the vanna sign — dealers sell instead of buy. (2) Holidays / shortened-session days break the timing. (3) Fed-day mornings — windowed flow gets washed out by macro flow.

Verification: same grep, `LENS_SLUG="1.4 Vanna"`.

- [ ] **Step 2.5: Write lens 1.5 — Implied Volatility Surface**

Content checklist:
- *What it is:* The 3D shape of IV across strikes (skew) and expiries (term structure). Skew = put IV minus call IV at equidistant strikes. Term structure = front-month IV vs back-month IV.
- *Why for ES/NQ scalp:* Surface shifts are *leading* — put-skew steepening fast (last 30min, last hour, overnight) signals hedge demand → distribution incoming. Term inversion (front > back) signals macro stress. Both precede price moves by hours-to-days.
- *Data source:* yfinance for chain → compute skew (free). CBOE term structure data (free). Volfeed/Tradier paid feeds for cleaner data. UW IV-rank dashboard.
- *Refresh cadence:* Pre-market + check at 14:00 ET (mid-session shifts matter most).
- *Signal interpretation:*
  - `SKEW_STEEPENING`: put-skew widening last 30-90 min → distribution warning, defensive bias.
  - `SKEW_FLATTENING`: put-skew narrowing → complacency / risk-on / continuation in current direction.
  - `TERM_INVERSION`: front-month > back-month IV → macro stress; reduce size, expect tail risk.
  - `TERM_CONTANGO`: normal upward-sloping; carry-on environment.
- *Validation questions:* probe Zion on how he measures "skew steepening" (delta-25 vs delta-10? lookback window?), whether he treats inversion as veto or signal, how this interacts with COT positioning, etc.
- *Failure modes:* (1) Earnings season distorts single-name skew but ES/NQ surface is broader; less affected but still noisy. (2) Quarterly rebalance Mondays — skew jumps mechanically from put-roll, not flow. (3) Low-OI strikes have noisy IV — use mid-strike data only.

Verification: same grep, `LENS_SLUG="1.5 Implied Volatility"`.

- [ ] **Step 2.6: Write lens 1.6 — Options Flow Tape (Blocks, Sweeps, Dark Pools)**

Content checklist:
- *What it is:* Real-time large-print options trades, classified into Block (single-print, often negotiated), Sweep (urgent, multi-exchange aggressive), Dark-Pool (off-exchange equity prints that often hedge a paired options trade).
- *Why for ES/NQ scalp:* Aggressive sweeps premium > $100K signal directional bets, not hedges. A series of sweeps stacking same-direction is read-the-tape evidence of institutional flow that ES/NQ futures will follow within minutes-to-hours.
- *Data source:* UW Premium / Tradytics flow / FlowAlgo. Free: limited or none — institutional-grade only.
- *Refresh cadence:* Live during session; review last hour each evening for next-day context.
- *Signal interpretation:*
  - `SWEEP_AGGRESSIVE`: ask-side, premium > $100K, single-symbol cluster → directional bet from informed flow.
  - `BLOCK_HEDGING`: paired with equity dark-pool print of opposite delta → hedge, not signal.
  - `BLOCK_DIRECTIONAL`: not paired, premium > $500K, OTM strikes → institutional speculation. Strongest signal.
- *Validation questions:* probe Zion on his trust threshold for following flow, how he handles conflicting flow (calls + puts both bought aggressively), whether he trades the underlying directly or the same options, etc.
- *Failure modes:* (1) Hedging trades look identical to directional trades to anyone not seeing the paired equity print — high false-positive rate without dark-pool pairing data. (2) Index/ETF flow (SPY/QQQ) is often portfolio rebalancing, not bet-taking. (3) End-of-day prints can be settlement/roll, not new exposure.

Verification: same grep, `LENS_SLUG="1.6 Options Flow"`.

- [ ] **Step 2.7: Stage commit for Part 1**

```bash
cd "$HOME/Desktop/AI Brain/03 Projects/TD Trades"
git add "01 Refinement/(C) Microstructure_Lenses_Synthesis.md"
git commit -m "feat(synthesis): write Part 1 — Dealer/Options Regime (6 lenses)"
```

---

### Task 3: Part 2 — Positioning Intel (3 lenses)

**Files:**
- Modify: `01 Refinement/(C) Microstructure_Lenses_Synthesis.md` (replace Part 2 placeholder content)

- [ ] **Step 3.1: Write lens 2.1 — CFTC COT**

Content checklist:
- *What it is:* Weekly report (every Friday 15:30 ET, data as-of Tuesday close) of futures positioning by trader category: commercials (hedgers), large speculators (CTAs/funds), small speculators (retail), and a disaggregated breakdown (dealers, asset managers, leveraged funds, other).
- *Why for ES/NQ scalp:* Sets the *background regime tide* for the week. Extreme positioning (large specs at 90%+ net long historically) is fadeable in 5-10 day swings — too slow for intraday entries but defines whether you're scalping with or against the underlying tide.
- *Data source:* `https://www.cftc.gov/MarketReports/CommitmentsofTraders/index.htm` (free, official). Pulled weekly Fri-night.
- *Refresh cadence:* Weekly — Fri-close consumption, valid Mon-Fri.
- *Signal interpretation:*
  - `LARGE_SPEC_STRETCHED_LONG`: large specs net long > 80th %ile of trailing year → mean-revert pressure builds; intraday longs face headwind.
  - `LARGE_SPEC_STRETCHED_SHORT`: < 20th %ile → mean-revert squeeze risk; intraday shorts face headwind.
  - `COMMERCIAL_NET_FLIP`: commercial net position flips sign → strongest divergence signal, look for major regime change in 1-2 weeks.
  - `BALANCED`: 30-70th %ile → no positional tide; trade clean technicals.
- *Validation questions:* probe Zion on whether he treats COT as veto or just context, what percentile threshold he'd use, whether he tracks commercials or large specs as primary, etc.
- *Failure modes:* (1) 5-day reporting lag — data is always Tue-close-snapshot, by Fri-publish positioning can have shifted materially. (2) ES futures positioning is muddled by ETF arb (institutions hedge SPY/QQQ shares via ES) — pure positioning intent is opaque. (3) Holiday weeks publish on Mon — different schedule disrupts the ritual.

Verification: same grep, `LENS_SLUG="2.1 CFTC COT"`.

- [ ] **Step 3.2: Write lens 2.2 — Open Interest by Strike**

Content checklist:
- *What it is:* Number of open contracts at each strike, broken out by call/put and expiry. The OI distribution shows where positioning concentrates → defines the gravity walls.
- *Why for ES/NQ scalp:* Top-OI strikes are gravity walls — price gravitates toward them on positive-gamma days, struggles to penetrate them without strong flow. ES/NQ futures don't have direct OI (well, they do, but it's less behaviorally relevant than SPX options OI driving ES through delta hedging).
- *Data source:* CME public data (`https://www.cmegroup.com/markets/equities/sp/e-mini-sandp500.quotes.options.html`) for ES options. CBOE for SPX. UW dashboard for filtered view.
- *Refresh cadence:* Daily (pre-market). Monthly OPEX week = special attention.
- *Signal interpretation:*
  - `OI_WALL_RESISTANCE`: top call-OI strike near current price → ceiling, fade rejection setups.
  - `OI_WALL_SUPPORT`: top put-OI strike near current price → floor, fade rejection setups.
  - `OI_CONFLUENCE_WITH_GAMMA`: top OI strike = top gamma magnet → highest-confidence level; full-conviction trades against it.
  - `OI_DISTRIBUTED`: no concentration, top strike < 2× next-rank → low usefulness for the day.
- *Validation questions:* probe Zion on how far above/below current price an OI wall must be to ignore, whether he stacks OI with gamma walls or treats them separately, how he handles unwinds into OPEX, etc.
- *Failure modes:* (1) Built-up OI from old months can dominate without being behaviorally live — filter for current-month and front-week. (2) Dealer-driven OI (volatility selling programs) doesn't behave like directional OI; same number, different meaning. (3) OPEX-week OI degrades fast — by Friday morning, much of it is rolled or unwound.

Verification: same grep, `LENS_SLUG="2.2 Open Interest"`.

- [ ] **Step 3.3: Write lens 2.3 — "Goldman PB" Realistic Substitute**

Content checklist:
- *What it is:* Goldman Sachs' actual Prime Brokerage flow data is institutional-only and not accessible publicly. The realistic substitutes that aggregate similar signal are: (a) BofA's monthly "Flow Show" by Michael Hartnett (drops Sunday PM via leaked PDFs), (b) Goldman's *public* market commentary by David Kostin (equity strategy) and Jan Hatzius (econ) — often leaked Sunday nights to flow aggregators, (c) Twitter aggregators (@unusual_whales, @SpotGamma, @ZeroHedge) screenshot excerpts irregularly.
- *Why for ES/NQ scalp:* These give *the weekly narrative* — what flows are positioning around, what themes are dominant. Sets the conviction-level for trading aligned-vs-against the week's narrative. Background, not intraday.
- *Data source:*
  - BofA Flow Show: leaked PDF screenshots on Twitter Sunday 18:00-22:00 ET, sometimes Mon AM.
  - Goldman Hatzius/Kostin: public on goldmansachs.com/insights when published; flow aggregators tweet excerpts Sunday-night.
  - Aggregator accounts: @unusual_whales, @SpotGamma, @ZeroHedge, @themarketear.
- *Refresh cadence:* Sunday 18:00-22:00 ET — 30-min ritual to ingest.
- *Signal interpretation:*
  - `FLOW_NARRATIVE_BULL`: BofA Flow Show + Goldman public skew bullish on US equities → align bias.
  - `FLOW_NARRATIVE_BEAR`: skew bearish → defensive bias.
  - `FLOW_NARRATIVE_MIXED`: institutional opinion split → no thumb on scale, trade clean technicals.
- *Validation questions:* probe Zion on which aggregators he trusts most, whether he treats flow narrative as veto or just context, how he handles conflicting narratives, etc.
- *Failure modes:* (1) Hartnett and Kostin can be wrong (often are) — narrative is sentiment indicator, not edge. Sometimes the right move is faded narrative. (2) Twitter excerpts are out-of-context fragments — easy to misread. (3) Skipped Sundays (holidays) leave a stale read for the week.

Verification: same grep, `LENS_SLUG="2.3"`.

- [ ] **Step 3.4: Stage commit for Part 2**

```bash
cd "$HOME/Desktop/AI Brain/03 Projects/TD Trades"
git add "01 Refinement/(C) Microstructure_Lenses_Synthesis.md"
git commit -m "feat(synthesis): write Part 2 — Positioning Intel (3 lenses)"
```

---

### Task 4: Part 3 — Microstructure (3 lenses, theoretical until Bookmap)

**Files:**
- Modify: `01 Refinement/(C) Microstructure_Lenses_Synthesis.md` (replace Part 3 placeholder content)

- [ ] **Step 4.1: Write lens 3.1 — Bookmap Concepts (Heatmap / Iceberg / Absorption)**

Content checklist:
- *What it is:* Bookmap is L2 order-book visualization software. Heatmap = limit-order density over time as a color gradient. Iceberg = hidden orders that refill instantly when hit (institutions hiding size). Absorption = aggressive market orders meeting a wall of limits without moving price (one side is being absorbed by the other; reversal precursor).
- *Why for ES/NQ scalp:* Reads as the *operational layer* of the ICT institutional-flow thesis. Order blocks become visible as iceberg refills; liquidity sweeps become visible as heatmap layers disappearing. *Currently theoretical for Zion until subscription.*
- *Data source:* Bookmap subscription (paid, ~$100/mo). Provides ES/NQ L2 feed integration with most futures brokers.
- *Refresh cadence:* Real-time, scalp execution overlay.
- *Signal interpretation:* Theoretical pending subscription. Examples:
  - `ICEBERG_REFILL_DETECTED`: institutional defense of a level; tradeable as continuation-with-the-defender or reversal-when-defender-quits.
  - `ABSORPTION_AT_LEVEL`: one side absorbing aggressive flow without moving; reversal precursor.
  - `HEATMAP_WITHDRAWAL`: liquidity layers pulling away ahead of price; precursor to liquidity sweep.
- *Validation questions:* probe Zion on whether he's planning to subscribe, what threshold of conviction unlocks the spend, what setups he expects to validate first, etc.
- *Failure modes:* (1) Bookmap is a tool, not an edge — bad reads come from interpretation, not data. (2) L2 spoofing is common in equity index futures; ESMA/CFTC rules don't fully prevent it. (3) High-frequency dynamics on 5s charts blur the signal-to-noise — Bookmap reads better on 1m-15m timeframes than tick-level.

Verification: same grep, `LENS_SLUG="3.1 Bookmap"`.

- [ ] **Step 4.2: Write lens 3.2 — Free-Substitute Order Flow**

Content checklist:
- *What it is:* Approximate order-flow signals from broadly-available tools, no Bookmap subscription required. Cumulative Volume Delta (CVD) = running sum of (buy volume − sell volume). Volume profile / TPO = price distribution over time. Footprint = bid/ask volume at each price level (paid TradingView indicator).
- *Why for ES/NQ scalp:* Crude but real signals on whether moves are flow-supported or thin-volume churn. CVD divergence (price up + CVD down) is a classic absorption signal, accessible without Bookmap.
- *Data source:*
  - CVD: TradingView built-in indicator (free).
  - Volume profile / TPO: TradingView native (free for basic, premium for session-specific).
  - Footprint: TradingView Premium indicator.
- *Refresh cadence:* Real-time during session.
- *Signal interpretation:*
  - `CVD_DIVERGENCE_BEARISH`: price making new highs, CVD failing to make new highs → absorption; reversal precursor.
  - `CVD_DIVERGENCE_BULLISH`: inverse.
  - `VP_HIGH_VOLUME_NODE`: price magnet zone (chop level); fade extensions toward it.
  - `VP_LOW_VOLUME_NODE`: price-rejection zone (gap level); fast moves through.
- *Validation questions:* probe Zion on whether he uses CVD now (likely yes from existing ICT material), what TPO timeframe he frames his draw-of-the-day around, etc.
- *Failure modes:* (1) TradingView's CVD uses trade-tick exchange-classification rules that are imperfect for futures vs equities — small errors compound. (2) Volume profile depends on session anchor — wrong anchor (RTH vs ETH) gives wrong levels. (3) Footprint at 5s tick interval is mostly noise.

Verification: same grep, `LENS_SLUG="3.2 Free-Substitute"`.

- [ ] **Step 4.3: Write lens 3.3 — What's Actually Noise Without Bookmap**

Content checklist (different from per-lens template — this is a short *honesty section*, not a full lens):

```markdown
### 3.3 What's Actually Noise Without Bookmap

This section is intentionally short. It documents what microstructure concepts you should *not* try to chase without Bookmap or equivalent L2 data.

**Genuinely require Bookmap (or paid L2 feed):**
- Real-time iceberg detection — invisible without seeing limit-order refills
- Heatmap-based liquidity-withdrawal reads — invisible without limit-order book persistence over time
- Spoofing identification — invisible without order placement/cancellation history
- High-resolution absorption — visible-ish in CVD but the L2 confirmation is what makes it tradeable

**Workable with free tools:**
- CVD divergence (TradingView)
- Volume profile / VPVR (TradingView)
- TPO market-profile structure (TradingView/Sierra Chart free tier)

**Recommendation:** Do not read ICT order-block material *as if* you have Bookmap data when you don't. The conceptual framework (institutional levels, displacement, OB validity) still applies — but the *real-time confirmation* requires the L2 feed. Until subscribed, treat OB-level entries as higher-risk than the ICT material's confidence implies.

**Threshold for subscribing:** [Validation question for Zion: at what monthly P/L baseline does $100/mo Bookmap become a no-brainer? Lock this number to avoid analysis-paralysis.]
```

This subsection doesn't use the per-lens template — it's prose + recommendation. The verification step is different:

```bash
LENS_SLUG="3.3 What's Actually Noise" FILE="01 Refinement/(C) Microstructure_Lenses_Synthesis.md"
cd "$HOME/Desktop/AI Brain/03 Projects/TD Trades"
awk "/### $LENS_SLUG/,/^### /" "$FILE" | grep -qE "Genuinely require|Workable with free|Recommendation|Threshold for subscribing" && echo "  ✓ Section structure intact" || echo "  ✗ FIX SECTION STRUCTURE"
```

Expected: ✓.

- [ ] **Step 4.4: Stage commit for Part 3**

```bash
cd "$HOME/Desktop/AI Brain/03 Projects/TD Trades"
git add "01 Refinement/(C) Microstructure_Lenses_Synthesis.md"
git commit -m "feat(synthesis): write Part 3 — Microstructure (theoretical-until-Bookmap)"
```

---

### Task 5: Part 4 — Strategy Frame (Mean Reversion as Regime Tactic)

**Files:**
- Modify: `01 Refinement/(C) Microstructure_Lenses_Synthesis.md` (replace Part 4 placeholder content)

This part doesn't use the per-lens template — it's narrative-style synthesis. Each subsection is a tactical-implication block tying the gamma regime to Zion's existing ICT playbook.

- [ ] **Step 5.1: Write subsection 4.1 — Positive Gamma Days = Fade Extremes**

Content checklist:

```markdown
### 4.1 Positive Gamma Days = Fade Extremes

**The mechanics:** When dealers are net long gamma (positive GEX), every move against them shrinks their gamma exposure → they must trade *against* the move to stay hedged. As price rises, dealers sell; as price falls, dealers buy. The systemic effect is **range compression** — extremes get faded by the largest counterparty in the market.

**What this means for your scalping:**
- ICT FVG-fill setups have *higher* hit-rate. Liquidity sweeps fail and reverse faster.
- Draws-of-the-day get hit but rarely overshoot meaningfully.
- Stops should be **tight** — moves that look like they're breaking out usually aren't.
- Be willing to *fade extension* into known magnet strikes (top-OI walls, gamma magnets).

**Practical filter:**
- Net GEX > +$2B (or whichever threshold Zion lands on during validation) AND
- Current price is between top call-side magnet and top put-side magnet
- → trade *toward* the nearest magnet from current price, with tight stop beyond it.

**Anti-pattern:** Chasing breakouts on positive-gamma days. Dealer flow will fade you. Even if the move *feels* strong, look for the magnet pull and fade.

**Cross-reference:** [[(C) ICT_Concepts_Synthesis]] — your existing draw-of-the-day work runs cleanly here; the regime classifier *boosts your win rate on existing setups* rather than introducing new ones.
```

Verification:

```bash
cd "$HOME/Desktop/AI Brain/03 Projects/TD Trades"
awk '/### 4.1/,/### 4.2/' "01 Refinement/(C) Microstructure_Lenses_Synthesis.md" | grep -qE "mechanics|scalping|Practical filter|Anti-pattern|Cross-reference" && echo "  ✓ 4.1 structure intact" || echo "  ✗ FIX 4.1"
```

Expected: ✓.

- [ ] **Step 5.2: Write subsection 4.2 — Negative Gamma Days = Chase Impulses**

Content checklist:

```markdown
### 4.2 Negative Gamma Days = Chase Impulses

**The mechanics:** When dealers are net short gamma (negative GEX), every move against them grows their gamma exposure → they must trade *with* the move to stay hedged. As price rises, dealers buy more; as price falls, they sell more. The systemic effect is **range expansion** — moves accelerate, sweeps run, momentum extends.

**What this means for your scalping:**
- Liquidity sweeps *run further than usual* — premature counter-trades get steamrolled.
- ICT order-block holds happen *less reliably* — breakouts break out and stay broken.
- Stops should be **wider** to give legitimate moves room.
- Be willing to *chase impulses* once displacement is confirmed — momentum is real.

**Practical filter:**
- Net GEX < −$1B (or Zion's threshold) AND
- Confirmed displacement on 5m chart (your existing ICT trigger)
- → enter on first pullback, hold for extension toward next OI wall or gamma magnet.

**Anti-pattern:** Fading extremes on negative-gamma days. The mean-reversion bias *does not apply* here. What looks like exhaustion is usually mid-trend.

**Cross-reference:** [[(C) ICT_Concepts_Synthesis]] — your liquidity-sweep work is **made for this regime**. Sweeps that would fail in positive gamma actually deliver in negative gamma. This is where the highest-conviction ICT trades live.
```

Verification: `awk '/### 4.2/,/### 4.3/'` + grep for "mechanics|scalping|Practical filter|Anti-pattern|Cross-reference".

- [ ] **Step 5.3: Write subsection 4.3 — Gamma Flip Level as Regime Line**

Content checklist:

```markdown
### 4.3 The Gamma Flip Level — Regime Line

**What it is:** The price level at which net dealer GEX flips from positive to negative. Above = positive-gamma regime (fade extremes). Below = negative-gamma regime (chase impulses). Service-defined: SpotGamma calls it the "Volatility Trigger." UW calls it the "Zero Gamma Level."

**Why it's the most important single number on the pre-market card:**
- It's the *regime classifier* — defines which tactic dominates today.
- A clean break-and-close across the flip is a regime change *for the rest of the session*.
- VIX often spikes when ES/NQ crosses the flip — confirms the regime change with vol expansion.

**Pre-market read:**
- Where is the flip vs current price? Above → buying support is structurally there; below → no dealer floor.
- How far is the flip from key OI walls? Flip *coincident* with a wall → exceptionally strong level.
- How wide is the "flip-pending zone" (±10% of zero GEX in absolute terms)? Narrow → regime is unstable, expect chop; wide → conviction in current regime.

**Intraday playbook:**
- If price is approaching the flip from above and showing momentum → reduce size, prepare for chase-regime entry on confirmed close-through.
- If price chops at the flip → no-trade zone; wait for direction.
- If price holds rejection at the flip and reverses → regime *defends*; high-conviction continuation in the existing regime tactic.

**Cross-reference:** This level often sits at or near an ICT "premium/discount" boundary or a key liquidity pool. When they overlap, the trade conviction compounds.
```

Verification: grep for "What it is|Why it's the most important|Pre-market read|Intraday playbook|Cross-reference".

- [ ] **Step 5.4: Write subsection 4.4 — Layering Regime onto ICT (The Connective Tissue)**

Content checklist:

```markdown
### 4.4 Layering Regime onto ICT — The Connective Tissue

This is the load-bearing insight of Part 4 and possibly the entire document:

> **The regime classifier is a multiplier on your existing ICT setups, not a replacement.**

Concretely, every ICT setup you currently trade gets a regime-modifier applied:

| ICT Setup | Positive-Gamma Modifier | Negative-Gamma Modifier |
|---|---|---|
| FVG fill | High-quality, tight stops | Lower hit-rate, wider stops needed |
| Liquidity sweep & reverse | Fades quickly to mean | Runs further; sometimes doesn't reverse |
| Order block hold | More reliable as bounce | Less reliable; OB can fail |
| MSS / BOS chase | Often a fakeout, fade it | Often real, chase with size |
| Draw-of-the-day reach | Reaches but rarely overshoots | Reaches and overshoots; manage exits |

**This is why the synthesis matters:** without the regime classifier, you trade the same setup the same way every day — and on the wrong regime, the same setup has *opposite expected value*. Regime + ICT is the integration.

**Operational protocol:**
1. Pre-market: read GEX → set regime → identify gamma flip as today's regime invalidation.
2. Pre-bell: confirm with COT (week's tide) + IV surface (today's bias). If two agree with regime, conviction high. If one or both disagree, size down.
3. Intraday: take only your existing ICT setups, but *modify aggression per regime*. The setup library doesn't change. The position-sizing, stop-discipline, and target-discipline change.

**Validation questions for Zion** *(end-of-part roll-up — these are the highest-priority answers for the whole synthesis):*
- [ ] What's your gut-check on the regime-modifier table? Anything backwards based on your tape time?
- [ ] At what GEX threshold does the regime modifier *override* your existing ICT bias?
- [ ] On a flip-pending day (regime unstable), do you reduce size to your normal, or stop trading entirely?
- [ ] Do you trust this enough to log it as Gate-1 in the validation tagging from day 1, or do you want a 2-week soft-launch period first?
```

Verification: grep for "regime classifier is a multiplier|Operational protocol|Validation questions for Zion".

- [ ] **Step 5.5: Stage commit for Part 4**

```bash
cd "$HOME/Desktop/AI Brain/03 Projects/TD Trades"
git add "01 Refinement/(C) Microstructure_Lenses_Synthesis.md"
git commit -m "feat(synthesis): write Part 4 — Strategy Frame (mean reversion as regime tactic)"
```

---

### Task 6: Part 5 — Validation Questions (Consolidated Roll-Up)

**Files:**
- Modify: `01 Refinement/(C) Microstructure_Lenses_Synthesis.md` (replace Part 5 placeholder content)

- [ ] **Step 6.1: Write the consolidated validation-question checklist**

Content checklist:

```markdown
## Part 5 — Validation Questions (Consolidated)

The questions below are the same as those embedded per-lens in Parts 1-4. This roll-up gives you a single checklist you can work through in one sitting. As you answer one, mark it `- [x]` here *and* fill the answer inline in the lens-specific section.

### Dealer / Options Regime
- [ ] **1.1 GEX:** What's your GEX threshold for `POSITIVE_GAMMA` vs `FLIP_PENDING` vs `NEGATIVE_GAMMA`?
- [ ] **1.1 GEX:** How do you treat overnight GEX vs intra-day re-pricing?
- [ ] **1.1 GEX:** SpotGamma's "Vol Trigger" or your own zero-gamma level?
- [ ] **1.1 GEX:** What happens to your ICT setups on flip days?
- [ ] **1.2 Gamma profile:** Which strikes do you trust as magnets vs walls?
- [ ] **1.2 Gamma profile:** How do you distinguish "magnet" from "wall"?
- [ ] **1.2 Gamma profile:** Two magnets straddling current price — how do you handle?
- [ ] **1.3 0DTE:** How do you time the pin trade?
- [ ] **1.3 0DTE:** Gamma threshold for "high enough to pin"?
- [ ] **1.3 0DTE:** OPEX days vs daily-0DTE — different rules?
- [ ] **1.4 Vanna:** Which window do you prioritize?
- [ ] **1.4 Vanna:** Position for it, or let it run and react?
- [ ] **1.4 Vanna:** IV-rising morning — what's the play?
- [ ] **1.5 IV surface:** How do you measure "skew steepening"? Lookback?
- [ ] **1.5 IV surface:** Term inversion = veto or signal?
- [ ] **1.5 IV surface:** Interaction with COT positioning?
- [ ] **1.6 Options flow:** Trust threshold for following flow?
- [ ] **1.6 Options flow:** Conflicting flow (calls and puts both bought) — how to read?
- [ ] **1.6 Options flow:** Trade the underlying or the same options?

### Positioning Intel
- [ ] **2.1 COT:** Veto or just context?
- [ ] **2.1 COT:** What percentile threshold for "stretched"?
- [ ] **2.1 COT:** Commercials or large specs as primary read?
- [ ] **2.2 OI:** How far from current price before you ignore a wall?
- [ ] **2.2 OI:** Stack OI with gamma walls or treat separately?
- [ ] **2.2 OI:** OPEX-week behavior?
- [ ] **2.3 "Goldman PB":** Which aggregator do you trust most?
- [ ] **2.3 "Goldman PB":** Veto or just context?
- [ ] **2.3 "Goldman PB":** Conflicting narratives — how to resolve?

### Microstructure
- [ ] **3.1 Bookmap:** Planning to subscribe? At what trigger?
- [ ] **3.1 Bookmap:** What setups do you expect to validate first?
- [ ] **3.2 Free-substitute:** Already use CVD? At what timeframe?
- [ ] **3.2 Free-substitute:** TPO timeframe for your draw-of-the-day?
- [ ] **3.3 Subscription threshold:** At what monthly P/L baseline is Bookmap a no-brainer?

### Strategy Frame
- [ ] **4.4 Regime-modifier table:** Anything backwards based on tape time?
- [ ] **4.4 GEX threshold for ICT override:** Locked at?
- [ ] **4.4 Flip-pending day:** Size-down or no-trade?
- [ ] **4.4 Validation tagging:** Day 1 from synthesis, or 2-week soft launch?
```

Verification:

```bash
cd "$HOME/Desktop/AI Brain/03 Projects/TD Trades"
TOTAL=$(awk '/## Part 5/,/## Part 6/' "01 Refinement/(C) Microstructure_Lenses_Synthesis.md" | grep -c '^- \[ \]')
echo "Total validation questions: $TOTAL"
```

Expected: between 35 and 45 unchecked questions.

- [ ] **Step 6.2: Stage commit for Part 5**

```bash
cd "$HOME/Desktop/AI Brain/03 Projects/TD Trades"
git add "01 Refinement/(C) Microstructure_Lenses_Synthesis.md"
git commit -m "feat(synthesis): write Part 5 — consolidated validation-question roll-up"
```

---

### Task 7: Part 6 — Playbook Graduation Map

**Files:**
- Modify: `01 Refinement/(C) Microstructure_Lenses_Synthesis.md` (replace Part 6 placeholder content)

- [ ] **Step 7.1: Write the graduation map**

Content checklist:

```markdown
## Part 6 — Playbook Graduation Map

A lens lives here in **draft** until all 5 graduation gates pass. When they pass, it becomes a `02 Playbook/(C) <Lens_Name>.md` entry with codified rules. Recommended pacing: max 2 lenses graduate per week.

### Graduation gates (all must pass)

1. **Conceptual clarity** — all validation questions for this lens answered inline.
2. **Operational definition** — signal has a number/threshold attached (not "GEX gets low" — "GEX < −$1B").
3. **Tactical mapping** — known trade action this lens triggers / modifies / vetoes.
4. **Failure modes documented** — at least 2 specific lying scenarios listed.
5. **≥5 live observations** — seen in real time across 5+ sessions, tagged in journal.

### Status tracker

| Lens | Gate 1 (concept) | Gate 2 (operational) | Gate 3 (tactic) | Gate 4 (failure modes) | Gate 5 (5 obs) | Status |
|---|---|---|---|---|---|---|
| 1.1 GEX | ☐ | ☐ | ☐ | ☐ | ☐ | Draft |
| 1.2 Gamma profile | ☐ | ☐ | ☐ | ☐ | ☐ | Draft |
| 1.3 0DTE & pin | ☐ | ☐ | ☐ | ☐ | ☐ | Draft |
| 1.4 Vanna windows | ☐ | ☐ | ☐ | ☐ | ☐ | Draft |
| 1.5 IV surface | ☐ | ☐ | ☐ | ☐ | ☐ | Draft |
| 1.6 Options flow | ☐ | ☐ | ☐ | ☐ | ☐ | Draft |
| 2.1 CFTC COT | ☐ | ☐ | ☐ | ☐ | ☐ | Draft |
| 2.2 OI by strike | ☐ | ☐ | ☐ | ☐ | ☐ | Draft |
| 2.3 "Goldman PB" sub | ☐ | ☐ | ☐ | ☐ | ☐ | Draft |
| 3.1 Bookmap concepts | ☐ | ☐ | ☐ | ☐ | ☐ | Theoretical-pending-sub |
| 3.2 Free-sub order flow | ☐ | ☐ | ☐ | ☐ | ☐ | Draft |
| 4.x Strategy frame | ☐ | ☐ | ☐ | ☐ | ☐ | Draft |

### Graduation order recommendation

Start with the 3 lenses that have the highest expected EV given Zion's setup (paid options-flow service, ES/NQ scalp):

1. **1.1 GEX** — fastest to operationalize (single number, daily refresh) and biggest impact (defines regime).
2. **4.x Strategy frame** — operationalizes the gamma-ICT integration; depends on 1.1 being clear.
3. **1.3 0DTE & pin** — highest-value intraday setup in the 15:00-15:30 window.

Lower priority for early graduation (long lead-time data or theoretical-only):
- 2.1 COT (weekly cadence; takes 5+ weeks to get 5 observations)
- 3.1 Bookmap (no subscription)
- 2.3 "Goldman PB" (long-feedback-loop signal)
```

Verification:

```bash
cd "$HOME/Desktop/AI Brain/03 Projects/TD Trades"
ROWS=$(awk '/## Part 6/,/## Part 7/' "01 Refinement/(C) Microstructure_Lenses_Synthesis.md" | grep -cE '^\| [0-9]\.')
echo "Status-tracker rows: $ROWS"
```

Expected: 12 rows.

- [ ] **Step 7.2: Stage commit for Part 6**

```bash
cd "$HOME/Desktop/AI Brain/03 Projects/TD Trades"
git add "01 Refinement/(C) Microstructure_Lenses_Synthesis.md"
git commit -m "feat(synthesis): write Part 6 — playbook graduation map + status tracker"
```

---

### Task 8: Part 7 — Phase 3 Forward Look

**Files:**
- Modify: `01 Refinement/(C) Microstructure_Lenses_Synthesis.md` (replace Part 7 placeholder content)

- [ ] **Step 8.1: Write Phase 3 forward look**

Content:

```markdown
## Part 7 — Forward Look: Phase 3 (TradingAgents Code)

> **Status:** Sketch only. Phase 3 has its own future spec when the time comes. Listed here so synthesis content stays code-friendly.

### Likely analyst nodes (LangGraph)

| Node | Source data | Decision contribution |
|---|---|---|
| `GammaAnalyst` | Paid service API (UW / SpotGamma / Tradytics) | Regime call (POSITIVE / NEGATIVE / FLIP_PENDING) + key levels (flip, call wall, put wall) |
| `OptionsFlowAnalyst` | UW unusual-flow endpoint | Aggressive sweeps, dark-pool prints, block-vs-hedge classification |
| `FuturesPositioningAnalyst` | CFTC weekly + CME OI public data | Stretched-positioning flag + OI-wall gravity strikes |
| `IVSurfaceAnalyst` | yfinance + CBOE term-structure | Skew shift direction, term inversion flag |
| `MicrostructureAnalyst` *(deferred)* | Bookmap API (subscription required) | CVD, absorption, iceberg signals |

### Decisions deferred to Phase 3 spec

- **Paid-service vendor lock-in** — which API the GammaAnalyst and OptionsFlowAnalyst depend on. Affects rate limits, cost, and data shapes.
- **Researcher-debate-room integration** — do these analysts get their own bull/bear voices in the debate, or do they augment the existing Technical analyst?
- **Backtesting** — historical gamma data is expensive; do we cache CFTC weekly back N years? How long?
- **Caching strategy** — paid-API calls are not free; per-day-per-symbol cache with 1-day TTL is the likely default.

### What the synthesis must do to enable Phase 3

Every lens in this synthesis has:
- An explicit enum-shaped `Signal interpretation` (e.g. `POSITIVE_GAMMA` / `NEGATIVE_GAMMA` / `FLIP_PENDING`). These map 1:1 to Python enums.
- An explicit `Data source` URL or service. These map to Python data-fetch modules.
- An explicit `Refresh cadence`. This maps to cache TTL.
- `Failure modes` that map to unit-test cases (e.g. "GEX distorted around quad-witching" → test that asserts GammaAnalyst flags quad-witching weeks).

Once Zion completes the validation questions, those answers become additional test cases.
```

Verification:

```bash
cd "$HOME/Desktop/AI Brain/03 Projects/TD Trades"
awk '/## Part 7/,/^---/' "01 Refinement/(C) Microstructure_Lenses_Synthesis.md" | grep -qE "Likely analyst nodes|Decisions deferred|What the synthesis must do" && echo "  ✓ Part 7 structure intact" || echo "  ✗ FIX Part 7"
```

Expected: ✓.

- [ ] **Step 8.2: Stage commit for Part 7**

```bash
cd "$HOME/Desktop/AI Brain/03 Projects/TD Trades"
git add "01 Refinement/(C) Microstructure_Lenses_Synthesis.md"
git commit -m "feat(synthesis): write Part 7 — Phase 3 forward look"
```

---

### Task 9: Synthesis polish — Executive Summary, Framework section, ToC, cross-links

**Files:**
- Modify: `01 Refinement/(C) Microstructure_Lenses_Synthesis.md` (replace Executive Summary + "How These Lenses Plug" content)

- [ ] **Step 9.1: Write the Executive Summary**

Replace `[~150-250 words. Cover: ...]` placeholder with actual prose.

Content:

```markdown
## Executive Summary

This document layers eleven market-analysis lenses onto your existing ICT/Smart Money Concepts framework. It is *not* a replacement for the ICT synthesis — it's a regime-and-positioning context layer that *modifies how you trade your existing setups*.

**What it covers:**
- **Dealer / Options regime (Tier-1 priority):** Net gamma exposure, dealer gamma profile, 0DTE pin dynamics, vanna flow windows, IV surface, options-flow tape.
- **Positioning intel:** CFTC COT, OI by strike, "Goldman PB" realistic substitute.
- **Microstructure:** Bookmap concepts (theoretical until subscription), free-substitute order flow, honest caveats.
- **Strategy frame:** Mean reversion reframed as the positive-gamma-regime tactic alongside the negative-gamma chase tactic. *This is the connective tissue.*

**Three honest caveats baked in:**
1. **"Goldman PB data" is not accessible publicly.** The substitute is BofA Hartnett Flow Show + public Goldman commentary + Twitter aggregators. We don't pretend otherwise.
2. **Microstructure stays theoretical** until Bookmap (or equivalent L2) subscription. The conceptual framework still applies; the real-time confirmation does not.
3. **Mean reversion is a regime tactic, not a separate strategy.** It's the positive-gamma-day tactic layered onto your liquidity-hunting work.

**Reading order:**
1. Read this Executive Summary + "How These Lenses Plug Into Your Existing Framework" (next section).
2. Skim Parts 1-4 to understand the lens family.
3. **Most important:** read **Part 4** — that's where regime classifier × ICT integration lives.
4. Work through Part 5 (validation questions) over time. Don't try to answer them all in one sitting.
5. Use Part 6 graduation map as your operational checklist.

**Sister doc:** [[(C) ICT_Concepts_Synthesis]] is the methodological foundation; this doc is the institutional-positioning overlay.

**Knowledge graph link:** [[(C) Knowledge_Graph_Master]] — this document sits at the State/Context layer (L2-L3). *Insertion point requires Zion's approval before any KG edit.*
```

- [ ] **Step 9.2: Write the "How These Lenses Plug" section**

Replace `[~200-300 words. Cover: ...]` placeholder.

Content:

```markdown
## How These Lenses Plug Into Your Existing Framework

You're an ES/NQ scalper (1m/5s execution, 5-30 min holds) operating ICT/SMC methodology — liquidity hunting, draw-of-the-day, FVG fills, MSS/BOS confirmations. These eleven lenses don't compete with that. They *contextualize* it.

**The integration in one sentence:**

> Read GEX before the bell → set today's regime → adjust how aggressively you trade your existing ICT setups → use OI walls and gamma magnets as enhanced target levels → fill in the day's narrative with COT (weekly) and flow (Sunday-night).

**Mapping into the 10-Layer Knowledge Graph (your existing framework):**

| KG Layer | Existing role | What this synthesis adds |
|---|---|---|
| L1 — Edge / Thesis | Liquidity hunting | *No change* — liquidity hunting still the edge. The regime classifier modulates how it's expressed. |
| L2 — State | Order flow, SMT divergence | + Dealer gamma regime + IV surface state |
| L3 — Context | (existing context) | + COT positioning + BofA Flow narrative |
| L4-L7 — (existing layers) | (your setups) | Setups don't change. Regime modifier alters position size / stop discipline / target selection. |
| L8-L10 — (execution, journaling, review) | (existing) | + Lens-attribution tagging on every trade. + Weekly regime-call accuracy scoring. |

**What changes about your daily workflow:**
- **Sunday 18:00-22:00 ET:** 30-min ritual — ingest BofA Flow Show + Goldman public + weekly COT. Updates *background tide*.
- **Pre-market (~30 min before bell):** Read GEX + gamma flip + key OI walls + IV state. Commit to a one-sentence regime call on the pre-market card. Updates *today's frame*.
- **Intraday:** Trade your existing ICT setups. Modify aggression per regime. Tag every trade with the lens(es) that supported it.
- **Post-close:** Score the regime call (right/wrong) on the pre-market card. Note any surprises in `00 Notes/(C)lessons.md`.

**What does NOT change:**
- Your setup library.
- Your draw-of-the-day work.
- Your liquidity-hunting thesis.
- The 10-Layer Knowledge Graph structure.
```

- [ ] **Step 9.3: Insert a table of contents at the top of the document**

Insert immediately after the existing top-of-file metadata block (after `> **Sister doc:** [[(C) ICT_Concepts_Synthesis]] ...`), before `## Executive Summary`:

```markdown
---

## Table of Contents
- [Executive Summary](#executive-summary)
- [How These Lenses Plug Into Your Existing Framework](#how-these-lenses-plug-into-your-existing-framework)
- [Part 1 — Dealer / Options Regime](#part-1--dealer--options-regime-tier-1-priority-for-esnq-scalp)
  - [1.1 GEX](#11-net-gamma-exposure-gex--daily-framing)
  - [1.2 Dealer Gamma Profile](#12-dealer-gamma-profile-by-strike--magnet--repel-levels)
  - [1.3 0DTE & Pin](#13-0dte--pin-dynamics)
  - [1.4 Vanna Windows](#14-vanna-flow-windows)
  - [1.5 IV Surface](#15-implied-volatility-surface--skew-shift-as-leading-indicator)
  - [1.6 Options Flow](#16-options-flow-tape--blocks-sweeps-dark-pools)
- [Part 2 — Positioning Intel](#part-2--positioning-intel)
  - [2.1 CFTC COT](#21-cftc-cot--commitments-of-traders)
  - [2.2 OI by Strike](#22-open-interest-by-strike--gravity-walls)
  - [2.3 "Goldman PB" Substitute](#23-goldman-pb-realistic-substitute)
- [Part 3 — Microstructure](#part-3--microstructure-theoretical-until-bookmap-subscription)
  - [3.1 Bookmap Concepts](#31-bookmap-concepts--heatmap-iceberg-absorption)
  - [3.2 Free-Substitute Order Flow](#32-free-substitute-order-flow)
  - [3.3 What's Noise Without Bookmap](#33-whats-actually-noise-without-bookmap)
- [Part 4 — Strategy Frame: Mean Reversion as Regime Tactic](#part-4--strategy-frame-mean-reversion-as-regime-tactic) **← load-bearing section**
- [Part 5 — Validation Questions (Consolidated)](#part-5--validation-questions-consolidated)
- [Part 6 — Playbook Graduation Map](#part-6--playbook-graduation-map)
- [Part 7 — Forward Look: Phase 3](#part-7--forward-look-phase-3-tradingagents-code)

---
```

- [ ] **Step 9.4: Verify file size and structure**

```bash
cd "$HOME/Desktop/AI Brain/03 Projects/TD Trades"
FILE="01 Refinement/(C) Microstructure_Lenses_Synthesis.md"
echo "Size: $(wc -c < "$FILE") bytes"
echo "Parts: $(grep -c '^## Part ' "$FILE")"
echo "Lens subsections: $(grep -c '^### ' "$FILE")"
echo "Validation question checkboxes: $(grep -c '^- \[ \]' "$FILE")"
echo "Tables: $(grep -c '^|' "$FILE")"
```

Expected:
- Size between 28,000 and 45,000 bytes
- Parts: 7
- Lens subsections: 16
- Validation checkboxes: 35-50
- Tables: significant count (gamma profile, COT, regime modifier, graduation map, Phase 3) — should be 30+ table rows

- [ ] **Step 9.5: Stage commit for synthesis polish**

```bash
cd "$HOME/Desktop/AI Brain/03 Projects/TD Trades"
git add "01 Refinement/(C) Microstructure_Lenses_Synthesis.md"
git commit -m "polish(synthesis): exec summary, framework-integration section, ToC"
```

---

### Task 10: Pre-Market Lens Card template

**Files:**
- Create: `07 Outputs/(C) Pre_Market_Lens_Card.md`

This is the Phase 2 deliverable. Template-only — daily fills happen later (manually for now; auto-populated by TradingAgents nodes in Phase 3).

- [ ] **Step 10.1: Create the pre-market card template file**

File content:

````markdown
# (C) Pre_Market_Lens_Card — [YYYY-MM-DD]

> **Usage:** Copy this template each morning to `07 Outputs/(C) Pre_Market_Lens_Card_YYYY-MM-DD.md` and fill in. Target: 15-minute morning ritual. The Sunday-night addendum (Section 7) is filled only on Sundays.
>
> **Source-of-truth for lens definitions:** [[(C) Microstructure_Lenses_Synthesis]]

---

## TODAY'S READ
> *(One sentence. Regime call + bias + key invalidation level. Forced commitment before scanning the rest.)*
>
> Example: *"Positive gamma above 5860 / regime flips negative below 5840 / vanna window at 14:00. Bias: fade extremes intraday; chase only on flip-level break with conviction."*

---

## 1 ⋅ Regime (Dealer Gamma)

| Metric | Value | Implication |
|---|---|---|
| Net GEX | | POSITIVE / NEGATIVE / FLIP_PENDING |
| Gamma flip level | | Today's regime line |
| Call wall (top magnet) | | Upside gravity / resistance |
| Put wall (top magnet) | | Downside gravity / support |
| Implied 1d range | ±    pts | From IV term structure |

**Lens reference:** [[(C) Microstructure_Lenses_Synthesis#1.1 Net Gamma Exposure]], [[(C) Microstructure_Lenses_Synthesis#1.2 Dealer Gamma Profile]]

---

## 2 ⋅ 0DTE & Options Flow (Yesterday Close → Overnight)

- **0DTE positioning skew:** *(call-skewed / put-skewed / balanced)*
- **Largest sweeps overnight (premium > $100K):**
  - 
- **Block prints (institutional, timestamped):**
  - 
- **Dark-pool prints:**
  - 

**Lens reference:** [[(C) Microstructure_Lenses_Synthesis#1.3 0DTE]], [[(C) Microstructure_Lenses_Synthesis#1.6 Options Flow]]

---

## 3 ⋅ Positioning Context

| Source | Latest | Read |
|---|---|---|
| COT (last Fri close) | | Stretched / Neutral / Counter |
| OI walls ES | | Confluence with gamma walls? |
| Hartnett Flow* | *(Mon-am if BofA dropped)* | Bull / Bear / Mixed |
| Goldman public | *(Sun-night Hatzius if available)* | Theme |

*Reminder: BofA Flow Show + public Goldman — **NOT** actual Goldman PB data.*

**Lens reference:** [[(C) Microstructure_Lenses_Synthesis#2.1 CFTC COT]], [[(C) Microstructure_Lenses_Synthesis#2.2 Open Interest]], [[(C) Microstructure_Lenses_Synthesis#2.3]]

---

## 4 ⋅ Volatility State

- **VIX level:**         → vanna-window aggressiveness: AGGRESSIVE / MODERATE / LATENT
- **Term structure:** contango / backwardation / flat
- **Skew direction:** steepening / flattening / stable
- **IV-rank ES:**         %ile

**Lens reference:** [[(C) Microstructure_Lenses_Synthesis#1.5 Implied Volatility Surface]]

---

## 5 ⋅ Today's Time Map (ET)

- 09:30 — Open (first liquidity sweep — ICT framework)
- 10:00 — Vanna window #1
- 14:00 — Vanna window #2 (typically highest impact)
- 15:30 — 0DTE pin pressure / closing imbalance
- 16:00 — Close

**Today's key intraday events:** *(FOMC, CPI, Fed-speak, earnings if mega-cap)*
- 

---

## 6 ⋅ Today's Plan (ICT × Regime)

- **HTF bias** *(from daily / 4H read):*
- **Draw of the day** *(liquidity objective):*
- **Regime modifier:**
  - *POSITIVE_GAMMA* → tight stops, fade extremes toward magnets
  - *NEGATIVE_GAMMA* → wider stops, chase confirmed displacement
  - *FLIP_PENDING* → smaller size, wait for confirmation
- **Invalidation:** *(price level + behaviour that flips today's regime call)*

**Lens reference:** [[(C) Microstructure_Lenses_Synthesis#4 Strategy Frame]] — the connective tissue.

---

## 7 ⋅ Sunday-Night Addendum *(Sunday only — skip on other weekdays)*

- **BofA Flow Show summary:**
  - 
- **Week-ahead catalysts:**
  - FOMC:
  - NFP / CPI:
  - Mega-cap earnings:
- **Cross-asset signals:**
  - DXY trend:
  - 10Y yield direction:
  - Oil / commodities:

---

## End-of-Day Scoring *(filled at close)*

- **Was the regime call right?** ☐ Yes ☐ No ☐ Partial (explain)
- **Which lenses earned their keep today?** *(comma-separated tags: gamma+, 0DTE-pin, vanna-14, cot-stretch, etc.)*
- **Any surprises?** *(if yes, log to `00 Notes/(C)lessons.md`)*
````

- [ ] **Step 10.2: Verify card template structure**

```bash
cd "$HOME/Desktop/AI Brain/03 Projects/TD Trades"
FILE="07 Outputs/(C) Pre_Market_Lens_Card.md"
test -f "$FILE" && echo "FILE_OK"
echo "Sections: $(grep -c '^## ' "$FILE")"
echo "Lens references: $(grep -c 'Microstructure_Lenses_Synthesis' "$FILE")"
```

Expected: `FILE_OK`, 7-9 sections (TODAY'S READ + 7 numbered + end-of-day scoring), 5+ lens references.

- [ ] **Step 10.3: Stage commit for pre-market card template**

```bash
cd "$HOME/Desktop/AI Brain/03 Projects/TD Trades"
git add "07 Outputs/(C) Pre_Market_Lens_Card.md"
git commit -m "feat(card): pre-market lens card template (Phase 2 deliverable)"
```

---

### Task 11: Final integration verification

**Files:**
- Read-only checks across both new files.

- [ ] **Step 11.1: Render both files in Obsidian to verify visual integrity**

Manual step:
1. Open Obsidian to AI Brain vault.
2. Navigate to `03 Projects/TD Trades/01 Refinement/(C) Microstructure_Lenses_Synthesis.md`.
3. Verify: ToC renders, all wiki-links resolve (no broken `[[]]`), tables format correctly, headings nest properly.
4. Navigate to `03 Projects/TD Trades/07 Outputs/(C) Pre_Market_Lens_Card.md`.
5. Verify: section headings render, lens-reference wiki-links resolve back into the synthesis.

Expected: both files render clean. No red broken-link indicators.

- [ ] **Step 11.2: Run a final completeness scan against the spec**

```bash
cd "$HOME/Desktop/AI Brain/03 Projects/TD Trades"
SYN="01 Refinement/(C) Microstructure_Lenses_Synthesis.md"
CARD="07 Outputs/(C) Pre_Market_Lens_Card.md"

echo "=== Spec coverage check ==="
echo "Synthesis size: $(wc -c < "$SYN") bytes (target: 28-45 KB)"
echo "Card size: $(wc -c < "$CARD") bytes (target: 4-8 KB)"
echo ""
echo "Synthesis structure:"
echo "  - Parts: $(grep -c '^## Part ' "$SYN") (expected: 7)"
echo "  - Lens subsections: $(grep -c '^### ' "$SYN") (expected: 16)"
echo "  - Validation questions: $(grep -c '^- \[ \]' "$SYN") (expected: 35-50)"
echo "  - Failure-mode sections: $(grep -c 'Failure modes' "$SYN") (expected: 9+ — one per lens with template)"
echo ""
echo "Cross-links:"
echo "  - References to ICT synthesis: $(grep -c 'ICT_Concepts_Synthesis' "$SYN") (expected: 3+)"
echo "  - References to Knowledge Graph: $(grep -c 'Knowledge_Graph_Master' "$SYN") (expected: 1+)"
echo "  - Card references back to synthesis: $(grep -c 'Microstructure_Lenses_Synthesis' "$CARD") (expected: 5+)"
echo ""
echo "Honesty caveats present in synthesis:"
grep -c 'BofA' "$SYN" | xargs echo "  - BofA Flow Show references:"
grep -c 'theoretical' "$SYN" | xargs echo "  - 'theoretical' (Bookmap caveat) mentions:"
grep -c 'regime tactic' "$SYN" | xargs echo "  - 'regime tactic' mentions (mean rev reframe):"
```

Expected: all numbers within tolerance. If any are below target, return to the relevant Task and add coverage.

- [ ] **Step 11.3: Capture acceptance criteria status**

Update spec acceptance criteria. Open `docs/superpowers/specs/(C) Microstructure_Lenses_Design.md` and mark Section 10 checkboxes:

```markdown
- [x] Zion approves all five design sections. **Approved 2026-05-22.**
- [x] This spec written, committed, self-reviewed. **Done.**
- [x] Zion reviews the committed spec file and signs off. **Approved 2026-05-22 with "write the plan."**
- [x] Spec hands off to `superpowers:writing-plans` for the implementation plan. **Done.**
```

Add a new section at the end of the spec:

```markdown
---

## 12. Implementation status

**Plan file:** `docs/superpowers/plans/(C) Microstructure_Lenses_Implementation_Plan.md`
**Implementation start date:** [fill at Task 1 start]
**Implementation complete date:** [fill at Task 11 complete]
**Files produced:**
- [x] `01 Refinement/(C) Microstructure_Lenses_Synthesis.md`
- [x] `07 Outputs/(C) Pre_Market_Lens_Card.md`
**Files NOT modified (per spec non-goals):**
- [x] `01 Refinement/(C) Knowledge_Graph_Master.md`
- [x] `01 Refinement/(C) ICT_Concepts_Synthesis.md`
**Validation question completion:** [fill as Zion answers — track count of [x] vs [ ] in Part 5]
**Lenses graduated to playbook:** 0 / 12 (pending live-observation gates)
```

- [ ] **Step 11.4: Stage final commit**

```bash
cd "$HOME/Desktop/AI Brain/03 Projects/TD Trades"
git add "docs/superpowers/specs/(C) Microstructure_Lenses_Design.md"
git commit -m "docs(spec): mark implementation status complete"
```

---

## Plan completion checklist

When all tasks pass:
- [ ] Synthesis file exists, sized appropriately, structurally complete.
- [ ] Card template file exists, structurally complete.
- [ ] All cross-links resolve in Obsidian.
- [ ] Spec acceptance criteria marked complete.
- [ ] Zion notified that synthesis is ready for him to start answering validation questions.

**Next steps for Zion (outside this plan):**
1. Pick a paid options-flow vendor (UW / SpotGamma / Tradytics) — affects future Phase 3 spec.
2. Start answering validation questions in Part 5 of the synthesis. No urgency; one lens per session is fine.
3. Begin lens-attribution tagging in trade journal (tag every trade with lens(es) that supported it).
4. After 5+ live observations of a lens, graduate it to `02 Playbook/`.
5. When ready, kick off Phase 2 (start using the pre-market card daily).
6. When vault material is solid + paid-vendor chosen, brainstorm Phase 3 (TradingAgents code).

---

## Self-review pass

**Spec coverage:** All spec sections have implementing tasks. §3 (synthesis structure) → Tasks 1, 2-9. §4 (pre-market card) → Task 10. §5 (graduation rules) → Task 7. §6 (validation) → Task 6. §7 (Phase 3 sketch) → Task 8. §8 (risks) → flagged in synthesis exec summary (Task 9). §9 (phase plan) → covered in execution sequencing. §10 (acceptance criteria) → Task 11. §11 (open questions) → flagged in synthesis cross-references; not blocking.

**Placeholder scan:** All task content checklists list specific topics, specific terminology, specific signal enums. No "TBD" or "TODO" in tasks. Verification commands are runnable.

**Type consistency:** Signal enums used consistently across all lenses (`POSITIVE_GAMMA`, `NEGATIVE_GAMMA`, `FLIP_PENDING`, `OI_WALL_SUPPORT`, etc.). Lens-template field names identical across all task references. File paths consistent: `01 Refinement/(C) Microstructure_Lenses_Synthesis.md` and `07 Outputs/(C) Pre_Market_Lens_Card.md` everywhere.

**Adapted for non-code work:** TDD red/green replaced with template-conformance grep checks. Each task still produces a self-contained, commit-ready change. Frequent commits preserved.
