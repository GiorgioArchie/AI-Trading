# Playbook Architecture — Where Each Concept Lives
**Ruflo-Generated Mapping Guide** | Use this to structure Phase 1 (Playbook Build)

---

## Current State
- **Playbook folder** (`02 Playbook/`): Empty (ready to build)
- **Input material**: Comprehensive ICT/SMC framework (1,400+ lines)
- **Task**: Translate education → executable playbook entries

---

## Proposed Playbook Structure

### Core Files to Create

```
02 Playbook/
├── 01_Core_Edge.md           ← Your liquidity-hunting thesis
├── 02_Market_Structure.md    ← Structure recognition rules
├── 03_Trading_Models/
│   ├── Rev_Model.md
│   ├── Continuation_Model.md
│   ├── IFVG_Model.md
│   └── MFD_Model.md
├── 04_Risk_Management.md     ← Position sizing, stops, targets
├── 05_Multi_Timeframe_Bias.md ← HTF/LTF alignment rules
├── 06_Session_Timing.md      ← Kill zones, optimal hours
└── 07_Entry_Decision_Tree.md ← Which model to use when?
```

---

## Concept → Playbook Mapping

| Concept | Current Status | Destination | Priority | Notes |
|---------|---|---|---|---|
| **Liquidity-Based Edge** | ❌ Not in playbook | `01_Core_Edge.md` | 🔴 CRITICAL | Define: Do you hunt liquidity, or trade structure? |
| **Order Blocks (OBs)** | 📚 In education | `02_Market_Structure.md` | 🔴 CRITICAL | Add: How do you mark them? Screenshots needed. |
| **Fair Value Gaps (FVGs)** | 📚 In education | `02_Market_Structure.md` | 🔴 CRITICAL | Add: Entry criteria? Size threshold? |
| **ERL/IRL Liquidity Cycle** | 📚 In education | `05_Multi_Timeframe_Bias.md` | 🔴 CRITICAL | Add: Marking method? HTF/LTF rules? |
| **Market Structure Shift (MSS)** | 📚 In education | `02_Market_Structure.md` | 🟡 HIGH | Add: False break detection. |
| **Break of Structure (BOS)** | 📚 In education | `02_Market_Structure.md` | 🟡 HIGH | Add: Confirmation candles? Volume? |
| **Protected Lows/Highs** | 📚 In education | `02_Market_Structure.md` | 🟡 HIGH | Add: # retests = protected? |
| **Liquidity Sweeps** | 📚 In education | `02_Market_Structure.md` | 🟡 HIGH | Add: Reversal timing after sweep? |
| **Rev Model (Full Checklist)** | 📚 In education | `03_Trading_Models/Rev_Model.md` | 🔴 CRITICAL | Add: Flip candle definition? Real trade examples? |
| **Continuation Model** | 📚 In education | `03_Trading_Models/Continuation_Model.md` | 🟡 HIGH | Add: FTSH visualization? HTF/LTF alignment rules? |
| **IFVG Model** | 📚 In education | `03_Trading_Models/IFVG_Model.md` | 🟢 MEDIUM | Add: Entry trigger? Scaling rules? |
| **MFD Model (News-Based)** | 📚 In education | `03_Trading_Models/MFD_Model.md` | 🟢 MEDIUM | Add: Pre-market prep? Live vs. post-news entry? |
| **Risk-to-Reward Ratio** | 📚 In education | `04_Risk_Management.md` | 🔴 CRITICAL | Add: Your min/max R:R? Scaling rules? |
| **Position Sizing** | 📚 In education | `04_Risk_Management.md` | 🔴 CRITICAL | Add: 1% per trade? Cumulative daily max? |
| **Stop Loss Placement** | 📚 In education | `04_Risk_Management.md` | 🔴 CRITICAL | Add: 20p fixed, or ATR-based? |
| **Take Profit Targets** | 📚 In education | `04_Risk_Management.md` | 🟡 HIGH | Add: PT scaling? Partial exits? |
| **Multi-TF Bias** | 📚 In education | `05_Multi_Timeframe_Bias.md` | 🔴 CRITICAL | Add: Which HTF? Daily structure rules? |
| **Confluence Stacking** | 📚 In education | `05_Multi_Timeframe_Bias.md` | 🟡 HIGH | Add: How many = high-prob? Weighting? |
| **Session Timing / Kill Zones** | 📚 In education | `06_Session_Timing.md` | 🟡 HIGH | Add: Which sessions? Sit-out hours? |
| **Failure to Seek Low (FTSL)** | 📚 In education | `02_Market_Structure.md` | 🟢 MEDIUM | Add: Candle confirmation? Trade signal timing? |
| **Smart Money Manipulation** | 📚 In education | `02_Market_Structure.md` | 🟢 MEDIUM | Add: How do you spot a trap? |

---

## Phase 1 Build Checklist

### Week 1: Foundation
- [ ] **`01_Core_Edge.md`** — 500 words on your liquidity-hunting philosophy
  - Why does price move? (Institutions + order flow)
  - How you profit from it? (Hunt liquidity before institutions)
  - What's your edge over random traders?
  
