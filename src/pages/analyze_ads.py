# Author: Ty Andrews
# March 13, 2023

import os
import sys

import dash

dash.register_page(
    __name__,
    title="Fortunato Wheels | Analyze Ads",
    name="Fortunato Wheels | Analyze Ads",
)

from dash import Dash, dcc, html, Input, Output, State, callback, ctx
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import dash_loading_spinners as dls
import pandas as pd
import time
import datetime as dt
import plotly.express as px
import plotly.graph_objects as go

from src.visualizations.utils import blank_placeholder_plot
from src.visualizations.analyze_ads_plots import (
    plot_price_prediction_by_year,
    plot_price_quality,
)
from src.pages.dash_styles import SIDEBAR_STYLE, CONTENT_STYLE
from src.logs import get_logger
from src.analytics.google_analytics import log_to_GA_list_of_items
from src.models.predict_price import predict_car_price

# Create a custom logger
logger = get_logger(__name__)

INVALID_MODELS = ["other"]
DEFAULT_MODELS = ["ghost", "model-x", "911", "m3"]
DEFAULT_MAKES = []

# Step 1: Dropdowns to select make and model
step1_layout = html.Div(
    [
        dbc.Col(
            [
                # center the H3 text
                html.H3(
                    "Step 1: Select a Vehicle Model",
                    style={"text-align": "center", "font-family": "Poppins"},
                ),
                dmc.Select(
                    label="Filter by Vehicle Make",
                    placeholder="All Makes",
                    id="analyze-make-select",
                    searchable=True,
                    clearable=True,
                    nothingFound="No matching makes found",
                    persistence=True,
                    persistence_type="session",
                    value=[],
                ),
                dmc.Select(
                    label="Select Model",
                    placeholder="No models selected.",
                    id="analyze-model-select",
                    searchable=True,
                    clearable=True,
                    persistence=True,
                    persistence_type="session",
                    nothingFound="No matching models found",
                    value=[],
                    required=True,
                ),
                # have a modal that opens if not all criteria are selected
                dbc.Modal(
                    [
                        dbc.ModalHeader("Missing Vehicle Model Selection"),
                        dbc.ModalBody("Please select a model before continuing."),
                    ],
                    id="step1-invalid-selection-modal",
                    centered=True,
                    is_open=False,
                ),
            ],
            width={"size": 12, "offset": 0},
            lg={"size": 6, "offset": 3},
        ),
    ]
)

# Step 2: Slider to select budget range
step2_layout = html.Div(
    [
        html.H3(
            "Step 2: Vehicle Info",
            style={"text-align": "center", "font-family": "Poppins"},
        ),
        # make input for vehicle year, mileage and wheel system optional
        dbc.Col(
            [
                dmc.NumberInput(
                    label="Advertised Price ($CAD)",
                    id="vehicle-price-input",
                    required=True,
                    persistence=True,
                    persistence_type="session",
                    min=0,
                    step=250,
                ),
                dmc.NumberInput(
                    label="Vehicle Year",
                    id="vehicle-year-input",
                    required=True,
                    persistence=True,
                    persistence_type="session",
                    min=1970,
                    max=dt.datetime.now().year,
                    step=1,
                ),
                dmc.NumberInput(
                    label="Odometer Reading (km)",
                    id="vehicle-mileage-input",
                    required=True,
                    persistence=True,
                    persistence_type="session",
                    min=0,
                    step=2000,
                ),
                dmc.Select(
                    label="(Optional) Vehicle Drive System",
                    description="If you don't know, leave this blank.",
                    placeholder="e.g. All Wheel Drive, etc.",
                    id="vehicle-wheel-system-input",
                    required=False,
                    persistence=True,
                    persistence_type="session",
                    clearable=True,
                    data=[
                        {"value": "AWD", "label": "All Wheel Drive"},
                        {"value": "FWD", "label": "Front Wheel Drive"},
                        {"value": "RWD", "label": "Rear Wheel Drive"},
                        {"value": "4WD", "label": "4 Wheel Drive"},
                        {"value": "4x4", "label": "4x4"},
                        {"value": "2WD", "label": "2 Wheel Drive"},
                    ],
                ),
                dbc.Modal(
                    [
                        dbc.ModalHeader(
                            "Missing one of Price, Year or Odometer Reading"
                        ),
                        dbc.ModalBody(
                            "Please select enter a price, year, mileage and odometer reading. Vehicle drive system is optional"
                        ),
                    ],
                    id="step2-invalid-selection-modal",
                    centered=True,
                    is_open=False,
                ),
            ],
            # on small screens make width full width, on large screens make width half
            width={"size": 12, "offset": 0},
            lg={"size": 6, "offset": 3},
        ),
    ]
)

