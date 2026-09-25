"""JSON CLI fallback for environments without MCP support."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from .bridge import DataBridge


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="serenity-data", description="Read-only A-share and US-equity data bridge"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    prices = sub.add_parser("prices")
    prices.add_argument("ticker")
    prices.add_argument("--start", required=True)
    prices.add_argument("--end", required=True)

    fundamentals = sub.add_parser("fundamentals")
    fundamentals.add_argument("ticker")
    fundamentals.add_argument("--as-of")

    statement = sub.add_parser("statement")
    statement.add_argument("ticker")
    statement.add_argument("statement", choices=["income", "balance", "cashflow"])
    statement.add_argument("--frequency", choices=["quarterly", "annual"], default="quarterly")
    statement.add_argument("--as-of")

    news = sub.add_parser("news")
    news.add_argument("ticker")
    news.add_argument("--start", required=True)
    news.add_argument("--end", required=True)

    owners = sub.add_parser("shareholders")
    owners.add_argument("ticker")

    sector = sub.add_parser("sector")
    sector.add_argument("ticker")
    sector.add_argument("--as-of")

    signals = sub.add_parser("signals")
    signals.add_argument("ticker")
    signals.add_argument("--as-of")
    signals.add_argument("--look-back-days", type=int, default=30)
    signals.add_argument("--forward-days", type=int, default=90)
    return parser


def _dispatch(args: argparse.Namespace, bridge: DataBridge) -> dict[str, Any]:
    if args.command == "prices":
        return bridge.stock_prices(args.ticker, args.start, args.end)
    if args.command == "fundamentals":
        return bridge.fundamentals(args.ticker, args.as_of)
    if args.command == "statement":
        return bridge.financial_statement(args.ticker, args.statement, args.frequency, args.as_of)
    if args.command == "news":
        return bridge.company_news(args.ticker, args.start, args.end)
    if args.command == "shareholders":
        return bridge.shareholder_activity(args.ticker)
    if args.command == "sector":
        return bridge.sector_context(args.ticker, args.as_of)
    return bridge.market_signals(
        args.ticker, args.as_of, args.look_back_days, args.forward_days
    )


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    args = _parser().parse_args()
    print(json.dumps(_dispatch(args, DataBridge()), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
