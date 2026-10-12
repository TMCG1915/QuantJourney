"""Tests for the data helpers. yfinance is faked, so these never touch the internet."""

import sys
import types

import numpy as np
import pandas as pd

from bs_pricer.smile import smile_from_chain
from common import data


def fake_yfinance(monkeypatch, download):
    monkeypatch.setitem(sys.modules, "yfinance", types.SimpleNamespace(download=download))


def test_download_prices_parses_yfinance_columns(monkeypatch):
    index = pd.bdate_range("2024-01-01", periods=5)
    columns = pd.MultiIndex.from_product([["Close", "Open"], ["AAA", "BBB"]])
    table = pd.DataFrame(np.arange(20.0).reshape(5, 4), index=index, columns=columns)
    fake_yfinance(monkeypatch, lambda *args, **kwargs: table)

    prices = data.download_prices(["BBB", "AAA"])
    assert list(prices.columns) == ["BBB", "AAA"]  # requested order is kept
    assert prices.shape == (5, 2)


def test_download_prices_returns_none_on_failure(monkeypatch):
    def broken(*args, **kwargs):
        raise RuntimeError("Too Many Requests")

    fake_yfinance(monkeypatch, broken)
    assert data.download_prices(["AAA"]) is None


def test_load_prices_falls_back_to_simulation(monkeypatch):
    monkeypatch.setattr(data, "download_prices", lambda *args, **kwargs: None)
    prices, is_real = data.load_prices(["AAA", "BBB", "CCC"])
    assert is_real is False
    assert list(prices.columns) == ["AAA", "BBB", "CCC"]
    assert (prices > 0).all().all()


def test_simulated_prices_are_reproducible():
    first = data.simulate_prices(["A", "B"], n_days=100, seed=3)
    second = data.simulate_prices(["A", "B"], n_days=100, seed=3)
    assert first.equals(second)


def test_option_chain_failure_returns_none(monkeypatch):
    class BrokenTicker:
        def __init__(self, symbol):
            raise RuntimeError("no internet")

    monkeypatch.setitem(sys.modules, "yfinance", types.SimpleNamespace(Ticker=BrokenTicker))
    assert smile_from_chain("SPY") is None
