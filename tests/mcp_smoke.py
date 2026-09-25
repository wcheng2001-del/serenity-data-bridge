"""Start the stdio MCP server and verify its advertised read-only tools."""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


EXPECTED = {
    "get_stock_prices",
    "get_company_fundamentals",
    "get_financial_statement",
    "get_company_news",
    "get_shareholder_activity",
    "get_sector_context",
    "get_market_signals",
}


async def verify() -> None:
    root = Path(__file__).resolve().parents[1]
    parameters = StdioServerParameters(
        command=sys.executable,
        args=[str(root / "scripts" / "run_mcp.py")],
        cwd=str(root),
    )
    async with stdio_client(parameters) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            names = {tool.name for tool in tools.tools}
            missing = EXPECTED - names
            if missing:
                raise RuntimeError(f"missing MCP tools: {sorted(missing)}")
            print(f"MCP smoke test passed with {len(names)} tools")


if __name__ == "__main__":
    asyncio.run(verify())