# Step 3: Results page with plot
step3_layout = html.Div(
    children=[
        html.H3(
            "Step 3: Results", style={"text-align": "center", "font-family": "Poppins"}
        ),
        html.Div(id="trigger-results-update", children=True, style={"display": "none"}),
        html.Div(
            id="price-result",
            children=[
                dcc.Graph(
                    # put in blank placeholder plot until results are generated
                    id="temp-placeholder-plot",
                    figure=blank_placeholder_plot(),
                )
            ],
        ),
    ],
    id="price-analysis-result",
)

min_step = 0
max_step = 2
active = 0

stepper = html.Div(
    [
        dmc.Group(
            position="center",
            mt="xl",
            children=[
                dmc.Button("Back", id="back-basic-usage", variant="default"),
                dmc.Button("Next step", id="next-basic-usage"),
            ],
        ),
        html.Br(),
        dmc.Stepper(
            id="stepper-basic-usage",
            active=active,
            breakpoint="md",
            children=[
                dmc.StepperStep(
                    label="Step 1: Select a Vehicle",
                    icon=DashIconify(icon="mingcute:car-fill", height=20),
                    description="What vehicle are you looking at",
                    children=step1_layout,
                ),
                dmc.StepperStep(
                    label="Step 2: Vehicle Info",
                    description="Price, age, mileage, etc.",
                    icon=DashIconify(icon="ep:odometer", height=20),
                    children=step2_layout,
                ),
                dmc.StepperStep(
                    label="Step 3: Results",
                    description="Find out how good of a deal you're getting",
                    icon=DashIconify(icon="mdi:magic", height=20),
                    children=dls.Target(
                        children=step3_layout,
                        color="#3358FB",
                    ),
                    id="results-step",
                ),
                dmc.StepperCompleted(
                    children=dmc.Text(
                        "Completed, click back button to get to previous step",
                        align="center",
                    )
                ),
            ],
        ),
    ]
)


layout = html.Div(
    [
        dcc.Store(id="session-data", storage_type="session"),
        # create an invisible div to trigger on first load
        html.Div(id="analyze-first-load", children=True, style={"display": "none"}),
        dcc.Store(id="predict-makes-models-store", storage_type="session"),
        # put the stepper in a dbc.Col that is 12 width when small, 6 when lg
        dbc.Col(
            [
                html.Div(
                    [
                        html.Br(),
                        html.H1("Analyze an Ad", style={"text-align": "center"}),
                        html.Br(),
                        html.P(
                            "Figure out whether the car you're looking at is a steal or a ripoff using our AI model.",
                            style={"text-align": "center"},
                        ),
                        html.Hr(),
                    ]
                ),
                stepper,
                html.Div(
                    style={"height": "60vh"},
                ),
            ],
            width={"size": 12, "offset": 0},
            lg={"size": 6, "offset": 3},
        ),
    ]
)