- [ ] **`02_Market_Structure.md`** — Structure recognition rules
  - How to mark swing highs/lows
  - How to identify bullish/bearish structure
  - Order block marking (with 3 screenshot examples)
  - FVG identification (with 3 screenshot examples)
  - Protected low/high definition

### Week 2: Trading Models
- [ ] **`03_Trading_Models/Rev_Model.md`** — Full 10-step checklist + annotated examples
  - Checklist (as a table for easy reference)
  - 3+ real trade examples (screenshots with labels)
  - Common mistakes (what breaks the model?)
  - Back-tested win rate (honest number)

- [ ] **`03_Trading_Models/Continuation_Model.md`** — Step-by-step guide
  - How you identify "trend continuation opportunity"
  - FTSH detection method
  - HTF/LTF alignment rules
  - When do you scale out? (PT1 at IRL, full at ERL?)

- [ ] **`03_Trading_Models/IFVG_Model.md`** — When & how to use
- [ ] **`03_Trading_Models/MFD_Model.md`** — Pre-news prep + execution

### Week 3: Risk & Multi-TF
- [ ] **`04_Risk_Management.md`** — Your fixed rules
  - Position sizing formula
  - Stop loss placement rule
  - Take profit scaling rule
  - Daily/weekly loss limits
  - Average R:R target

- [ ] **`05_Multi_Timeframe_Bias.md`** — Bias establishment
  - Which timeframes for HTF/LTF?
  - How to establish daily bias (structure-based?)
  - Confluence requirements (how many = trade?)
  - How to resolve HTF/LTF conflict

- [ ] **`06_Session_Timing.md`** — Which hours you trade
- [ ] **`07_Entry_Decision_Tree.md`** — "Given X, which model should I use?"

---

## Knowledge Gaps (Critical to Resolve)

| Gap | Why Critical | Zion's Input Needed |
|---|---|---|
| **What's your actual edge?** | Without defining it, you can't teach it. | "Institutions hunt X liquidity" — be specific. |
| **How do you mark IRL/ERL?** | You mention it constantly but never show. | Screenshots of your charts with markings. |
| **Rev Model win rate** | "85-90% if done properly" is vague. | Over how many trades? Last 100? Last year? |
| **Which model when?** | You have 4 models; how do you choose? | Decision tree or flowchart. |
| **HTF/LTF conflict** | What if daily says up but 5m says down? | Which one wins? How do you resolve? |
| **Session filtering** | Do you sit out 12-3pm or trade all day? | Your actual trading schedule. |
| **Stop loss rule** | "20p or prev wick high" is imprecise. | Is 20p on 1m? 5m? Does it change? |

---

## Ruflo Memory Integration

**Patterns learned so far:**
```
✓ trading_concepts:core_liquidity_thesis (stored)
✓ trading_concepts:rev_model_checklist (stored)
→ trading_concepts:continuation_model (pending)
→ trading_concepts:erl_irl_marking_rules (pending)
→ trading_concepts:multi_tf_decision_rules (pending)
→ trading_concepts:risk_management_rules (pending)
```

**Each pattern is vector-indexed** for fast retrieval during:
- Live trading (1-second concept lookup)
- Trade reviews (find similar past setups)
- Refinement sessions (search by concept or tag)

---

## Next Actions

### For Claude (This Session)
1. ✅ Extract concepts → [[ICT_Concepts_Synthesis.md]]
2. ✅ Create mapping guide → You're reading it
3. ⏳ Await Zion's answers to refinement questions
4. ⏳ Create annotated playbook entries (with examples)

### For Zion (Before Next Session)
1. **Answer the 7 refinement questions** in [[ICT_Concepts_Synthesis.md]]
2. **Provide 3-5 trade screenshots** annotated with:
   - ERL/IRL markings
   - Order block identification
   - Which model it was
   - Entry reason + target + result
3. **Clarify your biggest gap** — which concept feels weakest?
4. **(Optional) Record a 10-min voiceover** of a trade walkthrough

---

## Success Metric for Phase 1

**Playbook is done when:**
- ✅ Every concept has an executable checklist (not just explanation)
- ✅ Every model has 3+ annotated real-trade examples
- ✅ Every rule is quantified (no vague language like "about," "usually," "might")
- ✅ You can teach a trader to follow your checklists and get 70%+ of your win rate
- ✅ It's under 50 pages (concise, not verbose)

**Estimated timeline:** 2-3 weeks of refinement sessions + 10-15 hours of annotating examples.

---

## Questions for Zion

1. **Priority order** — Which concepts are most urgent to codify first?
2. **Example availability** — Can you share trade screenshots, or should I find examples in price action education?
3. **Scope** — Do you want playbook to cover ONLY NQ/ES, or all instruments?
4. **Automation goal** — Are these rules for YOUR manual trading, or to train me (Claude) to execute autonomously?
5. **Backtesting** — Have you quantified your claims (85-90% WR, etc.), or are they intuitive?

---

**Status:** Awaiting Zion's refinement session answers. Once received, I'll build Phase 1 with surgical precision.
