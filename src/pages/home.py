import dash

dash.register_page(
    __name__,
    path="/",
    title="Fortunato Wheels",
    name="Fortunato Wheels",
)

import sys, os
from dash import Dash, dcc, html, Input, Output, callback, State
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import plotly.express as px
import time

cur_dir = os.getcwd()
SRC_PATH = cur_dir[: cur_dir.index("fortunato-wheels") + len("fortunato-wheels")]
if SRC_PATH not in sys.path:
    sys.path.append(SRC_PATH)

from src.logs import get_logger

# Create a custom logger
logger = get_logger(__name__)

explore_ads_card = dbc.Card(
    [
        dbc.CardHeader(
            [
                html.H5(
                    "Figure Out What Used Cars Cost",
                    style={"text-align": "center"},
                ),
            ]
        ),
        dbc.CardBody(
            [
                html.H6(
                    "Explore past ads from multiple websites to figure out what the car you're looking for might cost.",
                    style={"text-align": "center"},
                ),
                dmc.Divider(variant="solid"),
                dmc.Anchor(
                    dmc.Button(
                        "Explore Past Ads",
                        variant="gradient",
                        gradient={"from": "indigo", "to": "cyan"},
                        leftIcon=[
                            DashIconify(
                                icon="material-symbols:nest-clock-farsight-analog-outline",
                                width=25,
                            )
                        ],
                        size="xl",
                        radius="xl",
                        fullWidth=True,
                        style={
                            "margin-right": "5px",
                            "margin-left": "5px",
                            "margin-top": "10px",
                            "margin-bottom": "10px",
                        },
                    ),
                    href="explore-ads",
                ),
            ],
            className="align-self-center",
        ),
    ],
)

analyze_ad_card = dbc.Card(
    [
        dbc.CardHeader(
            [
                dmc.Group(
                    [
                        dmc.Badge("BETA", color="blue", variant="light"),
                        html.H5(
                            "Analyze an Ad I Already Found",
                            style={"text-align": "center"},
                        ),
                    ],
                    position="left",
                ),
            ]
        ),
        dbc.CardBody(
            [
                html.H6(
                    "Analyze an ad you found on a website to figure out if it's a good deal.",
                    style={"text-align": "center"},
                ),
                dmc.Divider(variant="solid"),
                dmc.Anchor(
                    dmc.Button(
                        "(BETA) Analyze an Ad",
                        leftIcon=[
                            DashIconify(
                                icon="material-symbols:lab-research-outline-rounded",
                                width=25,
                            )
                        ],
                        variant="gradient",
                        gradient={"from": "indigo", "to": "cyan"},
                        disabled=True,
                        size="xl",
                        radius="xl",
                        fullWidth=True,
                        style={
                            "margin-right": "5px",
                            "margin-left": "5px",
                            "margin-top": "10px",
                            "margin-bottom": "10px",
                        },
                    ),
                    href="/",
                ),
            ],
            className="align-self-center",
        ),
    ],
)


layout = dbc.Container(  # html.Div(
    [
        dbc.Row(
            dbc.Col(
                [
                    dbc.Row(
                        html.Img(
                            src="assets/fortunato-wheels_logo_black.png",
                            # height="40px",
                            style={
                                "textAlign": "center",
                                "width": "60%",
                                "margin-top": "30px",
                            },
                        ),
                        justify="center",
                    ),
                    html.H1(
                        "Turning buying used cars from luck into science",
                        style={"text-align": "center", "margin-top": "20px"},
                    ),
                    html.H4(
                        "Fortunato Wheels is a data science project that aims to help you find the best deal on a used car.",
                        style={
                            "text-align": "center",
                            "margin-top": "50px",
                            "margin-bottom": "50px",
                        },
                    ),
                    dmc.Divider(
                        size="sm",
                        class_name=".h4",
                        labelPosition="center",
                    ),
                    html.H5(
                        "I want to:",
                        style={
                            "text-align": "center",
                            "margin-top": "40px",
                            "margin-bottom": "20px",
                        },
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                explore_ads_card,
                                width={"size": 12, "order": "last", "offset": 0},
                                xl={"size": 6, "order": "last", "offset": 0},
                            ),
                            dbc.Col(
                                analyze_ad_card,
                                width={"size": 12, "order": "last", "offset": 0},
                                xl={"size": 6, "order": "last", "offset": 0},
                            ),
                        ]
                    ),
                ],
                width={"size": 12, "order": "last", "offset": 0},
                lg={"size": 6, "order": "last", "offset": 3},
            )
        ),
    ],
    fluid=True,
)
