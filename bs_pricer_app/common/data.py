"""Load market data, with a simulated fallback so every demo runs offline."""

import numpy as np
import pandas as pd


def download_prices(tickers, start="2010-01-01", end=None):
    """Download adjusted close prices from Yahoo Finance.

    Returns a DataFrame (one column per ticker), or None if the download fails.
    """
    try:
        import yfinance as yf

        data = yf.download(list(tickers), start=start, end=end, auto_adjust=True, progress=False)[
            "Close"
        ]
    except Exception as error:  # no internet, bad ticker, yfinance missing, ...
        print(f"Download failed: {error}")
        return None

    data = data.dropna()
    if data.empty:
        return None
    return data[list(tickers)]


def simulate_prices(tickers, n_days=2500, seed=0, start="2010-01-01"):
    """Simulate correlated GBM prices (one common 'market' factor plus noise)."""
    rng = np.random.default_rng(seed)
    n_assets = len(tickers)
    dt = 1 / 252

    mu = rng.uniform(0.03, 0.10, n_assets)  # annual drift
    vol = rng.uniform(0.08, 0.25, n_assets)  # annual volatility
    rho = 0.4  # correlation between any two assets

    market = rng.standard_normal((n_days, 1))
    noise = rng.standard_normal((n_days, n_assets))
    z = np.sqrt(rho) * market + np.sqrt(1 - rho) * noise

    log_returns = (mu - 0.5 * vol**2) * dt + vol * np.sqrt(dt) * z
    prices = 100 * np.exp(np.cumsum(log_returns, axis=0))
    index = pd.bdate_range(start, periods=n_days)
    return pd.DataFrame(prices, index=index, columns=list(tickers))


def load_prices(tickers, start="2010-01-01", end=None):
    """Try Yahoo Finance first; fall back to simulated prices.

    Returns (prices, is_real) so callers can label their output honestly.
    """
    prices = download_prices(tickers, start, end)
    if prices is not None:
        return prices, True

    print("WARNING: could not download data - using SIMULATED prices instead.")
    return simulate_prices(tickers, start=start), False
