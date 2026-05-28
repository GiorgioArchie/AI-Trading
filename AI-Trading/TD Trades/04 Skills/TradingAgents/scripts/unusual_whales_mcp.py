#!/usr/bin/env python3
"""
MCP Server for Unusual Whales API.

Provides tools for options flow, dark pool trades, congressional trading,
insider activity, and market/stock data via the Unusual Whales API.

Usage:
    export UNUSUAL_WHALES_API_KEY="your_api_key_here"
    python unusual_whales_mcp.py
"""

import json
import os
import sys
from enum import Enum
from typing import Any, Dict, List, Optional

import httpx
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, ConfigDict, Field, field_validator

# ---------------------------------------------------------------------------
# Server init
# ---------------------------------------------------------------------------
mcp = FastMCP("unusual_whales_mcp")

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
API_BASE_URL = "https://api.unusualwhales.com"

# ---------------------------------------------------------------------------
# Shared enums
# ---------------------------------------------------------------------------


class ResponseFormat(str, Enum):
    """Output format for tool responses."""

    MARKDOWN = "markdown"
    JSON = "json"


class CandleSize(str, Enum):
    """OHLC candle sizes."""

    ONE_MIN = "1"
    FIVE_MIN = "5"
    FIFTEEN_MIN = "15"
    THIRTY_MIN = "30"
    ONE_HOUR = "60"
    FOUR_HOUR = "240"
    ONE_DAY = "D"
    ONE_WEEK = "W"


# ---------------------------------------------------------------------------
# Shared utilities
# ---------------------------------------------------------------------------


def _get_api_key() -> str:
    key = os.environ.get("UNUSUAL_WHALES_API_KEY", "")
    if not key:
        raise ValueError(
            "UNUSUAL_WHALES_API_KEY environment variable is not set. "
            "Set it with: export UNUSUAL_WHALES_API_KEY=your_key"
        )
    return key


async def _api_get(path: str, params: Optional[Dict[str, Any]] = None) -> Any:
    """Make an authenticated GET request to the Unusual Whales API."""
    headers = {
        "Authorization": f"Bearer {_get_api_key()}",
        "Accept": "application/json",
    }
    # Strip None values from params
    clean_params = {k: v for k, v in (params or {}).items() if v is not None}
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{API_BASE_URL}{path}",
            headers=headers,
            params=clean_params,
            timeout=30.0,
        )
        response.raise_for_status()
        return response.json()


def _handle_api_error(e: Exception) -> str:
    """Return a clear, actionable error string."""
    if isinstance(e, ValueError):
        return f"Configuration error: {e}"
    if isinstance(e, httpx.HTTPStatusError):
        code = e.response.status_code
        if code == 401:
            return "Error 401: Invalid API key. Check your UNUSUAL_WHALES_API_KEY."
        if code == 403:
            return "Error 403: Access denied. Your plan may not include this endpoint."
        if code == 404:
            return "Error 404: Not found. Check the ticker symbol or other parameters."
        if code == 422:
            try:
                detail = e.response.json()
                return f"Error 422: Invalid parameters – {json.dumps(detail)}"
            except Exception:
                return "Error 422: Invalid request parameters."
        if code == 429:
            return "Error 429: Rate limit exceeded. Wait a moment and try again."
        return f"API error {code}: {e.response.text[:300]}"
    if isinstance(e, httpx.TimeoutException):
        return "Error: Request timed out. The API may be slow – try again."
    return f"Unexpected error ({type(e).__name__}): {e}"


def _to_json(data: Any) -> str:
    return json.dumps(data, indent=2, default=str)


def _ticker_upper(v: str) -> str:
    return v.strip().upper()


# ---------------------------------------------------------------------------
# Pydantic input models
# ---------------------------------------------------------------------------


class TickerInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True)
    ticker: str = Field(..., description="Stock ticker symbol (e.g. 'AAPL', 'SPY')", min_length=1, max_length=10)
    response_format: ResponseFormat = Field(default=ResponseFormat.MARKDOWN, description="'markdown' or 'json'")

    @field_validator("ticker")
    @classmethod
    def upper_ticker(cls, v: str) -> str:
        return _ticker_upper(v)


class TickerPaginatedInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True)
    ticker: str = Field(..., description="Stock ticker symbol (e.g. 'AAPL', 'SPY')", min_length=1, max_length=10)
    limit: Optional[int] = Field(default=25, description="Max results to return (1–100)", ge=1, le=100)
    page: Optional[int] = Field(default=0, description="Page number for pagination (0-based)", ge=0)
    response_format: ResponseFormat = Field(default=ResponseFormat.MARKDOWN, description="'markdown' or 'json'")

    @field_validator("ticker")
    @classmethod
    def upper_ticker(cls, v: str) -> str:
        return _ticker_upper(v)


class FlowAlertsInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True)
    ticker: Optional[str] = Field(default=None, description="Filter by ticker symbol (e.g. 'AAPL'). Leave blank for all tickers.")
    limit: Optional[int] = Field(default=25, description="Max results (1–100)", ge=1, le=100)
    page: Optional[int] = Field(default=0, description="Page number (0-based)", ge=0)
    response_format: ResponseFormat = Field(default=ResponseFormat.MARKDOWN, description="'markdown' or 'json'")

    @field_validator("ticker")
    @classmethod
    def upper_ticker(cls, v: Optional[str]) -> Optional[str]:
        return _ticker_upper(v) if v else None


class DarkpoolRecentInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True)
    limit: Optional[int] = Field(default=25, description="Max results (1–100)", ge=1, le=100)
    page: Optional[int] = Field(default=0, description="Page number (0-based)", ge=0)
    response_format: ResponseFormat = Field(default=ResponseFormat.MARKDOWN, description="'markdown' or 'json'")


class CongressTradesInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True)
    limit: Optional[int] = Field(default=25, description="Max results (1–100)", ge=1, le=100)
    page: Optional[int] = Field(default=0, description="Page number (0-based)", ge=0)
    response_format: ResponseFormat = Field(default=ResponseFormat.MARKDOWN, description="'markdown' or 'json'")


class CongressTraderInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True)
    politician_name: str = Field(..., description="Full name of the politician (e.g. 'Nancy Pelosi')", min_length=2)
    limit: Optional[int] = Field(default=25, description="Max results (1–100)", ge=1, le=100)
    response_format: ResponseFormat = Field(default=ResponseFormat.MARKDOWN, description="'markdown' or 'json'")


class InsiderTransactionsInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True)
    limit: Optional[int] = Field(default=25, description="Max results (1–100)", ge=1, le=100)
    page: Optional[int] = Field(default=0, description="Page number (0-based)", ge=0)
    response_format: ResponseFormat = Field(default=ResponseFormat.MARKDOWN, description="'markdown' or 'json'")


class OhlcInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True)
    ticker: str = Field(..., description="Stock ticker symbol (e.g. 'AAPL')", min_length=1, max_length=10)
    candle_size: CandleSize = Field(default=CandleSize.ONE_DAY, description="Candle size: 1, 5, 15, 30, 60, 240, D, W")
    response_format: ResponseFormat = Field(default=ResponseFormat.MARKDOWN, description="'markdown' or 'json'")

    @field_validator("ticker")
    @classmethod
    def upper_ticker(cls, v: str) -> str:
        return _ticker_upper(v)


class ScreenerInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True)
    limit: Optional[int] = Field(default=25, description="Max results (1–100)", ge=1, le=100)
    response_format: ResponseFormat = Field(default=ResponseFormat.MARKDOWN, description="'markdown' or 'json'")


class MarketMoversInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True)
    response_format: ResponseFormat = Field(default=ResponseFormat.MARKDOWN, description="'markdown' or 'json'")


class NewsInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True)
    limit: Optional[int] = Field(default=25, description="Max results (1–100)", ge=1, le=100)
    response_format: ResponseFormat = Field(default=ResponseFormat.MARKDOWN, description="'markdown' or 'json'")


class FullTapeInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True)
    date: str = Field(..., description="Date in YYYY-MM-DD format (e.g. '2025-01-15')", pattern=r"^\d{4}-\d{2}-\d{2}$")
    ticker: Optional[str] = Field(default=None, description="Optional ticker filter")
    limit: Optional[int] = Field(default=50, description="Max results (1–200)", ge=1, le=200)
    response_format: ResponseFormat = Field(default=ResponseFormat.MARKDOWN, description="'markdown' or 'json'")

    @field_validator("ticker")
    @classmethod
    def upper_ticker(cls, v: Optional[str]) -> Optional[str]:
        return _ticker_upper(v) if v else None


class UnusualCongressTradesInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True)
    limit: Optional[int] = Field(default=25, description="Max results (1–100)", ge=1, le=100)
    response_format: ResponseFormat = Field(default=ResponseFormat.MARKDOWN, description="'markdown' or 'json'")


# ---------------------------------------------------------------------------
# Helper formatters
# ---------------------------------------------------------------------------


def _fmt_flow_alert(item: dict) -> str:
    return (
        f"**{item.get('ticker', '?')}** | "
        f"{item.get('option_symbol', item.get('contract', '?'))} | "
        f"Type: {item.get('type', '?')} | "
        f"Strike: {item.get('strike', '?')} | "
        f"Exp: {item.get('expiry', item.get('expiration_date', '?'))} | "
        f"Premium: ${item.get('total_premium', item.get('premium', '?'))} | "
        f"Vol: {item.get('volume', '?')} | "
        f"OI: {item.get('open_interest', '?')} | "
        f"Side: {item.get('side', item.get('put_call', '?'))}"
    )


def _fmt_darkpool(item: dict) -> str:
    return (
        f"**{item.get('ticker', '?')}** | "
        f"Price: ${item.get('price', item.get('executed_price', '?'))} | "
        f"Size: {item.get('size', item.get('shares', item.get('volume', '?')))} | "
        f"Premium: ${item.get('premium', item.get('notional_value', '?'))} | "
        f"Time: {item.get('executed_at', item.get('date', '?'))}"
    )


def _fmt_congress(item: dict) -> str:
    return (
        f"**{item.get('politician_name', item.get('full_name', '?'))}** | "
        f"{item.get('ticker', '?')} | "
        f"Type: {item.get('transaction_type', item.get('type', '?'))} | "
        f"Amount: {item.get('amount', item.get('trade_size_range', '?'))} | "
        f"Date: {item.get('transaction_date', item.get('date', item.get('disclosure_date', '?')))}"
    )


def _fmt_insider(item: dict) -> str:
    return (
        f"**{item.get('ticker', '?')}** | "
        f"{item.get('insider_name', item.get('name', '?'))} ({item.get('relationship', item.get('title', '?'))}) | "
        f"Type: {item.get('transaction_type', item.get('type', '?'))} | "
        f"Shares: {item.get('shares', '?')} | "
        f"Price: ${item.get('price', '?')} | "
        f"Date: {item.get('date', item.get('filed_date', '?'))}"
    )


