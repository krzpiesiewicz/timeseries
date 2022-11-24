import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from matplotlib import colors as mcolors
from plotly.subplots import make_subplots

from timeseries.plotting.pyplot_fig_with_vertical_subplots import (
    fig_with_vertical_subplots
)
from timeseries.utils.init_structs import init_if_none


def plot_hist(values, **kwargs):
    if "fig" in kwargs and kwargs["fig"] is not None:
        engine = (
            "pyplot" if "matplotlib" in f"{type(kwargs['fig'])}" else "plotly"
        )
    else:
        engine = kwargs["engine"] if "engine" in kwargs else "pyplot"
    kwargs.pop("engine", None)
    if engine == "pyplot":
        return pyplot_hist(values, **kwargs)
    elif engine == "plotly":
        return plotly_hist(values, **kwargs)
    else:
        raise Exception("Unknown plotting engine")
    return fig


def pyplot_hist(
        values,
        bins=100,
        alpha=0.5,
        label=None,
        name=None,
        fig=None,
        ax=None,
        title=None,
        subtitle=None,
        fontsize=13.5,
        title_fontsize=26,
        axs_heights_ratios=None,
        ax_height=None,
        xmargin=None,
        width=None,
        height=None,
        showgrid=False,
        **kwargs):
    plt.ioff()
    if fig is None and ax is None:
        plt.rcParams.update({"font.size": fontsize})
        fig, axs = fig_with_vertical_subplots(
            n_axes=1,
            axs_heights_ratios=axs_heights_ratios,
            ax_height=ax_height,
            xmargin=xmargin,
            width=width,
            height=height,
            fontsize=fontsize,
            title_fontsize=title_fontsize,
            title=title,
            subplots_titles=[subtitle],
            showgrid=showgrid,
        )
        ax = axs[0]
    if ax is None:
        ax = fig.get_axes()[0]
    if subtitle is not None:
        ax.set_title(subtitle)
    if label is None:
        label = name
    ax.hist(values, bins=bins, alpha=alpha, label=label, **kwargs)
    if label is not None:
        ax.legend()
    return fig


def plotly_hist(values, title=None, name=None, label=None, fig=None,
                width=None, height=None, fontsize=14, color=None,
                go_kwargs=None, trace_kwargs=None, layout_kwargs=None, **kwargs):
    go_kwargs = init_if_none(go_kwargs, dict)
    trace_kwargs = init_if_none(trace_kwargs, dict)
    layout_kwargs = init_if_none(layout_kwargs, dict)
    if type(values) is pd.Series:
        if name is None:
            name = label if label is not None else values.name
        values = values.values
    if fig is None:
        fig = make_subplots(rows=1, cols=1)
        if width is None:
            width = 1030
        if height is None:
            height = 700
        width = int(width * 0.9)
        height = int(height * 0.9)
        fig.update_layout(
            width=width,
            height=height,
            font_size=fontsize,
            title=title,
            title_x=0.5,
            title_yanchor="top",
            template="simple_white",
            **layout_kwargs,
        )
    hist = px.histogram(values, **kwargs)

    if "marker" in go_kwargs:
        marker = go_kwargs["marker"]
    else:
        marker = {}
        go_kwargs["marker"] = marker

    def get_go_hist(color=None):
        if color is not None:
            marker["color"] = color
        else:
            marker.pop("color", None)
        return go.Histogram(x=hist.data[0].x,
                            y=hist.data[0].y,
                            name=name,
                            **go_kwargs
                            )

    try:
        go_hist = get_go_hist(color=color)
    except ValueError as _:
        try:
            color = mcolors.to_hex(color)
            go_hist = get_go_hist(color=color)
        except BaseException as _:
            go_hist = get_go_hist()

    fig.add_trace(
        go_hist,
        secondary_y=False,
        **trace_kwargs
    )
    return fig
