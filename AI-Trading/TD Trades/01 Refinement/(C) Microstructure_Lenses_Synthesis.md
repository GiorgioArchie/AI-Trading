# Microstructure & Positioning Lenses — Synthesis & Playbook Mapping

> **Status:** Draft — Zion fills validation questions inline as he works through each lens.
> **Source spec:** [[(C) Microstructure_Lenses_Design]]
> **Sister doc:** [[(C) ICT_Concepts_Synthesis]] (the existing methodology this layers onto)

---

## Table of Contents
- [Executive Summary](#executive-summary)
- [How These Lenses Plug Into Your Existing Framework](#how-these-lenses-plug-into-your-existing-framework)
- [Part 1 — Dealer / Options Regime](#part-1--dealer--options-regime-tier-1-priority-for-esnq-scalp)
  - [1.1 Net Gamma Exposure (GEX)](#11-net-gamma-exposure-gex--daily-framing)
  - [1.2 Dealer Gamma Profile](#12-dealer-gamma-profile-by-strike--magnet--repel-levels)
  - [1.3 0DTE & Pin Dynamics](#13-0dte--pin-dynamics)
  - [1.4 Vanna Flow Windows](#14-vanna-flow-windows)
  - [1.5 IV Surface](#15-implied-volatility-surface--skew-shift-as-leading-indicator)
  - [1.6 Options Flow Tape](#16-options-flow-tape--blocks-sweeps-dark-pools)
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

---

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

---

## Part 1 — Dealer / Options Regime *(Tier-1 priority for ES/NQ scalp)*

### 1.1 Net Gamma Exposure (GEX) — Daily Framing

**What it is:** Net dealer gamma position across all SPX/SPY options, summed by strike and expressed in dollars per 1-point spot move. Positive GEX means dealers are net long gamma — they sell into rallies and buy dips to stay hedged. Negative GEX means dealers are net short gamma — they buy strength and sell weakness, amplifying every move.

**Why it matters for ES/NQ scalp:** GEX sign defines the regime before the bell rings. Positive GEX days compress range and reward fading extremes; negative GEX days expand range and reward chasing impulses. ES tracks SPX dealer flow nearly 1:1 intraday, so this is the single most important pre-bell read for sizing and setup selection.

**Data source:**
- SpotGamma daily "Volatility Trigger" + "Net GEX" (paid)
- Unusual Whales gamma exposure view (paid, included in your subscription)
- Tradytics GEX dashboard (paid alternative)
- Free crude approximation: scrape CBOE OI by strike, multiply by ATM gamma estimate

**Refresh cadence:** Pre-market daily. Data is stale ~30min after prior close; the pre-bell read is best.

**Signal interpretation:**
- `POSITIVE_GAMMA` — net GEX > 0; range compression, fade extremes, sell rips / buy dips inside the day's range
- `NEGATIVE_GAMMA` — net GEX < 0; range expansion, chase impulses, momentum continuation favored
- `FLIP_PENDING` — net GEX within ~10% of zero; regime unstable, size down, expect false signals from both sides

**Validation questions for Zion:**
- [ ] What's your specific GEX threshold for calling a day `POSITIVE_GAMMA` vs `FLIP_PENDING`? (dollar value or percentile vs trailing 20d)
- [ ] When GEX flips overnight, do you trust the new sign immediately at open or wait for the first 30min to confirm?
- [ ] Do you use SpotGamma's published Vol Trigger as your zero-gamma reference, or compute your own from UW raw data?
- [ ] On flip days, do your ICT setups (FVG fills, MSS) still work or do you stand aside?
- [ ] How does your position size scale with |GEX| magnitude — fixed, linear, or stepped tiers?

**Playbook mapping target:** `02 Playbook/(C) GEX_Regime_Framing.md`

**Failure modes / when this lens lies:**
- Quad-witching weeks (March/June/Sept/Dec 3rd Friday) distort GEX badly — values can flip artificially as quarterly OI rolls. Discount the read for the full week leading into it.
- Late-session GEX shifts materially as 0DTE volume reshapes the profile. The pre-bell read degrades after 14:00 ET; don't trade the close off a morning number.

### 1.2 Dealer Gamma Profile by Strike — Magnet & Repel Levels

**What it is:** Gamma exposure distributed strike-by-strike rather than aggregated. The profile shows where dealer hedging concentrates and produces two distinct behaviors: **magnets** (strikes that attract price as dealers hedge into them) and **walls** (strikes that repel price as dealers defend them). The same gamma sign can produce either behavior depending on distance from spot — a strong call-gamma strike near current price acts as a magnet; the same strike far above spot acts as a wall. The chart is the day's intraday gravity map.

**Why it matters for ES/NQ scalp:** Trading toward a top-magnet strike has materially higher hit rate than trading away from one. Top magnets work as natural profit targets for 5-30 min holds. Charm decay reshapes the profile through the session, so a strike that was a wall at 09:30 may become a magnet by 13:00.

**Data source:**
- SpotGamma daily gamma profile chart (paid)
- UW gamma exposure by strike (paid, in your subscription)
- Tradytics gamma chart (paid alternative)
- Free crude: CBOE OI table → strike-by-strike gamma via Black-Scholes approximation

**Refresh cadence:** Pre-market read + mandatory mid-session re-read. Charm decay shifts the profile materially by 12:00 ET.

**Signal interpretation:** Identify top-3 call-side and top-3 put-side strikes. Each is classified:
- `MAGNET` — price gravitates toward this strike; use as profit target when price is approaching it
- `WALL` — price struggles to penetrate without fresh flow; use as fade level or stop reference

**Validation questions for Zion:**
- [ ] Which strikes do you actually trust as magnets — only the #1 by gamma, or do you weight the top 3?
- [ ] How do you distinguish a magnet from a wall when both are dealer-positive gamma? (open interest? distance from spot? recent flow into that strike?)
- [ ] When two magnets straddle current price within 0.5%, which side do you favor and why?
- [ ] Do you trade strikes from SPX gamma profile or convert them to ES levels (SPX × 0.1 + basis)?
- [ ] What's your rule for invalidating a magnet mid-session if price approaches and rejects cleanly?

**Playbook mapping target:** `02 Playbook/(C) Gamma_Strike_Profile.md`

**Failure modes / when this lens lies:**
- The profile lies overnight when no flow is moving it — early-bell action can dissolve a "wall" inside 15 minutes if size leans against it.
- Heavy 0DTE volume rebuilds the profile faster than daily snapshots reflect. By 14:00 ET the morning chart is stale; trading off it into the close is a known mistake.

### 1.3 0DTE & Pin Dynamics

**What it is:** Zero-days-to-expiry options. SPX prints daily 0DTE. As expiry approaches inside the 15:00-16:00 ET window, dealers' net delta exposure flips fast and forces hedging that pulls spot toward the strike with the highest gamma concentration. This is the "pin."

**Why it matters for ES/NQ scalp:** The 15:00-15:30 ET window is the most predictable scalp setup on positive-gamma days — price gets pulled toward the pin strike on rails. ES tracks SPX 1:1 here, so the trade is just "long ES toward pin" or "short ES toward pin" depending on where spot sits relative to the magnet.

**Data source:**
- UW 0DTE-specific flow filter (paid, in your subscription)
- SpotGamma "Hiro" or 0DTE positioning report (paid)
- Tradytics 0DTE dashboard (paid)
- Free: CBOE same-day-expiry OI by strike

**Refresh cadence:** Pre-market for positioning bias; live during the 14:00-16:00 ET window.

**Signal interpretation:**
- `PIN_LEVEL` — strike with highest 0DTE gamma; magnet for the 15:00-15:30 closing pull
- `0DTE_CALL_SKEWED` — call-side 0DTE notional dominates; telegraphs closing imbalance to the upside
- `0DTE_PUT_SKEWED` — put-side 0DTE notional dominates; telegraphs closing imbalance to the downside
- `0DTE_BALANCED` — call/put exposure roughly even; low usefulness, ignore as a signal that day

**Validation questions for Zion:**
- [ ] What's your entry trigger for the pin trade — do you wait for price to start gravitating, or position by 14:30?
- [ ] What minimum gamma concentration at a strike qualifies it as a "pin-able" level vs noise?
- [ ] How do you treat monthly OPEX Fridays differently from daily 0DTE — same playbook, smaller size, or stand aside?
- [ ] When skew is `0DTE_CALL_SKEWED` but spot is above the pin, do you fade toward the pin or trust the call skew?
- [ ] Do you pull the pin trade if VIX > a threshold? What threshold?

**Playbook mapping target:** `02 Playbook/(C) 0DTE_Pin_Dynamics.md`

**Failure modes / when this lens lies:**
- OPEX Fridays (3rd Fri monthly + quarterlies) — daily 0DTE positioning gets overwhelmed by monthly OI roll. The pin signal degrades.
- High-VIX days — vanna unwind dominates and overrides pin attempts. Spot wanders from the pin strike with no pull-back.
- FOMC / CPI / NFP days — macro flow drowns out 0DTE positioning entirely. The pin signal is unreliable; the lens lies most of these sessions.

### 1.4 Vanna Flow Windows

**What it is:** Vanna is the sensitivity of option delta to changes in implied volatility. When IV falls — common from open through mid-session — dealer net delta shifts and they buy underlying to stay hedged. This buying clusters at three predictable windows: ~10:00 ET (post-open IV crush), ~14:00 ET (post-lunch IV reset / institutional rebalance), ~15:30 ET (closing-rotation vol crush).

**Why it matters for ES/NQ scalp:** Those three windows are known dealer-bid moments — exploitable as long-bias entry timing on positive-gamma days. The pattern most traders miss: low-VIX days have under-appreciated vanna size; the moves at these windows are bigger than the headline VIX would suggest because the unwind is mechanically the same regardless of starting vol.

**Data source:**
- No direct data feed — read VIX/VVIX trajectory + IV term-structure shape
- UW intraday vol flow if visible in your subscription
- SpotGamma "Charm/Vanna model" if subscribed

**Refresh cadence:** Live during the three windows; pre-market for "expected size" estimate via VIX level and term-structure slope.

**Signal interpretation:**
- `VANNA_AGGRESSIVE` — VIX > 18; larger unwinds, headline windowed moves, size up
- `VANNA_MODERATE` — VIX 13-18; meaningful but not dramatic, normal sizing
- `VANNA_LATENT` — VIX < 13; still meaningful but quieter, easy to miss — set alerts on the three timestamps

**Validation questions for Zion:**
- [ ] Which of the three windows (10:00 / 14:00 / 15:30 ET) has the highest hit rate in your replay? Do you prioritize one?
- [ ] Do you position into the window pre-emptively (entry by 09:55) or wait for the window to start showing flow before entering?
- [ ] On IV-rising mornings, do you flip the trade (short into the window) or stand aside?
- [ ] What VIX level changes your sizing — do you actually trade larger on `VANNA_AGGRESSIVE` days?
- [ ] How long do you hold the vanna trade — to the window's end (~30min) or trail until structure breaks?

**Playbook mapping target:** `02 Playbook/(C) Vanna_Flow_Windows.md`

**Failure modes / when this lens lies:**
- IV-rising days (sell-off mornings) reverse the vanna sign — dealers sell instead of buy. Mechanically taking the long-bias entry on these days produces a clean losing trade.
- Holidays and shortened sessions break the timing of the three windows entirely; the EU-close and closing-rotation windows shift or vanish.
- Fed-day mornings — windowed flow gets washed out by macro positioning. The 10:00 window in particular becomes unreliable on FOMC.

### 1.5 Implied Volatility Surface — Skew Shift as Leading Indicator

**What it is:** The 3D shape of IV across strikes (skew) and expiries (term structure). Skew is put IV minus call IV at equidistant strikes. Term structure is front-month IV vs back-month IV. Shifts in this surface are leading indicators — hedge demand rises before price falls.

**Why it matters for ES/NQ scalp:** Surface shifts precede price moves by hours to days. Put-skew steepening over the last 30-90 min flags hedge demand building → distribution is incoming. Term inversion (front > back) signals macro stress and is reason to cut size. Both warnings fire before the move hits, which is exactly the signal type a 5-30 min scalp can act on.

**Data source:**
- yfinance for chain → compute skew (free, sufficient for daily read)
- CBOE term structure data (free)
- Volfeed / Tradier (paid, cleaner data if you graduate the lens)
- UW IV-rank dashboard (paid, in your subscription)

**Refresh cadence:** Pre-market + mandatory check at 14:00 ET. Mid-session shifts matter most.

**Signal interpretation:**
- `SKEW_STEEPENING` — put-skew widening over 30-90 min; distribution warning, bias defensive, fade longs
- `SKEW_FLATTENING` — put-skew narrowing; complacency / risk-on / trend continuation favored
- `TERM_INVERSION` — front-month > back-month IV; macro stress, reduce size, expect overnight gaps
- `TERM_CONTANGO` — normal upward-sloping term structure; carry-on environment, normal sizing

**Validation questions for Zion:**
- [ ] How do you measure "skew steepening" precisely — delta-25 vs delta-10 puts, what lookback window (30/60/90 min)?
- [ ] Do you treat `TERM_INVERSION` as a hard veto on longs or a sizing reduction?
- [ ] When skew and COT positioning disagree (e.g. skew flattening but COT shows record net long), which lens wins?
- [ ] Do you use skew shift to time exits on existing winners, or only for new-entry filtering?
- [ ] What's your threshold for "fast" steepening (X basis points in Y minutes) before you act on it?

**Playbook mapping target:** `02 Playbook/(C) IV_Surface_Skew_Shift.md`

**Failure modes / when this lens lies:**
- Earnings season distorts single-name skew; SPX/ES is less affected but still noisy in mega-cap-driven weeks (AAPL/NVDA/MSFT prints).
- Quarterly rebalance Mondays — skew jumps mechanically from put-roll demand, not from actual hedge appetite. The signal misfires.
- Low-OI strikes have noisy IV that contaminates skew calculations. Use mid-strike data only (delta 20-30 range) to keep the signal clean.

### 1.6 Options Flow Tape — Blocks, Sweeps, Dark Pools

**What it is:** Real-time large-print options trades, classified by execution style. Blocks are single-print, often negotiated off-exchange. Sweeps are urgent multi-exchange aggressive fills hitting the offer (or bid) across venues. Dark pools are off-exchange equity prints — meaningful here because they often pair with a same-time options trade as the hedge.

**Why it matters for ES/NQ scalp:** Aggressive ask-side sweeps with premium > $100K signal directional bets, not hedges. A cluster of same-direction sweeps stacking in a 10-15 min window is read-the-tape evidence of institutional positioning that ES/NQ will track within minutes to hours. This is the lens that catches the move before structure prints.

**Data source:**
- UW Premium (paid, in your subscription — primary)
- Tradytics flow / FlowAlgo (paid alternatives)
- Free: limited to none — institutional-grade only

**Refresh cadence:** Live during session; review the last hour each evening for next-day context.

**Signal interpretation:**
- `SWEEP_AGGRESSIVE` — ask-side, premium > $100K, single-symbol cluster; directional informed flow, follow it
- `BLOCK_HEDGING` — paired with equity dark-pool of opposite delta; it's a hedge, not a signal, ignore
- `BLOCK_DIRECTIONAL` — unpaired, premium > $500K, OTM strikes; institutional speculation — strongest single signal in this lens

**Validation questions for Zion:**
- [ ] What's your premium threshold for "trust this and follow it" — do you stick at $100K for sweeps or scale up by name liquidity?
- [ ] When you see conflicting flow (aggressive calls AND aggressive puts on the same name in the same hour) how do you read it — straddle hedge, indecision, or stand aside?
- [ ] Do you trade the underlying directly (ES/NQ) or take the same options the flow took?
- [ ] How long is your hold horizon when following a sweep cluster — minutes or hours?
- [ ] What's your invalidation — does the flow trade die if price doesn't move within X minutes of the cluster?

**Playbook mapping target:** `02 Playbook/(C) Options_Flow_Tape.md`

**Failure modes / when this lens lies:**
- Hedging trades look identical to directional trades on the tape without paired dark-pool data. False-positive rate is high — a $1M call sweep can be a delta hedge against a much larger short equity position you can't see.
- Index/ETF flow (SPY/QQQ) is often portfolio rebalancing rather than directional bet-taking. Sweeps in SPY are noisier than sweeps in individual names.
- End-of-day prints can be settlement or roll activity rather than new exposure. Discount tape signal in the final 15 minutes unless you can confirm new OI prints next morning.

---

## Part 2 — Positioning Intel

### 2.1 CFTC COT — Commitments of Traders

**What it is:** Weekly CFTC report released Friday 15:30 ET, snapshotting positioning as-of Tuesday close. Breaks futures open interest into trader categories — commercials (hedgers), large speculators (CTAs/funds), small speculators (retail). The disaggregated format further splits dealers, asset managers, leveraged funds, and other reportables. ES futures positioning is reported directly.

**Why it matters for ES/NQ scalp:** Sets the background regime tide for the week — defines whether intraday scalps are running WITH or AGAINST the underlying institutional positioning. Extreme readings are fadeable in 5-10 day swings, too slow to enter on but loud enough to bias direction. A stretched-long large-spec print means longs are crowded and headline pops will get sold; that's a green light for fade-shorts and a yellow light for breakout-longs.

**Data source:**
- `https://www.cftc.gov/MarketReports/CommitmentsofTraders/index.htm` (official, free)
- Free — no paid tier needed

**Refresh cadence:** Weekly — Friday post-close ingestion, read carries Mon–Fri.

**Signal interpretation:**
- `LARGE_SPEC_STRETCHED_LONG` — large specs > 80th %ile trailing 52w; mean-revert pressure builds, intraday longs face headwind
- `LARGE_SPEC_STRETCHED_SHORT` — large specs < 20th %ile; squeeze risk live, intraday shorts face headwind
- `COMMERCIAL_NET_FLIP` — commercial net position changes sign week-over-week; strongest divergence signal, regime change typically inside 1–2 weeks
- `BALANCED` — 30–70th %ile; no tide present, trade clean technicals without positioning bias

**Validation questions for Zion:**
- [ ] When COT says STRETCHED_LONG and your intraday setup says long, does the lens veto the trade, downsize it, or just sit as context?
- [ ] What percentile band do you consider "stretched" — strict 80/20, looser 70/30, or rolling z-score?
- [ ] Do you weight commercials or large specs as the primary read, and why?
- [ ] How do you reconcile a COT signal that disagrees with options skew (e.g. COT says stretched-long, skew says calls bid)?
- [ ] Friday-night ingestion vs Monday open — do you let weekend news override the read, or hold it?

**Playbook mapping target:** `02 Playbook/(C) CFTC_COT.md`

**Failure modes / when this lens lies:**
- 5-day reporting lag — Tuesday-close snapshot lands Friday-close, positioning can have shifted materially across CPI/FOMC/NFP weeks before you ever see it
- ES futures positioning is muddled by ETF arbitrage — institutions hedge SPY/QQQ creation/redemption flow via ES, so the raw net number mixes directional intent with mechanical hedging
- Holiday weeks publish Monday on a delayed schedule — disrupts the Friday-night ritual and the read effectively covers a 7+ day stale window
- CTA-heavy positioning prints can flip on a single trend-model threshold breach, faster than the weekly cadence shows

---

### 2.2 Open Interest by Strike — Gravity Walls

**What it is:** The count of open option contracts at each strike, broken out by call/put and expiry. The OI distribution surfaces where positioning concentrates — those concentrations act as gravity walls. ES options OI exists and is tradeable, but SPX options OI is the more behaviorally relevant read because dealer delta-hedging against SPX positioning is what physically pushes ES.

**Why it matters for ES/NQ scalp:** Top-OI strikes are gravity walls. On positive-gamma days price drifts toward them and struggles to penetrate without strong flow. Confluence with the day's top gamma magnet creates the highest-confidence levels for 5–30 min scalp targets — you know where price wants to sit and where it wants to reject.

**Data source:**
- CME public chain — `https://www.cmegroup.com/markets/equities/sp/e-mini-sandp500.quotes.options.html` for ES options
- CBOE chain for SPX options (the behaviorally dominant book)
- UW dashboard for filtered front-week / front-month view
- CME + CBOE free; UW paid (already subscribed)

**Refresh cadence:** Daily pre-market snapshot. Monthly OPEX week gets a second mid-day refresh.

**Signal interpretation:**
- `OI_WALL_RESISTANCE` — top call-OI strike sits near or just above current price; ceiling, fade-rejection setups favored
- `OI_WALL_SUPPORT` — top put-OI strike sits near or just below current price; floor, fade-rejection setups favored
- `OI_CONFLUENCE_WITH_GAMMA` — top OI strike = top gamma magnet; highest-conviction level of the day, full-size trades green-lit here
- `OI_DISTRIBUTED` — top strike's OI < 2× the next-rank strike; no dominant wall, lens contributes nothing usable that session

**Validation questions for Zion:**
- [ ] How far above/below current price does an OI wall have to sit before you stop respecting it (50 ES points? 100?)
- [ ] Do you stack OI walls with gamma walls into one combined level, or read them as separate signals that need to agree?
- [ ] On OPEX week, do you trust front-week OI through Thursday, or cut it off Wednesday close?
- [ ] When a wall gets broken intraday, how long before you accept the break vs treat it as a sweep?
- [ ] Do you weight SPX OI more than ES OI for the actual ES scalp decision?

**Playbook mapping target:** `02 Playbook/(C) Open_Interest_Walls.md`

**Failure modes / when this lens lies:**
- Stale OI from back-month contracts can dominate the raw chain without being behaviorally live — filter ruthlessly for current-month and front-week only
- Dealer-driven OI from systematic vol-selling programs doesn't behave like directional retail/institutional OI; same number on the screen, completely different gravitational pull
- OPEX-week OI degrades fast — by Friday morning much of the headline OI is already rolled, exercised early, or unwound through Thursday-night hedging
- A wall built from a single large block trade can vanish overnight if that desk unwinds; volume-weighted OI tells you whether the wall is structural or one-printer

---

### 2.3 "Goldman PB" Realistic Substitute

**What it is:** Goldman Sachs' actual Prime Brokerage flow data is institutional-only and not publicly accessible — no retail substitute reproduces it directly. The realistic public proxies that aggregate similar signal are: (a) BofA's monthly "Flow Show" by Michael Hartnett, which drops Sunday PM via leaked PDF screenshots, (b) Goldman's *public* market commentary from David Kostin (equity strategy) and Jan Hatzius (econ), and (c) Twitter aggregators (@unusual_whales, @SpotGamma, @ZeroHedge, @themarketear) screenshotting excerpts irregularly through the week.

**Why it matters for ES/NQ scalp:** Gives the *weekly narrative* — what institutional flows are positioning around, what themes the desks are pitching, where the conviction sits. Sets the conviction multiplier for trading aligned-with vs against-the-week's narrative. Pure background context, never an intraday signal — but it tells you whether to size up on bull setups or bear setups for the week.

**Data source:**
- BofA Flow Show — leaked PDF screenshots on Twitter Sunday 18:00–22:00 ET, occasionally Monday AM
- Goldman Hatzius / Kostin — goldmansachs.com/insights at publication; flow aggregators tweet excerpts Sunday night
- Aggregator accounts: @unusual_whales, @SpotGamma, @ZeroHedge, @themarketear
- Free (Twitter), paid (UW already covered, no incremental cost)

**Refresh cadence:** Sunday 18:00–22:00 ET — 30-minute ritual to ingest the week's narrative.

**Signal interpretation:**
- `FLOW_NARRATIVE_BULL` — BofA Flow Show + Goldman public skew both bullish on US equities; size up bull setups, downsize fade-shorts
- `FLOW_NARRATIVE_BEAR` — both lean bearish/defensive; size up fade-shorts and breakdown plays, downsize breakout-longs
- `FLOW_NARRATIVE_MIXED` — institutional opinion split between bulls and bears; no thumb on the scale, trade clean technicals at base size

**Validation questions for Zion:**
- [ ] Which of the four aggregators do you actually trust to relay the read faithfully vs cherry-pick for engagement?
- [ ] Does the narrative ever veto a trade, or only adjust size?
- [ ] When BofA and Goldman public skew disagree, which one wins your read?
- [ ] Holiday Sundays with no Flow Show drop — do you carry last week's read forward, or go to FLOW_NARRATIVE_MIXED by default?
- [ ] Have you ever profitably *faded* a strong consensus narrative? If so, what was the tell?

**Playbook mapping target:** `02 Playbook/(C) Institutional_Flow_Narrative.md`

**Failure modes / when this lens lies:**
- Hartnett and Kostin are wrong often enough that the narrative is a sentiment indicator, not edge — at extremes (everyone bullish, everyone bearish) the right move is sometimes to fade the consensus
- Twitter excerpts are out-of-context fragments cropped for engagement; easy to misread the actual qualifications and conditionals in the source PDF
- Skipped Sunday (holiday weekend, no drop) leaves a stale read carrying into Mon-Fri without anyone flagging that the input is missing
- Aggregator accounts have their own books and biases — screenshots are filtered through whatever position the account is talking

---

## Part 3 — Microstructure *(theoretical until Bookmap subscription)*

### 3.1 Bookmap Concepts — Heatmap, Iceberg, Absorption

**What it is:** Bookmap is L2 order-book visualization software. Heatmap renders limit-order density over time as a color gradient — thick yellow/red rows are stacked resting liquidity. Iceberg orders are hidden size that refills instantly when hit, the fingerprint of institutions defending a level without showing the full book. Absorption is aggressive market orders meeting a wall of limits without moving price — one side is being absorbed and a reversal usually follows.

**Why it matters for ES/NQ scalp:** This is the operational layer underneath the ICT institutional-flow thesis. Order blocks become *visible* as iceberg refills at the OB price; liquidity sweeps become visible as heatmap layers disappearing milliseconds before price runs the level. Without it, you're inferring institutional behavior from candles instead of watching it directly. **Currently theoretical for Zion until subscription.**

**Data source:**
- Bookmap subscription (~$100/mo)
- ES/NQ L2 feed routed through most futures brokers (Rithmic, CQG, AMP)

**Refresh cadence:** Real-time, scalp execution overlay (1m chart pairing, 5s confirmation).

**Signal interpretation:**
- `ICEBERG_REFILL_DETECTED` → institutional defense of a level. Bias: continuation while defender holds, reversal the moment refills stop.
- `ABSORPTION_AT_LEVEL` → aggressive flow eating into resting limits with zero price progress. Reversal precursor.
- `HEATMAP_WITHDRAWAL` → resting liquidity vanishes ahead of price. Precursor to a liquidity sweep through the level.

**Validation questions for Zion:**
- [ ] Do you plan to subscribe to Bookmap inside the $50k window, or after?
- [ ] What conviction level (P/L baseline, win-rate floor) unlocks the spend without it feeling like a hope-purchase?
- [ ] Which of your existing setups would you validate against Bookmap *first* to prove it adds edge?

**Playbook mapping target:** `02 Playbook/(C) Bookmap_Microstructure.md`

**Failure modes / when this lens lies:**
- Bookmap is a tool, not an edge. Bad reads come from interpretation, not from the data feed.
- Spoofing remains common in ES/NQ — large limit-order layers placed to fake intent then cancelled. ESMA/CFTC rules don't fully suppress it.
- 5s tick-level reads blur into noise. Bookmap reads cleanest on 1m–15m structure, not raw tick.

### 3.2 Free-Substitute Order Flow

**What it is:** Approximate order-flow signals from broadly-available tools, no Bookmap required. CVD (Cumulative Volume Delta) is a running sum of buy minus sell volume — shows whether moves are flow-supported or hollow. Volume Profile / TPO maps price distribution over time, surfacing high-volume nodes (magnets) and low-volume nodes (rejection zones). Footprint charts plot bid/ask volume at every price level, visible through TradingView Premium indicators.

**Why it matters for ES/NQ scalp:** Crude relative to L2, but real. CVD divergence — price making a new high while CVD fails to confirm — is the classic absorption tell and is accessible *today* without spending a dollar. TPO/Volume-Profile gives draw-of-the-day targets and chop zones that pair directly with ICT liquidity logic.

**Data source:**
- TradingView built-in CVD indicator (free)
- TradingView Volume Profile / VPVR (free basic, premium for session-anchored)
- TradingView Premium footprint indicators (paid, ~$15-60/mo)

**Refresh cadence:** Real-time during RTH session.

**Signal interpretation:**
- `CVD_DIVERGENCE_BEARISH` → price prints new highs, CVD fails to confirm. Absorption. Reversal precursor.
- `CVD_DIVERGENCE_BULLISH` → inverse. Bullish absorption at lows.
- `VP_HIGH_VOLUME_NODE` → price magnet and chop zone. Fade extensions back toward it.
- `VP_LOW_VOLUME_NODE` → rejection zone. Expect fast moves *through* the level, not into it.

**Validation questions for Zion:**
- [ ] Do you already run CVD on your TradingView ES/NQ charts, and if so on what timeframe?
- [ ] Which session anchor do you use for Volume Profile — RTH only, ETH, or weekly composite?
- [ ] At 1m/5s execution, does footprint add signal over plain CVD, or is it noise at your timeframe?

**Playbook mapping target:** `02 Playbook/(C) Free_Order_Flow.md`

**Failure modes / when this lens lies:**
- TradingView's CVD relies on trade-tick exchange classification that isn't perfect — small misclassifications compound over the session.
- Volume Profile is anchor-dependent. Wrong anchor (RTH vs ETH vs custom) gives wrong levels and wrong draws.
- Footprint at 5s tick interval is mostly noise. Bid/ask deltas need bars wide enough to mean something.

### 3.3 What's Actually Noise Without Bookmap

This section is intentionally short. It documents what microstructure concepts you should *not* try to chase without Bookmap or equivalent L2 data.

**Genuinely require Bookmap (or paid L2 feed):**
- Real-time iceberg detection — invisible without seeing limit-order refills
- Heatmap-based liquidity-withdrawal reads — invisible without limit-order book persistence over time
- Spoofing identification — invisible without order placement/cancellation history
- High-resolution absorption — visible-ish in CVD but L2 confirmation is what makes it tradeable

**Workable with free tools:**
- CVD divergence (TradingView)
- Volume profile / VPVR (TradingView)
- TPO market-profile structure (TradingView / Sierra Chart free tier)

**Recommendation:** Do not read ICT order-block material *as if* you have Bookmap data when you don't. The conceptual framework (institutional levels, displacement, OB validity) still applies — but the *real-time confirmation* requires the L2 feed. Until subscribed, treat OB-level entries as higher-risk than the ICT material's confidence implies.

**Threshold for subscribing:** [Validation question for Zion: at what monthly P/L baseline does $100/mo Bookmap become a no-brainer? Lock this number to avoid analysis-paralysis.]

---

## Part 4 — Strategy Frame: Mean Reversion as Regime Tactic

### 4.1 Positive Gamma Days = Fade Extremes

**The mechanics:** When dealers are net long gamma (positive GEX), every move against them shrinks their gamma exposure → they must trade *against* the move to stay hedged. As price rises, dealers sell; as price falls, dealers buy. Systemic effect: **range compression** — extremes get faded by the largest counterparty in the market.

**What this means for your scalping:**
- ICT FVG-fill setups have *higher* hit-rate. Liquidity sweeps fail and reverse faster.
- Draws-of-the-day get hit but rarely overshoot meaningfully.
- Stops should be **tight** — moves that look like they're breaking out usually aren't.
- Be willing to *fade extension* into known magnet strikes (top-OI walls, gamma magnets).

**Practical filter:**
- Net GEX > +$2B (Zion-tuned threshold) AND
- Current price is between top call-side magnet and top put-side magnet
- → trade *toward* the nearest magnet from current price, with tight stop beyond it.

**Anti-pattern:** Chasing breakouts on positive-gamma days. Dealer flow will fade you. Even if the move *feels* strong, look for the magnet pull and fade.

**Cross-reference:** [[(C) ICT_Concepts_Synthesis]] — your draw-of-the-day work runs cleanly here; the regime classifier *boosts your win rate on existing setups* rather than introducing new ones.

---

### 4.2 Negative Gamma Days = Chase Impulses

**The mechanics:** When dealers are net short gamma (negative GEX), every move against them grows their gamma exposure → they must trade *with* the move to stay hedged. As price rises, dealers buy more; as price falls, they sell more. Systemic effect: **range expansion** — moves accelerate, sweeps run, momentum extends.

**What this means for your scalping:**
- Liquidity sweeps *run further than usual* — premature counter-trades get steamrolled.
- ICT order-block holds happen *less reliably* — breakouts break out and stay broken.
- Stops should be **wider** to give legitimate moves room.
- Be willing to *chase impulses* once displacement is confirmed — momentum is real.

**Practical filter:**
- Net GEX < −$1B (Zion-tuned threshold) AND
- Confirmed displacement on 5m chart (your existing ICT trigger)
- → enter on first pullback, hold for extension toward next OI wall or gamma magnet.

**Anti-pattern:** Fading extremes on negative-gamma days. The mean-reversion bias *does not apply* here. What looks like exhaustion is usually mid-trend.

**Cross-reference:** [[(C) ICT_Concepts_Synthesis]] — your liquidity-sweep work is **made for this regime**. Sweeps that would fail in positive gamma deliver in negative gamma. This is where the highest-conviction ICT trades live.

---

### 4.3 The Gamma Flip Level — Regime Line

**What it is:** The price level at which net dealer GEX flips from positive to negative. Above = positive-gamma regime (fade extremes). Below = negative-gamma regime (chase impulses). Service-defined: SpotGamma calls it the "Volatility Trigger." UW calls it the "Zero Gamma Level."

**Why it's the most important single number on the pre-market card:**
- It's the *regime classifier* — defines which tactic dominates today.
- A clean break-and-close across the flip is a regime change *for the rest of the session*.
- VIX often spikes when ES/NQ crosses the flip — confirms regime change with vol expansion.

**Pre-market read:**
- Where is the flip vs current price? Above → buying support structurally there; below → no dealer floor.
- How far is the flip from key OI walls? Flip *coincident* with a wall → exceptionally strong level.
- How wide is the "flip-pending zone" (±10% of zero GEX in absolute terms)? Narrow → regime unstable, expect chop; wide → conviction in current regime.

**Intraday playbook:**
- If price is approaching the flip from above and showing momentum → reduce size, prepare for chase-regime entry on confirmed close-through.
- If price chops at the flip → no-trade zone; wait for direction.
- If price holds rejection at the flip and reverses → regime *defends*; high-conviction continuation in the existing regime tactic.

**Cross-reference:** This level often sits at or near an ICT "premium/discount" boundary or a key liquidity pool. When they overlap, the trade conviction compounds.

---

### 4.4 Layering Regime onto ICT — The Connective Tissue

This is the load-bearing insight of Part 4 and possibly the entire document:

> **The gamma regime transitions from a sizing modifier to a structural filter once its influence exceeds a threshold relative to price volatility and proximity to gamma levels.**

- **Below threshold** (regime influence low relative to current volatility and distance from gamma levels): regime = sizing modifier only. Same ICT setups apply, just with adjusted position size, stop discipline, and target discipline.
- **Above threshold** (regime dominates): regime = structural filter. Certain setup types are vetoed until key gamma levels are cleared (e.g., continuation breakouts in confirmed long-gamma are not taken until price clears the gamma wall).

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

---

## Part 5 — Validation Questions (Consolidated)

The questions below are the same as those embedded per-lens in Parts 1-4. This roll-up gives you a single checklist you can work through in one sitting. As you answer one, mark it `- [x]` here *and* fill the answer inline in the lens-specific section.

### Dealer / Options Regime
- [ ] **1.1 GEX:** What's your specific GEX threshold for calling a day `POSITIVE_GAMMA` vs `FLIP_PENDING`?
- [ ] **1.1 GEX:** When GEX flips overnight, trust the new sign at open or wait 30 min to confirm?
- [ ] **1.1 GEX:** Use SpotGamma's published Vol Trigger as zero-gamma reference, or compute from UW raw?
- [ ] **1.1 GEX:** On flip days, do your ICT setups still work or do you stand aside?
- [ ] **1.1 GEX:** How does position size scale with |GEX| magnitude — fixed, linear, or stepped tiers?
- [ ] **1.2 Gamma profile:** Trust #1 by gamma only, or weight the top 3?
- [ ] **1.2 Gamma profile:** Magnet vs wall — what's your distinguishing rule? (OI? distance? recent flow?)
- [ ] **1.2 Gamma profile:** Two magnets straddling current price within 0.5% — which side and why?
- [ ] **1.2 Gamma profile:** Trade SPX strikes or convert to ES levels?
- [ ] **1.2 Gamma profile:** Magnet invalidation rule on clean rejection?
- [ ] **1.3 0DTE:** Entry trigger for the pin trade — wait for gravitation or position by 14:30?
- [ ] **1.3 0DTE:** Minimum gamma concentration to qualify as "pin-able"?
- [ ] **1.3 0DTE:** OPEX Fridays — same playbook, smaller size, or stand aside?
- [ ] **1.3 0DTE:** `0DTE_CALL_SKEWED` but spot above pin — fade to pin or trust skew?
- [ ] **1.3 0DTE:** Pull the pin trade above what VIX threshold?
- [ ] **1.4 Vanna:** Which window has highest hit-rate in your replay (10:00 / 14:00 / 15:30)?
- [ ] **1.4 Vanna:** Position pre-emptively (entry by 09:55) or wait for window to start showing flow?
- [ ] **1.4 Vanna:** IV-rising morning — flip the trade short or stand aside?
- [ ] **1.4 Vanna:** What VIX level actually changes your sizing?
- [ ] **1.4 Vanna:** Hold to window end (~30 min) or trail until structure breaks?
- [ ] **1.5 IV surface:** Measure skew steepening — delta-25 vs delta-10, what lookback?
- [ ] **1.5 IV surface:** `TERM_INVERSION` = hard veto on longs or sizing reduction?
- [ ] **1.5 IV surface:** Skew vs COT disagreement — which lens wins?
- [ ] **1.5 IV surface:** Use skew shift to time exits on winners, or only new-entry filtering?
- [ ] **1.5 IV surface:** Threshold for "fast" steepening (X bps in Y min) before acting?
- [ ] **1.6 Options flow:** Trust threshold for following flow (premium / direction confluence)?
- [ ] **1.6 Options flow:** Conflicting flow (calls AND puts bought aggressively) — how to read?
- [ ] **1.6 Options flow:** Trade underlying directly or same options?

### Positioning Intel
- [ ] **2.1 COT:** Veto or just context?
- [ ] **2.1 COT:** What percentile threshold for "stretched"?
- [ ] **2.1 COT:** Commercials or large specs as primary read?
- [ ] **2.1 COT:** COT-vs-skew disagreement — which lens wins?
- [ ] **2.2 OI:** How far from current price before you ignore a wall?
- [ ] **2.2 OI:** Stack OI with gamma walls or treat separately?
- [ ] **2.2 OI:** OPEX-week behavior?
- [ ] **2.3 "Goldman PB":** Which aggregator do you trust most?
- [ ] **2.3 "Goldman PB":** Veto or just context?
- [ ] **2.3 "Goldman PB":** Conflicting narratives — how to resolve?

### Microstructure
- [ ] **3.1 Bookmap:** Planning to subscribe? At what P/L trigger?
- [ ] **3.1 Bookmap:** What setups do you expect to validate first?
- [ ] **3.2 Free-substitute:** Already use CVD? At what timeframe?
- [ ] **3.2 Free-substitute:** TPO timeframe for your draw-of-the-day?
- [ ] **3.2 Free-substitute:** Footprint useful at your execution timeframe?
- [ ] **3.3 Subscription threshold:** At what monthly P/L baseline is Bookmap a no-brainer?

### Strategy Frame
- [ ] **4.4 Regime-modifier table:** Anything backwards based on your tape time?
- [ ] **4.4 GEX threshold for ICT override:** Locked at?
- [ ] **4.4 Flip-pending day:** Size-down or no-trade?
- [ ] **4.4 Validation tagging:** Day 1 from synthesis, or 2-week soft launch first?

---

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

Start with the 3 lenses with highest expected EV given Zion's setup (paid options-flow service, ES/NQ scalp):

1. **1.1 GEX** — fastest to operationalize (single number, daily refresh) and biggest impact (defines regime).
2. **4.x Strategy frame** — operationalizes the gamma-ICT integration; depends on 1.1 being clear.
3. **1.3 0DTE & pin** — highest-value intraday setup in the 15:00-15:30 window.

Lower priority for early graduation (long lead-time data or theoretical-only):
- 2.1 COT (weekly cadence; takes 5+ weeks to get 5 observations)
- 3.1 Bookmap (no subscription)
- 2.3 "Goldman PB" (long-feedback-loop signal)

---

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
