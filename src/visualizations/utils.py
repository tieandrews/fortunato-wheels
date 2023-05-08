# Author: Ty Andrews
# Date: 2023-05-06

import plotly.express as px


def blank_placeholder_plot(background_color="white", height=None, width=None):
    """Creates an empty plot to be used on page load before callbacks complete,
    allows page load and all figure updates/data loading to be managed in callbacks
    without empty plots being shown.

    Args:
        background_color (str, optional): What color the background should match to be "invisible" until updated.
                                         Defaults to "white".

    Returns:
        px.Scatter : Empty plot with lines removed and formatting updated to be blank.
    """

    blank_plot = px.scatter(x=[0, 1], y=[0, 1], height=height, width=width)
    blank_plot.update_xaxes(showgrid=False, showticklabels=False, visible=False)
    blank_plot.update_yaxes(showgrid=False, showticklabels=False, visible=False)

    blank_plot.update_traces(marker=dict(color=background_color))

    blank_plot.layout.plot_bgcolor = background_color
    blank_plot.layout.paper_bgcolor = background_color
    return blank_plot
