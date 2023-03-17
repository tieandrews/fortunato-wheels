from dash import html
import dash_bootstrap_components as dbc
import dash

dash.register_page(__name__, path="/404")


layout = layout = dbc.Container(  # html.Div(
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
                        "Whoops! Looks like you're lost.",
                        style={"text-align": "center", "margin-top": "20px"},
                    ),
                    html.H4(
                        "404: Page Not Found",
                        style={
                            "text-align": "center",
                            "margin-top": "50px",
                            "margin-bottom": "50px",
                        },
                    ),
                ],
                width={"size": 12, "order": "last", "offset": 0},
                md={"size": 6, "order": "last", "offset": 3},
            )
        ),
    ],
    fluid=True,
)
