import matplotlib.pyplot as plt
import numpy as np

from timeseries.analysis import acf, pacf


def __plot_stat_fun__(stat_fun, *args, kind_of_statistics=None,
                      plot_params={}, **kwargs):
    for param in ["zero", "label", "fig", "ax", "title", "width", "height",
                  "figsize"]:
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
    if "fig" in kwargs:
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
        zero=True,
        kind_of_statistics=None,
        label=None,
        fig=None,
        ax=None,
        title=None,
        fontsize=14,
        width=1030,
        height=700,
        **kwargs):
    plt.ioff()
    plt.rcParams.update({"font.size": fontsize})
    if fig is None and ax is None:
        fig = plt.figure()
        if title is None:
            if kind_of_statistics == "ACF":
                title = "Autocorrelation"
            if kind_of_statistics == "PACF":
                title = "Partial Autocorrelation"
        if title != "":
            fig.suptitle(title, fontsize=26)
        ax = fig.subplots(1)
    else:
        if ax is None:
            ax = fig.get_axes()[0]

    xs = np.arange(not zero, len(values), dtype=float)
    if not zero:
        values = values[1:]
    ymin = np.vectorize(lambda x: min(x, 0.0))(values)
    ymax = np.vectorize(lambda x: max(x, 0.0))(values)
    if "markersize" not in kwargs:
        kwargs["markersize"] = 5
    ax.plot(xs, values, "o", label=label, **kwargs)
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
            alpha=0.25
        )

    if label is not None:
        ax.legend()
    if fig is not None:
        dpi = fig.get_dpi()
        c = 1
        fig.set_size_inches((int(width / dpi * c), int(height / dpi * c)))
    return fig
