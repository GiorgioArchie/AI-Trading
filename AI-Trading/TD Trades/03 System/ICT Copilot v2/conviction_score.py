"""
Conviction Score — Gate 1 (Selection), from
`02 Playbook/(C) 02 Selection — Conviction (Lenses + Flow).md`.

Scores a structurally-valid setup 0–100 from the live Unusual Whales read that
uw_data.summarize() already parses (the `parsed` dict). Base 50, adjusted by the
lenses we can actually source from UW today. Verdict:
    TAKE ≥ 62 · HALF 45–61 · SKIP < 45
Commodities with no equity-options proxy → STRUCTURE_ONLY.

We compute BOTH a long and a short score before analysis; after Claude returns a
direction the matching score is attached to the response as `conviction`.

DATA NOTE — what is and isn't sourced:
  Live (from uw_data parsed dict): market tide, directional sweeps (flow ask
  premium), gamma proxy (one-sided flow spike), dark-pool prints.
  TODO — IV-rank lens (L2): uw_data does NOT currently parse `iv_rank`, so the
  IV-rank adjustments (>70 / <30 / 40–60) are EXCLUDED from the score. Add an
  `iv_rank` field to uw_data.summarize() to unlock this lens.
"""

# Verdict thresholds (02 Selection)
TAKE_FLOOR = 62
HALF_FLOOR = 45
BASE_SCORE = 50

# Symbol roots that have an equity-options proxy (NQ→QQQ, ES→SPY).
INDEX_ROOTS = {"NQ", "ES"}


def _root(symbol):
    if not symbol:
        return ""
    root = symbol.split(":")[-1].upper()
    # strip trailing digits / '!' (NQ1! -> NQ, MNQ1! -> MNQ)
    out = []
    for ch in root:
        if ch.isdigit() or ch == "!":
            break
        out.append(ch)
    r = "".join(out)
    if r.startswith("M") and r[1:] in {"NQ", "ES", "CL", "GC"}:
        r = r[1:]   # micro -> base root
    return r


def _has_equity_proxy(symbol):
    return _root(symbol) in INDEX_ROOTS


def _verdict(score):
    if score >= TAKE_FLOOR:
        return "TAKE"
    if score >= HALF_FLOOR:
        return "HALF"
    return "SKIP"


def _score_direction(uw, direction):
    """Score one direction ('long' or 'short') from the parsed UW dict.

    Long adjustments per 02 Selection; shorts mirror the sign on the directional
    lenses (tide, sweeps, dark pool). The gamma proxy (negative/positive gamma)
    is NON-directional — negative gamma favors trending/continuation regardless
    of side, so its sign is not mirrored.
    """
    is_long = (direction == "long")
    sign = 1 if is_long else -1
    score = BASE_SCORE
    breakdown = []

    # ── L3 flow — market tide net premium (UW market_tide) ──────
    # bullish tide +18 / bearish tide −25 (asymmetric per doctrine: a tide
    # against you is a stronger veto than a tide with you is a confirmation).
    tide = (uw or {}).get("tide", {})
    tide_bias = tide.get("bias", "")
    if "BULLISH" in tide_bias:
        pts = (18 if is_long else -25)
        score += pts
        breakdown.append({"lens": "L3 flow (tide)", "signal": "bullish tide", "points": pts})
    elif "BEARISH" in tide_bias:
        pts = (-25 if is_long else 18)
        score += pts
        breakdown.append({"lens": "L3 flow (tide)", "signal": "bearish tide", "points": pts})
    else:
        breakdown.append({"lens": "L3 flow (tide)", "signal": "neutral / no tide", "points": 0})

    # ── L3 sweeps — directional sweep flow (UW flow alerts) ─────
    # bullish (call-side aggressor) +10 / bearish (put-side) −10 for a long.
    flow = (uw or {}).get("flow", {})
    call_ask = flow.get("call_ask_prem", 0) or 0
    put_ask  = flow.get("put_ask_prem", 0) or 0
    if call_ask or put_ask:
        if call_ask > put_ask * 1.5:
            pts = sign * 10
            score += pts
            breakdown.append({"lens": "L3 sweeps", "signal": "bullish call-side aggressor", "points": pts})
        elif put_ask > call_ask * 1.5:
            pts = sign * -10
            score += pts
            breakdown.append({"lens": "L3 sweeps", "signal": "bearish put-side aggressor", "points": pts})
        else:
            breakdown.append({"lens": "L3 sweeps", "signal": "balanced sweep flow", "points": 0})
    else:
        breakdown.append({"lens": "L3 sweeps", "signal": "no sweep flow", "points": 0})

    # ── L1 gamma (proxy) — flow-alert spike ≈ negative gamma ────
    # negative gamma (one-sided aggressive spike) → trending favors continuation
    # (+15); a balanced/positive read (−15). Non-directional.
    total_ask = call_ask + put_ask
    if total_ask > 0:
        dominance = max(call_ask, put_ask) / total_ask
        if dominance >= 0.70:            # one-sided spike → negative-gamma proxy
            pts = 15
            score += pts
            breakdown.append({"lens": "L1 gamma (proxy)", "signal": "one-sided flow spike (neg-gamma proxy, trending)", "points": pts})
        else:                            # balanced → positive-gamma / mean-revert proxy
            pts = -15
            score += pts
            breakdown.append({"lens": "L1 gamma (proxy)", "signal": "balanced flow (pos-gamma proxy, mean-revert)", "points": pts})
    else:
        breakdown.append({"lens": "L1 gamma (proxy)", "signal": "no flow data", "points": 0})

    # ── L3 dark pool — supportive prints (UW darkpool) ──────────
    # supportive prints +8 (treated as supportive when present; mirror by side).
    dp = (uw or {}).get("darkpool", {})
    if dp.get("trades"):
        pts = sign * 8
        score += pts
        breakdown.append({"lens": "L3 dark pool", "signal": f"{dp['trades']} prints present", "points": pts})
    else:
        breakdown.append({"lens": "L3 dark pool", "signal": "no dark-pool prints", "points": 0})

    # ── L2 IV-rank lens — TODO (uw_data has no iv_rank) ─────────
    if (uw or {}).get("iv_rank") is not None:
        # Implement only if uw_data starts providing iv_rank.
        iv = uw["iv_rank"]
        if iv > 70:
            pts = 10
        elif iv < 30:
            pts = -15
        else:
            pts = -5
        score += pts
        breakdown.append({"lens": "L2 IV rank", "signal": f"iv_rank={iv}", "points": pts})
    else:
        breakdown.append({"lens": "L2 IV rank", "signal": "TODO — uw_data does not provide iv_rank (excluded)", "points": 0})

    score = max(0, min(100, score))
    return {"score": score, "verdict": _verdict(score), "breakdown": breakdown}


