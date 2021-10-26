import matplotlib.pyplot as plt
import numpy as np

from timeseries.plotting.fig_with_vertical_subplots import (
    fig_with_vertical_subplots
)
from timeseries.analysis import acf, pacf


def __plot_stat_fun__(stat_fun, *args, kind_of_statistics=None,
                      plot_params={}, **kwargs):
    plot_params = plot_params.copy()
    for param in ["zero", "label", "fig", "ax", "title", "subtitle", "width",
                  "height", "ax_height", "axs_heights_ratios", "fontsize",
                  "title_fontsize", "figsize", "xmargin", "color",
                  "showgrid", "conf_alpha"]:
        if param in kwargs:
            plot_params[param] = kwargs[param]
            kwargs.pop(param)

    res = stat_fun(*args, **kwargs)
    if type(res) is tuple:
        res = list(res)
    else:
        res = [res]
    assert len(res) <= 2
    return plot_stats(*res, kind_of_statistics=kind_of_statistics,
                      **plot_params)


def plot_acf(*args, plot_params={}, **kwargs):
    return __plot_stat_fun__(acf, *args, kind_of_statistics="ACF",
                             plot_params=plot_params, **kwargs)


def plot_pacf(*args, plot_params={}, **kwargs):
    return __plot_stat_fun__(pacf, *args, kind_of_statistics="PACF",
                             plot_params=plot_params, **kwargs)


def plot_stats(*args, **kwargs):
    if "fig" in kwargs and kwargs["fig"] is not None:
        engine = (
            "pyplot" if "matplotlib" in f"{type(kwargs['fig'])}" else "plotly"
        )
    else:
        engine = kwargs["engine"] if "engine" in kwargs else "pyplot"
    kwargs.pop("engine", None)
    if engine == "pyplot":
        return pyplot_stats(*args, **kwargs)
    elif engine == "plotly":
        raise Exception("Plottly not supported by this function yet")
    else:
        raise Exception("Unknown plotting engine")


def pyplot_stats(
        values,
        conf_intvs=None,
        xs=None,
        zero=True,
        color=None,
        alpha=1.0,
        conf_alpha=0.25,
        kind_of_statistics=None,
        label=None,
        fig=None,
        ax=None,
        title=None,
        subtitle=None,
        fontsize=14,
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
        if title is None:
            if kind_of_statistics == "ACF":
                title = "Autocorrelation"
            if kind_of_statistics == "PACF":
                title = "Partial Autocorrelation"
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

    if xs is None:
        xs = np.arange(not zero, len(values), dtype=float)
    if not zero:
        values = values[1:]
    ymin = np.vectorize(lambda x: min(x, 0.0))(values)
    ymax = np.vectorize(lambda x: max(x, 0.0))(values)
    if "markersize" not in kwargs:
        kwargs["markersize"] = 5
    ax.plot(xs, values, "o", label=label, color=color, alpha=alpha, **kwargs)
    color = ax.lines[-1].get_color()
    if label is not None:
        ax.legend()
    ax.vlines(
        xs,
        ymin,
        ymax,
        colors=None,
        linestyles="solid",
        label="",
    )

    ax.margins(0.05)
    ax.axhline()

    if conf_intvs is not None:
        conf_intvs = conf_intvs[1:]
        if xs[0] == 0:
            xs = xs[1:]
            values = values[1:]
        xs[0] -= 0.5
        xs[-1] += 0.5
        ax.fill_between(
            xs, conf_intvs[:, 0] - values, conf_intvs[:, 1] - values,
            alpha=conf_alpha,
            color=color,
        )
    return fig
