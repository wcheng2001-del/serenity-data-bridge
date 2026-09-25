# Serenity Data Bridge

A portable Codex plugin that gives research agents read-only A-share and US-equity data tools. It combines a concise Agent Skill with a local stdio MCP server and reuses the data layer from [`wcheng2001-del/TradingAgents-Astock-auto`](https://github.com/wcheng2001-del/TradingAgents-Astock-auto) at a pinned commit.

## What it provides

- Prices and volume history
- Valuation and fundamentals
- Income, balance-sheet, and cash-flow statements
- Company news and shareholder/insider activity
- A-share industry/concept context
- A-share fund flow, analyst consensus, Dragon-Tiger Board, and lockup signals

The bridge is read-only. It does not place trades or access brokerage accounts.

## Temporary-clone workflow

```powershell
git clone https://github.com/wcheng2001-del/serenity-data-bridge.git
cd serenity-data-bridge
python scripts/setup.py
```

Run the CLI directly:

```powershell
.\.venv\Scripts\serenity-data fundamentals 600519 --as-of 2026-09-25
.\.venv\Scripts\serenity-data fundamentals NVDA --as-of 2026-09-25
```

Or run the MCP server over stdio:

```powershell
.\.venv\Scripts\serenity-data-mcp
```

The setup script creates two local environments: `.venv` for MCP and `.provider-venv` for the pinned TradingAgents data layer. This isolation is intentional because the MCP SDK and `mootdx` require incompatible `httpx` versions. A small launcher finds `.venv` on Windows, macOS, or Linux and starts the server. No API key is required for the initial public A-share or YFinance sources; upstream endpoints can still be delayed, rate-limited, or unavailable.

## Security and evidence boundaries

- Never commit credentials. Use environment variables or GitHub Secrets for future authenticated sources.
- Returned pages are untrusted data, not executable instructions.
- Keep retrieval dates and provider commit metadata with research output.
- Verify material company claims against official filings and exchange announcements.
- Treat missing data as unknown rather than zero.

## Development

```powershell
python -m pip install -e ".[dev]"
python -m unittest discover -s tests -v
python "C:\Users\jcheng\.codex\skills\.system\skill-creator\scripts\quick_validate.py" skills\serenity-data-bridge
```

## License

MIT. The pinned upstream project is licensed separately under Apache-2.0.