def _extract_list(data: Any, *keys: str) -> List[dict]:
    """Try to pull a list from common response structures."""
    if isinstance(data, list):
        return data
    for k in keys:
        if isinstance(data, dict) and k in data:
            val = data[k]
            if isinstance(val, list):
                return val
    if isinstance(data, dict):
        for v in data.values():
            if isinstance(v, list):
                return v
    return []


# ---------------------------------------------------------------------------
# TOOLS — Options Flow
# ---------------------------------------------------------------------------


@mcp.tool(
    name="uw_flow_alerts",
    annotations={
        "title": "Unusual Whales: Options Flow Alerts",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def uw_flow_alerts(params: FlowAlertsInput) -> str:
    """
    Fetch unusual options flow alerts from Unusual Whales.

    Returns flagged options trades with large premiums, sweep activity,
    or other signals of unusual positioning. Can filter by ticker or
    return the global feed.

    Args:
        params (FlowAlertsInput):
            - ticker (Optional[str]): Filter by ticker (e.g. 'TSLA'). Omit for all.
            - limit (int): Max results (1–100, default 25).
            - page (int): Pagination page (0-based, default 0).
            - response_format: 'markdown' (default) or 'json'.

    Returns:
        str: Formatted list of options flow alerts.

    Examples:
        - "Show me unusual options flow" → params with no ticker
        - "AAPL unusual options flow" → params with ticker='AAPL'
    """
    try:
        if params.ticker:
            data = await _api_get(f"/api/stock/{params.ticker}/flow-alerts", {"limit": params.limit, "page": params.page})
        else:
            data = await _api_get("/api/option-trades/flow-alerts", {"limit": params.limit, "page": params.page})

        items = _extract_list(data, "data", "flow_alerts", "alerts", "results")

        if not items:
            return f"No flow alerts found{' for ' + params.ticker if params.ticker else ''}."

        if params.response_format == ResponseFormat.JSON:
            return _to_json({"count": len(items), "page": params.page, "items": items})

        label = f" for {params.ticker}" if params.ticker else ""
        lines = [f"# Options Flow Alerts{label}", f"*{len(items)} alerts (page {params.page})*", ""]
        for item in items:
            lines.append(f"- {_fmt_flow_alert(item)}")
        return "\n".join(lines)

    except Exception as e:
        return _handle_api_error(e)


@mcp.tool(
    name="uw_flow_recent",
    annotations={
        "title": "Unusual Whales: Recent Options Flow for Ticker",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def uw_flow_recent(params: TickerPaginatedInput) -> str:
    """
    Fetch recent options flow trades for a specific ticker.

    Returns the latest options transactions for the given stock symbol,
    including premiums, volume, and directional bias.

    Args:
        params (TickerPaginatedInput):
            - ticker (str): Stock ticker symbol (e.g. 'SPY').
            - limit (int): Max results (1–100, default 25).
            - page (int): Pagination page (0-based, default 0).
            - response_format: 'markdown' or 'json'.

    Returns:
        str: Formatted recent options flow trades.

    Examples:
        - "Recent options flow for SPY" → ticker='SPY'
        - "What options are being traded on NVDA?" → ticker='NVDA'
    """
    try:
        data = await _api_get(
            f"/api/stock/{params.ticker}/flow-recent",
            {"limit": params.limit, "page": params.page},
        )
        items = _extract_list(data, "data", "flow", "results", "trades")

        if not items:
            return f"No recent flow found for {params.ticker}."

        if params.response_format == ResponseFormat.JSON:
            return _to_json({"ticker": params.ticker, "count": len(items), "items": items})

        lines = [f"# Recent Options Flow: {params.ticker}", f"*{len(items)} trades*", ""]
        for item in items:
            lines.append(f"- {_fmt_flow_alert(item)}")
        return "\n".join(lines)

    except Exception as e:
        return _handle_api_error(e)


@mcp.tool(
    name="uw_flow_full_tape",
    annotations={
        "title": "Unusual Whales: Full Options Tape by Date",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def uw_flow_full_tape(params: FullTapeInput) -> str:
    """
    Retrieve the full options tape for a specific trading date.

    Returns all flagged options trades recorded on the given date.
    Useful for end-of-day review or backtesting flow signals.

    Args:
        params (FullTapeInput):
            - date (str): Date in YYYY-MM-DD format (e.g. '2025-06-10').
            - ticker (Optional[str]): Filter by ticker.
            - limit (int): Max results (1–200, default 50).
            - response_format: 'markdown' or 'json'.

    Returns:
        str: Formatted full options tape for the date.
    """
    try:
        query: Dict[str, Any] = {"limit": params.limit}
        if params.ticker:
            query["ticker"] = params.ticker
        data = await _api_get(f"/api/option-trades/full-tape/{params.date}", query)
        items = _extract_list(data, "data", "trades", "results")

        if not items:
            label = f" for {params.ticker}" if params.ticker else ""
            return f"No tape data found on {params.date}{label}."

        if params.response_format == ResponseFormat.JSON:
            return _to_json({"date": params.date, "count": len(items), "items": items})

        label = f" — {params.ticker}" if params.ticker else ""
        lines = [f"# Full Options Tape: {params.date}{label}", f"*{len(items)} trades*", ""]
        for item in items:
            lines.append(f"- {_fmt_flow_alert(item)}")
        return "\n".join(lines)

    except Exception as e:
        return _handle_api_error(e)


@mcp.tool(
    name="uw_flow_per_expiry",
    annotations={
        "title": "Unusual Whales: Options Flow Breakdown by Expiry",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def uw_flow_per_expiry(params: TickerInput) -> str:
    """
    Get options flow grouped by expiration date for a ticker.

    Shows where premium and volume are concentrated across different
    expiry dates, helping identify near-term vs. long-dated positioning.

    Args:
        params (TickerInput):
            - ticker (str): Stock ticker symbol.
            - response_format: 'markdown' or 'json'.

    Returns:
        str: Options flow broken down by expiry.
    """
    try:
        data = await _api_get(f"/api/stock/{params.ticker}/flow-per-expiry")
        items = _extract_list(data, "data", "expirations", "results")

        if not items:
            return f"No flow-by-expiry data found for {params.ticker}."

        if params.response_format == ResponseFormat.JSON:
            return _to_json({"ticker": params.ticker, "items": items})

        lines = [f"# Options Flow by Expiry: {params.ticker}", ""]
        for item in items:
            expiry = item.get("expiry", item.get("expiration_date", "?"))
            calls = item.get("call_premium", item.get("calls_premium", "?"))
            puts = item.get("put_premium", item.get("puts_premium", "?"))
            lines.append(f"- **{expiry}**: Calls ${calls} | Puts ${puts}")
        return "\n".join(lines)

    except Exception as e:
        return _handle_api_error(e)


@mcp.tool(
    name="uw_iv_rank",
    annotations={
        "title": "Unusual Whales: IV Rank for Ticker",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def uw_iv_rank(params: TickerInput) -> str:
    """
    Get the Implied Volatility (IV) Rank for a stock ticker.

    IV Rank indicates how current implied volatility compares to its
    52-week range (0 = lowest, 100 = highest). Useful for options pricing.

    Args:
        params (TickerInput):
            - ticker (str): Stock ticker symbol.
            - response_format: 'markdown' or 'json'.

    Returns:
        str: Current IV rank and related volatility metrics.
    """
    try:
        data = await _api_get(f"/api/stock/{params.ticker}/iv-rank")

        if params.response_format == ResponseFormat.JSON:
            return _to_json(data)

        if isinstance(data, dict):
            d = data.get("data", data)
            lines = [f"# IV Rank: {params.ticker}", ""]
            for k, v in d.items():
                lines.append(f"- **{k}**: {v}")
            return "\n".join(lines)
        return _to_json(data)

    except Exception as e:
        return _handle_api_error(e)


# ---------------------------------------------------------------------------
# TOOLS — Dark Pool
# ---------------------------------------------------------------------------


@mcp.tool(
    name="uw_darkpool_recent",
    annotations={
        "title": "Unusual Whales: Recent Dark Pool Trades",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def uw_darkpool_recent(params: DarkpoolRecentInput) -> str:
    """
    Fetch the most recent dark pool (off-exchange) trades across all tickers.

    Dark pool prints represent large block trades executed away from public
    exchanges. High-value prints often indicate institutional positioning.

    Args:
        params (DarkpoolRecentInput):
            - limit (int): Max results (1–100, default 25).
            - page (int): Pagination page (0-based, default 0).
            - response_format: 'markdown' or 'json'.

    Returns:
        str: Formatted list of recent dark pool trades.

    Examples:
        - "Show me the latest dark pool trades" → default params
        - "Top 50 dark pool prints" → limit=50
    """
    try:
        data = await _api_get("/api/darkpool/recent", {"limit": params.limit, "page": params.page})
        items = _extract_list(data, "data", "darkpool", "trades", "results")

        if not items:
            return "No recent dark pool trades found."

        if params.response_format == ResponseFormat.JSON:
            return _to_json({"count": len(items), "page": params.page, "items": items})

        lines = [f"# Recent Dark Pool Trades", f"*{len(items)} trades (page {params.page})*", ""]
        for item in items:
            lines.append(f"- {_fmt_darkpool(item)}")
        return "\n".join(lines)

    except Exception as e:
        return _handle_api_error(e)


@mcp.tool(
    name="uw_darkpool_ticker",
    annotations={
        "title": "Unusual Whales: Dark Pool Trades for Ticker",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def uw_darkpool_ticker(params: TickerPaginatedInput) -> str:
    """
    Fetch dark pool trades for a specific stock ticker.

    Shows off-exchange block prints for the given symbol, helping identify
    large institutional buying or selling activity.

    Args:
        params (TickerPaginatedInput):
            - ticker (str): Stock ticker symbol (e.g. 'AAPL').
            - limit (int): Max results (1–100, default 25).
            - page (int): Pagination page (0-based, default 0).
            - response_format: 'markdown' or 'json'.

    Returns:
        str: Formatted dark pool trades for the ticker.

    Examples:
        - "Dark pool activity for NVDA" → ticker='NVDA'
        - "AAPL dark pool prints" → ticker='AAPL'
    """
    try:
        data = await _api_get(
            f"/api/darkpool/{params.ticker}",
            {"limit": params.limit, "page": params.page},
        )
        items = _extract_list(data, "data", "darkpool", "trades", "results")

        if not items:
            return f"No dark pool trades found for {params.ticker}."

        if params.response_format == ResponseFormat.JSON:
            return _to_json({"ticker": params.ticker, "count": len(items), "items": items})

        lines = [f"# Dark Pool Trades: {params.ticker}", f"*{len(items)} trades*", ""]
        for item in items:
            lines.append(f"- {_fmt_darkpool(item)}")
        return "\n".join(lines)

    except Exception as e:
        return _handle_api_error(e)


# ---------------------------------------------------------------------------
# TOOLS — Congressional / Insider
# ---------------------------------------------------------------------------


@mcp.tool(
    name="uw_congress_recent_trades",
    annotations={
        "title": "Unusual Whales: Recent Congressional Trades",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def uw_congress_recent_trades(params: CongressTradesInput) -> str:
    """
    Fetch the most recently disclosed congressional stock trades.

    Members of Congress must disclose stock transactions within 45 days.
    This tool returns the latest filings across all politicians.

    Args:
        params (CongressTradesInput):
            - limit (int): Max results (1–100, default 25).
            - page (int): Pagination page (0-based, default 0).
            - response_format: 'markdown' or 'json'.

    Returns:
        str: Recent congressional trade disclosures.

    Examples:
        - "What stocks did congress buy recently?" → default params
        - "Show 50 congressional trades" → limit=50
    """
    try:
        data = await _api_get("/api/congress/recent-trades", {"limit": params.limit, "page": params.page})
        items = _extract_list(data, "data", "trades", "results")

        if not items:
            return "No recent congressional trades found."

        if params.response_format == ResponseFormat.JSON:
            return _to_json({"count": len(items), "page": params.page, "items": items})

        lines = [f"# Recent Congressional Trades", f"*{len(items)} disclosures (page {params.page})*", ""]
        for item in items:
            lines.append(f"- {_fmt_congress(item)}")
        return "\n".join(lines)

    except Exception as e:
        return _handle_api_error(e)


@mcp.tool(
    name="uw_congress_politician_trades",
    annotations={
        "title": "Unusual Whales: Congressional Trades by Politician",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def uw_congress_politician_trades(params: CongressTraderInput) -> str:
    """
    Fetch disclosed stock trades for a specific politician.

    Look up the trading history for a named member of Congress.

    Args:
        params (CongressTraderInput):
            - politician_name (str): Full name of the politician (e.g. 'Nancy Pelosi').
            - limit (int): Max results (1–100, default 25).
            - response_format: 'markdown' or 'json'.

    Returns:
        str: Trade disclosures for the specified politician.

    Examples:
        - "What has Nancy Pelosi been buying?" → politician_name='Nancy Pelosi'
        - "Show me trades from Austin Scott" → politician_name='Austin Scott'
    """
    try:
        data = await _api_get(
            "/api/congress/congress-trader",
            {"politician_name": params.politician_name, "limit": params.limit},
        )
        items = _extract_list(data, "data", "trades", "results")

        if not items:
            return f"No trades found for '{params.politician_name}'."

        if params.response_format == ResponseFormat.JSON:
            return _to_json({"politician": params.politician_name, "count": len(items), "items": items})

        lines = [f"# Congressional Trades: {params.politician_name}", f"*{len(items)} disclosures*", ""]
        for item in items:
            lines.append(f"- {_fmt_congress(item)}")
        return "\n".join(lines)

    except Exception as e:
        return _handle_api_error(e)


@mcp.tool(
    name="uw_congress_politicians",
    annotations={
        "title": "Unusual Whales: List Politicians with Trade Data",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def uw_congress_politicians(params: MarketMoversInput) -> str:
    """
    List all politicians who have filed stock trade disclosures.

    Returns names and metadata for members of Congress tracked by
    Unusual Whales. Use the names here with uw_congress_politician_trades.

    Args:
        params (MarketMoversInput):
            - response_format: 'markdown' or 'json'.

    Returns:
        str: List of politicians with trade disclosure data.
    """
    try:
        data = await _api_get("/api/congress/politicians")
        items = _extract_list(data, "data", "politicians", "results")

        if not items:
            return "No politician data found."

        if params.response_format == ResponseFormat.JSON:
            return _to_json({"count": len(items), "politicians": items})

        lines = [f"# Politicians with Trade Disclosures", f"*{len(items)} politicians*", ""]
        for item in items:
            name = item.get("full_name", item.get("name", "?"))
            party = item.get("party", "?")
            chamber = item.get("chamber", item.get("house", "?"))
            state = item.get("state", "?")
            lines.append(f"- **{name}** ({party}, {chamber}, {state})")
        return "\n".join(lines)

    except Exception as e:
        return _handle_api_error(e)


@mcp.tool(
    name="uw_congress_unusual_trades",
    annotations={
        "title": "Unusual Whales: Unusual Congressional Trades",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def uw_congress_unusual_trades(params: UnusualCongressTradesInput) -> str:
    """
    Fetch flagged unusual congressional stock trades.

    Returns congressional disclosures that Unusual Whales has flagged
    as particularly notable based on timing, size, or other signals.

    Args:
        params (UnusualCongressTradesInput):
            - limit (int): Max results (1–100, default 25).
            - response_format: 'markdown' or 'json'.

    Returns:
        str: Unusual congressional trades.
    """
    try:
        data = await _api_get("/api/congress/unusual-trades", {"limit": params.limit})
        items = _extract_list(data, "data", "trades", "results")

        if not items:
            return "No unusual congressional trades found."

        if params.response_format == ResponseFormat.JSON:
            return _to_json({"count": len(items), "items": items})

        lines = [f"# Unusual Congressional Trades", f"*{len(items)} flagged trades*", ""]
        for item in items:
            lines.append(f"- {_fmt_congress(item)}")
        return "\n".join(lines)

    except Exception as e:
        return _handle_api_error(e)


@mcp.tool(
    name="uw_insider_transactions",
    annotations={
        "title": "Unusual Whales: Recent Insider Transactions",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def uw_insider_transactions(params: InsiderTransactionsInput) -> str:
    """
    Fetch recent SEC Form 4 insider transactions across all companies.

    Returns buy and sell filings from corporate officers, directors,
    and 10%+ shareholders as reported to the SEC.

    Args:
        params (InsiderTransactionsInput):
            - limit (int): Max results (1–100, default 25).
            - page (int): Pagination page (0-based, default 0).
            - response_format: 'markdown' or 'json'.

    Returns:
        str: Recent insider transaction filings.

    Examples:
        - "Who's been buying their own stock?" → default params
        - "Recent insider selling" → default params (filter by type in results)
    """
    try:
        data = await _api_get("/api/insider/transactions", {"limit": params.limit, "page": params.page})
        items = _extract_list(data, "data", "transactions", "results")

        if not items:
            return "No insider transactions found."

        if params.response_format == ResponseFormat.JSON:
            return _to_json({"count": len(items), "page": params.page, "items": items})

        lines = [f"# Recent Insider Transactions", f"*{len(items)} filings*", ""]
        for item in items:
            lines.append(f"- {_fmt_insider(item)}")
        return "\n".join(lines)

    except Exception as e:
        return _handle_api_error(e)


@mcp.tool(
    name="uw_insider_ticker",
    annotations={
        "title": "Unusual Whales: Insider Activity for Ticker",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def uw_insider_ticker(params: TickerPaginatedInput) -> str:
    """
    Fetch insider transaction filings for a specific stock.

    Returns SEC Form 4 filings for the given ticker, showing who inside
    the company is buying or selling their shares.

    Args:
        params (TickerPaginatedInput):
            - ticker (str): Stock ticker symbol (e.g. 'MSFT').
            - limit (int): Max results (1–100, default 25).
            - page (int): Pagination page (0-based, default 0).
            - response_format: 'markdown' or 'json'.

    Returns:
        str: Insider transactions for the ticker.

    Examples:
        - "Have TSLA insiders been selling?" → ticker='TSLA'
        - "Who is buying META stock inside the company?" → ticker='META'
    """
    try:
        data = await _api_get(
            f"/api/insider/{params.ticker}",
            {"limit": params.limit, "page": params.page},
        )
        items = _extract_list(data, "data", "insiders", "transactions", "results")

        if not items:
            return f"No insider transactions found for {params.ticker}."

        if params.response_format == ResponseFormat.JSON:
            return _to_json({"ticker": params.ticker, "count": len(items), "items": items})

        lines = [f"# Insider Activity: {params.ticker}", f"*{len(items)} filings*", ""]
        for item in items:
            lines.append(f"- {_fmt_insider(item)}")
        return "\n".join(lines)

    except Exception as e:
        return _handle_api_error(e)


# ---------------------------------------------------------------------------
# TOOLS — Market & Stock Data
# ---------------------------------------------------------------------------


@mcp.tool(
    name="uw_stock_info",
    annotations={
        "title": "Unusual Whales: Stock Information",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def uw_stock_info(params: TickerInput) -> str:
    """
    Get key information and metadata for a stock ticker.

    Returns price, market cap, sector, beta, and other snapshot data
    for the given symbol.

    Args:
        params (TickerInput):
            - ticker (str): Stock ticker symbol (e.g. 'GOOGL').
            - response_format: 'markdown' or 'json'.

    Returns:
        str: Stock information and metadata.

    Examples:
        - "Tell me about AAPL" → ticker='AAPL'
        - "What sector is NVDA in?" → ticker='NVDA'
    """
    try:
        data = await _api_get(f"/api/stock/{params.ticker}/info")

        if params.response_format == ResponseFormat.JSON:
            return _to_json(data)

        d = data.get("data", data) if isinstance(data, dict) else data
        if not isinstance(d, dict):
            return _to_json(data)

        lines = [f"# Stock Info: {params.ticker}", ""]
        for k, v in d.items():
            if v is not None:
                lines.append(f"- **{k}**: {v}")
        return "\n".join(lines)

    except Exception as e:
        return _handle_api_error(e)


@mcp.tool(
    name="uw_stock_ohlc",
    annotations={
        "title": "Unusual Whales: OHLC Price Candles",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def uw_stock_ohlc(params: OhlcInput) -> str:
    """
    Get OHLC (Open/High/Low/Close) price candle data for a stock.

    Returns historical price data at the specified candle granularity.
    Useful for charting, trend analysis, or technical setups.

    Args:
        params (OhlcInput):
            - ticker (str): Stock ticker symbol.
            - candle_size (CandleSize): '1', '5', '15', '30', '60', '240', 'D', or 'W'.
            - response_format: 'markdown' or 'json'.

    Returns:
        str: OHLC candle data.

    Examples:
        - "AAPL daily price chart data" → ticker='AAPL', candle_size='D'
        - "SPY 5-minute candles" → ticker='SPY', candle_size='5'
    """
    try:
        data = await _api_get(f"/api/stock/{params.ticker}/ohlc/{params.candle_size.value}")
        items = _extract_list(data, "data", "candles", "ohlc", "results")

        if not items:
            return f"No OHLC data found for {params.ticker} at {params.candle_size.value} candles."

        if params.response_format == ResponseFormat.JSON:
            return _to_json({"ticker": params.ticker, "candle_size": params.candle_size, "count": len(items), "items": items})

        lines = [f"# OHLC Candles: {params.ticker} ({params.candle_size.value})", f"*{len(items)} candles*", ""]
        # Show last 20 candles max in markdown
        for item in items[-20:]:
            t = item.get("timestamp", item.get("date", item.get("time", "?")))
            o = item.get("open", "?")
            h = item.get("high", "?")
            lo = item.get("low", "?")
            c = item.get("close", "?")
            v = item.get("volume", "")
            vol_str = f" | Vol: {v}" if v else ""
            lines.append(f"- `{t}` O:{o} H:{h} L:{lo} C:{c}{vol_str}")
        if len(items) > 20:
            lines.append(f"\n*(showing last 20 of {len(items)} candles — use json format for full data)*")
        return "\n".join(lines)

    except Exception as e:
        return _handle_api_error(e)


@mcp.tool(
    name="uw_stock_state",
    annotations={
        "title": "Unusual Whales: Current Stock State / Quote",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def uw_stock_state(params: TickerInput) -> str:
    """
    Get the current real-time stock state (quote) for a ticker.

    Returns the latest price, bid/ask, volume, and other live
    market data for the specified symbol.

    Args:
        params (TickerInput):
            - ticker (str): Stock ticker symbol (e.g. 'SPY').
            - response_format: 'markdown' or 'json'.

    Returns:
        str: Current stock state / quote.

    Examples:
        - "What is TSLA trading at?" → ticker='TSLA'
        - "Current price of SPY" → ticker='SPY'
    """
    try:
        data = await _api_get(f"/api/stock/{params.ticker}/stock-state")

        if params.response_format == ResponseFormat.JSON:
            return _to_json(data)

        d = data.get("data", data) if isinstance(data, dict) else data
        if not isinstance(d, dict):
            return _to_json(data)

        lines = [f"# Stock State: {params.ticker}", ""]
        priority = ["price", "last", "bid", "ask", "volume", "change", "change_percent", "market_cap"]
        shown = set()
        for k in priority:
            if k in d and d[k] is not None:
                lines.append(f"- **{k}**: {d[k]}")
                shown.add(k)
        for k, v in d.items():
            if k not in shown and v is not None:
                lines.append(f"- **{k}**: {v}")
        return "\n".join(lines)

    except Exception as e:
        return _handle_api_error(e)


@mcp.tool(
    name="uw_market_movers",
    annotations={
        "title": "Unusual Whales: Market Top Movers",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def uw_market_movers(params: MarketMoversInput) -> str:
    """
    Get today's top market movers by price change percentage.

    Returns the biggest gainers and losers in the market, helping
    identify momentum stocks and sector rotation.

    Args:
        params (MarketMoversInput):
            - response_format: 'markdown' or 'json'.

    Returns:
        str: Top market movers for the day.

    Examples:
        - "What stocks are moving today?" → default
        - "Biggest gainers right now" → default
    """
    try:
        data = await _api_get("/api/market/movers")

        if params.response_format == ResponseFormat.JSON:
            return _to_json(data)

        gainers = _extract_list(data.get("gainers", data.get("data", {}).get("gainers", [])))
        losers = _extract_list(data.get("losers", data.get("data", {}).get("losers", [])))

        lines = [f"# Top Market Movers", ""]
        if gainers:
            lines.append("## 📈 Top Gainers")
            for item in gainers[:10]:
                ticker = item.get("ticker", item.get("symbol", "?"))
                chg = item.get("change_percent", item.get("change", "?"))
                price = item.get("price", item.get("close", "?"))
                lines.append(f"- **{ticker}**: {chg}% | ${price}")
        if losers:
            lines.append("\n## 📉 Top Losers")
            for item in losers[:10]:
                ticker = item.get("ticker", item.get("symbol", "?"))
                chg = item.get("change_percent", item.get("change", "?"))
                price = item.get("price", item.get("close", "?"))
                lines.append(f"- **{ticker}**: {chg}% | ${price}")

        if not gainers and not losers:
            all_items = _extract_list(data, "data", "movers", "results")
            if all_items:
                lines = [f"# Top Market Movers", f"*{len(all_items)} movers*", ""]
                for item in all_items[:20]:
                    ticker = item.get("ticker", item.get("symbol", "?"))
                    chg = item.get("change_percent", item.get("change", "?"))
                    lines.append(f"- **{ticker}**: {chg}%")
            else:
                return "No market mover data available right now."

        return "\n".join(lines)

    except Exception as e:
        return _handle_api_error(e)


@mcp.tool(
    name="uw_market_tide",
    annotations={
        "title": "Unusual Whales: Market Tide (Net Options Flow)",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def uw_market_tide(params: MarketMoversInput) -> str:
    """
    Get the Unusual Whales Market Tide — net options premium flow.

    Market Tide shows the aggregate net bullish vs. bearish options
    premium across the market over time. A rising tide = bullish flow,
    falling = bearish. One of Unusual Whales' signature indicators.

    Args:
        params (MarketMoversInput):
            - response_format: 'markdown' or 'json'.

    Returns:
        str: Market tide data points.

    Examples:
        - "What does the market tide look like?" → default
        - "Is options flow bullish or bearish today?" → default
    """
    try:
        data = await _api_get("/api/market/market-tide")

        if params.response_format == ResponseFormat.JSON:
            return _to_json(data)

        items = _extract_list(data, "data", "tide", "results")
        if not items:
            d = data.get("data", data)
            return f"# Market Tide\n\n{_to_json(d)}"

        lines = [f"# Market Tide (Net Options Premium Flow)", f"*{len(items)} data points*", ""]
        for item in items[-20:]:
            t = item.get("timestamp", item.get("time", item.get("date", "?")))
            net = item.get("net_premium", item.get("net", item.get("value", "?")))
            lines.append(f"- `{t}`: Net ${net}")
        return "\n".join(lines)

    except Exception as e:
        return _handle_api_error(e)


@mcp.tool(
    name="uw_options_volume",
    annotations={
        "title": "Unusual Whales: Options Volume for Ticker",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def uw_options_volume(params: TickerInput) -> str:
    """
    Get total options volume data for a specific ticker.

    Returns call/put volume, ratios, and total options volume for
    the given stock symbol. Useful for gauging sentiment.

    Args:
        params (TickerInput):
            - ticker (str): Stock ticker symbol.
            - response_format: 'markdown' or 'json'.

    Returns:
        str: Options volume summary for the ticker.

    Examples:
        - "How much options volume does QQQ have?" → ticker='QQQ'
        - "AAPL call/put volume ratio" → ticker='AAPL'
    """
    try:
        data = await _api_get(f"/api/stock/{params.ticker}/options-volume")

        if params.response_format == ResponseFormat.JSON:
            return _to_json(data)

        d = data.get("data", data) if isinstance(data, dict) else data
        if isinstance(d, list) and d:
            d = d[0]
        if not isinstance(d, dict):
            return _to_json(data)

        lines = [f"# Options Volume: {params.ticker}", ""]
        for k, v in d.items():
            if v is not None:
                lines.append(f"- **{k}**: {v}")
        return "\n".join(lines)

    except Exception as e:
        return _handle_api_error(e)


@mcp.tool(
    name="uw_stock_screener",
    annotations={
        "title": "Unusual Whales: Stock Screener",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def uw_stock_screener(params: ScreenerInput) -> str:
    """
    Run the Unusual Whales stock screener for notable stocks.

    Returns stocks that meet Unusual Whales' screening criteria for
    unusual options or flow activity.

    Args:
        params (ScreenerInput):
            - limit (int): Max results (1–100, default 25).
            - response_format: 'markdown' or 'json'.

    Returns:
        str: Screener results — stocks with notable activity.

    Examples:
        - "Screen for stocks with unusual activity" → default
        - "Top 50 stocks to watch" → limit=50
    """
    try:
        data = await _api_get("/api/screener/stocks", {"limit": params.limit})
        items = _extract_list(data, "data", "stocks", "results")

        if not items:
            return "No screener results found."

        if params.response_format == ResponseFormat.JSON:
            return _to_json({"count": len(items), "items": items})

        lines = [f"# Stock Screener Results", f"*{len(items)} stocks*", ""]
        for item in items:
            ticker = item.get("ticker", item.get("symbol", "?"))
            price = item.get("price", item.get("close", "?"))
            vol = item.get("volume", "?")
            chg = item.get("change_percent", item.get("change", ""))
            chg_str = f" | {chg}%" if chg else ""
            lines.append(f"- **{ticker}**: ${price}{chg_str} | Vol: {vol}")
        return "\n".join(lines)

    except Exception as e:
        return _handle_api_error(e)


@mcp.tool(
    name="uw_news_headlines",
    annotations={
        "title": "Unusual Whales: Market News Headlines",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def uw_news_headlines(params: NewsInput) -> str:
    """
    Fetch the latest market news headlines from Unusual Whales.

    Returns recent financial news articles relevant to markets and
    individual stocks.

    Args:
        params (NewsInput):
            - limit (int): Max results (1–100, default 25).
            - response_format: 'markdown' or 'json'.

    Returns:
        str: Latest market news headlines.

    Examples:
        - "What's in the news today?" → default
        - "Latest market headlines" → default
    """
    try:
        data = await _api_get("/api/news/headlines", {"limit": params.limit})
        items = _extract_list(data, "data", "headlines", "news", "results")

        if not items:
            return "No news headlines found."

        if params.response_format == ResponseFormat.JSON:
            return _to_json({"count": len(items), "items": items})

        lines = [f"# Market News Headlines", f"*{len(items)} articles*", ""]
        for item in items:
            title = item.get("title", item.get("headline", "?"))
            source = item.get("source", item.get("publisher", ""))
            ts = item.get("published_at", item.get("timestamp", item.get("date", "")))
            tickers = item.get("tickers", item.get("symbols", []))
            ticker_str = f" [{', '.join(tickers[:3])}]" if tickers else ""
            src_str = f" — *{source}*" if source else ""
            ts_str = f" `{ts}`" if ts else ""
            lines.append(f"- **{title}**{ticker_str}{src_str}{ts_str}")
        return "\n".join(lines)

    except Exception as e:
        return _handle_api_error(e)


@mcp.tool(
    name="uw_company_profile",
    annotations={
        "title": "Unusual Whales: Company Profile",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def uw_company_profile(params: TickerInput) -> str:
    """
    Get a detailed company profile for a stock ticker.

    Returns company description, sector, industry, employee count,
    website, and fundamental metadata.

    Args:
        params (TickerInput):
            - ticker (str): Stock ticker symbol.
            - response_format: 'markdown' or 'json'.

    Returns:
        str: Company profile information.

    Examples:
        - "What does NVDA do?" → ticker='NVDA'
        - "Company info for AMZN" → ticker='AMZN'
    """
    try:
        data = await _api_get(f"/api/companies/{params.ticker}/profile")

        if params.response_format == ResponseFormat.JSON:
            return _to_json(data)

        d = data.get("data", data) if isinstance(data, dict) else data
        if not isinstance(d, dict):
            return _to_json(data)

        lines = [f"# Company Profile: {params.ticker}", ""]
        priority = ["name", "description", "sector", "industry", "employees", "website", "exchange", "market_cap", "ipo_date"]
        shown = set()
        for k in priority:
            if k in d and d[k]:
                lines.append(f"- **{k}**: {d[k]}")
                shown.add(k)
        for k, v in d.items():
            if k not in shown and v:
                lines.append(f"- **{k}**: {v}")
        return "\n".join(lines)

    except Exception as e:
        return _handle_api_error(e)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    api_key = os.environ.get("UNUSUAL_WHALES_API_KEY", "")
    if not api_key:
        print(
            "WARNING: UNUSUAL_WHALES_API_KEY is not set.\n"
            "Set it before running: export UNUSUAL_WHALES_API_KEY=your_key",
            file=sys.stderr,
        )
    mcp.run()
