import matplotlib.pyplot as plt
import statsmodels.api as sm
import pandas as pd


def plot_acf(ts, **kwargs):
    return plot_acf_or_pacf(ts, "ACF", **kwargs)


def plot_pacf(ts, **kwargs):
    return plot_acf_or_pacf(ts, "PACF", **kwargs)


def plot_acf_or_pacf(ts, kind_of_statistics, **kwargs):
    if "fig" in kwargs:
        engine = (
            "pyplot" if "matplotlib" in f"{type(kwargs['fig'])}" else "plotly"
        )
    else:
        engine = kwargs["engine"] if "engine" in kwargs else "pyplot"
    kwargs.pop("engine", None)
    if engine == "pyplot":
        return pyplot_acf_or_pacf(ts, kind_of_statistics, **kwargs)
    elif engine == "plotly":
        raise Exception("Plottly not supported by plot_pacf yet")
    else:
        raise Exception("Unknown plotting engine")


def pyplot_acf_or_pacf(
        ts,
        kind_of_statistics,
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

    if type(ts) is pd.Series:
        ts = ts.values
    if kind_of_statistics == "ACF":
        if title is None:
            title = "Autocorrelation"
        sm.graphics.tsa.plot_acf(
            ts,
            label=name,
            title=None,
            ax=axs[0],
            **kwargs
        )
    else:
        if kind_of_statistics == "PACF":
            if title is None:
                title = "Partial Autocorrelation"
            sm.graphics.tsa.plot_pacf(
                ts,
                label=name,
                title=None,
                ax=axs[0],
                **kwargs
            )
        else:
            raise Exception("kind_of_statistics must be 'ACF' or 'PACF")

    if title is not None:
        fig.suptitle(title, fontsize=26)

    if name is not None:
        axs[0].legend()
    dpi = fig.get_dpi()
    c = 1
    fig.set_size_inches((int(width / dpi * c), int(height / dpi * c)))
    return fig
