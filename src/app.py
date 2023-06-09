"""
 # @ Create Time: 2023-03-13 11:07:55.038078
"""
import sys, os
import dash
from dash import Dash, dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
from dash import dcc
import dash_mantine_components as dmc
from dash_iconify import DashIconify
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

from src.logs import get_logger
from src.data.azure_blob_storage import AzureBlob
from src.analytics.google_analytics import custom_event_to_GA

# Create a custom logger
logger = get_logger(__name__)

external_stylesheets = [
    dbc.themes.BOOTSTRAP,
    "https://fonts.google.com/specimen/Poppins",
]

app = dash.Dash(
    __name__,
    use_pages=True,
    external_stylesheets=external_stylesheets,
    title="fortunato-wheels",
)

navbar_logo = html.Img(
    src="/assets/fortunato-wheels_logo_white.png",
    height="40px",
    # style={"margin-top": "10px", "margin-bottom": "10px"},
)

logo = html.Img(
    src="/assets/fortunato-wheels_logo_white.png",
    height="40px",
    style={"margin-top": "10px", "margin-bottom": "10px"},
    # on medium screen hide logo
    className="d-none d-lg-block",
)

server = app.server

nav_buttons = dbc.Row(
    [
        dbc.Col(
            children=[
                dmc.Anchor(
                    dmc.Button(
                        "Home",
                        variant="gradient",
                        gradient={"from": "indigo", "to": "cyan"},
                        leftIcon=[
                            DashIconify(
                                icon="material-symbols:home-outline-rounded",
                                width=25,
                            )
                        ],
                        style={
                            "margin-right": "5px",
                            "margin-left": "5px",
                        },
                    ),
                    href="/",
                ),
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
                        style={"margin-right": "5px", "margin-left": "5px"},
                    ),
                    href="/explore-ads",
                ),
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
                        style={"margin-right": "5px", "margin-left": "5px"},
                    ),
                    href="/analyze-ads",
                ),
                dmc.Anchor(
                    dmc.Button(
                        "Blog",
                        leftIcon=[
                            DashIconify(
                                icon="mdi:learn-outline",
                                width=25,
                            )
                        ],
                        variant="gradient",
                        gradient={"from": "indigo", "to": "cyan"},
                        style={"margin-right": "5px", "margin-left": "5px"},
                    ),
                    href="/blog",
                ),
                dmc.Anchor(
                    dmc.Button(
                        "About",
                        leftIcon=[
                            DashIconify(
                                icon="mingcute:information-line",
                                width=25,
                            )
                        ],
                        variant="gradient",
                        gradient={"from": "indigo", "to": "cyan"},
                        style={"margin-right": "5px", "margin-left": "5px"},
                    ),
                    href="/about",
                ),
            ],
            width="auto",
            align="center",
        ),
    ],
    className="g-0 flex-nowrap ms-auto mt-3 mt-md-0",  #
    align="center",
)

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(
                            navbar_logo,
                        ),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="https://www.fortunatowheels.com",
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
                nav_buttons,
                id="navbar-collapse",
                is_open=False,
                navbar=True,
            ),
        ]
    ),
    color="primary",
    dark=True,
)

# About page link
about_link = dbc.Col(
    dbc.NavLink("About", href="/about", style={"color": "white"}),
    width={"size": 12},
    lg={"size": 4},
)

footer = dbc.Navbar(
    [
        dbc.Col(logo, width=0, lg=4),
        dbc.Col(
            "Copyright " + "\u00A9" + " 2023 Fortunato Wheels. All Rights Reserved",
            style={"textAlign": "center", "font-size": "0.8rem", "color": "white"},
            width=12,
            md=4,
        ),
        dbc.Col(
            [
                dbc.NavLink(
                    "(BETA) Analyze an Ad",
                    href="/analyze-ads",
                    style={"color": "white"},
                ),
                dbc.NavLink(
                    "Explore Past Ads",
                    href="/explore-ads",
                    style={"color": "white"},
                ),
                dbc.NavLink(
                    "Home",
                    href="/",
                    style={"color": "white"},
                ),
                dbc.NavLink(
                    "Blog",
                    href="/blog",
                    style={"color": "white"},
                ),
                dbc.NavLink(
                    "About",
                    href="/about",
                    style={"color": "white"},
                ),
            ],
            width=12,
            lg=4,
            style={"textAlign": "center"},
        ),
    ],
    color="secondary",
    dark=True,
)

