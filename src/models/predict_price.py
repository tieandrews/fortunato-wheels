# Author: Ty Andrews
# Date: May 19, 2023

import os, sys

import pandas as pd
import requests
import time
import dotenv

dotenv.load_dotenv(dotenv.find_dotenv())

AZ_ML_ENDPOINT = os.getenv("AZ_ML_ENDPOINT")


def predict_car_price(
    model: str, make: str, age_at_posting: int, mileage_per_year: int, wheel_system: str
) -> int:
    """Takes in car info and predicts it's price.

    Parameters
    ----------
    model : str
        The model of vehicle to predict for.

    Returns
    -------
    int
        The predicted price.
    """

    data = {
        "request_data": {
            "data": {
                "vehicle_data": {
                    "model": model,
                    "age_at_posting": age_at_posting,
                    "mileage_per_year": mileage_per_year,
                    "make": make,
                    "wheel_system": wheel_system,
                }
            }
        }
    }

    headers = {"Content-Type": "application/json"}

    resp = requests.post(AZ_ML_ENDPOINT, json=data, headers=headers)

    prediction = round(resp.json()["predicted_price"][0])

    upper_ci = round(resp.json()["upper_ci"][0])
    lower_ci = round(resp.json()["lower_ci"][0])

    return prediction, upper_ci, lower_ci
