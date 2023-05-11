# Author: Ty Andrews
# Date: 2023-05-11

import os, sys

import os, sys
import requests
import json
from dotenv import load_dotenv, find_dotenv
import time

from src.logs import get_logger

logger = get_logger(__name__)

load_dotenv(find_dotenv())

GA4_CLIENT_SECRET = os.getenv("GA4_CLIENT_SECRET")
GA4_MEASUREMENT_ID = "G-CKDC8LRCRB"


def log_to_GA_list_of_items(event_name: str, item_name: str, list_of_items: list):
    """Sends a custom event to google analytics 4

    Parameters
    ----------
    list_of_items : list
        list of items to be logged
    list_name : str
        name of the list to be logged
    """
    success = True
    client_id = get_ga4_client_id()
    try:
        for item in list_of_items:
            event_params = {item_name: item}
            custom_event_to_GA(client_id, event_name, event_params)
    except Exception as e:
        logger.error(f"Failed to log {event_name} to GA4: {e}")
        success = False

    return success


def custom_event_to_GA(client_id: str, event_name: str, event_params: dict):
    """Sends a custom event to google analytics 4

    Parameters
    ----------
    event_name : str
        name of the event to be sent to google analytics 4
    event_params : dict
        dictionary of event parameters to be sent to google analytics 4, must
        contain only one instance of unique keys but can contain multiple key
        value pairs.

    Raises
    ------
    ValueError
        if event_params does not contain only one key value pair
    """

    # placeholder until access to live gtag clinet id is setup
    api_secret = GA4_CLIENT_SECRET
    measurement_id = GA4_MEASUREMENT_ID

    url = f"https://www.google-analytics.com/mp/collect?measurement_id={measurement_id}&api_secret={api_secret}"

    payload = {
        "client_id": client_id,
        "non_personalized_ads": False,
        "events": [{"name": event_name, "params": event_params}],
    }

    r = requests.post(url, data=json.dumps(payload), verify=True)

    print(r.status_code)


def get_ga4_client_id():
    """Placeholder function to return a client id for google analytics

    Returns
    -------
    str
        client id for google analytics, currently a timestamp in ns.
    """

    return str(time.time_ns())
