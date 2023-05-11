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
import pandas as pd
import time

from src.visualizations.explore_ads_plots import (
    plot_vehicle_prices_summary,
    plot_mileage_distribution_summary,
    plot_num_ads_summary,
)
from src.visualizations.utils import blank_placeholder_plot
from src.pages.dash_styles import SIDEBAR_STYLE, CONTENT_STYLE
from src.logs import get_logger
from src.analytics.google_analytics import log_to_GA_list_of_items

INVALID_MODELS = ["other"]
DEFAULT_MODELS = ["ghost", "model-x", "911", "m3"]
DEFAULT_MAKES = []

# Create a custom logger
logger = get_logger(__name__)

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
                        placeholder="No models selected, defaults used.",
                        id="explore-model-select",
                        searchable=True,
                        clearable=True,
                        nothingFound="No matching models found",
                        value=DEFAULT_MODELS,
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
                                            config={"displayModeBar": False},
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
                                            config={"displayModeBar": False},
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


# update the model select options based on the make select, price, age etc.
@callback(
    Output("explore-model-select", "data"),
    Output("explore-make-select", "data"),
    Output("explore-price-slider", "max"),
    Output("explore-price-slider", "value"),
    [
        Input("explore-first-load", "children"),
        Input("explore-make-select", "value"),
        Input("explore-make-select", "data"),
        Input("explore-model-select", "value"),
        Input("explore-model-select", "data"),
        Input("explore-price-slider", "max"),
        Input("explore-price-slider", "value"),
    ],
    [
        State("makes-models-store", "data"),
        State("price-summary-store", "data"),
        State("num-ads-summary-store", "data"),
    ],
)
def update_filter_options(
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
):
    """Update the data filtering options based on the selected make, model, price, age etc.

    Parameters
    ----------
    _first_load : bool
        True if this is the first time the page is loaded
    make_values : list
        List of selected makes from the drop down.
    make_options : list
        List of all available makes.
    model_values : list
        List of selected models from the drop down.
    model_options : list
        List of all available models.
    price_slider_max : int
        Maximum value of the price slider.
    price_slider_values : list
        List of values of the price slider.
    makes_models_store : dict
        Dictionary of makes and models.
    price_summary_store : dict
        Dictionary of price prices with columns being model names and rows being price bins
        by age of vehicle at posting in 'age' column
    num_ads_summary_store : dict
        Dictionary of number of ads summary with columns being model names and rows being bins
        of how many ads by age of vehicles at posting in 'age' column

    Returns
    -------
    make_options : dict
        List of all available makes and always has all makes available with number of ads
        for each make in the 'label' field.
    model_options : dict
        List of all available models and is updated based on the makes selected with number of ads
        for each model in the 'label' field.
    price_slider_max : int
        Maximum value of the price slider is updated if the user hasn't changed it, otherwise it remains as previously set.
    price_slider_values : list
        List of values of the price slider is set at, if the price range changes based
        on the selected makes and models, then the price slider is reset to the new range.
    """
    start_time = time.time()

    make_model_df = pd.DataFrame.from_dict(makes_models_store, orient="columns")
    price_summary_df = pd.DataFrame.from_dict(price_summary_store, orient="columns")
    num_ads_summary_df = pd.DataFrame.from_dict(num_ads_summary_store, orient="columns")

    # if make options is None, then we set it to all makes and always allow all makes selectable
    if make_options is None:
        make_options = make_model_df.make.unique().tolist()
        make_options.sort()
        models_list = (
            make_model_df.query("model not in @INVALID_MODELS").model.unique().tolist()
        )
        num_ads_per_make = (
            num_ads_summary_df[models_list].sum(axis=0).to_frame(name="num_ads")
        )
        num_ads_per_make["model"] = models_list
        # ad the matching make for each model to the dataframe
        num_ads_per_make["make"] = num_ads_per_make.model.apply(
            lambda x: make_model_df.query("model == @x").make.values[0]
        )
        num_ads_per_make = num_ads_per_make.groupby("make", as_index=False).agg(
            {"num_ads": "sum"}
        )
        # filter for a minimum of 200 ads per make
        num_ads_per_make = num_ads_per_make.query("num_ads > 200")

        make_options = [
            {
                "label": f'{make.replace("-", " ").title()} ({num_ads/1000:.1f}k ads)',
                "value": make,
            }
            for make, num_ads in zip(num_ads_per_make.make, num_ads_per_make.num_ads)
        ]

    # if model options is not initialized or no make is selected, then we set it to all models
    if (model_options is None) or (len(make_values) == 0):
        models_list = (
            make_model_df.query("model not in @INVALID_MODELS").model.unique().tolist()
            + model_values
        )
        models_list.sort()
    # if a make is selected then retrun model_options only of that make but
    # keep the current model_values visible in the list
    elif len(make_values) > 0:
        models_list = (
            make_model_df.query("make == @make_values & model not in @INVALID_MODELS")
            .model.unique()
            .tolist()
            + model_values
        )
        models_list.sort()
    # generate the model options
    num_ads_per_model = (
        num_ads_summary_df[models_list].sum(axis=0).to_frame(name="num_ads")
    )
    num_ads_per_model["model"] = models_list

    num_ads_per_model = num_ads_per_model.query("num_ads > 10")

    # create the model options for the drop down including number of ads per model
    model_options = [
        {
            "label": f'{model.replace("-", " ").title()} ({num_ads} ads)',
            "value": model,
        }
        for model, num_ads in zip(num_ads_per_model.model, num_ads_per_model.num_ads)
    ]

    # get max price for price slider
    if len(model_values) > 0:
        max_price = price_summary_df[model_values].max().max()
    elif len(make_values) > 0:
        models = make_model_df.query(
            "make in @make_values & model not in @INVALID_MODELS"
        ).model.unique()
        max_price = price_summary_df[models].max().max()
    else:
        max_price = price_summary_df.max().max()

    # if price slider has not been adjusted, set it to include the full range of prices
    if price_slider_values[1] == price_slider_max:
        price_slider_values[1] = max_price

    log_success = log_to_GA_list_of_items(
        event_name="explore_update_filters_time",
        item_name="time_ms",
        list_of_items=[int((time.time() - start_time) * 1000)],
    )
    logger.debug(
        f"explore_update_filters_time log success - {log_success}: {int((time.time() - start_time) * 1000)}"
    )
    return model_options, make_options, max_price, price_slider_values


