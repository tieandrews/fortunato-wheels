# Author: Ty Andrews
# March 13, 2023

import os

import pandas as pd


def load_craigslist_data():
    df = pd.read_csv(os.path.join("data", "processed", "cleaned-vehicles.csv"))
    return df
