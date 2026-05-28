# (C) Bootcamp Week 3 — Distillation: Liquidity & Market Behavior
*Claude-generated distillation of Korabi's Week 3 bootcamp lecture* | Source: `00 Inputs/Education/Bootcamp Week 3.mp4` (27:59) | Distilled 2026-05-27

> **What Week 3 is about:** This lecture is a single deep dive on **liquidity** — what it is, how price moves between pools, and how to tell the difference between the *draw* (your real objective) and *manipulation* (the noise in between). Korabi's central thesis is that price moves from liquidity pool to liquidity pool, and your only job is to *ride the wave* into the daily objective using one of exactly two models — **continuation** or **reversal** — never trying to predict the move. The hardest, most repeated lessons are psychological: define the objective before you trade, stop trading once it's taken, enter at previous structure (never chase), and accept that your achievable R changes with market conditions.

---

## 1. Topics Taught (with timestamps)

| Time | Topic |
|---|---|
| 0:00–0:01 | **What is liquidity** — resting stops/pending orders; level-2 visibility; price moves pool-to-pool |
| 0:01–0:05 | **Draw vs. Manipulation** — the objective (draw) vs. internal stop-hunts between it |
| 0:04–0:06 | **The "objectives taken = I'm off" rule** + only two models (continuation / reversal) |
| 0:06–0:09 | **Equal highs / equal lows ("stacked liquidity")** + failure-to-seek tolerance |
| 0:09–0:11 | **Q&A: marking externals on 1m, breakeven, waiting for reversal, FTSL confirmation, engineered pools** |
| 0:11–0:14 | **Liquidity → objective → sweep/manipulation** step-by-step + a worked trade (2.4R/2.8R/6.3R, trailing) |
| 0:14–0:15 | **Session highs/lows, stop placement, prop firm hold rules** |
| 0:15–0:19 | **Reversal vs. Continuation model anatomy** + the previous-structure pullback rule + "don't chase" |
| 0:18–0:20 | **All pools are identical; rebalance vs. distribute phases** (ties to Week 2) |
| 0:19–0:22 | **R expectations change with conditions** — trending vs. consolidating months |
| 0:21–0:23 | **"You can't miss a move without an entry"** + systematic mindset |
| 0:22–0:27 | **Forward-test, don't back-test** — why replay tool fails; context/sequence argument |

---

## 2. Specific Rules, Numbers & Definitions

### Liquidity (definition)
> *"Liquidity is where money is sitting in the market — for retail, it's stops, pending orders, buy stops, sell stops."* Price moves **to** liquidity highs / liquidity lows. Visible in level 2 as large resting orders; sometimes so large that price "full reverses straight into your next pool of liquidity." [0:00]

### Draw vs. Manipulation (core distinction of the lecture)
- **Draw = an objective.** *"In the morning you'll have one or two objectives."* It is the swing high / swing low / important high — the **magnet**. [0:01, 0:03]
- **Manipulation = price tagging out sell stops / buy stops in between a range or consolidation** until it goes to tag the draw. [0:01]
- **Rule for telling them apart:** *"The swing high will be a draw. Anything in between is manipulation."* Mark internal manipulation with an **X**; look for your model toward the swing high. [0:03–0:04]
- Internals (small wicks, small internals, small gaps) = **manipulation / sweeps**. Larger pools = **draws/objectives**. [0:02]

### What counts as a "larger pool" (valid objectives)
Ranging highs, swing highs/lows, range highs/lows, **MFD models** (data highs/lows, CPI, FOMC high/low), Asia high/low, multi-session highs/lows. [0:02]
*Transcription note: "MFD models, so the data highs" confirms MFD = Macro Fueled Data (news-driven pools), consistent with the vault.*

### The two models — and only two
> *"There's only two models you need: **continuation to the high** or **reversal into the high**."* [0:05]
- **Continuation model:** lower-timeframe order flow **already aligns** with the higher timeframe → ride it. [0:05]
- **Reversal model:** lower timeframe is **bearish** while higher timeframe is **bullish** (and you want the high) → you need a reversal. [0:05, 0:06, 0:16]
- **Explicitly NOT traded:** manipulation models, consolidation models, accumulation models, "little scout" models (5 points / 0.3R). *"I'm looking for the larger approach — less trades, more efficient, cleaner."* [0:05]

### The strongest psychological rule (verbatim)
> *"You have your objectives for the day. Once they're taken, I'm off. I don't care. Everyone starts crying, boo hoo, move on… That objective is the reason I'm very consistent."* [0:04–0:05]

