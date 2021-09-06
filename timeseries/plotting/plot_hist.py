import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


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
        name=None,
        fig=None,
        title=None,
        fontsize=14,
        width=900,
        height=500,
        **kwargs):
    plt.ioff()
    plt.rcParams.update({"font.size": fontsize})
    if fig is None:
        fig = plt.figure()
        axs = [fig.subplots(1)]
    else:
        axs = fig.get_axes()
    if title is not None:
        fig.suptitle(title, fontsize=26)
    axs[0].hist(values, bins=bins, alpha=alpha, label=name, **kwargs)
    if name is not None:
        axs[0].legend()
    dpi = fig.get_dpi()
    c = 1
    fig.set_size_inches((int(width / dpi * c), int(height / dpi * c)))
    return fig


def plotly_hist(values, title=None, name=None, fig=None, width=None,
                height=None, fontsize=14, **kwargs):
    if type(values) is pd.Series:
        if name is None:
            name = values.name
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
        )
    hist = px.histogram(values, **kwargs)
    fig.add_trace(
        go.Histogram(x=hist.data[0].x,
                     y=hist.data[0].y,
                     name=name,
                     ),
        secondary_y=False
    )
    return fig