def compute(uw, symbol):
    """Compute BOTH long and short conviction from the parsed UW dict.

    Returns:
      {
        "structure_only": bool,         # True for commodities (no equity proxy)
        "long":  {score, verdict, breakdown} | None,
        "short": {score, verdict, breakdown} | None,
        "note":  str,
      }
    """
    if not _has_equity_proxy(symbol):
        return {
            "structure_only": True,
            "long": None,
            "short": None,
            "note": (f"STRUCTURE_ONLY — '{symbol}' has no equity-options proxy "
                     "(only NQ→QQQ / ES→SPY get conviction). Structure + chop decide."),
        }
    if not uw:
        return {
            "structure_only": False,
            "long": None,
            "short": None,
            "note": "UW data unavailable — conviction not scored this pass.",
        }
    return {
        "structure_only": False,
        "long":  _score_direction(uw, "long"),
        "short": _score_direction(uw, "short"),
        "note":  "",
    }


def for_direction(conviction, direction):
    """Pick the matching {score, verdict, breakdown} for a returned direction."""
    if not conviction:
        return None
    if conviction.get("structure_only"):
        return {"verdict": "STRUCTURE_ONLY", "score": None,
                "breakdown": [], "note": conviction.get("note", "")}
    d = (direction or "").strip().lower()
    if d == "long":
        return conviction.get("long")
    if d == "short":
        return conviction.get("short")
    return None


def context_block(conviction, symbol):
    """A short text block summarizing both scores for the Claude user message."""
    if not conviction:
        return ""
    if conviction.get("structure_only"):
        return f"## GATE 1 (SELECTION) CONTEXT\n{conviction['note']}"
    if conviction.get("long") is None:
        return f"## GATE 1 (SELECTION) CONTEXT\n{conviction.get('note', '')}"
    lng = conviction["long"]
    sht = conviction["short"]
    lines = [
        "## GATE 1 (SELECTION) CONTEXT — pre-computed from live UW (02 Selection)",
        f"LONG  conviction: {lng['score']}/100 → {lng['verdict']}",
        f"SHORT conviction: {sht['score']}/100 → {sht['verdict']}",
        "(TAKE ≥62 / HALF 45–61 / SKIP <45. The lens regime should AGREE with the "
        "model: negative-gamma/trending favors CONT; positive-gamma/mean-revert "
        "favors REV at extremes. Weigh this against structure; it does not override it.)",
    ]
    return "\n".join(lines)
