import numpy as np
import pytest

from bs_pricer.binomial_tree import binomial_price
from bs_pricer.black_scholes import bs_greeks, bs_price, implied_vol
from bs_pricer.hedging import delta_hedge_pnl
from bs_pricer.monte_carlo import mc_price
from bs_pricer.smile import synthetic_smile

S, K, T, R, SIGMA = 100.0, 100.0, 1.0, 0.05, 0.20


def test_known_values():
    # Textbook values for S=K=100, T=1, r=5%, sigma=20%.
    assert bs_price(S, K, T, R, SIGMA, "call") == pytest.approx(10.4506, abs=1e-3)
    assert bs_price(S, K, T, R, SIGMA, "put") == pytest.approx(5.5735, abs=1e-3)


def test_put_call_parity():
    call = bs_price(S, 110, T, R, SIGMA, "call")
    put = bs_price(S, 110, T, R, SIGMA, "put")
    assert call - put == pytest.approx(S - 110 * np.exp(-R * T))


@pytest.mark.parametrize("option_type", ["call", "put"])
def test_greeks_match_finite_differences(option_type):
    greeks = bs_greeks(S, K, T, R, SIGMA, option_type)
    h = 1e-4

    def price(s=S, sigma=SIGMA, t=T, r=R):
        return bs_price(s, K, t, r, sigma, option_type)

    delta = (price(s=S + h) - price(s=S - h)) / (2 * h)
    gamma = (price(s=S + h) - 2 * price() + price(s=S - h)) / h**2
    vega = (price(sigma=SIGMA + h) - price(sigma=SIGMA - h)) / (2 * h)
    theta = -(price(t=T + h) - price(t=T - h)) / (2 * h)
    rho = (price(r=R + h) - price(r=R - h)) / (2 * h)

    assert greeks["delta"] == pytest.approx(delta, abs=1e-5)
    assert greeks["gamma"] == pytest.approx(gamma, abs=1e-4)
    assert greeks["vega"] == pytest.approx(vega, abs=1e-4)
    assert greeks["theta"] == pytest.approx(theta, abs=1e-4)
    assert greeks["rho"] == pytest.approx(rho, abs=1e-4)


@pytest.mark.parametrize("strike", [60, 90, 100, 120, 200])
@pytest.mark.parametrize("option_type", ["call", "put"])
def test_implied_vol_round_trip(strike, option_type):
    price = bs_price(S, strike, 0.5, R, 0.35, option_type)
    assert implied_vol(price, S, strike, 0.5, R, option_type) == pytest.approx(0.35, abs=1e-5)


def test_implied_vol_rejects_arbitrage_price():
    assert np.isnan(implied_vol(0.5, S, 80, T, R, "call"))  # below intrinsic value


def test_tree_converges_to_black_scholes():
    exact = bs_price(S, K, T, R, SIGMA)
    assert binomial_price(S, K, T, R, SIGMA, steps=1000) == pytest.approx(exact, abs=0.02)


def test_american_put_is_worth_more_than_european():
    european = binomial_price(S, K, T, R, SIGMA, 300, "put", american=False)
    american = binomial_price(S, K, T, R, SIGMA, 300, "put", american=True)
    assert american > european


def test_monte_carlo_within_error_bars():
    exact = bs_price(S, K, T, R, SIGMA)
    price, se = mc_price(S, K, T, R, SIGMA, n_paths=200_000, seed=0)
    assert abs(price - exact) < 4 * se


def test_more_frequent_hedging_reduces_pnl_spread():
    spread_weekly = delta_hedge_pnl(S, K, T, R, SIGMA, 52).std()
    spread_daily = delta_hedge_pnl(S, K, T, R, SIGMA, 252).std()
    assert spread_daily < spread_weekly


def test_synthetic_smile_recovers_true_vols():
    smile, spot, _ = synthetic_smile()
    assert smile["iv"].notna().all()
    assert smile["iv"].min() > 0.1
