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

from logs import get_logger
from data.azure_blob_storage import AzureBlob

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
                    href="explore-ads",
                ),
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
                    style={"margin-right": "5px", "margin-left": "5px"},
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
                            html.Img(
                                src="assets/fortunato-wheels_logo_white.png",
                                height="40px",
                            )
                        ),
                        # dbc.Col(dbc.NavbarBrand("Fortunato WHe", className="ms-2")),
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
        start_time = time.time()
        azure_blob = AzureBlob()
        ad_price_summary = azure_blob.load_parquet(
            "processed/avg_price_summary.parquet"
        ).to_dict()
        mileage_summary = azure_blob.load_parquet(
            "processed/mileage_distribution_summary.parquet"
        ).to_dict()
        num_ads_summary = azure_blob.load_parquet(
            "processed/num_ads_summary.parquet"
        ).to_dict()
        makes_models = azure_blob.load_parquet(
            "processed/makes_models.parquet"
        ).to_dict()
        logger.debug(
            f"Loaded data from Azure Blob Storage in {time.time() - start_time} seconds"
        )
        return ad_price_summary, num_ads_summary, mileage_summary, makes_models
    else:
        logger.debug("Data already loaded, skipping")
        raise dash.exceptions.PreventUpdate


if __name__ == "__main__":
    app.run_server(debug=False, port=8050, host="0.0.0.0")
