"""Black-Scholes pricing, Greeks and implied volatility for European options.

Conventions:
    S = spot, K = strike, T = time to expiry in years, r = risk-free rate,
    sigma = volatility, q = continuous dividend yield.
    Greeks are "raw": vega is per 1.00 of vol, theta is per year and rho is per
    1.00 of rate. Divide by 100 / 365 / 100 for per-1% / per-day / per-1% numbers.
"""

import numpy as np
from scipy.stats import norm


def vanilla_payoff(S, K, option_type="call"):
    """Payoff of a European option at expiry."""
    if option_type == "call":
        return np.maximum(S - K, 0.0)
    if option_type == "put":
        return np.maximum(K - S, 0.0)
    raise ValueError("option_type must be 'call' or 'put'")


def _d1_d2(S, K, T, r, sigma, q=0.0):
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return d1, d2


def bs_price(S, K, T, r, sigma, option_type="call", q=0.0):
    """Black-Scholes price of a European call or put."""
    d1, d2 = _d1_d2(S, K, T, r, sigma, q)
    if option_type == "call":
        return S * np.exp(-q * T) * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    if option_type == "put":
        return K * np.exp(-r * T) * norm.cdf(-d2) - S * np.exp(-q * T) * norm.cdf(-d1)
    raise ValueError("option_type must be 'call' or 'put'")


def bs_delta(S, K, T, r, sigma, option_type="call", q=0.0):
    """Delta only (used a lot in hedging, so it gets its own function)."""
    d1, _ = _d1_d2(S, K, T, r, sigma, q)
    if option_type == "call":
        return np.exp(-q * T) * norm.cdf(d1)
    return np.exp(-q * T) * (norm.cdf(d1) - 1.0)


def bs_greeks(S, K, T, r, sigma, option_type="call", q=0.0):
    """Delta, gamma, vega, theta and rho as a dictionary."""
    d1, d2 = _d1_d2(S, K, T, r, sigma, q)
    pdf_d1 = norm.pdf(d1)
    disc_q = np.exp(-q * T)
    disc_r = np.exp(-r * T)

    # Gamma and vega are the same for calls and puts.
    gamma = disc_q * pdf_d1 / (S * sigma * np.sqrt(T))
    vega = S * disc_q * pdf_d1 * np.sqrt(T)
    decay = -S * disc_q * pdf_d1 * sigma / (2 * np.sqrt(T))

    if option_type == "call":
        theta = decay - r * K * disc_r * norm.cdf(d2) + q * S * disc_q * norm.cdf(d1)
        rho = K * T * disc_r * norm.cdf(d2)
    elif option_type == "put":
        theta = decay + r * K * disc_r * norm.cdf(-d2) - q * S * disc_q * norm.cdf(-d1)
        rho = -K * T * disc_r * norm.cdf(-d2)
    else:
        raise ValueError("option_type must be 'call' or 'put'")

    return {
        "delta": bs_delta(S, K, T, r, sigma, option_type, q),
        "gamma": gamma,
        "vega": vega,
        "theta": theta,
        "rho": rho,
    }


def implied_vol(price, S, K, T, r, option_type="call", q=0.0, tol=1e-8):
    """Back out implied volatility from an option price.

    Tries Newton-Raphson first (fast). If Newton wanders off or vega is tiny, it
    falls back to bisection (slow but cannot fail). Returns NaN if the price
    breaks the no-arbitrage bounds.
    """
    # The price cannot be below the discounted intrinsic value.
    forward_value = S * np.exp(-q * T) - K * np.exp(-r * T)
    intrinsic = max(forward_value if option_type == "call" else -forward_value, 0.0)
    if price < intrinsic - 1e-12:
        return np.nan

    # --- Newton-Raphson ---
    sigma = 0.2
    for _ in range(50):
        diff = bs_price(S, K, T, r, sigma, option_type, q) - price
        if abs(diff) < tol:
            return sigma
        vega = bs_greeks(S, K, T, r, sigma, option_type, q)["vega"]
        if vega < 1e-10:
            break
        sigma_new = sigma - diff / vega
        if sigma_new <= 0 or sigma_new > 5:
            break
        sigma = sigma_new

    # --- Bisection fallback ---
    low, high = 1e-6, 5.0
    if bs_price(S, K, T, r, low, option_type, q) > price:
        return np.nan
    if bs_price(S, K, T, r, high, option_type, q) < price:
        return np.nan
    for _ in range(200):
        mid = 0.5 * (low + high)
        if bs_price(S, K, T, r, mid, option_type, q) > price:
            high = mid
        else:
            low = mid
        if high - low < tol:
            break
    return 0.5 * (low + high)
