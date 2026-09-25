"""JSON stdin/stdout worker running inside the isolated provider environment."""

from __future__ import annotations

import contextlib
import json
import sys
from importlib import import_module

ALLOWED_FUNCTIONS = {
    "a_share.get_stock_data": ("tradingagents.dataflows.a_stock", "get_stock_data"),
    "a_share.get_fundamentals": ("tradingagents.dataflows.a_stock", "get_fundamentals"),
    "a_share.get_balance_sheet": ("tradingagents.dataflows.a_stock", "get_balance_sheet"),
    "a_share.get_cashflow": ("tradingagents.dataflows.a_stock", "get_cashflow"),
    "a_share.get_income_statement": ("tradingagents.dataflows.a_stock", "get_income_statement"),
    "a_share.get_news": ("tradingagents.dataflows.a_stock", "get_news"),
    "a_share.get_insider_transactions": (
        "tradingagents.dataflows.a_stock",
        "get_insider_transactions",
    ),
    "a_share.get_profit_forecast": ("tradingagents.dataflows.a_stock", "get_profit_forecast"),
    "a_share.get_concept_blocks": ("tradingagents.dataflows.a_stock", "get_concept_blocks"),
    "a_share.get_fund_flow": ("tradingagents.dataflows.a_stock", "get_fund_flow"),
    "a_share.get_dragon_tiger_board": (
        "tradingagents.dataflows.a_stock",
        "get_dragon_tiger_board",
    ),
    "a_share.get_lockup_expiry": ("tradingagents.dataflows.a_stock", "get_lockup_expiry"),
    "a_share.get_industry_comparison": (
        "tradingagents.dataflows.a_stock",
        "get_industry_comparison",
    ),
    "us.get_stock_data": ("tradingagents.dataflows.y_finance", "get_YFin_data_online"),
    "us.get_fundamentals": ("tradingagents.dataflows.y_finance", "get_fundamentals"),
    "us.get_balance_sheet": ("tradingagents.dataflows.y_finance", "get_balance_sheet"),
    "us.get_cashflow": ("tradingagents.dataflows.y_finance", "get_cashflow"),
    "us.get_income_statement": (
        "tradingagents.dataflows.y_finance",
        "get_income_statement",
    ),
    "us.get_news": ("tradingagents.dataflows.yfinance_news", "get_news_yfinance"),
    "us.get_insider_transactions": (
        "tradingagents.dataflows.y_finance",
        "get_insider_transactions",
    ),
}


def main() -> None:
    try:
        request = json.load(sys.stdin)
        name = request.get("function")
        if name not in ALLOWED_FUNCTIONS:
            raise ValueError(f"provider function is not allowed: {name}")
        module_name, function_name = ALLOWED_FUNCTIONS[name]
        with contextlib.redirect_stdout(sys.stderr):
            module = import_module(module_name)
            function = getattr(module, function_name)
            result = function(*request.get("args", []), **request.get("kwargs", {}))
        json.dump({"ok": True, "result": result}, sys.stdout, ensure_ascii=False)
    except Exception as exc:  # noqa: BLE001 - worker must serialize provider failures
        json.dump({"ok": False, "error": f"{type(exc).__name__}: {exc}"}, sys.stdout)


if __name__ == "__main__":
    main()
