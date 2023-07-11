import os, sys

import pytest
import pandas as pd
import time

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

# import app so that dash app is created for page registration
from src.app import app

from src.pages.explore_ads import update_filter_options

INVALID_MODELS = ["Other"]

@pytest.fixture
def sample_data():
    makes_models_store = {
        "make": ["toyota", "honda", "ford"],
        "model": ["camry", "accord", "f150"]
    }
    price_summary_store = {
        "camry": [10000, 20000, 30000],
        "accord": [15000, 25000, 35000],
        "f150": [20000, 40000, 60000]
    }
    num_ads_summary_store = {
        "camry": [1000, 2000, 3000],
        "accord": [2000, 4000, 6000],
        "f150": [3000, 6000, 9000]
    }
    return (makes_models_store, price_summary_store, num_ads_summary_store)

# basic test with all features empty
def test_update_filter_options(sample_data):
    makes_models_store, price_summary_store, num_ads_summary_store = sample_data
    _first_load = True
    make_values = []
    make_options = None
    model_values = []
    model_options = None
    price_slider_max = 60000
    price_slider_values = [0, 60_000]
    model_options, make_options, max_price, price_slider_values = update_filter_options(
        _first_load,
        make_values,
        make_options,
        model_values,
        model_options,
        price_slider_max,
        price_slider_values,
        makes_models_store,
        price_summary_store,
        num_ads_summary_store,
    )
    # liists should be in alphabetical order
    assert model_options == [
        {'label': 'Accord (12000 ads)', 'value': 'accord'}, 
        {'label': 'Camry (6000 ads)', 'value': 'camry'}, 
        {'label': 'F150 (18000 ads)', 'value': 'f150'}
    ]
    assert make_options == [
        {'label': 'Ford (18.0k ads)', 'value': 'ford'},
        {'label': 'Honda (12.0k ads)', 'value': 'honda'}, 
        {'label': 'Toyota (6.0k ads)', 'value': 'toyota'}, 
    ]
    assert max_price == 60000
    assert price_slider_values == [0, 60000]

# basic test with all features empty
def test_update_filter_option_single_make(sample_data):
    makes_models_store, price_summary_store, num_ads_summary_store = sample_data
    _first_load = True
    make_values = ["toyota"]
    make_options = None
    model_values = []
    model_options = []
    price_slider_max = 60000
    price_slider_values = [0, 60_000]
    model_options, make_options, max_price, price_slider_values = update_filter_options(
        _first_load,
        make_values,
        make_options,
        model_values,
        model_options,
        price_slider_max,
        price_slider_values,
        makes_models_store,
        price_summary_store,
        num_ads_summary_store,
    )
    assert model_options == [
        {'label': 'Camry (6000 ads)', 'value': 'camry'}, 
    ]
    assert max_price == 30000
    assert price_slider_values == [0, 30000]    