"""Local stdio MCP server for Serenity Data Bridge."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from .bridge import DataBridge


mcp = FastMCP(
    "serenity-data-bridge",
    instructions=(
        "Read-only A-share research data. Preserve provider dates and warnings. "
        "Verify material investment claims against official filings. Never place trades."
    ),
)
bridge = DataBridge()


@mcp.tool()
def get_stock_prices(ticker: str, start_date: str, end_date: str) -> dict:
    """Get read-only OHLCV history for an A-share over an inclusive ISO date range."""
    return bridge.stock_prices(ticker, start_date, end_date)


@mcp.tool()
def get_company_fundamentals(ticker: str, as_of_date: str | None = None) -> dict:
    """Get current valuation and available fundamental data for an A-share."""
    return bridge.fundamentals(ticker, as_of_date)


@mcp.tool()
def get_financial_statement(
    ticker: str,
    statement: str,
    frequency: str = "quarterly",
    as_of_date: str | None = None,
) -> dict:
    """Get an income, balance, or cash-flow statement for an A-share."""
    return bridge.financial_statement(ticker, statement, frequency, as_of_date)


@mcp.tool()
def get_company_news(ticker: str, start_date: str, end_date: str) -> dict:
    """Get recent company news for an A-share, including upstream links when available."""
    return bridge.company_news(ticker, start_date, end_date)


@mcp.tool()
def get_shareholder_activity(ticker: str) -> dict:
    """Get A-share shareholder research and ownership-change information."""
    return bridge.shareholder_activity(ticker)


@mcp.tool()
def get_sector_context(ticker: str, as_of_date: str | None = None) -> dict:
    """Get concept membership and industry comparison for an A-share."""
    return bridge.sector_context(ticker, as_of_date)


@mcp.tool()
def get_market_signals(
    ticker: str,
    as_of_date: str | None = None,
    look_back_days: int = 30,
    forward_days: int = 90,
) -> dict:
    """Get analyst consensus, fund flow, Dragon-Tiger Board, and lockup signals."""
    return bridge.market_signals(ticker, as_of_date, look_back_days, forward_days)


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
