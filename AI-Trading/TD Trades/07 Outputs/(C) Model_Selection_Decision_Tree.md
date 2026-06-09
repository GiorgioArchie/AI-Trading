# Trading Model Decision Tree — Which Model When?
**Ruflo-Generated Quick Reference** | Print this, laminate it, keep at your desk

---

## The Question Tree

Three layers run in sequence. Each layer narrows context — Layer A makes the final ICT model decision.

```
START: You see a setup forming on your chart

    ╔═════════════════════════════════════════╗
    ║  LAYER C — GAMMA REGIME                 ║
    ║  (Statistical backdrop — runs pre-market)║
    ╚═════════════════════════════════════════╝
    
    Is gamma regime influence LOW relative
    to current volatility and distance from
    gamma levels?
      YES → Regime = sizing modifier only. All models available.
      NO  → Regime = structural filter. Veto continuation
            breakouts until key gamma wall is cleared.
    
    ↓
    
    ╔═════════════════════════════════════════╗
    ║  LAYER B — NEWS / MFD FILTER            ║
    ║  (Event gate)                           ║
    ╚═════════════════════════════════════════╝
    
    ┌─────────────────────────────────────────┐
    │ Is there a HIGH-IMPACT NEWS event       │
    │ happening in the next 1-2 hours?        │
    │ YES → Go to MFD MODEL                   │
    │ NO → Continue to Layer A               │
    └─────────────────────────────────────────┘
    
    ↓
    
    ╔═════════════════════════════════════════╗
    ║  LAYER A — ICT ORDER FLOW               ║
    ║  (Actual model selection)               ║
    ╚═════════════════════════════════════════╝
    
    ┌─────────────────────────────────────────┐
    │ Did order flow just FLIP?               │
    │ (ERL taken + neckline shift)            │
    │ YES → Go to REV MODEL                   │
    │ NO → Continue                          │
    └─────────────────────────────────────────┘
    
    ↓
    
    ┌─────────────────────────────────────────┐
    │ Is order flow STRONG and aligned        │
    │ across timeframes?                      │
    │ YES → Go to CONTINUATION MODEL          │
    │ NO → Continue                          │
    └─────────────────────────────────────────┘
    
    ↓
    
    ┌─────────────────────────────────────────┐
    │ Is there an IFVG retesting in a         │
    │ structured environment?                 │
    │ YES → Go to IFVG MODEL                  │
    │ NO → SKIP, No Setup                    │
    └─────────────────────────────────────────┘
```

---

## Model Profiles (Quick Ref)

### 🔄 REV MODEL (Reversal)
**When:** Price seeks ERL, creates structure low, then shows impulsive reversal below structure

**Setup Requirements:**
- [ ] HTF trend confirmed
- [ ] Price has swept ERL
- [ ] Structure low/neckline formed
- [ ] Impulsive reaction below structure
- [ ] IRL fair value zone identified
- [ ] Clear draw above (ERL target)

**Entry:** Flip candle off neckline break  
**SL:** Below structure (previous wick / neckline). Scale with IV rank and GEX regime — never fixed pips. In negative-GEX regime, multiply normal stop by ~1.5×.  
**PT1:** IRL (fair value) — scale 50%, move SL to BE  
**PT2:** ERL (premium target) — run remaining position  

**Win Rate (Claimed):** 85-90% if all conditions met  
**Best For:** Scalping to medium-term (5m-15m timeframes)  

**Red Flags (Abort if):**
- [ ] HTF structure shows no clear bias
- [ ] Price hasn't actually swept the ERL
- [ ] Neckline is too recent (no structure confirmation)
- [ ] Multiple competing fair value zones

---

### ➡️ CONTINUATION MODEL (Ride the Wave)
**When:** Strong trend in place, price pulls back to fair value (IRL), then continues toward premium (ERL)

**Setup Requirements:**
- [ ] HTF shows clear bullish/bearish structure (HH/HL or LL/LH)
- [ ] Price has swept IRL recently
- [ ] No major reversal signals
- [ ] FTSL/FTSH checked — if present, treat as additional confluence (not mandatory)
- [ ] Fair value zone identified (multiple TF alignment)
- [ ] Clear external draw/liquidity above/below

**Entry:** After retracement into IRL + model confirmation  
**SL:** Below structure low. Scale with IV rank and GEX regime — never fixed pips.  
**PT1:** IRL (scale 50%, move SL to BE)  
**PT2:** Full ERL (run remaining position)  

**Win Rate:** Depends on HTF/LTF alignment  
**Best For:** Momentum traders, riding strong trends, scalping with direction

**Red Flags (Abort if):**
- [ ] HTF bias weak or conflicted
- [ ] Price creates a reversal structure before reaching IRL
- [ ] FTSL forms instead of expected retracement

---

### 📊 IFVG MODEL (Gap Filling)
**When:** Price has moved too fast, creating a fair value gap or imbalance that will be retested

**Setup Requirements:**
- [ ] Clear FVG or imbalance visible on chart
- [ ] Price has moved impulsively away from the gap
- [ ] Gap is "recent" (within last few candles, not old)
- [ ] Price structure suggests it will return

**Entry:** When price retraces back toward the FVG  
**SL:** Beyond the FVG opposite side  
**PT1:** Inside the FVG  
**PT2:** Full fair value fill + continuation toward premium  

**Win Rate:** High-probability if structure supports  
**Best For:** Counter-trend scalps, gap fills, rebalancing after impulses

**Red Flags (Abort if):**
- [ ] Old FVG (3+ candles ago) — likely already priced in
- [ ] Massive impulse move — may not retrace to gap
- [ ] No supporting structure for a reversal

---