# update the model select options based on the make select, price, age etc.
@callback(
    Output("analyze-model-select", "data"),
    Output("analyze-make-select", "data"),
    Output("predict-makes-models-store", "data"),
    [
        Input("analyze-first-load", "children"),
        Input("analyze-make-select", "value"),
        Input("analyze-make-select", "data"),
        Input("analyze-model-select", "value"),
        Input("analyze-model-select", "data"),
    ],
    [
        State("predict-makes-models-store", "data"),
    ],
)
def update_filter_options(
    _first_load,
    make_values,
    make_options,
    model_values,
    model_options,
    predict_makes_models_store,
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
    makes_models_store : dict
        Dictionary of makes and models.


    Returns
    -------
    make_options : dict
        List of all available makes and always has all makes available with number of ads
        for each make in the 'label' field.
    model_options : dict
        List of all available models and is updated based on the makes selected with number of ads
        for each model in the 'label' field.
    """
    start_time = time.time()

    if predict_makes_models_store is None:
        predict_makes_models_store = pd.read_csv(
            os.path.join("data", "raw", "prediction-vehicle-make-model-config.csv")
        ).to_dict()

    make_model_df = pd.DataFrame.from_dict(predict_makes_models_store, orient="columns")

    # if make options is None, then we set it to all makes and always allow all makes selectable
    if make_options is None:
        make_options = make_model_df.make.unique().tolist()
        make_options.sort()
        models_list = (
            make_model_df.query("model not in @INVALID_MODELS").model.unique().tolist()
        )

        make_options = [
            {
                "label": f'{make.replace("-", " ").title()}',
                "value": make,
            }
            for make in make_options
        ]

    # if model options is not initialized or no make is selected, then we set it to all models
    # if (model_options is None) or (len(make_values) == 0):
    if make_values is None:
        models_list = (
            make_model_df.query("model not in @INVALID_MODELS").model.unique().tolist()
        )
        models_list.sort()
    # if a make is selected then retrun model_options only of that make but
    # keep the current model_values visible in the list
    elif len(make_values) > 0:
        models_list = (
            make_model_df.query("make == @make_values & model not in @INVALID_MODELS")
            .model.unique()
            .tolist()
        )
        models_list.sort()

    # create the model options for the drop down including number of ads per model
    model_options = [
        {
            "label": f'{model.replace("-", " ").title()}',
            "value": f'{model.replace("-", " ").title()}',
        }
        for model in models_list
    ]

    log_success = log_to_GA_list_of_items(
        event_name="analyze_update_filters_time",
        item_name="time_ms",
        list_of_items=[int((time.time() - start_time) * 1000)],
    )
    logger.debug(
        f"explore_update_filters_time log success - {log_success}: {int((time.time() - start_time) * 1000)}"
    )
    return model_options, make_options, predict_makes_models_store


@callback(
    # update next button to be disabled when step ==2
    Output("stepper-basic-usage", "active"),
    Output("next-basic-usage", "disabled"),
    Output("step1-invalid-selection-modal", "is_open"),
    Output("step2-invalid-selection-modal", "is_open"),
    Input("back-basic-usage", "n_clicks"),
    Input("next-basic-usage", "n_clicks"),
    State("analyze-model-select", "value"),
    State("vehicle-price-input", "value"),
    State("vehicle-year-input", "value"),
    State("vehicle-mileage-input", "value"),
    State("stepper-basic-usage", "active"),
    prevent_initial_call=True,
)
def update(back, next_, model, price, year, mileage, current):
    button_id = ctx.triggered_id

    step = current if current is not None else active

    # open the "step1-invalid-selection-modal" modal if no model is selected in step 1
    if (step == 0) & (button_id == "next-basic-usage") and (model is None):
        return step, False, True, False

    # open the "step2-invalid-selection-modal" modal if no price, year, mileage or wheel system is selected in step 2
    if (step == 1) & (button_id == "next-basic-usage") and (
        price == "" or year == "" or mileage == ""
    ):
        return step, False, False, True

    next_button_disabled = False
    if button_id == "back-basic-usage":
        step = step - 1 if step > min_step else step
    elif step == 2:
        # output an empty div to trigger the results update callback
        step = step + 1 if step < max_step else step
    else:
        step = step + 1 if step < max_step else step

    if step == 2:
        next_button_disabled = True

    return step, next_button_disabled, False, False


@callback(
    Output("price-result", "children"),
    Input("stepper-basic-usage", "active"),
    State("analyze-model-select", "value"),
    State("vehicle-price-input", "value"),
    State("vehicle-year-input", "value"),
    State("vehicle-mileage-input", "value"),
    State("vehicle-wheel-system-input", "value"),
    State("makes-models-store", "data"),
)
def generate_price_results(
    current, model, price, year, mileage, wheel_system, makes_models_store
):
    if current != 2:
        raise dash.exceptions.PreventUpdate
    else:
        makes_models_df = pd.DataFrame.from_dict(makes_models_store, orient="columns")

        model_formatted = model.lower().replace(" ", "-")

        make = makes_models_df.query("model == @model_formatted").make.values[0].title()

        age_at_posting = dt.datetime.now().year - year

        mileage_per_year = round(mileage / age_at_posting, 0)

        if wheel_system is None:
            wheel_system = "fwd"

        pred_price, upper_ci, lower_ci = predict_car_price(
            model=model,
            make=make,
            age_at_posting=age_at_posting,
            mileage_per_year=mileage_per_year,
            wheel_system=wheel_system,
        )

        # generate predictions for a range of years above/below year
        # and plot the results
        price_year_results = pd.DataFrame(
            columns=["year", "pred_price", "upper_ci", "lower_ci"]
        )
        for y in range(year - 5, year + 5):
            if y > dt.datetime.now().year:
                continue

            age_at_posting = dt.datetime.now().year - y

            if y == dt.datetime.now().year:
                mileage_per_year = mileage
            else:
                mileage_per_year = round(mileage / age_at_posting, 0)

            if wheel_system is None:
                wheel_system = "fwd"

            p, up_ci, low_ci = predict_car_price(
                model=model,
                make=make,
                age_at_posting=age_at_posting,
                mileage_per_year=mileage_per_year,
                wheel_system=wheel_system,
            )

            price_year_results = pd.concat(
                [
                    price_year_results,
                    pd.DataFrame(
                        {
                            "year": [y],
                            "pred_price": [p],
                            "upper_ci": [up_ci],
                            "lower_ci": [low_ci],
                        }
                    ),
                ]
            )

        year_results_plot = plot_price_prediction_by_year(
            year, price, price_year_results
        )

        # plot the price vs. quality plot
        price_quality_plot = plot_price_quality(price, pred_price, upper_ci, lower_ci)

        results_layout = html.Div(
            [
                html.Br(),
                dcc.Graph(
                    id="price-quality-results-plot",
                    figure=price_quality_plot,
                    config={
                        "displayModeBar": False,
                    },
                ),
                html.Br(),
                html.Div(
                    [
                        html.H5(
                            f"Vehicle Info:",
                            # make sure the dash template font is used
                            style={
                                "text-align": "center",
                                "font-weight": "bold",
                                "font-family": "Poppins",
                            },
                        ),
                        html.Hr(),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H6(
                                            # add horizantal white space after the word Mileage
                                            "Mileage:",
                                            style={
                                                "text-align": "right",
                                                "margin-right": "10px",
                                            },
                                        ),
                                        html.H6(
                                            "Year:",
                                            style={
                                                "text-align": "right",
                                                "margin-right": "10px",
                                            },
                                        ),
                                        html.H6(
                                            "Wheel System:",
                                            style={
                                                "text-align": "right",
                                                "margin-right": "10px",
                                            },
                                        ),
                                    ],
                                    style={"width": "50%", "display": "inline-block"},
                                ),
                                html.Div(
                                    [
                                        html.H6(
                                            f"{mileage:,.0f} km",
                                            style={"text-align": "left"},
                                        ),
                                        html.H6(
                                            f"{year}",
                                            style={"text-align": "left"},
                                        ),
                                        html.H6(
                                            f"{wheel_system.upper()}",
                                            style={"text-align": "left"},
                                        ),
                                    ],
                                    style={"width": "50%", "display": "inline-block"},
                                ),
                            ],
                            style={"text-align": "center"},
                        ),
                    ]
                ),
                html.Hr(),
                html.H5(
                    f"Predicted Price vs. Year for a {make.title()} {model.title()}"
                ),
                dcc.Graph(
                    id="price-year-results-plot",
                    figure=year_results_plot,
                    config={
                        "displayModeBar": False,
                    },
                ),
            ]
        )

    search_str = f"{make}_{model}_{year}_{mileage}_{wheel_system}_{price}"

    log_success = log_to_GA_list_of_items(
        event_name="analyze_ads_search_str",
        item_name="search_str",
        list_of_items=[search_str],
    )

    return results_layout
