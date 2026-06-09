# 🧠 TD Trades — Master Knowledge Graph
**The connected mental model of your entire strategy** | Generated 2026-05-22

> **How to use this file:** This is your **operating system** — the layer of abstraction that sits above every individual concept. When you're confused about which model to use, or whether a setup is valid, come back here. Every concept has a defined position in this hierarchy.

---

## 🎯 The Single Sentence

> **You hunt the daily objective by reading order flow, waiting for the algorithm to deliver price to a model entry within a confluence zone — and you do not trade if the objective is taken before the model forms.**

That's the whole strategy. Everything below is how to operationalize it.

---

## 🏛️ The 10-Layer Hierarchy (Top → Bottom)

```
┌─────────────────────────────────────────────────────────────┐
│  L10. PSYCHOLOGY                  ← Daily objective rules     │
├─────────────────────────────────────────────────────────────┤
│  L9.  RISK MANAGEMENT             ← Position, SL, TP, BE      │
├─────────────────────────────────────────────────────────────┤
│  L8.  CONFLUENCES (stack to fire) ← SMT, HTF FVG, Protected   │
├─────────────────────────────────────────────────────────────┤
│  L7.  TIME (when to act)          ← Sessions, Killzones, Macro│
├─────────────────────────────────────────────────────────────┤
│  L6.  MODELS (how to enter)       ← Rev, Cont, IFVG, MFD      │
├─────────────────────────────────────────────────────────────┤
│  L5.  DELIVERY MECHANISMS         ← FVG, OB, Imbalance        │
├─────────────────────────────────────────────────────────────┤
│  L4.  LIQUIDITY MAP               ← ERL, IRL, Draw/Objective  │
├─────────────────────────────────────────────────────────────┤
│  L3.  STRUCTURE                   ← STH/STL/ITH/ITL, Protected│
├─────────────────────────────────────────────────────────────┤
│  L2.  STATE (what is price doing) ← Order Flow phase, SMT     │
├─────────────────────────────────────────────────────────────┤
│  L1.  EDGE / THESIS               ← Liquidity hunting         │
└─────────────────────────────────────────────────────────────┘
```

**Read direction:** L1 → L10 is the *thought sequence* you run on every trade. You can't skip layers.

---

## L1 — EDGE / THESIS
### The Belief That Pays You

> Institutions don't trade price — they trade liquidity. Retail orders accumulate around obvious highs/lows as stops. Institutions deliberately drive price to those pools to fill their own orders. **Your job is to position with the institution, not against it.**

| Concept | What it means | Connects to |
|---|---|---|
| **Liquidity hunting** | Trading toward where stops/orders rest | All of L4 |
| **Algorithmic price delivery** | Price moves to seek inefficiencies + liquidity in a repeatable sequence | L5, L4 |
| **Daily objective ("draw" or "DOL")** | The dominant liquidity pool that price is being pulled toward today | L4, L10 |

**Zion's confirmed rule:** *"I target the significant liquidity pools of the day, calling them the 'objective' or 'draw' of the day. If it gets taken out before a model forms, I take no trades."*

🔗 [[ICT and Market Concepts]] | [[Trading With Precision.png]]

---

## L2 — STATE
### What Is Price Doing Right Now?

Every move on the chart is one of two things. **Classify first, then decide.**

### 2.1 Order Flow (Distribution vs. Rebalancing)
From [[ORDER FLOW BASICS.png]]:

| Phase | What you see | What to do |
|---|---|---|
| **Distribution Phase** | Impulsive moves driving into draw/liquidity | TRADE IT — this is the model |
| **Rebalancing Phase** | Retraces filling FVGs / inefficiencies | WAIT — this is the setup |

**Rule:** *"Order flow is when price has a clear trend in a buy sequence or sell sequence, with price rebalancing in FVGs."*

### 2.2 SMT (Smart Money Technique) Divergence
From [[SMT ALIGNING ORDERFLOW.png]] and [[HIGHER TIME FRAMED SMTI.png]]:

**The rule:** Compare two correlated assets (NQ vs. ES). 
- If **one makes a higher high but the other fails** → divergence → weakness → rebalancing likely
- If **both make matching highs/lows together** → alignment → strength → distribution into draw likely

**Why this matters:** SMT tells you WHICH PHASE you're in (L2.1). It's your phase-identifier.

🔗 [[HIGHER TIME FRAMED SMTI.png]] | [[SMT ALIGNING ORDERFLOW.png]]

---

