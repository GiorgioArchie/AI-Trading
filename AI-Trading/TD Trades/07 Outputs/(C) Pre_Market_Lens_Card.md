# Pre-Market Lens Card — [YYYY-MM-DD]

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
