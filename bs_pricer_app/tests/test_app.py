from pathlib import Path

import pytest

pytest.importorskip("streamlit")  # skip if Streamlit is not installed
from streamlit.testing.v1 import AppTest  # noqa: E402

APP = Path(__file__).resolve().parent.parent / "bs_pricer" / "app.py"


def test_dashboard_runs_and_shows_the_textbook_price():
    app = AppTest.from_file(str(APP), default_timeout=60).run()
    assert not app.exception

    prices = [metric.value for metric in app.metric[:3]]
    assert prices[0] == "10.4506"  # Black-Scholes with the default inputs
    assert abs(float(prices[1]) - 10.4506) < 0.05  # binomial tree
    assert abs(float(prices[2]) - 10.4506) < 0.2  # Monte Carlo


def test_dashboard_reacts_to_inputs():
    app = AppTest.from_file(str(APP), default_timeout=60).run()
    app.sidebar.radio[0].set_value("put").run()
    assert not app.exception
    assert app.metric[0].value == "5.5735"  # put price for the default inputs
