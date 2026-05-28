# Quant Lenses → ICT Framework: Master Integration
**How dealer positioning, volatility, order flow & institutional data plug into your liquidity edge**
*Claude-generated · 2026-05-27 · synthesizes the 4 Quant Lens research docs in `01 Refinement/`*

---

## Bottom Line (read this first)

You asked me to research 11 quant concepts and integrate them into your decision-making. After deep research, here's the punchline:

> **None of these replace your ICT edge. All of them tell you the same thing your edge already chases — where liquidity sits and whether it gets defended or run — but from the *dealer/institutional plumbing* side instead of the chart side.**

They don't add a new strategy. They add a **regime filter and a confirmation layer** to the strategy you already have. The single biggest unlock: they directly attack your two stated weaknesses —
1. **"Misidentifying bias/objective"** → COT + IV skew + gamma walls give you an *external, data-anchored* read on where the draw is.
2. **"Which model to use"** → the gamma regime (positive vs negative) is a clean, mechanical switch between **Reversal** and **Continuation**.

---

## The One Diagram: Everything Maps to ERL/IRL

Your whole framework is **price cycling between liquidity (ERL) and fair value (IRL)**. Every quant concept I researched is just *another lens on the same two things*:

| Your ICT term | Dealer/quant equivalent | Lens |
|---|---|---|
| **ERL** (external liquidity / premium) | Call Wall / Put Wall (gamma), big-OI strikes, max pain magnet | 1, 3 |
| **IRL** (internal / fair value) | High-gamma strike (HVL), VWAP, Bollinger midline, pin strike | 1, 2 |
| **Draw on liquidity** (the daily objective) | Put/call skew direction, gamma wall above/below, max-pain pull | 1, 2, 3 |
| **Order flow regime** (buy vs sell sequence) | GEX sign (positive = mean-revert, negative = trend) | 1, 2 |
| **Real MSS vs fakeout** (your gap) | Bookmap absorption (traded-through vs pulled), OI rising vs falling | 3 |
| **HTF bias** (your #1 failure) | COT net positioning + extremes | 4 |
| **Displacement** | At-ask repeat-strike sweeps, vanna/charm mechanical flows | 1, 3 |

**The insight:** the ERL↔IRL "pinball" you trade *is dealer gamma hedging made visible*. Positive-gamma dealers buy dips / sell rips → that's what *manufactures* the mean-reversion into IRL. Negative-gamma dealers sell dips / buy rips → that's what *manufactures* the expansion to ERL. You've been trading the footprint of this without seeing the machine.

---

## The Upgraded Decision Stack

Your current flow is roughly: HTF bias → find draw → wait for model → execute. Here's that same flow with the quant lenses layered in — **each layer is optional confluence, not a new dependency.** Your chart read still owns direction; this just stacks odds.

### Layer 0 — Weekly Bias Anchor (pre-week) · *Lens 4*
- Pull **CFTC COT (TFF report)** for ES + NQ. Tuesday data, released Friday 3:30pm ET. Free via CFTC.gov / Tradingster / TradingView COT Index overlay.
- Compute **COT Index** (Williams, 3yr lookback). >90 = crowd max-long (reversal-down fuel); <10 = max-short.
- **Rule:** your default daily bias should *agree* with Asset Manager net positioning. Only take the **Reversal Model** when Leveraged Funds sit at a >90/<10 extreme — a crowded book is a stop pool, i.e. the multi-day draw.
- ⚠️ Prime brokerage data (the "GS holy grail") is **institutional-only**. Anyone selling it retail is selling fakes. Realistic proxy: GS/MS desk headlines via `uw_news_headlines` + `uw_darkpool_recent` + `uw_market_tide`. **Confirmation only, never a trigger.**

### Layer 1 — Day-Type Map (pre-market) · *Lens 2*
- Check **IV rank** (`uw_iv_rank`) + **term structure** (VIX vs VIX9D) + **skew**.
- **Low IV rank + contango + positive GEX → "mean-revert into IRL" day.** Fade ERL edges, expect IRL to hold, take fast profits, tighten stops.
- **High IV rank + backwardation + negative GEX → "trend to ERL" day.** Don't fade; IRL fails; trail to ERL, widen stops, hold runners.
- **Skew points at the draw:** put skew → sell-side ERL is the magnet; call skew → buy-side ERL.

### Layer 2 — Regime Filter = Model Selector (pre-market / live) · *Lens 1* ⭐
**This is the highest-value addition — it solves "which model when."**
- Tag the **daily gamma regime** vs the **zero-gamma flip level** (SpotGamma / MenthorQ give clean levels; `uw_options_volume` + `flow_alerts` approximate).
- **Positive gamma / above flip → favor the REVERSAL MODEL.** Dealers fade moves → sweeps of ERL reverse. Your fades print.
- **Negative gamma / below flip → favor the CONTINUATION MODEL.** Dealers chase → breaks of structure actually run.
- **A+ trigger:** when an ERL you're watching sits *on* the zero-gamma flip → highest-probability Reversal.

### Layer 3 — Level Confirmation · *Lens 1 + 3*
- Overlay **gamma walls + big-OI strikes + max pain** on your ERL/IRL marks. When a gamma wall lines up with your chart ERL, that's a *reinforced* level — institutions and your chart agree on where liquidity is.
- **Wall break = breakout permission:** a real-volume break of a gamma wall ("unclenching") is the quant confirmation of your "impulsive break of structure." No wall break → the breakout chops (don't chase).

### Layer 4 — Trigger Validation = Your MSS-vs-Fakeout Gap · *Lens 3* ⭐
**This is the second-highest-value addition — it attacks your trap problem directly.**
- **Best single tell:** Bookmap **absorption**. Did the break *trade through* real resting liquidity (volume dots eating the book) → **real displacement, take it**. Or did the wall simply *pull/vanish* unhit → **spoof, fade it**.
- **OI conviction filter:** real MSS rides *rising* OI (new positioning). A break on *falling* OI = short-covering = fragile trap.
- **Cross-market SMT confirm:** ≥3× repeat **at-ask sweeps** on QQQ/SPY (`uw_flow_alerts`, `uw_flow_recent`) in the direction of your NQ/ES break = aggressor confirmation. (This is the same SMT-via-flow method we logged on 2026-05-27.)

---

## Vanna / Charm / 0DTE — the "invisible hand" notes · *Lens 1*
- **Vanna explains drifts that look newsless.** The classic post-FOMC grind-up is dealers *mechanically* buying as IV crushes (~60–80% of the drift), not the news. **Don't fade vanna flows** — they're a freight train with no driver.
- **0DTE gamma walls ARE intraday liquidity levels.** Call Wall ≈ upper session ERL, Put Wall ≈ lower session ERL, the high-gamma strike ≈ the IRL magnet price pins to. The intraday ERL↔IRL pinball *is* 0DTE dealer hedging.
- **Charm (time decay) accelerates into the close** → pin risk into 3–4pm ET; expiry-day afternoons favor mean-reversion to the pin unless negative gamma.

---

## Consolidated Rules to Test (next 20 paper trades)

Track each as pass/fail like your trade journal. These are *hypotheses*, not gospel — grade them.

1. **Regime → Model:** Only take Reversals in positive gamma; only take Continuations in negative gamma. Log win rate split by regime.
2. **Flip confluence:** Mark the zero-gamma flip daily. Grade whether ERL-sweeps *at the flip* reverse more often than ERL-sweeps elsewhere.
3. **Wall = ERL:** Before marking your ERL/IRL, overlay call/put walls. Measure how often your chart-drawn levels and gamma walls agree (high agreement = your read is calibrated).
4. **Absorption gate:** No MSS entry unless Bookmap shows the level traded *through* (not pulled). Count how many fakeouts this filters out.
5. **OI conviction:** Skip breaks on falling OI. Log avoided traps.
6. **COT bias:** Write a weekly bias from COT every Sunday; only fade it intraday with an A+ Reversal. Grade weeks where you held vs broke the thesis.
7. **IV day-type:** Pre-classify each day mean-revert vs trend from IV rank + term structure; grade how often the classification was right by EOD.
8. **Don't fade vanna:** On IV-crush days (post-FOMC/CPI), no counter-trend fades during the drift. Log any fade attempts and outcomes.

---

## Honest Caveats

- **You don't need to buy everything.** Clean gamma levels (SpotGamma ~$/mo, MenthorQ) and Bookmap (~$90–180/mo all-in) are the two paid tools that'd add the most. COT is free. Your UW MCP already approximates flow/IV/walls.
- **This is a lot of inputs.** Don't try to run all 5 layers day one — you'll freeze (your perfectionism risk). **Add ONE layer at a time**, prove it on 20 trades, then add the next. Recommended order: Layer 2 (regime→model) first, then Layer 4 (absorption), then Layer 0 (COT bias).
- **Direction is still yours.** Every lens here is regime/confirmation. None tells you long or short — your ICT liquidity read does. These just tell you *whether the environment agrees* with your read.

---

## Source Docs (detail)
- [[(C) Quant Lens 1 - Dealer Gamma & Vanna]] — GEX, gamma walls, vanna/charm, 0DTE
- [[(C) Quant Lens 2 - IV Surface & Mean Reversion]] — skew, term structure, IV rank, mean-reversion regimes
- [[(C) Quant Lens 3 - Order Flow, Bookmap & OI]] — DOM heatmap, absorption, options flow, open interest
- [[(C) Quant Lens 4 - COT & Prime Broker Positioning]] — CFTC COT, prime brokerage reality, positioning extremes

**Next:** integrate these layers into [[(C) Model_Selection_Decision_Tree]] and the [[(C) Knowledge_Graph_Master]] once you've picked which layer to test first.