@callback(
    Output("num-matching-entries", "children"),
    [
        Input("explore-age-slider", "value"),
        Input("explore-price-slider", "value"),
        Input("explore-model-select", "value"),
        Input("explore-make-select", "value"),
    ],
    State("num-ads-summary-store", "data"),
    State("makes-models-store", "data"),
)
def update_ad_filter_count(
    age_range, price_range, models, makes, num_ads_summary_dict, makes_models_dict
):
    start_time = time.time()

    num_ads_summary_df = pd.DataFrame.from_dict(num_ads_summary_dict, orient="columns")
    makes_models_df = pd.DataFrame.from_dict(makes_models_dict, orient="columns")

    if price_range is None:
        price_range = [0, vehicles_df.price.max()]

    if (len(models) == 0) & (len(makes) == 0):
        # remove some models that are not really models
        models = (
            makes_models_df.query("model not in @INVALID_MODELS")
            .model.unique()
            .tolist()
        )
    elif len(models) == 0:
        models = (
            makes_models_df.query("make in @makes & model not in @INVALID_MODELS")
            .model.unique()
            .tolist()
        )

    if len(makes) == 0:
        makes = makes_models_df.make.unique()

    if age_range is None:
        age_range = [vehicles_df.year.min(), vehicles_df.year.max()]

    matching_ads = (
        num_ads_summary_df.query("age >= @age_range[0] & age <= @age_range[1]")[models]
        .sum()
        .sum()
    )

    total_ads = num_ads_summary_df.drop(columns=["age"]).sum().sum()

    num_matching_entries = html.Div(
        [
            html.H4(
                str(matching_ads) + " matching ads",
                style={"font-family": "'Poppins'", "textAlign": "center"},
            ),
            html.H6(
                f"of {total_ads/1_000_000:.1f}" + "+ million ads analyzed",
                style={"font-family": "'Poppins'", "textAlign": "center"},
            ),
        ]
    )
    log_success = log_to_GA_list_of_items(
        event_name="explore_matching_ads_update_time",
        item_name="time_ms",
        list_of_items=[int((time.time() - start_time) * 1000)],
    )
    logger.debug(
        f"explore_matching_ads_update_time log success - {log_success}: {int((time.time() - start_time) * 1000)}"
    )

    return num_matching_entries


