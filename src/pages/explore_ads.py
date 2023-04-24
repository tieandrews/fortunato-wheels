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
                dmc.MultiSelect(
                    label="Select Manufacturers",
                    placeholder="All Manufacturers",
                    id="explore-manufacturer-select",
                    searchable=True,
                    clearable=True,
                    nothingFound="No matching manufacturers found",
                    value=["Toyota", "Honda"],
                    data=vehicles_df.manufacturer.unique(),
                ),
                title="Manufacturer",
            ),
            dbc.AccordionItem(
                dmc.MultiSelect(
                    label="Select Models",
                    placeholder="All Models",
                    id="explore-model-select",
                    searchable=True,
                    clearable=True,
                    nothingFound="No matching models found",
                    value=[],
                    data=vehicles_df.model.unique(),
                ),
                title="Model",
            ),
            dbc.AccordionItem(
                dcc.RangeSlider(
                    min=vehicles_df.price.min(),
                    max=vehicles_df.price.max(),
                    step=1,
                    id="explore-price-slider",
                    value=[0, vehicles_df.price.max()],
                    tooltip={"placement": "bottom", "always_visible": True},
                    marks=None,
                ),
                title="Price",
            ),
            dbc.AccordionItem(
                dcc.RangeSlider(
                    min=vehicles_df.year.min(),
                    max=vehicles_df.year.max(),
                    step=1,
                    id="explore-year-slider",
                    value=[vehicles_df.year.min(), vehicles_df.year.max()],
                    tooltip={"placement": "bottom", "always_visible": True},
                    marks=None,
                ),
                title="Year",
            ),
        ],
        flush=True,
        start_collapsed=True,
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
            dbc.CardHeader("Vehicle Condition"),
            dbc.CardBody(
                [
                    dbc.Spinner(
                        dcc.Graph(
                            id="vehicle-condition-plot",
                            figure=None,
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
                        dbc.CardHeader("Car Prices Over Time"),
                        dbc.CardBody(
                            [
                                dbc.Spinner(
                                    dcc.Graph(
                                        id="price-over-time-plot",
                                        figure=plot_vehicle_price_over_time(
                                            vehicles_df
                                        ),
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
                            dbc.CardHeader("Vehicle Condition"),
                            dbc.CardBody(
                                [
                                    dbc.Spinner(
                                        dcc.Graph(
                                            id="vehicle-condition-plot",
                                            figure=plot_vehicle_condition(vehicles_df),
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
                            dbc.CardHeader("Vehicle Mileage"),
                            dbc.CardBody(
                                [
                                    dbc.Spinner(
                                        dcc.Graph(
                                            id="vehicle-odometer-plot",
                                            figure=plot_odometer_histogram(vehicles_df),
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
)  # dcc.Location(id="url"),


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