### Equal highs / equal lows ("stacked liquidity")
- *"Think of a regular pool of a high or low and double it."* Especially strong if price reverses off it and goes right back. [0:06]
- Can be a previous-day high + previous-day low. **"If you can see a clean equal high or equal low, there's liquidity there, 100%."** [0:07]
- Usually formed **intraday**; rarely on the higher timeframe ("even more crazy"). [0:07]

### Failure-to-seek (FTSL/FTSH) tolerance — specific
- If price reverses aggressively before tagging the low, it's a **failure to seek**, not a sweep. [0:07–0:08]
- *"If it's a [failure-to-]seek low by a couple points… me personally it would be a fail-to-seek for sure, **because you didn't tag the low**. As long as you don't tag this low, you are completely fine."* A shorter (shallower) one is still valid; *"you are still in bullish order flow, nothing's changed."* [0:08]
- **FTSL confirmation requires:** an aggressive buy sequence (for a low), a reversal, **and a protected low**. [0:09–0:10]

### Marking & execution mechanics
- **Mark externals/objectives on the 1-minute.** *"Time is fractal… but when marking out externals you always want to mark out on the one minute."* [0:09]
- Zoom into 1m to find where to **go breakeven** — "This is where I go breakeven. And then if it wants this high, great. If not, next [trade]." [0:09–0:10]
- *"Don't over-complicate it."* [0:10]

### Worked trade example (the numbers) [0:11–0:14]
Setup: tag the low (X), instant buy sequence back above, **reversal model at previous structure in bullish order flow with a fail-to-seek**, using wick-low + balanced price range (BPR).
- **Entry** at the model, **stop** below, **target** = objective/draw (the magnet).
- **PT1** (a pool of liquidity) = **2.4R**
- **PT2** (the high) = **2.8R**
- **Final PT** ≈ **6.3R**
- **Trailing rule:** *"Once you displace above that previous structured high / previous pullback high… you can trail to the new low you just created."* In the example, trailed out for **~2.5R**. [0:13–0:14]

### Stop-loss viability rule (R floor)
> If putting the stop below the fail-to-seek wick gives you *"not even 1.3R… I wouldn't even take the trade if I had to put my stop here."* [0:14]
*Implied minimum: a trade isn't worth taking if R is ~1.3 or less with that stop.*

### Session highs/lows
- Not a primary focus. *"If it gets taken, great… market doesn't really focus on it too much."* But it **aligns with your trade ~80% of the time**, so keep trailing toward the next session pool (e.g., engineered NY high → Asia high next). [0:14]

### Prop-firm constraint
- **You cannot hold a trade from NY into Asia session** on prop firms. [0:14]

### Reversal model anatomy [0:15–0:17]
Scenario: 1m bearish, higher TF bullish, in bullish order flow, with a good **internal pool** of liquidity and an **external below it**. Price manipulates the low and **fails to seek the external** → reversal-ready.
Sequence: **wait for the liquidity → the rejection → confirmation with the model (the reversal).** Reason: *"your lower timeframe is in a bearish sequence,"* so you need the flip. [0:16–0:17]

### Continuation model anatomy [0:17–0:18]
Small internal liquidity gets taken **in trend / proper order flow**, then price keeps displacing. Enter on the **pullback, not the break of the low.**
- **Where to pull back: previous structure.** *"Add structure is usually — unless your bias is fully incorrect — the last place you will retrace into."* [0:17]

### The "don't chase" rule (verbatim, hard-hitting)
> *"The lower you go, the less of a chance you have of being green… If you missed the first one, that's okay. If you missed the second one, you're pushing it. You missed the third one, you deserve to lose every account you have, respectfully."* [0:18]

### Rebalance vs. Distribute (ties to Week 2)
- All pools (external/internal, big/small orders) are **identical — just pools of liquidity.** [0:18–0:19]
- Internals → continuations ("sweep a little like a baby then shoot later"). Full sweep + manipulation → the big reversal. [0:19]
- A reversal may sweep an external, then **rebalance on a higher timeframe for value**, then push. *"This is rebalancing, this is distributing. Being in between, you don't want to trade."* [0:19]

### R expectations are conditional (a key reframe)
- If price **displaced all night**, don't expect 10R/15R today — *"you'll be lucky to get a 2–3R trade, and that's with a really good stop."* [0:19–0:20]
- If price **rebalanced** (filled unfilled orders) then looks for continuation higher → *"any continuation pullback, you're pushing 4R, 5R, 7R, 6R."* [0:20]
- Why green one week / red the next: **conditions change**, AND you're trading the wrong sequences (longing the high, shorting the low). [0:20]
- Pure trending months ≈ **3 months out of the year.** You can't trade as if every month trends — "it's not sustainable." [0:20–0:21]
- Cycles exist: some months trend, some consolidate; March-type months might give one 15R day then 3 losing days. [0:26]

