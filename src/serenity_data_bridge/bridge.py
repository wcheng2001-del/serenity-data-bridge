"""Validated, structured read-only operations exposed by CLI and MCP."""

from __future__ import annotations

import re
from datetime import date, datetime, timezone
from typing import Any, Protocol

from .provider import SOURCE_COMMIT, SOURCE_REPOSITORY, TradingAgentsProvider


class Provider(Protocol):
    def call(self, function_name: str, *args: Any, **kwargs: Any) -> str: ...


_TICKER_PATTERN = re.compile(r"^(?:(?:SH|SZ|BJ)[.-]?)?(\d{6})$", re.IGNORECASE)
_STATEMENTS = {
    "income": "get_income_statement",
    "balance": "get_balance_sheet",
    "cashflow": "get_cashflow",
}


def _ticker(value: str) -> str:
    match = _TICKER_PATTERN.fullmatch(value.strip())
    if not match:
        raise ValueError("ticker must be a six-digit A-share code, optionally prefixed SH/SZ/BJ")
    return match.group(1)


def _iso_date(value: str | None, field: str) -> str:
    if value is None:
        return date.today().isoformat()
    try:
        return date.fromisoformat(value).isoformat()
    except ValueError as exc:
        raise ValueError(f"{field} must use YYYY-MM-DD") from exc


class DataBridge:
    def __init__(self, provider: Provider | None = None) -> None:
        self.provider = provider or TradingAgentsProvider()

    def _result(self, tool: str, ticker: str, payload: Any) -> dict[str, Any]:
        text = payload if isinstance(payload, str) else str(payload)
        warning = None
        lowered = text.lower()
        if (
            lowered.startswith("error")
            or lowered.startswith("no ")
            or "no data" in lowered
            or "获取失败" in text
        ):
            warning = "The upstream provider reported missing or failed data; do not treat it as zero."
        return {
            "tool": tool,
            "ticker": ticker,
            "retrieved_at": datetime.now(timezone.utc).isoformat(),
            "provider": {
                "repository": SOURCE_REPOSITORY,
                "commit": SOURCE_COMMIT,
            },
            "data": payload,
            "warnings": [warning] if warning else [],
        }

    def stock_prices(self, ticker: str, start_date: str, end_date: str) -> dict[str, Any]:
        code = _ticker(ticker)
        start = _iso_date(start_date, "start_date")
        end = _iso_date(end_date, "end_date")
        if start > end:
            raise ValueError("start_date must not be after end_date")
        data = self.provider.call("get_stock_data", code, start, end)
        return self._result("get_stock_prices", code, data)

    def fundamentals(self, ticker: str, as_of_date: str | None = None) -> dict[str, Any]:
        code = _ticker(ticker)
        as_of = _iso_date(as_of_date, "as_of_date")
        data = self.provider.call("get_fundamentals", code, as_of)
        return self._result("get_company_fundamentals", code, data)

    def financial_statement(
        self,
        ticker: str,
        statement: str,
        frequency: str = "quarterly",
        as_of_date: str | None = None,
    ) -> dict[str, Any]:
        code = _ticker(ticker)
        statement_key = statement.strip().lower()
        if statement_key not in _STATEMENTS:
            raise ValueError("statement must be income, balance, or cashflow")
        frequency_key = frequency.strip().lower()
        if frequency_key not in {"quarterly", "annual"}:
            raise ValueError("frequency must be quarterly or annual")
        as_of = _iso_date(as_of_date, "as_of_date")
        data = self.provider.call(_STATEMENTS[statement_key], code, frequency_key, as_of)
        return self._result("get_financial_statement", code, data)

    def company_news(self, ticker: str, start_date: str, end_date: str) -> dict[str, Any]:
        code = _ticker(ticker)
        start = _iso_date(start_date, "start_date")
        end = _iso_date(end_date, "end_date")
        if start > end:
            raise ValueError("start_date must not be after end_date")
        data = self.provider.call("get_news", code, start, end)
        return self._result("get_company_news", code, data)

    def shareholder_activity(self, ticker: str) -> dict[str, Any]:
        code = _ticker(ticker)
        data = self.provider.call("get_insider_transactions", code)
        return self._result("get_shareholder_activity", code, data)

    def sector_context(self, ticker: str, as_of_date: str | None = None) -> dict[str, Any]:
        code = _ticker(ticker)
        as_of = _iso_date(as_of_date, "as_of_date")
        concepts = self.provider.call("get_concept_blocks", code)
        industries = self.provider.call("get_industry_comparison", code, as_of, 15)
        return self._result(
            "get_sector_context",
            code,
            {"concepts": concepts, "industry_comparison": industries},
        )

    def market_signals(
        self,
        ticker: str,
        as_of_date: str | None = None,
        look_back_days: int = 30,
        forward_days: int = 90,
    ) -> dict[str, Any]:
        code = _ticker(ticker)
        as_of = _iso_date(as_of_date, "as_of_date")
        if not 1 <= look_back_days <= 365:
            raise ValueError("look_back_days must be between 1 and 365")
        if not 1 <= forward_days <= 365:
            raise ValueError("forward_days must be between 1 and 365")
        payload = {
            "profit_forecast": self.provider.call("get_profit_forecast", code, as_of),
            "fund_flow": self.provider.call("get_fund_flow", code, as_of, True),
            "dragon_tiger_board": self.provider.call(
                "get_dragon_tiger_board", code, as_of, look_back_days
            ),
            "lockup_expiry": self.provider.call("get_lockup_expiry", code, as_of, forward_days),
        }
        return self._result("get_market_signals", code, payload)