@callback(
    Output("price-age-summary-plot", "figure"),
    [Input("apply-filters-button", "n_clicks")],
    [
        State("explore-age-slider", "value"),
        State("explore-price-slider", "value"),
        State("explore-model-select", "value"),
        State("explore-make-select", "value"),
        State("price-summary-store", "data"),
        State("makes-models-store", "data"),
    ],
)
def update_price_summary_plot(
    n_clicks, age_range, price_range, models, makes, price_summary, makes_models
):
    start_time = time.time()
    # if no models selected, display the default models
    if len(models) == 0:
        models = DEFAULT_MODELS

    # log to GA the currently selected models & makes
    log_model_success = log_to_GA_list_of_items(
        event_name="explore_apply_filters_click",
        item_name="model",
        # remove default models from list of models
        list_of_items=[model for model in models if model not in DEFAULT_MODELS],
    )
    logger.debug(f"GA logging success for models: {log_model_success}")

    log_make_success = log_to_GA_list_of_items(
        event_name="explore_apply_filters_click",
        item_name="make",
        list_of_items=[make for make in makes if make not in DEFAULT_MAKES],
    )
    logger.debug(f"GA logging success for makes: {log_make_success}")

    # convert models to lower case and replace spaces with dashes
    models = [model.lower().replace(" ", "-") for model in models]

    price_summary_df = pd.DataFrame.from_dict(price_summary, orient="columns")
    makes_models_df = pd.DataFrame.from_dict(makes_models, orient="columns")

    price_summary_df = price_summary_df[models + ["age"]]

    if age_range is not None:
        price_summary_df = price_summary_df.query(
            "age >= @age_range[0] & age <= @age_range[1]"
        )

    # melt dataframe to long format with age, model, and price as columns
    price_summary_df = pd.melt(
        price_summary_df, id_vars=["age"], var_name="model", value_name="price"
    )

    # add make to the model field for the legend to be readable
    price_summary_df = price_summary_df.merge(
        makes_models_df, left_on="model", right_on="model", how="left"
    )
    price_summary_df["model"] = (
        price_summary_df["model"].str.title()
        + " ("
        + price_summary_df["make"].str.replace("-", " ").str.title()
        + ")"
    )

    # cast age to int
    price_summary_df["age"] = price_summary_df["age"].astype(int)
    # drop rows where price is less than 500
    price_summary_df = price_summary_df[price_summary_df["price"] > 500]

    price_summary_plot = plot_vehicle_prices_summary(price_summary_df)

    log_success = log_to_GA_list_of_items(
        event_name="explore_price_age_summary_update_time",
        item_name="time_ms",
        list_of_items=[int((time.time() - start_time) * 1000)],
    )
    logger.debug(
        f"explore_price_age_summary_update_time log success - {log_success}: {int((time.time() - start_time) * 1000)}"
    )

    return price_summary_plot


