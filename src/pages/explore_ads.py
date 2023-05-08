# Author: Ty Andrews
# March 13, 2023

import os
import sys

import dash

dash.register_page(
    __name__,
    title="Fortunato Wheels | Explore",
    name="Fortunato Wheels | Explore",
)

from dash import Dash, dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import plotly.express as px
import numpy as np
import time

cur_dir = os.getcwd()
try:
    SRC_PATH = cur_dir[: cur_dir.index("fortunato-wheels") + len("fortunato-wheels")]
except ValueError:
    # del with render not working with relative imports
    SRC_PATH = ""
    pass
if SRC_PATH not in sys.path:
    sys.path.append(SRC_PATH)

from src.data.load_preprocess_craigslist import load_craigslist_data
from src.visualizations.explore_ads_plots import (
    plot_vehicle_price_over_time,
    plot_vehicle_condition,
    plot_odometer_histogram,
)
from src.pages.dash_styles import SIDEBAR_STYLE, CONTENT_STYLE

vehicles_df = load_craigslist_data()

filtering_accordion = html.Div(
    dbc.Accordion(
        [
            dbc.AccordionItem(
                children=[
                    dmc.MultiSelect(
                        label="Select Vehicle Makes",
                        placeholder="All Makes",
                        id="explore-make-select",
                        searchable=True,
                        clearable=True,
                        nothingFound="No matching makes found",
                        value=[],
                    ),
                    dmc.MultiSelect(
                        label="Select Models",
                        placeholder="No models selected",
                        id="explore-model-select",
                        searchable=True,
                        clearable=True,
                        nothingFound="No matching models found",
                        value=["civic", "tundra", "cr-v"],
                        maxSelectedValues=6,
                        required=True,
                    ),
                ],
                title="Make & Model",
            ),
            dbc.AccordionItem(
                dcc.RangeSlider(
                    min=0,
                    max=100_000,
                    step=100,
                    id="explore-price-slider",
                    value=[0, 100_000],
                    tooltip={"placement": "bottom", "always_visible": True},
                    marks=None,
                ),
                title="Price",
            ),
            dbc.AccordionItem(
                dcc.RangeSlider(
                    min=0,
                    max=15,
                    step=1,
                    id="explore-age-slider",
                    value=[0, 15],
                    tooltip={"placement": "bottom", "always_visible": True},
                    marks=None,
                ),
                title="Vehicle Age",
            ),
        ],
        flush=True,
        always_open=True,
    ),
)

sidebar = html.Div(
    [
        html.P(
            "Select what type of vehicle you're looking for.",
            className="lead",
            style={"font-family": "'Poppins'"},
        ),
        html.Hr(),
        filtering_accordion,
        html.Center(
            html.A(
                dmc.Button(
                    "Apply Filters",
                    id="apply-filters-button",
                    leftIcon=[
                        DashIconify(
                            icon="material-symbols:filter-alt",
                            width=25,
                        )
                    ],
                    variant="gradient",
                    gradient={"from": "indigo", "to": "cyan"},
                    style={
                        "margin-right": "5px",
                        "margin-left": "5px",
                        "margin-top": "10px",
                        "margin-bottom": "10px",
                    },
                ),
                style={"textAlign": "center"},
            )
        ),
        html.Hr(),
        html.Div(id="num-matching-entries"),
    ],
    style=SIDEBAR_STYLE,
)

vehicle_condition_card = (
    dbc.Card(
        [
            dbc.CardHeader("Number of Ads Analyzed"),
            dbc.CardBody(
                [
                    dbc.Spinner(
                        dcc.Graph(
                            id="num-ads-summary-plot",
                            figure=blank_placeholder_plot(height=300),
                        ),
                        type="grow",
                        color="primary",
                    )
                ]
            ),
        ]
    ),
)


content = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader("Car Prices by Age"),
                        dbc.CardBody(
                            [
                                dbc.Spinner(
                                    dcc.Graph(
                                        id="price-age-summary-plot",
                                        figure=blank_placeholder_plot(height=300),
                                        config={"displayModeBar": False},
                                    ),
                                    type="grow",
                                    color="primary",
                                ),
                                dbc.Row(
                                    html.Label(
                                        [
                                            "* lines indicate LOWESS smoothing model, see ",
                                            html.A(
                                                "here for more info",
                                                href="https://en.wikipedia.org/wiki/Local_regression",
                                            ),
                                        ],
                                    ),
                                    style={"font-size": "12px"},
                                    justify="right",
                                ),
                            ]
                        ),
                    ]
                ),
                style=CONTENT_STYLE,
                width=12,
            ),
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader("Number of Ads Analyzed"),
                            dbc.CardBody(
                                [
                                    dbc.Spinner(
                                        dcc.Graph(
                                            id="num-ads-summary-plot",
                                            figure=blank_placeholder_plot(height=300),
                                        ),
                                        type="grow",
                                        color="primary",
                                    )
                                ]
                            ),
                        ]
                    ),
                    width=12,
                    lg=6,
                    style=CONTENT_STYLE,
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader("Average Yearly Mileage"),
                            dbc.CardBody(
                                [
                                    dbc.Spinner(
                                        dcc.Graph(
                                            id="vehicle-mileage-plot",
                                            figure=blank_placeholder_plot(height=300),
                                        ),
                                        type="grow",
                                        color="primary",
                                    )
                                ]
                            ),
                        ]
                    ),
                    width=12,
                    lg=6,
                    style=CONTENT_STYLE,
                ),
            ],
            style=CONTENT_STYLE,
        ),
    ],
    style=CONTENT_STYLE,
)


layout = html.Div(
    [
        html.Div(id="explore-first-load", children=True, style={"display": "none"}),
        dbc.Row(
            [
                dbc.Col(sidebar, width=12, lg=3, className="g-0"),
                dbc.Col(content, width=12, lg=9, className="g-0"),
            ],
            className="g-0",
            style={
                "height": "100vh",
            },  # "overflow": "hidden"
        ),
    ]
)


@callback(
    Output("num-matching-entries", "children"),
    [
        Input("explore-year-slider", "value"),
        Input("explore-price-slider", "value"),
        Input("explore-model-select", "value"),
        Input("explore-manufacturer-select", "value"),
    ],
)
def update_ad_filter_count(year_range, price_range, models, manufacturers):

    if price_range is None:
        price_range = [vehicles_df.price.min(), vehicles_df.price.max()]

    if len(models) == 0:
        models = vehicles_df.model.unique()

    if len(manufacturers) == 0:
        manufacturers = vehicles_df.manufacturer.unique()

    if year_range is None:
        year_range = [vehicles_df.year.min(), vehicles_df.year.max()]

    subset_df = vehicles_df.query(
        "manufacturer in @manufacturers & "
        "model in @models & "
        "price > @price_range[0] & "
        "price < @price_range[1] & "
        "year >= @year_range[0] & "
        "year <= @year_range[1]"
    )

    num_matching_entries = html.H4(
        str(len(subset_df)) + " matching ads",
        style={"font-family": "'Poppins'", "textAlign": "center"},
    )

    return num_matching_entries


@callback(
    Output("price-over-time-plot", "figure"),
    Output("vehicle-condition-plot", "figure"),
    Output("vehicle-odometer-plot", "figure"),
    [Input("apply-filters-button", "n_clicks")],
    [
        State("explore-year-slider", "value"),
        State("explore-price-slider", "value"),
        State("explore-model-select", "value"),
        State("explore-manufacturer-select", "value"),
    ],
)
def update_explorer_plots(n_clicks, year_range, price_range, models, manufacturers):

    if price_range is None:
        price_range = [vehicles_df.price.min(), vehicles_df.price.max()]

    if len(models) == 0:
        models = vehicles_df.model.unique()

    if len(manufacturers) == 0:
        manufacturers = vehicles_df.manufacturer.unique()

    if year_range is None:
        year_range = [vehicles_df.year.min(), vehicles_df.year.max()]

    subset_df = vehicles_df.query(
        "manufacturer in @manufacturers & "
        "model in @models & "
        "price > @price_range[0] & "
        "price < @price_range[1] & "
        "year >= @year_range[0] & "
        "year <= @year_range[1]"
    )

    price_fig = plot_vehicle_price_over_time(subset_df)

    condition_fig = plot_vehicle_condition(subset_df)

    odometer_fig = plot_odometer_histogram(subset_df)

    num_matching_entries = html.H4(
        str(len(subset_df)) + " matching ads",
        style={"font-family": "'Poppins'", "textAlign": "center"},
    )

    return price_fig, condition_fig, odometer_fig
