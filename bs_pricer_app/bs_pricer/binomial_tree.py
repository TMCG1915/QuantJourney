"""Cox-Ross-Rubinstein binomial tree (European and American options)."""

import numpy as np

from bs_pricer.black_scholes import vanilla_payoff


def binomial_price(S, K, T, r, sigma, steps=200, option_type="call", american=False, q=0.0):
    """Price an option on a recombining binomial tree."""
    dt = T / steps
    u = np.exp(sigma * np.sqrt(dt))
    d = 1 / u
    p = (np.exp((r - q) * dt) - d) / (u - d)  # risk-neutral up probability
    discount = np.exp(-r * dt)

    # Stock prices at expiry: node j has j down-moves and (steps - j) up-moves.
    j = np.arange(steps + 1)
    values = vanilla_payoff(S * u ** (steps - j) * d**j, K, option_type)

    # Step backwards through the tree.
    for i in range(steps - 1, -1, -1):
        values = discount * (p * values[:-1] + (1 - p) * values[1:])
        if american:
            j = np.arange(i + 1)
            stock = S * u ** (i - j) * d**j
            values = np.maximum(values, vanilla_payoff(stock, K, option_type))

    return values[0]
