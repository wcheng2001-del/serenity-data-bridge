# CLI fallback

From the repository root, create the isolated environments and run a command:

```powershell
python scripts/setup.py
serenity-data fundamentals 600519 --as-of 2026-09-25
serenity-data prices 600519 --start 2026-08-01 --end 2026-09-25
serenity-data news 600519 --start 2026-09-01 --end 2026-09-25
```

The CLI prints the same JSON envelope returned by MCP. Run `serenity-data --help` for all commands.
