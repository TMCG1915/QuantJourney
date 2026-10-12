"""Delta-hedging simulation: how does hedging frequency change the P&L?"""

import numpy as np

from bs_pricer.black_scholes import bs_delta, bs_price, vanilla_payoff


def delta_hedge_pnl(S0, K, T, r, sigma, n_steps, mu=None, n_paths=5000, option_type="call", seed=0):
    """P&L at expiry from selling an option and delta-hedging it n_steps times.

    The option is sold at its Black-Scholes price. We then hold `delta` shares
    (financed by borrowing at r) and rebalance at n_steps equally spaced dates.
    Stock paths use drift `mu` (defaults to r). The P&L is in expiry-date money.
    """
    mu = r if mu is None else mu
    rng = np.random.default_rng(seed)
    dt = T / n_steps

    # Simulate stock paths, shape (n_paths, n_steps + 1).
    z = rng.standard_normal((n_paths, n_steps))
    log_steps = (mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * z
    S = S0 * np.exp(np.hstack([np.zeros((n_paths, 1)), np.cumsum(log_steps, axis=1)]))

    # Day 0: sell the option, buy delta shares, put the rest in the bank.
    premium = bs_price(S0, K, T, r, sigma, option_type)
    delta = bs_delta(S0, K, T, r, sigma, option_type) * np.ones(n_paths)
    cash = premium - delta * S[:, 0]

    # Rebalance at each later date (the final date only settles, no new trade).
    for i in range(1, n_steps):
        cash = cash * np.exp(r * dt)
        new_delta = bs_delta(S[:, i], K, T - i * dt, r, sigma, option_type)
        cash = cash - (new_delta - delta) * S[:, i]
        delta = new_delta

    cash = cash * np.exp(r * dt)
    final_value = cash + delta * S[:, -1] - vanilla_payoff(S[:, -1], K, option_type)
    return final_value
