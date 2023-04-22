"""
 # @ Create Time: 2023-03-13 11:07:55.038078
"""

import dash
from dash import Dash, dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify

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
                href="https://plotly.com",
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
        navbar,
        dbc.Container(
            children=[dash.page_container],
            fluid=True,
        ),
    ],
)

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


if __name__ == "__main__":
    app.run_server(debug=False, port=8050, host="0.0.0.0")
