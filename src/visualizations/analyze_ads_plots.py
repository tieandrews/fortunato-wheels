# Author: Ty Andrews
# Date: 2023-06-06

import os, sys

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

pio.templates["explore_ads"] = go.layout.Template(
    layout=go.Layout(
        font_family="Poppins",
    )
)
pio.templates.default = "plotly+explore_ads"


def plot_price_prediction_by_year(year, price, price_year_results):
    year_results_plot = px.line(
        price_year_results,
        x="year",
        y=["pred_price"],
        text=price_year_results["pred_price"].apply(lambda x: f"${x/1000:,.0f}k"),
        labels={
            "year": "Year",
            "value": "Price ($CAD)",
            "variable": "Price",
            "pred_price": "Predicted Price",
        },
        color_discrete_map={
            "pred_price": "#3358FB",
        },
        markers=True,
        line_shape="spline",
    )

    # add grey lines above and below the predicted price ci's and fill in the area
    year_results_plot.add_traces(
        [
            go.Scatter(
                x=price_year_results["year"],
                y=price_year_results["lower_ci"],
                line=dict(color="rgba(51, 88, 251, 0.35)", width=0, dash="dash"),
                fill=None,
                mode="lines",
                legendgroup="lower_ci",
                line_shape="spline",
                showlegend=False,
            ),
            go.Scatter(
                x=price_year_results["year"],
                y=price_year_results["upper_ci"],
                line=dict(color="rgba(51, 88, 251, 0.35)", width=0, dash="dash"),
                fill="tonexty",
                mode="lines",
                line_shape="spline",
                name="95% CI",
            ),
        ]
    )

    year_results_plot.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),
        margin=dict(l=0, r=0, t=50, b=0),
    )
    year_results_plot.update_xaxes(showgrid=False)
    year_results_plot.update_yaxes(showgrid=False)
    year_results_plot.update_traces(
        hovertemplate="<b>%{x}</b><br>" + "%{y:$,.0f}<extra></extra>",
        textposition="bottom right",
        textfont_size=14,
    )

    # set plot limits to min/max year
    year_results_plot.update_xaxes(
        range=[price_year_results["year"].min(), price_year_results["year"].max()]
    )

    # add a horizontal line for their inputted price colored green
    year_results_plot.add_hline(
        y=price,
        line_width=3,
        line_dash="dot",
        line_color="#021169",
        annotation_text=f"Your Price: ${price:,.0f}",
        annotation_position="top right",
        annotation_font_color="#021169",
        annotation_font_size=18,
    )

    # add a single plotted point for their inputted year and predicted price
    year_results_plot.add_trace(
        go.Scatter(
            x=[year],
            y=[price],
            mode="markers",
            marker=dict(
                color="#021169",
                size=10,
                line=dict(
                    color="#021169",
                    width=2,
                ),
            ),
            name="Your Price",
            showlegend=True,
        )
    )

    return year_results_plot


