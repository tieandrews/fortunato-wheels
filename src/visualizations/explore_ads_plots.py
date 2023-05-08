# Author: Ty Andrews
# March 13, 2023

import pandas as pd
import plotly.express as px


def hex_to_rgba(hex: str, opacity: float = 1.0):
    """Converts a hex color code to an rgba color code.

    Parameters
    ----------
    hex : str
        Hex color code.

    Returns
    -------
    str
        RGBA color code.
    """
    hex = hex.lstrip("#")
    hlen = len(hex)
    return (
        "rgba("
        + str(int(hex[: hlen // 3], 16))
        + ","
        + str(int(hex[hlen // 3 : 2 * hlen // 3], 16))
        + ","
        + str(int(hex[2 * hlen // 3 :], 16))
        + f",{opacity:.2f})"
    )
    fig = px.scatter(
        vehicles_df,
        x="year",
        y="price",
        color="manufacturer",
        opacity=0.5,
        trendline="lowess",
        # title="Price of used vehicles over time",
        labels={
            "year": "Year",
            "price": "Price",
            "manufacturer": "Manufacturer",
        },
        hover_name="model",
        hover_data=["odometer_km", "condition", "cylinders", "fuel", "transmission"],
        template="plotly_white",
        # width=800,
        height=300,
    )

    fig.update_layout(
        xaxis=dict(
            tickmode="linear",
            tick0=1990,
            dtick=5,
        ),
        yaxis=dict(
            tickmode="linear",
            tick0=0,
            dtick=10000,
        ),
        margin=dict(l=5, r=5, t=5, b=5),
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
    )

    return fig


def plot_vehicle_condition(vehicles_df):

    fig = (
        px.histogram(
            vehicles_df,
            y="condition",
            color="condition",
            text_auto=True,
            orientation="h",
            height=300,
            labels={
                "condition": "Vehicle Condition",
            },
            color_discrete_map={
                "new": "darkgreen",
                "like new": "lime",
                "excellent": "greenyellow",
                "good": "yellow",
                "fair": "orange",
                "salvage": "red",
            },
        )
        .update_layout(
            showlegend=False,
            xaxis_title="No. of Vehicles",
            margin=dict(l=5, r=5, t=5, b=5),
        )
        .update_yaxes(
            categoryorder="array",
            categoryarray=["salvage", "fair", "good", "excellent", "like new", "new"],
        )
    )

    return fig


def plot_odometer_histogram(vehicles):
    fig = px.histogram(
        vehicles,
        x="odometer_km",
        color="manufacturer",
        labels={
            "odometer_km": "Odometer (km)",
            "manufacturer": "Manufacturer",
        },
        hover_name="model",
        hover_data=["year", "condition", "cylinders", "fuel", "transmission"],
        template="plotly_white",
        height=300,
    )

    fig.update_layout(
        xaxis_range=[0, min(vehicles.odometer_km.max(), 600000)],
        legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99),
        yaxis_title="No. of Vehicles",
        margin=dict(l=5, r=5, t=5, b=5),
    )

    return fig
