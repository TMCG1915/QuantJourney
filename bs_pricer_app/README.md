# Black-Scholes pricer app

Prices European options three ways (Black-Scholes formula, binomial tree, Monte Carlo)
and shows the Greeks in an interactive Streamlit dashboard.
See [bs_pricer/README.md](bs_pricer/README.md) for the maths and results.

## Run it

From this folder:

```
python -m pip install -e ".[app,dev]"   # one time only
streamlit run bs_pricer/app.py          # opens the dashboard in your browser
```

The `-e .` install is what lets Python find the `bs_pricer` and `common` packages.
Without it you get `ModuleNotFoundError`.

## Run the tests

```
python -m pytest
```