### 📰 MFD MODEL (Macro Fueled Data / News-Based)
**When:** High-impact news event creates volatility + new liquidity pools

**Setup Requirements:**
- [ ] Red-folder news identified (CPI, NFP, FOMC, etc.)
- [ ] News timing known (hours/minutes until event)
- [ ] Pre-news bias established (HTF structure)
- [ ] Key price levels marked (expected reaction zones)
- [ ] Order flow shows institutional movement

**Entry:** AFTER news prints + structure confirmation (NOT during the spike)  
**SL:** Outside the news-generated high/low  
**PT1:** Previous key level (fair value)  
**PT2:** Larger objective (ERL or premium)  

**Win Rate:** "Precision" when setup aligns; variable otherwise  
**Best For:** Anticipating macro-driven moves, larger trends, institutional order flow

**Red Flags (Abort if):**
- [ ] You don't have a pre-news thesis
- [ ] You're trying to trade DURING the news (too chaotic)
- [ ] News already priced in (no surprise)
- [ ] Structure doesn't align with news direction

---

## Model Comparison Matrix

| Aspect | Rev | Continuation | IFVG | MFD |
|--------|-----|--------------|------|-----|
| **Setup Frequency** | Medium | High | High | Low (news-dependent) |
| **Time to Develop** | 2-5m | 5-15m+ | 1-3m | Minutes (post-news) |
| **Scalping vs Trend** | Both | Trend | Scalp | Trend |
| **Risk Level** | Low (tight SL) | Low-Med | Low | Med-High |
| **R:R Potential** | 1:2-1:3 | 1:3-1:5 | 1:1.5-1:2 | 1:3-1:5+ |
| **Skill Required** | High | High | Medium | High |
| **Best TF** | 1-5m | 5-15m | 1-5m | 5-15m+ |

---

## Decision Flowchart (Text Version)

### Scenario 1: You see price spike suddenly up
```
↓ Is it news-driven? → YES → MFD check: did structure confirm? → Rev or Cont
                     → NO  → Rev Model: is there a structure low forming? → Rev or Ifvg
```

### Scenario 2: Price is in a clear trend
```
↓ Does it pull back to fair value? → YES → Continuation Model (entry on retrace)
                                   → NO  → Price still impulse, wait for structure
```

### Scenario 3: Price gaps quickly, leaving inefficiency
```
↓ Is the gap recent? → YES → IFVG Model (wait for retrace into gap)
                     → NO  → Gap already filled, find next setup
```

### Scenario 4: Price is choppy, no clear direction
```
↓ Skip. No setup. Wait for:
  - Clearer structure
  - HTF bias confirmation
  - Major news catalyst
```

---

## Model Combination (Advanced)

### HTF Rev + LTF Continuation = Highest Probability
**Scenario:** Daily chart shows reversal setup. Hourly shows continuation trend.

**Interpretation:** Reversal is forming on daily; take continuation trades on the pullback (5m) while the reversal structures. Once daily reversal confirmed, full position sizing.

**Your note from education:** "Using HTF models can make it much easier to identify what you need for confirmations. If price has a HTF rev model and you zoom back into the 1-5min and see a continuation model, the probability will be much higher per trade you take."

---

## Common Mistakes (Avoid These)

| Mistake | Impact | Fix |
|---------|--------|-----|
| **Using Continuation Model when Rev is forming** | Whipsawed into trend, then reversal | Check HTF structure first |
| **Trading IFVG on old gaps (3+ candles old)** | Gap already priced in, fails to retrace | Only trade fresh gaps |
| **Forcing MFD without pre-news thesis** | Entering chaos, no plan | Prep thesis before news |
| **Mixing models mid-trade** | Unclear exit criteria, emotional exits | Stick to one model per setup |
| **Ignoring HTF when trading LTF** | Fighting the trend, high SL cost | HTF bias ALWAYS first |
| **Entering Rev without neckline break** | False breakout into old structure | Wait for clear neckline |
| **Scalping Continuation without SL** | One bad extension wipes profit | Always SL below structure |

---

## Pre-Trade Checklist (60 Seconds)

Before EVERY trade, ask:

1. **[ ] HTF Bias** — What's the daily/4h structure? Which direction?
2. **[ ] Model Confirmation** — Which model? Is the checklist complete?
3. **[ ] Confluence** — How many signals align? (FVG + OB + structure?)
4. **[ ] Entry Logic** — Why am I entering NOW, not 5 min ago/later?
5. **[ ] Risk Defined** — SL price? Position size? R:R calculated?
6. **[ ] Exit Plan** — PT1? PT2? How do I scale?
7. **[ ] Time Context** — What's the session? Any news?
8. **[ ] Emotional State** — Am I chase/FOMO, or patient entry?

**If you answer "no" or "unclear" to ANY, skip the trade.**

---

## Quick Model Identifier (Look at This When Confused)

**You see:**
- ERL taken + structure low + reversal impulse below neckline = **REV MODEL**
- Strong trend + pullback to IRL + resume direction = **CONTINUATION**
- Fast move leaving unfilled gap = **IFVG**
- News print + structure shift + new liquidity = **MFD**
- Multiple FVG/imbalances aligning on multi-TF = **All models** (highest confluenc)

---

## Your Next Step

**Print this decision tree.** Next 10 trades, annotate:
1. Which model was it? (Rev / Cont / IFVG / MFD / None)
2. Did you identify it pre-trade or post?
3. If you missed it, why?
4. Did the model play out?

**This data → improves your pattern recognition in real-time.**

---

**Status:** Awaiting Zion's first 10-trade annotations. After that, we'll refine this tree with YOUR specific model frequencies + patterns.