### "You can't miss a move without an entry"
> *"You didn't miss the move without an entry. That's not how it works… You can't miss the move when you don't have an area for you to fill off of."* Use your objective to know if you're chasing: if you've already tagged PT1 and you're longing higher with no entry, **you missed it.** [0:21–0:22]

### Forward-test, not back-test [0:22–0:27]
- Korabi **does not back-test / does not use the replay tool.** Reasons: you subconsciously memorize the day; replay lacks context — *"I don't know what sequence price was in seven months ago."* [0:22, 0:25–0:26]
- **Forward test** = mark an A+ model live, then either don't take it and watch it play out, or **take it with very light size (one micro)** until you've got the model down. [0:24, 0:27]

### One-line summary of liquidity (Korabi's own)
> *"We move from liquidity to liquidity, whether internal or external. Your job is to catch it during the sequence into it. Your job is to **ride the wave** — I don't recommend predicting the wave… Most traders I know are wave riders. They flow into these pools, into the draw. That's the game of trading."* [0:23]

---

## 3. Direct Quotes Capturing the Mental Model

- *"There's only two models you need: continuation to the high or reversal into the high."*
- *"The swing high will be a draw. Anything in between is manipulation."*
- *"Once they're taken, I'm off. I don't care… That objective is the reason I'm very consistent."*
- *"The lower you go, the less of a chance you'll be green. Drill that in your brain."*
- *"You can't miss the move when you don't have an area for you to fill off of."*
- *"Conditions change… you're also trading the wrong sequences. You're trying to long at the high, you're trying to short at the low."*
- *"Ride the wave. I don't recommend predicting the wave."*
- *"Trading isn't difficult… you're just lacking that mindset, the discipline. It's a systematic approach."*

---

## 4. Knowledge-Graph Mapping

| Week 3 concept | Maps to (Master Graph) | Notes |
|---|---|---|
| Liquidity = resting stops/orders | **L1 Edge / L4 Liquidity Map** | Reinforces the thesis verbatim |
| Draw vs. Manipulation | **L4 (Draw/DOL)** + **L2 State** | Sharpens "objective" vs internal noise |
| Larger pools list (swing/range/session/MFD) | **L4 (ERL/DOL)** | Concrete list of valid objectives |
| Two-model rule (Cont / Rev) | **L6 Models** | *See contradiction below re: IFVG/MFD* |
| Continuation = LTF aligns HTF | **L6 Continuation** + **L2 Distribution** | |
| Reversal = LTF bearish, HTF bullish | **L6 Rev Model** | Matches "order flow flips" |
| Equal highs/lows = stacked liquidity | **L4 + Cross-Ref "Equal Highs/Lows"** | New depth on the term |
| FTSL "by a couple points still valid; don't tag the low" | **L2 confluence (FTSH/FTSL)** | New precision tolerance |
| Protected low confirms FTSL | **L3 Protected Highs/Lows** | Confirms protected as confluence |
| Mark externals on 1m | **L7 Time / execution** | New mechanic |
| Enter on pullback to **previous structure** | **L3 Structure + L6 Continuation** | New entry-location rule |
| Trail past previous structured high → to new low | **L9 Risk (trailing)** | Fills a risk gap |
| R floor (~1.3R = skip) | **L9 Risk** | New min-R guidance |
| Rebalance vs. Distribute | **L2 Order Flow** | Direct continuity from Week 2 |
| Conditional R by market phase | **L9 / L10** | New mental model |
| Forward-test > back-test | **L10 Psychology** | New methodology rule |
| Ride the wave, don't predict | **L1 / L10** | New framing of the edge |

---

## 5. VALIDATE / CONTRADICT / EXTEND vs. the Written Framework

### ✅ VALIDATE
- **Daily objective rule** (L1/L10): *"Once they're taken, I'm off"* directly confirms Zion's "if DOL taken before a model forms, no trades." The mentor's own behavior backs the vault's strongest rule.
- **Rev vs. Continuation definitions** (L6): "Rev = order flow flips, Continuation = current order flow" — Week 3's "LTF bearish/HTF bullish → reversal; LTF aligns HTF → continuation" matches exactly.
- **Liquidity-hunting edge** (L1): pool-to-pool movement, institutions filling at resting orders — fully consistent.
- **Protected lows as confluence** (L3/L8): FTSL confirmation requiring a "protected low" validates the "confluence, not a model" stance.
- **ERL/IRL cycle** (L4): "internals for continuation, full external sweep for reversal, rebalance then push" mirrors ERL↔IRL.
- **MFD = news/data pools** (L6): "MFD models, so the data highs, CPI, FOMC" confirms MFD's definition.