## L3 — STRUCTURE
### The Skeleton of Price

From [[Intermediate Term HighLows.png]]:

```
LONG-TERM HIGH/LOW (LTH/LTL)   ← Daily / Weekly major swings
    │
    ├─ INTERMEDIATE-TERM HIGH/LOW (ITH/ITL)   ← Multi-hour swings
    │       │
    │       └─ SHORT-TERM HIGH/LOW (STH/STL)   ← LTF swings (1m-15m)
```

**Why this matters:** Each level has different significance. An STL taken doesn't mean trend over. An ITL taken DOES suggest structure shift.

### 3.1 Protected Highs/Lows
From [[What is the significance.png]] and [[Protected lows off HTF level.png]]:

**Rule:** *"In Bullish/Bearish Order Flow Market, Intermediate Term Lows/Highs Tend To Be Protected"*

- In bullish order flow: each ITL is "protected" by institutions → buy zone
- In bearish order flow: each ITH is "protected" → sell zone
- **Protected ≠ Model**. From [[A Confluence - Not A Model.png]]: *"This is only used in a clearly structured order flow environment, offering a defined outlook on protected highs and lows. It should be treated as a confluence, not a standalone model, and must align with the models you already use."*

🔗 Confluence for L6 models | Strongest at HTF POIs

---

## L4 — LIQUIDITY MAP
### Where Are the Magnets?

From [[ICT CONCEPTS.png]] and ICT official framework:

### 4.1 ERL (External Range Liquidity)
**Definition:** Liquidity OUTSIDE the dealing range — above the swing high (buy-side) and below the swing low (sell-side).
**How identified:** Created by the previous Asia and London session highs/lows. Dynamic intraday levels — not fixed HTF structures. Update as new session ranges form.
**Role:** The PREMIUM / target — where price is going.

### 4.2 IRL (Internal Range Liquidity)
**Definition:** The closest pools of liquidity to current price — specifically FVGs within the range. Per official ICT: IRL = FVGs ONLY (NOT order blocks, NOT VWAP, NOT Bollinger bands).
**How identified:** Dynamic — the nearest unmitigated FVG relative to current price. Updates continuously as gaps are filled.
**Role:** The FAIR VALUE / entry zone — where price comes back to first before pushing to the next ERL.
**Note:** VWAP, Bollinger midline, and gamma walls are quant filters for trade quality, not IRL substitutes.

### 4.3 The Cycle
```
ERL (premium) ←→ IRL (fair value) ←→ ERL (next premium)
   ↑                                       ↑
   Magnet                                  New magnet
```

Price seeks **fair value before premium**. After taking one ERL, expect retrace to IRL, then push to opposite ERL.

### 4.4 Draw / Objective (DOL)
**Definition:** The most extreme unswept swing high (bullish bias) or swing low (bearish bias) that price is being pulled toward.
**How to find it:** Identify swing highs/lows from price structure → filter out any already swept → determine current bias → select the most extreme remaining unswept level in that direction. Continuously updated as new swings form or levels get swept. Gamma walls and OI are quant quality filters — they do not replace or override the structural DOL.
**Zion's rule:** If DOL is taken without a model forming → **NO TRADES**. The setup is dead.

🔗 [[Trading With Precision.png]] (Pages 2-4 show Draw identification)

---

## L5 — DELIVERY MECHANISMS
### How the Algo Moves Price

These are the *tools* the algorithm uses. Each one creates a tradeable area.

