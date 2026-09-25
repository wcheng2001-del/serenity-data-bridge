# Tool reference

Core tools accept six-digit A-share tickers (optional `SH`, `SZ`, or `BJ` prefixes) and US tickers such as `NVDA`. Results are envelopes containing the normalized ticker, market, retrieval time, pinned provider repository and commit, raw provider output, and warnings.

## Tools

- `get_stock_prices(ticker, start_date, end_date)` — OHLCV history for an inclusive ISO date range.
- `get_company_fundamentals(ticker, as_of_date)` — name, current quote, valuation, market capitalization, quarterly snapshot, industry metadata, and consensus estimates when available.
- `get_financial_statement(ticker, statement, frequency, as_of_date)` — `income`, `balance`, or `cashflow`; frequency is `quarterly` or `annual`.
- `get_company_news(ticker, start_date, end_date)` — company news with source links when provided upstream.
- `get_shareholder_activity(ticker)` — A-share F10 ownership research or US insider transactions.
- `get_sector_context(ticker, as_of_date)` — A-share-only concept/sector membership plus current industry comparison.
- `get_market_signals(ticker, as_of_date, look_back_days, forward_days)` — A-share-only analyst consensus, fund flow, Dragon-Tiger Board history, and upcoming lockups.

## Coverage limits

Release 0.2 covers mainland A shares and US-listed equities. A-share-only tools reject US tickers explicitly. YFinance fields are secondary-source data and must be checked against SEC filings or issuer disclosures for material conclusions. Upstream public endpoints can be unavailable, rate-limited, delayed, or changed without notice. The bridge preserves upstream output rather than silently inventing missing values.