# put navbar in standard html.Div to till width of page
app.layout = html.Div(
    children=[
        html.Div(id="first-load", children=True, style={"display": "none"}),
        dcc.Store(id="price-summary-store", storage_type="session"),
        dcc.Store(id="num-ads-summary-store", storage_type="session"),
        dcc.Store(id="mileage-summary-store", storage_type="session"),
        dcc.Store(id="makes-models-store", storage_type="session"),
        html.Div(
            className="div-app",
            id="div-app",
            children=[
                navbar,
                dbc.Container(
                    children=[dash.page_container],
                    fluid=True,
                ),
                footer,
            ],
        ),
    ],
)

# Setup google analytics connection: https://aticoengineering.com/shootin-trouble-in-data-science/google-analytics-in-dash-web-apps/
app.index_string = """<!DOCTYPE html>
<html>
<head>

<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-CKDC8LRCRB"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-CKDC8LRCRB');
</script>

{%metas%}
<title>{%title%}</title>
{%favicon%}
{%css%}
</head>
<body>
{%app_entry%}
<footer>
{%config%}
{%scripts%}
{%renderer%}
</footer>
</body>
</html>
"""


# add callback for toggling the collapse on small screens
@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


# callback to load data on first load in the background
@callback(
    Output("price-summary-store", "data"),
    Output("num-ads-summary-store", "data"),
    Output("mileage-summary-store", "data"),
    Output("makes-models-store", "data"),
    Input("first-load", "children"),
    [
        State("price-summary-store", "data"),
        State("num-ads-summary-store", "data"),
        State("mileage-summary-store", "data"),
    ],
)
def load_data(first_load, price_summary, num_ads_summary, mileage_summary):
    # if any summary is None, then we need to load data
    if not price_summary or not num_ads_summary or not mileage_summary:
        azure_blob = AzureBlob()

        # placeholder until proper gtag id's can be extracted
        client_id = str(time.time_ns())

        start_time = time.time()
        ad_price_summary = azure_blob.load_parquet(
            "processed/avg_price_summary.parquet"
        ).to_dict()
        custom_event_to_GA(
            client_id,
            "price_data_load_time",
            {"time_ms": round((time.time() - start_time) * 1000, 0)},
        )
        logger

        start_time = time.time()
        mileage_summary = azure_blob.load_parquet(
            "processed/mileage_distribution_summary.parquet"
        ).to_dict()
        custom_event_to_GA(
            client_id,
            "mileage_data_load_time",
            {"time_ms": round((time.time() - start_time) * 1000, 0)},
        )

        start_time = time.time()
        num_ads_summary = azure_blob.load_parquet(
            "processed/num_ads_summary.parquet"
        ).to_dict()
        custom_event_to_GA(
            client_id,
            "num_ads_data_load_time",
            {"time_ms": round((time.time() - start_time) * 1000, 0)},
        )

        start_time = time.time()
        makes_models = azure_blob.load_parquet(
            "processed/makes_models.parquet"
        ).to_dict()
        custom_event_to_GA(
            client_id,
            "makes_models_data_load_time",
            {"time_ms": round((time.time() - start_time) * 1000, 0)},
        )

        logger.debug(
            f"Loaded data from Azure Blob Storage in {time.time() - start_time} seconds"
        )

        custom_event_to_GA(time.time_ns(), "summary_data_load_time", {})

        return ad_price_summary, num_ads_summary, mileage_summary, makes_models
    else:
        logger.debug("Data already loaded, skipping")
        raise dash.exceptions.PreventUpdate


if __name__ == "__main__":
    app.run_server(debug=False, port=8050, host="0.0.0.0")