| Mechanism | What it is | How to validate (Zion's rule) |
|---|---|---|
| **Fair Value Gap (FVG)** | 3-candle pattern with a gap between candle-1 high and candle-3 low (or vice versa) | "Price reacts inside it" — no fixed size. Test across timeframes. |
| **Order Block (OB)** | Last opposite-color candle before an impulsive move that sweeps liquidity AND breaks structure | "Clear institutional footprint" — must have momentum + structure break |
| **Imbalance** | Significant buy/sell pressure gap | Often equivalent to FVG; can be larger |
| **IFVG (Inverted FVG)** | A previously-violated FVG that flips role (resistance → support or vice versa) | Used for extra confirmation when traded with main model |
| **BPR (Balanced Price Range)** | Overlapping FVGs from opposite directions | Seen in [[Trade Example.png]] |
| **HTF FVG** | FVG on higher timeframe overlapping with LTF setup | Strong confirmation, speeds up models |

**Critical rule from [[FVG Trade Example]]:** *"FVGs are not entry signals by themselves — they are used as a point of interest to guide entries and exits."* 

🔗 Always combined with L6 models, never traded alone.

---

## L6 — MODELS (How You Enter)
### The Four Tools in Your Belt

| Model | Trigger condition | When to use |
|---|---|---|
| **Rev Model** | Order flow FLIPS (ERL taken + structure shift + neckline break) | Reversal opportunities — after price seeks a major ERL |
| **Continuation Model** | Order flow CONTINUES (HTF trend strong, retrace into IRL fills, push to next ERL) | Strong trends — when bias is locked in |
| **IFVG Model** | Inverted FVG retest after structure shift | Confluence trades, fast scalps |
| **MFD (Macro Fueled Data)** | News event creates new high/low → revisit for liquidity | News days only — CPI, FOMC, NFP |

### 6.1 Model Decision Rule (Zion's confirmed answer)
> *"The Rev Model is for when order flow flips, but the Continuation Model trades using current order flow. MFD is a different model which takes into account news candles for liquidity."*

**Three-layer decision hierarchy (C → B → A):**

**Layer C — Gamma Regime (statistical backdrop):**
Sets which models are statistically favored. Below the influence threshold = sizing modifier only. Above threshold = structural filter that can veto setup types until key gamma levels are cleared.

**Layer B — News/MFD Filter (event gate):**
```
Is there major news in the next 1-2 hours?
  YES → MFD (gather news liquidity)
  NO → proceed to Layer A
```

**Layer A — ICT Order Flow (actual model selection):**
```
Did order flow just FLIP (ERL taken + neckline shift)?
  YES → Rev Model
  NO ↓

Is order flow STRONG and aligned across timeframes?
  YES → Continuation Model
  NO ↓

Is there an Inverted FVG retesting in a structured environment?
  YES → IFVG Model
  NO → NO TRADE
```

**Note:** Layer A defines which ICT model applies. Layers B and C provide context that influences which models are likely to perform best — they do not replace the order flow read.

### 6.2 Master Combination (from [[Correctly Applying.png]])
> **"Bullish Order Flow + Rev Model + Protected Lows. Protected Areas will work best in HTF POIs."**

This is the holy trinity. When all three align, take the trade.

🔗 [[THE REV MODEL.png]] | [[MFD - Macro Fueled Data Model.png]] | [[A SWITCH IN ORDERFLOW.png]]

---

## L7 — TIME
### When the Algorithm Wakes Up

### 7.1 Sessions
- **London**: 02:00–05:00 ET (overlap with US 03:00–07:00)
- **NY AM**: 07:00–10:00 ET (NY Open at 09:30 is most volatile)
- **NY PM**: 13:30–16:00 ET
- **Asian**: low priority for NQ unless geopolitical events

### 7.2 Killzones (where models work best)
Most setups fire during these windows. Outside them = noise risk.

### 7.3 Macros
Two-tier model — use each tier for its specific purpose:

**6-window model (entry timing precision):**
- 09:50–10:10 ET (Silver Bullet window — most important)
- 10:50–11:10 ET
- 11:50–12:10 ET (lunch macro)
- 13:10–13:50 ET
- 14:50–15:10 ET
- 15:15–15:45 ET

**3-window model (directional bias & regime classification):**
- ~10:00 ET (post-open IV crush)
- ~14:00 ET (post-lunch IV reset / institutional rebalance)
- ~15:30 ET (closing vol crush)

**Rule:** Time entries within the 6-window model. Use the 3-window model to classify what the market is doing directionally and which gamma regime is in effect.

### 7.4 Quarterly Theory (NEW — major missing piece)
Time is fractal. Sessions divide into 90-min quarters, days into 6-hour quarters, etc. Each quarter follows AMD: Accumulation → Manipulation → Distribution.

This is mentioned in your education as "Power of Three" but not deeply integrated. **Recommendation:** Add a Quarterly Theory module — it could be the framework that finally answers your "which model when?" question.

🔗 [[2022 ICT Mentorship YouTube Playlist]] covers this extensively.

---

## L8 — CONFLUENCES
### What Stacks Onto a Model to Make It High-Probability?

A model alone is not enough. Confluences = the multiplier.

| Confluence | Weight | Why it matters |
|---|---|---|
| **HTF FVG alignment** | 🟢🟢🟢 HIGH | Higher TF context dominates |
| **SMT divergence/alignment** | 🟢🟢🟢 HIGH | Confirms which side has real order flow |
| **Protected high/low** | 🟢🟢 MEDIUM | Only in clearly structured environment |
| **Session timing** | 🟢🟢 MEDIUM | Killzone presence boosts probability |
| **Macro time window** | 🟢🟢 MEDIUM | Algorithmic precision moments |
| **Multiple FVGs stacked across TFs** | 🟢🟢🟢 HIGH | Institutional interest confirmed |
| **News alignment** | 🟢 LOW–MED | Use carefully; can also break things |

**Your validated rule:** *"Additional confluences can include: higher time frame orderflow, areas of interest, and I want to incorporate all world news that may affect price into the system."*

🔗 **3+ HIGH-weight confluences + a valid model = your A+ setup.**

---

## L9 — RISK MANAGEMENT
### Make the Edge Survive Variance

Current state from your notes:
- Position sizing: ~1% per trade (needs formal rule)
- Stop loss: **Adaptive — scales with IV rank and GEX regime. Never fixed pips.** In confirmed negative-GEX regime, multiply normal stop by ~1.5×. Stops must breathe with the regime, not be fixed in points.
- Take profit: PT1 at IRL (scale 50%), run remaining position to ERL (PT2), move SL to BE after PT1.

**GAPS — answer in next refinement:**
- [ ] Daily max loss?
- [ ] Cumulative weekly loss limit?
- [ ] How position size scales with setup quality?
- [ ] Exact IV rank thresholds for stop scaling?

🔗 [[(C) Desk_Reference_Card.md]] has the template to fill in.

---

## L10 — PSYCHOLOGY
### The Hardest Layer

### Your confirmed rules
1. **"If the DOL is taken before a model forms, I take no trades."** — This is the strongest psychological rule in your playbook. Protect it ferociously.

2. **"The biggest reason my trades fail is usually from misidentifying bias/objective of price."** — Your weakness is at L1/L4. Spend disproportionate prep time on bias each session.

3. **"I feel least confident on which model to use at times."** — Your weakness is at L6. The decision tree in this doc + the [[(C) Model_Selection_Decision_Tree.md]] are the medicine. Use them religiously until they're internalized.

### Universal trader rules
- Patience > Action. No trade is a trade.
- One bad model selection = a controlled loss. One revenge trade = a destroyed week.
- The market doesn't owe you a setup. Some days = zero trades.

---

## 🔗 The Connection Map (How Layers Interact)

```
          DAILY OBJECTIVE (L1)
                  │
                  ▼
   ┌──────────────────────────────┐
   │ Order Flow State (L2)         │  ←─── SMT Divergence (L2)
   │ "Distribution or Rebalancing?"│
   └──────────┬────────────────────┘
              │
              ▼
   ┌──────────────────────────────┐
   │ Structure Map (L3)            │  ← Where are protected H/L?
   │ "What's my STH/STL/ITH/ITL?"  │
   └──────────┬────────────────────┘
              │
              ▼
   ┌──────────────────────────────┐
   │ Liquidity Map (L4)            │
   │ "Where's ERL/IRL/DOL?"        │
   └──────────┬────────────────────┘
              │
              ▼
   ┌──────────────────────────────┐
   │ Delivery Mechanism (L5)       │
   │ "What FVG/OB is the algo using?"│
   └──────────┬────────────────────┘
              │
              ▼
   ┌──────────────────────────────┐
   │ Model Selection (L6)          │  ← Which one fits?
   │ "Rev / Cont / IFVG / MFD"     │
   └──────────┬────────────────────┘
              │
              ▼
   ┌──────────────────────────────┐
   │ Time Filter (L7)              │  ← Is this a killzone/macro?
   │ "Is this a tradeable window?" │
   └──────────┬────────────────────┘
              │
              ▼
   ┌──────────────────────────────┐
   │ Confluence Check (L8)         │  ← 3+ aligned?
   │ "How many things stack?"      │
   └──────────┬────────────────────┘
              │
              ▼
   ┌──────────────────────────────┐
   │ Risk Frame (L9)               │  ← Position, SL, TP
   │ "What's R:R? Size?"           │
   └──────────┬────────────────────┘
              │
              ▼
   ┌──────────────────────────────┐
   │ Psychology Gate (L10)         │  ← Am I patient or chasing?
   │ "Am I trading my system?"     │
   └──────────┬────────────────────┘
              │
              ▼
            EXECUTE
              or
           STAND DOWN
```

**Every trade flows top-down. If any layer fails, the trade is invalid.**

---

## 📚 Concept Cross-Reference Index

### Foundation Terms (alphabetical)
- **AMD** — Accumulation, Manipulation, Distribution (Power of Three) → L2, L7
- **BOS** (Break of Structure) → L3
- **BPR** (Balanced Price Range) — Overlapping FVGs → L5
- **Buy-side liquidity** — Stops/orders above swing high → L4
- **CISD** (Change in State of Delivery) — HTF order flow shift → L2
- **Displacement** — Strong impulsive move → L5
- **DOL** (Draw on Liquidity) — Daily objective → L4
- **ERL** (External Range Liquidity) → L4
- **FTSH/FTSL** (Failure to Seek High/Low) → L2 confluence
- **FVG** (Fair Value Gap) → L5
- **IFVG** (Inverted FVG) → L5/L6
- **IPDA** (Interbank Price Delivery Algorithm) — 20/40/60-day cycles → L1 (theory)
- **IRL** (Internal Range Liquidity) → L4
- **ITH/ITL** (Intermediate Term High/Low) → L3
- **LTH/LTL** (Long Term High/Low) → L3
- **MFD** (Macro Fueled Data) → L6 model
- **MSS** (Market Structure Shift) → L3 trigger
- **OB** (Order Block) → L5
- **PD Array** (Premium/Discount Array) — ICT term for HTF level → L4
- **POI** (Point of Interest) → L5 + L4 overlap
- **Sell-side liquidity** — Stops/orders below swing low → L4
- **SMT** (Smart Money Technique) divergence → L2 confluence
- **STH/STL** (Short Term High/Low) → L3

### Newly Discovered (from ICT research — add to playbook)
- **Silver Bullet** — Time-based ICT model (9:50–10:10 NY AM macro)
- **Quarterly Theory** — Fractal time decomposition
- **Macro Times** — Specific 20-min windows for algo runs
- **MMXM** (Market Maker eXternal Move) — Alternative IRL→ERL framework
- **CLS** — Central Bank Liquidity Sweep (advanced ICT)
- **90-Min Cycles** — Each session has 4 quarters of 90 minutes

---

## 🎬 What's Next

### Immediate (this week)
1. **You read this file 3 times.** Until it clicks as a unified system, not 10 separate ideas.
2. **You answer the remaining gap questions** (L9 risk, L7 macro times, Quarterly Theory integration).
3. **You add 5 annotated trade screenshots** showing this hierarchy in action — each trade labeled by layer.

### Next Week
4. **Build the actual playbook** (`02 Playbook/`) using this hierarchy as the table of contents.
5. **Watch the YouTube playlists** (you noted them — let's set aside time to convert them into structured notes).
6. **Decide on Quarterly Theory** — Yes/No, deep-integrate or skip.

### After Playbook Build
7. **Phase 2** — I start calling live setups using this hierarchy.
8. **Phase 3** — Paper trade with 50+ documented executions.

---

## 🗂️ Files Connected to This Graph

| File | Layer Covered | Purpose |
|---|---|---|
| [[ICT and Market Concepts]] | All | Source of truth (your input) |
| [[(C) ICT_Concepts_Synthesis]] | All | Your answers + my questions |
| [[(C) Model_Selection_Decision_Tree]] | L6 | Which model when |
| [[(C) Desk_Reference_Card]] | L6, L9, L10 | Live trading lookup |
| [[(C) Playbook_Mapping_Guide]] | All | Build roadmap |
| [[(C) Intelligence_Summary]] | Meta | Status + next steps |
| **This file** | All | The mental model |

---

## 💎 The One-Line Test

If at any point during a trade you can't answer YES to all 10 of these, you stand down:

1. ☐ Did I identify today's draw/objective before the session opened?
2. ☐ Do I know the current order flow phase (distribution or rebalancing)?
3. ☐ Have I mapped key structure points (STH/STL/ITH/ITL)?
4. ☐ Are ERL and IRL clearly marked on my chart?
5. ☐ Did the algo deliver to a clean FVG / OB / Imbalance?
6. ☐ Is this a valid model (Rev / Cont / IFVG / MFD)?
7. ☐ Am I trading inside a killzone (or macro time)?
8. ☐ Do I have 3+ confluences stacked?
9. ☐ Is my R:R ≥ 1:2 with a defined SL and TP?
10. ☐ Am I emotionally calm, not chasing, not revenge-trading?

10/10 = take it. 9/10 = pass. **You don't compromise the system to find a trade.**

---

**Status:** Living document. Updated each refinement session.
**Last update:** 2026-05-22
**Next review:** After Zion answers remaining gap questions
