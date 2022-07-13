import matplotlib.pyplot as plt
import numpy as np

from timeseries.plotting.pyplot_ax_settings import ax_params, ax_settings
from timeseries.plotting.pyplot_fig_with_vertical_subplots import (
    fig_with_vertical_subplots
)


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
        conf_intvs_xs=None,
        std=None,
        std_xs=None,
        fill_along_axis=True,
        fill_only_positive=False,
        color=None,
        linescolors=None,
        linestyles="solid",
        alpha=1.0,
        conf_alpha=0.25,
        label=None,
        name=None,
        fig=None,
        ax=None,
        title=None,
        subtitle=None,
        fontsize=14,
        title_fontsize=26,
        xtitle=None,
        ytitle=None,
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
            xtitle=xtitle,
            ytitle=ytitle,
            showgrid=showgrid,
        )
        ax = axs[0]
    if ax is None:
        ax = fig.get_axes()[0]

    ax_settings_kwargs = {k: v for k, v in kwargs.items() if k in ax_params}
    for k in ax_settings_kwargs:
        kwargs.pop(k)
    ax_settings_kwargs["showgrid"] = showgrid
    ax_settings_kwargs["subtitle"] = subtitle
    ax_settings_kwargs["xtitle"] = xtitle
    ax_settings_kwargs["ytitle"] = ytitle

    if xs is None:
        xs = np.arange(0, len(values), dtype=int)
    assert len(xs) == len(values)
    ymin = np.vectorize(lambda x: min(x, 0.0))(values)
    ymax = np.vectorize(lambda x: max(x, 0.0))(values)
    if "markersize" not in kwargs:
        kwargs["markersize"] = 5
    if label is None:
        label = name
    ax.plot(xs, values, "o", label=label, color=color, alpha=alpha, **kwargs)
    color = ax.lines[-1].get_color()
    if label is not None:
        ax.legend()
    ax.vlines(
        xs,
        ymin,
        ymax,
        colors=linescolors,
        linestyles=linestyles,
        label="",
    )

    ax.margins(0.05)
    ax.axhline()

    top_values = None
    bottom_values = None
    add_values_coeff = 0
    if conf_intvs is not None:
        fill_xs = conf_intvs_xs.copy() if conf_intvs_xs is not None else xs.copy()
        top_values = conf_intvs[:, 1].copy()
        bottom_values = np.zeros_like(
            conf_intvs[:, 0]) if fill_only_positive else conf_intvs[:, 0].copy()
        if fill_along_axis:
            add_values_coeff = -1
    if std is not None:
        fill_xs = std_xs.copy() if std_xs is not None else xs.copy()
        bottom_values = np.zeros_like(std) if fill_only_positive else -std.copy()
        top_values = std.copy()
        if not fill_along_axis:
            add_values_coeff = 1
    if top_values is not None:
        if add_values_coeff != 0:
            j = 0
            for i in range(len(fill_xs)):
                x = fill_xs[i]
                while j < len(xs) - 1 and xs[j] < x:
                    j += 1
                if xs[j] == x:
                    top_values[i] += add_values_coeff * values[j]
                    bottom_values[i] += add_values_coeff * values[j]
        if fill_along_axis:
            gap = float(np.min(np.diff(xs)[1:]))
            fill_xs = fill_xs.astype(float)
            fill_xs[0] -= gap / 2
            fill_xs[-1] += gap / 2
        ax.fill_between(
            fill_xs,
            top_values,
            bottom_values,
            alpha=conf_alpha,
            color=color,
        )

    ax_settings([ax], **ax_settings_kwargs)
    return fig
