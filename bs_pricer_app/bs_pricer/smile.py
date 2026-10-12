"""Implied volatility smile from a live option chain (or a synthetic one)."""

import numpy as np
import pandas as pd

from bs_pricer.black_scholes import bs_price, implied_vol


def smile_from_chain(ticker="SPY", min_days=20, r=0.04):
    """Download an option chain from Yahoo Finance and compute implied vols.

    Uses the first expiry at least `min_days` away, and only out-of-the-money
    options (puts below spot, calls above), which is standard practice.
    Returns (DataFrame, spot, days_to_expiry), or None if the download fails.
    """
    try:
        import yfinance as yf

        stock = yf.Ticker(ticker)
        spot = float(stock.history(period="5d")["Close"].iloc[-1])
        today = pd.Timestamp.today().normalize()
        expiries = [e for e in stock.options if (pd.Timestamp(e) - today).days >= min_days]
        expiry = expiries[0]
        days = (pd.Timestamp(expiry) - today).days
        chain = stock.option_chain(expiry)
    except Exception as error:  # no internet, no options listed, ...
        print(f"Option chain download failed: {error}")
        return None

    rows = []
    for option_type, table in [("call", chain.calls), ("put", chain.puts)]:
        for _, row in table.iterrows():
            strike = row["strike"]
            if (option_type == "call") != (strike >= spot):
                continue  # keep out-of-the-money options only
            if row["bid"] <= 0 or row["ask"] <= 0:
                continue
            mid = 0.5 * (row["bid"] + row["ask"])
            iv = implied_vol(mid, spot, strike, days / 365, r, option_type)
            if np.isfinite(iv) and 0.01 < iv < 3:
                rows.append({"strike": strike, "iv": iv, "type": option_type})

    if not rows:
        return None
    return pd.DataFrame(rows).sort_values("strike"), spot, days


def synthetic_smile(S=100.0, T=0.25, r=0.03):
    """A made-up but realistic skew, for when there is no internet.

    Prices are generated from a known vol curve, then `implied_vol` recovers the
    curve, which doubles as a check that the solver round-trips.
    """
    strikes = np.arange(70, 131, 2.5)
    moneyness = np.log(strikes / S)
    true_vol = 0.20 - 0.25 * moneyness + 0.6 * moneyness**2  # skew + smile

    rows = []
    for strike, vol in zip(strikes, true_vol):
        option_type = "call" if strike >= S else "put"
        price = bs_price(S, strike, T, r, vol, option_type)
        iv = implied_vol(price, S, strike, T, r, option_type)
        rows.append({"strike": strike, "iv": iv, "type": option_type})
    return pd.DataFrame(rows), S, int(T * 365)
