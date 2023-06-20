import dash

dash.register_page(
    __name__,
    path="/about",
    title="Fortunato Wheels | About",
    name="Fortunato Wheels | About",
)

from dash import html
import dash_bootstrap_components as dbc

from src.logs import get_logger

# Create a custom logger
logger = get_logger(__name__)

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(style={"height": "20px"}),
                        html.H1("About Fortunato Wheels"),
                        html.P(
                            "Fortunato Wheels helps individuals find the best price on a used car. Our goal is to provide accurate and reliable information to you, our users, so that you can make informed, unbiassed decisions when purchasing a used car."
                        ),
                        html.Img(
                            src="https://images.unsplash.com/photo-1541443131876-44b03de101c5",
                            style={
                                "width": "100%",
                                "border-radius": "10px",
                                "box-shadow": "0px 0px 10px 0px rgba(0,0,0,0.75)",
                            },
                        ),
                        html.Div(style={"height": "20px"}),
                        html.P(
                            "We use machine learning in conjunction with more than 3 million ads to provide the most accurate and up-to-date information on used car prices. Our team of experts is constantly working to improve our algorithms and provide the best service possible to our customers."
                        ),
                        html.Div(style={"height": "20px"}),
                        html.Img(
                            src="https://images.unsplash.com/photo-1519681393784-d120267933ba",
                            style={
                                "width": "100%",
                                "border-radius": "10px",
                                "box-shadow": "0px 0px 10px 0px rgba(0,0,0,0.75)",
                            },
                        ),
                        html.Div(style={"height": "20px"}),
                    ],
                    width={"size": 10, "offset": 1},
                    md={"size": 8, "offset": 2},
                    lg={"size": 6, "offset": 3},
                )
            ]
        )
    ]
)
