"""Interactive Black-Scholes dashboard.

Usage (from the quant_models folder, after `pip install -e .`):
    streamlit run bs_pricer/app.py
"""

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

from bs_pricer.binomial_tree import binomial_price
from bs_pricer.black_scholes import bs_greeks, bs_price
from bs_pricer.monte_carlo import mc_price
from common.plotting import COLORS

st.set_page_config(page_title="Black-Scholes explorer", layout="wide")
st.title("Black-Scholes explorer")

# --- Sidebar inputs ---
st.sidebar.header("Option inputs")
option_type = st.sidebar.radio("Type", ["call", "put"], horizontal=True)
S = st.sidebar.slider("Spot (S)", 50.0, 150.0, 100.0)
K = st.sidebar.slider("Strike (K)", 50.0, 150.0, 100.0)
T = st.sidebar.slider("Time to expiry (years)", 0.05, 3.0, 1.0)
r = st.sidebar.slider("Risk-free rate", 0.0, 0.10, 0.05, step=0.005)
sigma = st.sidebar.slider("Volatility", 0.05, 0.80, 0.20, step=0.01)

# --- Price three ways ---
exact = bs_price(S, K, T, r, sigma, option_type)
tree = binomial_price(S, K, T, r, sigma, steps=300, option_type=option_type)
mc, mc_se = mc_price(S, K, T, r, sigma, option_type, n_paths=100_000, seed=0)

col1, col2, col3 = st.columns(3)
col1.metric("Black-Scholes", f"{exact:.4f}")
col2.metric("Binomial tree (300 steps)", f"{tree:.4f}")
col3.metric("Monte Carlo (100k paths)", f"{mc:.4f}", f"+/- {2 * mc_se:.4f}", delta_color="off")

# --- Greeks at the chosen inputs ---
st.subheader("Greeks")
greeks = bs_greeks(S, K, T, r, sigma, option_type)
cols = st.columns(5)
cols[0].metric("Delta", f"{greeks['delta']:.4f}")
cols[1].metric("Gamma", f"{greeks['gamma']:.4f}")
cols[2].metric("Vega (per 1%)", f"{greeks['vega'] / 100:.4f}")
cols[3].metric("Theta (per day)", f"{greeks['theta'] / 365:.4f}")
cols[4].metric("Rho (per 1%)", f"{greeks['rho'] / 100:.4f}")

# --- Greeks and price as the spot moves ---
st.subheader("How things change with the spot price")
chosen = st.selectbox("Plot", ["price", "delta", "gamma", "vega", "theta", "rho"])
spots = np.linspace(0.5 * K, 1.5 * K, 200)

if chosen == "price":
    values = bs_price(spots, K, T, r, sigma, option_type)
else:
    values = bs_greeks(spots, K, T, r, sigma, option_type)[chosen]

fig, ax = plt.subplots(figsize=(8, 3.5))
ax.plot(spots, values, color=COLORS[0])
ax.axvline(S, color="#898781", linestyle="--", linewidth=1)
ax.set_xlabel("spot")
ax.set_ylabel(chosen)
st.pyplot(fig)
