# Tool reference

All tools accept six-digit A-share tickers, with optional `SH`, `SZ`, or `BJ` prefixes. Results are envelopes containing the normalized ticker, retrieval time, pinned provider repository and commit, raw provider output, and warnings.

## Tools

- `get_stock_prices(ticker, start_date, end_date)` — OHLCV history for an inclusive ISO date range.
- `get_company_fundamentals(ticker, as_of_date)` — name, current quote, valuation, market capitalization, quarterly snapshot, industry metadata, and consensus estimates when available.
- `get_financial_statement(ticker, statement, frequency, as_of_date)` — `income`, `balance`, or `cashflow`; frequency is `quarterly` or `annual`.
- `get_company_news(ticker, start_date, end_date)` — company news with source links when provided upstream.
- `get_shareholder_activity(ticker)` — F10 shareholder research and ownership changes.
- `get_sector_context(ticker, as_of_date)` — concept/sector membership plus current industry comparison.
- `get_market_signals(ticker, as_of_date, look_back_days, forward_days)` — analyst consensus, fund flow, Dragon-Tiger Board history, and upcoming lockups.

## Coverage limits

The initial release covers mainland A shares only. Upstream public endpoints can be unavailable, rate-limited, delayed, or changed without notice. The bridge preserves upstream output rather than silently inventing missing values.
