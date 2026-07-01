"""
Supabase database layer for ICT Co-pilot trade storage.

Table: trades
  id           TEXT PRIMARY KEY       — YYYYMMDD_HHMMSS
  created_at   TIMESTAMPTZ            — auto
  symbol       TEXT
  timeframe    TEXT
  model        TEXT
  direction    TEXT
  confidence   TEXT
  rr_ratio     FLOAT
  entry_zone   TEXT
  stop         TEXT
  pt1          TEXT
  pt2          TEXT
  call         JSONB                  — full Claude response
  outcome      TEXT DEFAULT 'pending'
  notes        TEXT DEFAULT ''
"""
from __future__ import annotations  # 3.9-safe: keep `dict | None` annotations lazy

import os
from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

_url         = os.environ.get("SUPABASE_URL", "")
_service_key = os.environ.get("SUPABASE_SERVICE_KEY", "")
_client      = None


def _db():
    global _client
    if _client is None:
        if not _url or not _service_key:
            raise RuntimeError("SUPABASE_URL / SUPABASE_SERVICE_KEY not set in .env")
        _client = create_client(_url, _service_key)
    return _client


# ── Write ──────────────────────────────────────────────────────────────────────

def log_trade(call_id: str, call: dict, symbol: str, timeframe: str) -> str:
    """Insert a new trade call. Returns the call_id."""
    row = {
        "id":         call_id,
        "symbol":     symbol,
        "timeframe":  timeframe,
        "model":      call.get("model"),
        "direction":  call.get("direction"),
        "confidence": call.get("confidence"),
        "rr_ratio":   call.get("rr_ratio"),
        "entry_zone": call.get("entry_zone"),
        "stop":       call.get("stop"),
        "pt1":        call.get("pt1"),
        "pt2":        call.get("pt2"),
        "call":       call,
        "outcome":    "pending",
        "notes":      "",
    }
    _db().table("trades").insert(row).execute()
    return call_id


def update_outcome(call_id: str, outcome: str, notes: str = "") -> None:
    """Update outcome and notes for an existing trade."""
    _db().table("trades").update({
        "outcome": outcome,
        "notes":   notes,
    }).eq("id", call_id).execute()


# ── Read ───────────────────────────────────────────────────────────────────────

def get_trade(call_id: str) -> dict | None:
    """Fetch a single trade by ID."""
    res = _db().table("trades").select("*").eq("id", call_id).limit(1).execute()
    return res.data[0] if res.data else None


def get_history(limit: int = 200) -> list[dict]:
    """Return most recent trades, newest first."""
    res = (
        _db().table("trades")
        .select("id,created_at,symbol,timeframe,model,direction,confidence,rr_ratio,outcome,notes,call")
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )
    return res.data or []


def get_resolved_feedback(limit: int = 50) -> list[dict]:
    """Return last N resolved (non-pending) trades for model learning context."""
    res = (
        _db().table("trades")
        .select("id,created_at,symbol,model,direction,confidence,outcome,notes,call")
        .neq("outcome", "pending")
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )
    return list(reversed(res.data or []))   # oldest-first for context
