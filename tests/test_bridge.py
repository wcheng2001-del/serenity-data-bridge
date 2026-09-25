from __future__ import annotations

import unittest

from serenity_data_bridge.bridge import DataBridge


class FakeProvider:
    def __init__(self) -> None:
        self.calls: list[tuple[str, tuple, dict]] = []

    def call(self, function_name: str, *args, **kwargs) -> str:
        self.calls.append((function_name, args, kwargs))
        return f"source result for {function_name}"


class DataBridgeTests(unittest.TestCase):
    def test_prices_normalizes_prefixed_ticker(self) -> None:
        provider = FakeProvider()
        result = DataBridge(provider).stock_prices(
            "SH600519", "2026-09-01", "2026-09-25"
        )
        self.assertEqual(result["ticker"], "600519")
        self.assertEqual(result["market"], "a_share")
        self.assertEqual(provider.calls[0][0], "a_share.get_stock_data")
        self.assertEqual(
            provider.calls[0][1], ("600519", "2026-09-01", "2026-09-25")
        )

    def test_invalid_ticker_is_rejected_before_provider_call(self) -> None:
        provider = FakeProvider()
        with self.assertRaisesRegex(ValueError, "six-digit"):
            DataBridge(provider).fundamentals("../../secret")
        self.assertEqual(provider.calls, [])

    def test_reversed_date_range_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "start_date"):
            DataBridge(FakeProvider()).company_news(
                "600519", "2026-09-25", "2026-09-01"
            )

    def test_statement_routes_to_selected_upstream_function(self) -> None:
        provider = FakeProvider()
        DataBridge(provider).financial_statement(
            "000001", "cashflow", "annual", "2026-09-25"
        )
        self.assertEqual(provider.calls[0][0], "a_share.get_cashflow")
        self.assertEqual(provider.calls[0][1], ("000001", "annual", "2026-09-25"))

    def test_us_ticker_routes_to_yfinance_provider(self) -> None:
        provider = FakeProvider()
        result = DataBridge(provider).fundamentals("nvda", "2026-09-25")
        self.assertEqual(result["ticker"], "NVDA")
        self.assertEqual(result["market"], "us")
        self.assertEqual(provider.calls[0][0], "us.get_fundamentals")
        self.assertEqual(provider.calls[0][1], ("NVDA", "2026-09-25"))

    def test_a_share_only_tools_reject_us_tickers(self) -> None:
        provider = FakeProvider()
        with self.assertRaisesRegex(ValueError, "A shares only"):
            DataBridge(provider).sector_context("NVDA", "2026-09-25")
        self.assertEqual(provider.calls, [])

    def test_market_signal_bounds_are_enforced(self) -> None:
        with self.assertRaisesRegex(ValueError, "look_back_days"):
            DataBridge(FakeProvider()).market_signals(
                "600519", "2026-09-25", 0, 90
            )


if __name__ == "__main__":
    unittest.main()
