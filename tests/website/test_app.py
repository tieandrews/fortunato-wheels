import os, sys

import pytest
import dash
import logging 
from dash.dependencies import Input, Output, State

# on launch ensure src is in path
cur_dir = os.getcwd()
try:
    SRC_PATH = cur_dir[: cur_dir.index("fortunato-wheels") + len("fortunato-wheels")]
except ValueError:
    # deal with Azure app service not working with relative imports
    SRC_PATH = ""
    pass
if SRC_PATH not in sys.path:
    sys.path.append(SRC_PATH)

from src.app import toggle_navbar_collapse, load_data

@pytest.fixture
def sample_data():
    return {
        'price_summary': {'make': 'Toyota', 'model': 'Camry', 'min_price': 10000, 'max_price': 15000},
        'num_ads_summary': {'make': 'Toyota', 'model': 'Camry', 'num_ads': 100},
        'mileage_summary': {'make': 'Toyota', 'model': 'Camry', 'min_mileage': 1000, 'max_mileage': 2000}
    }

# ensure if data is already loaded that load_data does not re-load data
def test_data_already_loaded(sample_data):
    price_summary, num_ads_summary, mileage_summary = sample_data['price_summary'], sample_data['num_ads_summary'], sample_data['mileage_summary']
    first_load = True
    pytest.raises(dash.exceptions.PreventUpdate, load_data, first_load, price_summary, num_ads_summary, mileage_summary)

# ensure the navbar collapse toggles correctly
@pytest.mark.parametrize(
    "n, is_open, expected",
    [
        (0, True, True),
        (1, False, True),
        (2, True, False)
    ]
)
def test_toggle_navbar_collapse(n, is_open, expected):
    assert toggle_navbar_collapse(n, is_open) == expected