@callback(
    Output("vehicle-mileage-plot", "figure"),
    [Input("apply-filters-button", "n_clicks")],
    [
        State("explore-age-slider", "value"),
        State("explore-price-slider", "value"),
        State("explore-model-select", "value"),
        State("explore-make-select", "value"),
        State("mileage-summary-store", "data"),
        State("makes-models-store", "data"),
    ],
)
def update_mileage_summary_plot(
    n_clicks, year_range, price_range, models, makes, mileage_summary, makes_models
):
    start_time = time.time()
    # if no models selected, display the default models
    if len(models) == 0:
        models = DEFAULT_MODELS

    # convert models to lower case and replace spaces with dashes
    models = [model.lower().replace(" ", "-") for model in models]

    mileage_summary_df = pd.DataFrame.from_dict(mileage_summary, orient="columns")
    makes_models_df = pd.DataFrame.from_dict(makes_models, orient="columns")

    if models is None:
        mileage_summary_df = mileage_summary_df[
            ["911", "4runner", "tundra", "skyline"] + ["yearly_mileage_range"]
        ]
    else:
        mileage_summary_df = mileage_summary_df[models + ["yearly_mileage_range"]]

    # melt dataframe to long format with age, model, and price as columns
    mileage_summary_df = pd.melt(
        mileage_summary_df,
        id_vars=["yearly_mileage_range"],
        var_name="model",
        value_name="percent_of_vehicles",
    )

    # add make to the model field for the legend to be readable
    mileage_summary_df = mileage_summary_df.merge(
        makes_models_df, left_on="model", right_on="model", how="left"
    )
    mileage_summary_df["model"] = (
        mileage_summary_df["model"].str.title()
        + " ("
        + mileage_summary_df["make"].str.replace("-", " ").str.title()
        + ")"
    )

    # cast age to int
    mileage_summary_df["yearly_mileage_range"] = mileage_summary_df[
        "yearly_mileage_range"
    ].astype(int)

    mileage_summary_plot = plot_mileage_distribution_summary(mileage_summary_df)

    log_success = log_to_GA_list_of_items(
        event_name="explore_mileage_summary_update_time",
        item_name="time_ms",
        list_of_items=[int((time.time() - start_time) * 1000)],
    )
    logger.debug(
        f"explore_mileage_summary_update_time log success - {log_success}: {int((time.time() - start_time) * 1000)}"
    )

    return mileage_summary_plot


@callback(
    Output("num-ads-summary-plot", "figure"),
    [Input("apply-filters-button", "n_clicks")],
    [
        State("explore-age-slider", "value"),
        State("explore-price-slider", "value"),
        State("explore-model-select", "value"),
        State("explore-make-select", "value"),
        State("num-ads-summary-store", "data"),
        State("makes-models-store", "data"),
    ],
)
def update_num_ads_summary_plot(
    n_clicks, age_range, price_range, models, makes, num_ads_summary, makes_models
):
    start_time = time.time()
    # if no models selected, display the default models
    if len(models) == 0:
        models = DEFAULT_MODELS

    # convert models to lower case and replace spaces with dashes
    models = [model.lower().replace(" ", "-") for model in models]
    num_ads_summary_df = pd.DataFrame.from_dict(num_ads_summary, orient="columns")
    makes_models_df = pd.DataFrame.from_dict(makes_models, orient="columns")
    num_ads_summary_df = num_ads_summary_df[models + ["age"]]

    if age_range is not None:
        num_ads_summary_df = num_ads_summary_df.query(
            "age >= @age_range[0] & age <= @age_range[1]"
        )

    make_options = makes_models_df.make.unique().tolist()
    make_options.sort()

    num_ads_per_model = num_ads_summary_df[models].sum(axis=0).to_frame(name="num_ads")
    num_ads_per_model["model"] = models
    # ad the matching make for each model to the dataframe
    num_ads_per_model["make"] = num_ads_per_model.model.apply(
        lambda x: makes_models_df.query("model == @x").make.values[0]
    )

    num_ads_per_model["model"] = (
        num_ads_per_model["model"].str.title()
        + "<br>("
        + num_ads_per_model["make"].str.replace("-", " ").str.title()
        + ")"
    )

    num_ads_summary_plot = plot_num_ads_summary(num_ads_per_model)

    log_success = log_to_GA_list_of_items(
        event_name="explore_num_ads_summary_update_time",
        item_name="time_ms",
        list_of_items=[int((time.time() - start_time) * 1000)],
    )
    logger.debug(
        f"explore_num_ads_summary_update_time log success - {log_success}: {int((time.time() - start_time) * 1000)}"
    )

    return num_ads_summary_plot
