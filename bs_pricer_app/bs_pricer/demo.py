"""Run every Black-Scholes demo and save the figures.

Usage (from the quant_models folder):
    python -m bs_pricer.demo
"""

import matplotlib.pyplot as plt

from bs_pricer.binomial_tree import binomial_price
from bs_pricer.black_scholes import bs_greeks, bs_price
from bs_pricer.hedging import delta_hedge_pnl
from bs_pricer.monte_carlo import mc_price
from bs_pricer.smile import smile_from_chain, synthetic_smile
from common.plotting import COLORS, save_figure

PROJECT = "bs_pricer"
S, K, T, R, SIGMA = 100.0, 100.0, 1.0, 0.05, 0.20


def price_three_ways():
    exact = bs_price(S, K, T, R, SIGMA)
    tree = binomial_price(S, K, T, R, SIGMA, steps=500)
    mc, se = mc_price(S, K, T, R, SIGMA, n_paths=500_000, seed=1)

    print("\n=== One call, three prices ===")
    print(f"Black-Scholes closed form : {exact:.4f}")
    print(f"Binomial tree (500 steps) : {tree:.4f}")
    print(f"Monte Carlo (500k paths)  : {mc:.4f}  (+/- {2 * se:.4f} at 95%)")

    print("\n=== Greeks of the same call (raw units) ===")
    for name, value in bs_greeks(S, K, T, R, SIGMA).items():
        print(f"{name:>6}: {value: .4f}")


def convergence_plot():
    exact = bs_price(S, K, T, R, SIGMA)

    steps = [10, 20, 50, 100, 200, 500, 1000, 2000]
    tree_error = [abs(binomial_price(S, K, T, R, SIGMA, n) - exact) for n in steps]

    paths = [10**3, 10**4, 10**5, 10**6]
    mc_error, mc_band = [], []
    for n in paths:
        price, se = mc_price(S, K, T, R, SIGMA, n_paths=n, seed=2)
        mc_error.append(abs(price - exact))
        mc_band.append(2 * se)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    ax1.loglog(steps, tree_error, "o-", color=COLORS[0], markersize=5)
    ax1.set_title("Binomial tree: error vs number of steps")
    ax1.set_xlabel("steps")
    ax1.set_ylabel("|tree - Black-Scholes|")

    ax2.loglog(paths, mc_error, "o-", color=COLORS[1], markersize=5, label="actual error")
    ax2.loglog(paths, mc_band, "--", color=COLORS[1], alpha=0.6, label="2 x std error")
    ax2.set_title("Monte Carlo: error vs number of paths")
    ax2.set_xlabel("paths")
    ax2.legend()
    save_figure(fig, PROJECT, "convergence.png")


def hedging_plot():
    print("\n=== Delta hedging a short call: P&L spread vs hedging frequency ===")
    frequencies = [
        ("quarterly (4)", 4),
        ("monthly (12)", 12),
        ("weekly (52)", 52),
        ("daily (252)", 252),
    ]
    fig, axes = plt.subplots(2, 2, figsize=(9, 6), sharex=True, sharey=True)

    for ax, (label, n_steps) in zip(axes.ravel(), frequencies):
        pnl = delta_hedge_pnl(S, K, T, R, SIGMA, n_steps, mu=0.10, n_paths=5000)
        print(f"{label:>14}: mean P&L {pnl.mean(): .3f}, std {pnl.std(): .3f}")
        ax.hist(pnl, bins=50, color=COLORS[2])
        ax.set_title(f"{label}  (std {pnl.std():.2f})")
    fig.supxlabel("P&L at expiry")
    save_figure(fig, PROJECT, "delta_hedging.png")


def smile_plot():
    result = smile_from_chain("SPY")
    if result is None:
        print("\nUsing a SYNTHETIC smile (no live option chain available).")
        smile, spot, days = synthetic_smile()
        source = "synthetic data"
    else:
        smile, spot, days = result
        source = "live SPY options"

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(smile["strike"], smile["iv"] * 100, "o", color=COLORS[0], markersize=4)
    ax.axvline(spot, color="#898781", linestyle="--", linewidth=1)
    ax.set_title(f"Implied vol smile ({source}, {days} days to expiry)")
    ax.set_xlabel("strike")
    ax.set_ylabel("implied vol (%)")
    ax.text(spot, ax.get_ylim()[1], " spot", color="#898781", va="top")
    save_figure(fig, PROJECT, "vol_smile.png")


if __name__ == "__main__":
    price_three_ways()
    convergence_plot()
    hedging_plot()
    smile_plot()
