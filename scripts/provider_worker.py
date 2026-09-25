"""JSON stdin/stdout worker running inside the isolated provider environment."""

from __future__ import annotations

import contextlib
import json
import sys
from importlib import import_module


ALLOWED_FUNCTIONS = {
    "get_stock_data",
    "get_fundamentals",
    "get_balance_sheet",
    "get_cashflow",
    "get_income_statement",
    "get_news",
    "get_insider_transactions",
    "get_profit_forecast",
    "get_concept_blocks",
    "get_fund_flow",
    "get_dragon_tiger_board",
    "get_lockup_expiry",
    "get_industry_comparison",
}


def main() -> None:
    try:
        request = json.load(sys.stdin)
        name = request.get("function")
        if name not in ALLOWED_FUNCTIONS:
            raise ValueError(f"provider function is not allowed: {name}")
        with contextlib.redirect_stdout(sys.stderr):
            module = import_module("tradingagents.dataflows.a_stock")
            function = getattr(module, name)
            result = function(*request.get("args", []), **request.get("kwargs", {}))
        json.dump({"ok": True, "result": result}, sys.stdout, ensure_ascii=False)
    except Exception as exc:
        json.dump({"ok": False, "error": f"{type(exc).__name__}: {exc}"}, sys.stdout)


if __name__ == "__main__":
    main()
