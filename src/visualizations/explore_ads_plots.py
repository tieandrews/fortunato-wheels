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


def plot_vehicle_prices_summary(price_summary_df):
    """Plots the price of selected vehicles by their age at posting.

    Parameters
    ----------
    price_summary_df : pd.DataFrame
        DataFrame with columns `age` and remaining columns as vehicle model names.

    Returns
    -------
    plotly.graph_objects.Figure
        Plotly figure object.
    """
    fig = px.scatter(
        price_summary_df,
        x="age",
        y="price",
        color="model",
        trendline="lowess",
        labels={
            "age": "Age of Vehicle (years)",
            "price": "Avg. Price ($CAD)",
            "model": "Vehicle Model",
        },
        height=300,
    ).update_xaxes(
        range=[price_summary_df["age"].min() - 0.1, price_summary_df["age"].max() + 0.1]
    )

    fig.update_layout(
        xaxis=dict(
            tickmode="linear",
            tick0=0,
            dtick=1,
        ),
        margin=dict(l=5, r=5, t=5, b=5),
        legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99),
        hovermode="x unified",
    )

    return fig


def plot_mileage_distribution_summary(mileage_summary_df):
    """Plots the mileage of selected vehicles by their age at posting.

    Parameters
    ----------
    mileage_summary_df : pd.DataFrame
        DataFrame with columns `mileage_per_year` and remaining columns as vehicle model names.

    Returns
    -------
    plotly.graph_objects.Figure
        Plotly figure object.
    """
    fig = (
        px.line(
            mileage_summary_df,
            x="yearly_mileage_range",
            y="percent_of_vehicles",
            color="model",
            # trendline="lowess",
            labels={
                "yearly_mileage_range": "Avg. Mileage Per Year (km)",
                "percent_of_vehicles": "Percent of Vehicles (%)",
                "model": "Vehicle Model",
            },
            height=300,
        )
        .update_xaxes(
            range=[-0.1, mileage_summary_df["yearly_mileage_range"].max() + 0.1]
        )
        .update_yaxes(range=[0, mileage_summary_df["percent_of_vehicles"].max() + 0.04])
    )

    fig.update_layout(
        margin=dict(l=5, r=5, t=5, b=5),
        legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99),
        # yaxis_ticksuffix="%",  # add percent sign to y-axis
        yaxis_tickformat=".0%",
        hovermode="x unified",
    )

    # inspiration for filled area below line: https://stackoverflow.com/questions/69331683/how-to-fill-in-the-area-below-trendline-in-plotly-express-scatterplot
    # opacitiy in rgba values fix from here: https://stackoverflow.com/questions/35213766/rgb-transparent-colors-in-plotly-and-r
    color_list = []
    for trace in fig.data:
        x = trace["x"]
        y = trace["y"]
        color = hex_to_rgba(trace["line"]["color"], opacity=0.1)
        color_list.append(hex_to_rgba(trace["line"]["color"]))
        fig.add_trace(
            go.Scatter(
                x=x,
                y=y,
                line_color=color,
                fillcolor=color,
                mode="lines",
                opacity=0.1,  # this is just for the line
                fill="tozeroy",
                showlegend=False,
            )
        )
    # add a vertical line at the mean milealge for each trace, use colors from traces before,
    # assumed they are ordered the same
    # color_index = 0
    # # to evaluate mean at upper bound of step sizes, add step size to upper bound
    # yearly_mileage_range_step_size = (
    #     mileage_summary_df["yearly_mileage_range"].diff().iloc[1]
    # )
    # for model in mileage_summary_df["model"].unique():
    #     mean_mileage = (
    #         mileage_summary_df.query("model == @model")
    #         .eval(
    #             "mean_mileage_per_year = (yearly_mileage_range + @yearly_mileage_range_step_size) * percent_of_vehicles"
    #         )
    #         .eval("mean_mileage_per_year = mean_mileage_per_year.sum()")
    #         .iloc[0]["mean_mileage_per_year"]
    #     )
    #     fig.add_vline(
    #         x=mean_mileage,
    #         line_width=3,
    #         line_dash="dot",
    #         line_color=color_list[color_index],
    #         annotation_text=f"{mean_mileage/1000:.1f}k",
    #         annotation_position="top left",
    #         annotation_font_color=color_list[color_index],
    #     )
    #     color_index += 1

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
