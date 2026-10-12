"""Plain Monte Carlo pricing of a European option under Black-Scholes."""

import numpy as np

from bs_pricer.black_scholes import vanilla_payoff


def mc_price(S, K, T, r, sigma, option_type="call", n_paths=100_000, q=0.0, seed=None):
    """Return (price, standard_error)."""
    rng = np.random.default_rng(seed)
    z = rng.standard_normal(n_paths)
    S_T = S * np.exp((r - q - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * z)
    discounted = np.exp(-r * T) * vanilla_payoff(S_T, K, option_type)
    return discounted.mean(), discounted.std(ddof=1) / np.sqrt(n_paths)