def plot_price_quality(price, predicted_price, upper_ci, lower_ci):
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=[lower_ci - 50],
            y=[0.5, 0.5],
            text=["Great<br>Deal", "Rip<br>Off"],
            mode="text",
            # increase font size
            textfont=dict(
                size=24,
            ),
            # align text on the bottom
            textposition="middle left",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[upper_ci + 50],
            y=[0.5],
            text=["Rip<br>Off"],
            mode="text",
            # increase font size
            textfont=dict(
                size=24,
            ),
            # align text on the bottom
            textposition="middle right",
        )
    )

    # draw a red rectangle from the predicted price to upper ci
    fig.add_shape(
        type="rect",
        xref="x",
        yref="y",
        x0=predicted_price,
        y0=0.25,
        x1=upper_ci,
        y1=0.75,
        fillcolor="red",
        opacity=0.5,
        layer="below",
        line_width=0,
    )

    # draw a green rectangle from the predicted price to lower ci
    fig.add_shape(
        type="rect",
        xref="x",
        yref="y",
        x0=predicted_price,
        y0=0.25,
        x1=lower_ci,
        y1=0.75,
        fillcolor="green",
        opacity=0.5,
        layer="below",
        line_width=0,
    )

    # add a vertical green line at the lower ci that goes from 0.25 to 0.80
    fig.add_shape(
        type="line",
        xref="x",
        yref="y",
        x0=lower_ci,
        y0=0.25,
        x1=lower_ci,
        y1=0.75,
        line=dict(
            color="green",
            width=2,
        ),
    )

    # add the lower ci value right above the vertical line
    fig.add_trace(
        go.Scatter(
            x=[lower_ci],
            y=[0.23],
            text=[f"${lower_ci/1000:,.1f}k"],
            mode="text",
            textfont=dict(
                size=20,
            ),
            textposition="bottom center",
        )
    )

    # add a vertical green line at the lower ci that goes from 0.25 to 0.80
    fig.add_shape(
        type="line",
        xref="x",
        yref="y",
        x0=upper_ci,
        y0=0.25,
        x1=upper_ci,
        y1=0.75,
        line=dict(
            color="red",
            width=2,
        ),
    )

    # add the lower ci value right above the vertical line
    fig.add_trace(
        go.Scatter(
            x=[upper_ci],
            y=[0.23],
            text=[f"${upper_ci/1000:,.1f}k"],
            mode="text",
            textfont=dict(
                size=20,
            ),
            textposition="bottom center",
        )
    )

    # add the lower ci value right above the vertical line
    fig.add_trace(
        go.Scatter(
            x=[predicted_price],
            y=[0.23],
            text=[f"${predicted_price/1000:,.1f}k<br>Predicted Price"],
            mode="text",
            textfont=dict(
                size=20,
            ),
            textposition="bottom center",
        )
    )

    # add the lower ci value right above the vertical line
    fig.add_trace(
        go.Scatter(
            x=[price],
            y=[0.80],
            text=[f"Your Price:<br>${price/1000:,.1f}k"],
            mode="text",
            textfont=dict(
                size=26,
            ),
            textposition="top center",
        )
    )

    # add a vertical green line at the lower ci that goes from 0.25 to 0.80
    fig.add_shape(
        type="line",
        xref="x",
        yref="y",
        x0=price,
        y0=0.25,
        x1=price,
        y1=0.80,
        line=dict(
            color="blue",
            width=4,
            dash="dot",
        ),
    )

    # remove all grid and background lines and color
    fig.update_layout(
        showlegend=False,
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            ticks="",
            showticklabels=False,
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            ticks="",
            showticklabels=False,
        ),
        margin=dict(l=0, r=0, t=40, b=0),
        plot_bgcolor="white",
        # set width and height of the figure
        # width=900,
        height=300,
    )
    offset_ratio = 0.2
    # set x limit to be above the upper ci and below the lower ci
    fig.update_xaxes(
        range=[
            min(lower_ci, price) - predicted_price * offset_ratio,
            max(upper_ci, price) + predicted_price * offset_ratio,
        ],
        fixedrange=True,
    )

    # set y limit to be between 0 and 1
    fig.update_yaxes(range=[-0.1, 1.5], fixedrange=True)

    title, subtitle = determine_price_quality_title(
        price, predicted_price, upper_ci, lower_ci
    )

    # add a title
    fig.update_layout(
        title={
            "text": title,
            # add subtitle
            "y": 0.95,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
        },
        # add subtitle
        annotations=[
            dict(
                x=0.5,
                y=0.97,
                xref="paper",
                yref="paper",
                text=subtitle,
                showarrow=False,
                font=dict(
                    size=16,
                ),
            )
        ],
        title_font_size=36,
    )

    return fig


def determine_price_quality_title(price, predicted_price, upper_ci, lower_ci):
    # the ratio either side of predicted price to consider ok deal
    center_ratio = 0.65

    lower_deal_limit = predicted_price - center_ratio * (predicted_price - lower_ci)
    upper_deal_limit = predicted_price + center_ratio * (upper_ci - predicted_price)

    if price < lower_ci:
        return "🔥Smoking Deal!🔥", "Get it while it's hot!"
    elif price < lower_deal_limit:
        return "Great Deal 😲", "That's a good price!"
    elif (price >= lower_deal_limit) & (price < upper_deal_limit):
        return "Fair Price👌", "It's in the right ball park."
    elif (price >= upper_deal_limit) & (price < upper_ci):
        return "Not a Great Deal 🧐", "It's a little pricey."
    elif price >= upper_ci:
        return (
            "Seems like a Rip Off 🤡",
            "Watch out for clowns, you might be getting ripped off!",
        )
    else:
        return (
            "Somethings Gone Wrong!",
            "Maybe go touch grass for a minute while we sort this out...",
        )