### 🔶 EXTEND (new precision the vault should absorb)
- **FTSL tolerance:** "a couple points short is still a valid fail-to-seek as long as you don't tag the low" — adds a concrete boundary the vault's FTSL entry currently lacks.
- **Trailing rule (fills an L9 gap):** trail only after displacement **above previous structured/pullback high**, then trail to the **newly created low.** Vault L9 had this as an open TODO.
- **Minimum-R floor:** ~1.3R with the required stop = skip the trade. Vault L9 risk gaps had no min-R; this is a usable rule.
- **Previous-structure pullback rule:** continuation entries belong at previous structure ("the last place you retrace unless bias is wrong") — sharper than the vault's generic "retrace into IRL."
- **Mark externals on the 1-minute:** specific execution mechanic not in the vault.
- **Conditional R expectations:** post-overnight-displacement days cap at ~2–3R; post-rebalance continuation days run 4–7R. New mental model for L9/L10.
- **Forward-test > back-test:** explicit methodology preference (light size / one micro) — belongs in L10 and the testing plan.

### 🚨 CONTRADICT (flag loudly)
1. **"There's only TWO models" vs. the vault's FOUR models.**
   The Master Graph (L6) and the Synthesis define **four** models: Rev, Continuation, **IFVG**, and **MFD**. In Week 3 Korabi says flatly: *"There's only two models you need — continuation to the high or reversal into the high,"* and lists what he will NOT trade (manipulation, consolidation, accumulation, scout). He does NOT name IFVG or MFD as standalone models here — he treats **MFD pools as just another draw/objective** and BPR/IFVG as **tools inside the reversal example**, not separate models.
   - **Why it matters:** the vault's L6 decision tree branches across 4 models; Zion's self-reported weakness is "which model to use." If the mentor genuinely runs a **two-model system** (with MFD as a *liquidity source* and IFVG/BPR as *delivery tools*, not models), the decision tree may be over-complicated and the real fork is just **Cont vs. Rev**.
   - **NEEDS RESOLUTION FROM ZION:** Are IFVG and MFD *models* (per the vault) or *tools/pools folded into Cont/Rev* (per Week 3)? This changes the L6 architecture.

2. **"I don't trade accumulation" vs. the vault's heavy AMD / Power-of-Three / Quarterly-Theory emphasis.**
   The Master Graph proposes integrating **AMD (Accumulation→Manipulation→Distribution)** and **Quarterly Theory** as a possible answer to "which model when." Korabi explicitly rejects trading accumulation and consolidation phases and never invokes AMD/quarters — his framing is purely **draw + the two trend-following models + ride the wave.** This is a *philosophical* contradiction with the vault's "consider adding Quarterly Theory" recommendation.
   - **NEEDS RESOLUTION:** Does Zion want to pursue Quarterly Theory (vault's suggestion) when his actual mentor doesn't use it? May be a dead-end branch.

3. **Back-testing stance.** The vault's "What's Next" plan includes **paper trading with 50+ documented executions** and implies back-testing for the autonomous phase. Korabi is openly **anti-back-test / anti-replay** and pro-forward-test. Not a hard contradiction, but the Phase 3 validation methodology should be aligned with the mentor's stance (forward-test with light size) rather than replay.

---

## 6. NEW Concepts (not yet in the vault)

- **"Stacked liquidity"** as the explicit name for equal highs/equal lows ("a pool doubled"). The vault lists "Equal Highs/Lows" but not this framing/strength heuristic.
- **The 1.3R floor** — skip any trade whose required stop drops it to ~1.3R or below.
- **Trail-after-displacement / trail-to-new-low** mechanic (concrete trailing rule).
- **Conditional R by phase** — overnight-displaced day ≈ 2–3R ceiling; rebalanced-then-continuation day ≈ 4–7R.
- **"You can't miss a move without an entry"** — a discipline rule that reframes FOMO.
- **"Three trending months a year"** — base-rate reality check for trend expectations.
- **"Ride the wave, don't predict the wave"** — the mentor's one-line philosophy; a clean framing for L1.
- **Forward-test protocol** — mark A+ model live, watch or take with one micro; do not use replay.
- **Mark externals on the 1-minute** — specific execution convention.

---

*Status: Distillation complete. Two structural contradictions (4-models-vs-2-models; Quarterly Theory relevance) flagged for Zion's resolution before the L6 playbook is finalized.*
