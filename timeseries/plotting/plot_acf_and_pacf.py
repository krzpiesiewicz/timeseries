import numpy as np

from timeseries.analysis import acf, pacf
from timeseries.plotting import plot_stats
from timeseries.utils.init_structs import init_if_none


def __split_plot_params__(params, extra_plot_params=None):
    extra_plot_params = init_if_none(extra_plot_params, dict)
    plain_params = params.copy()
    plot_params = extra_plot_params.copy()
    for param in ["label", "name", "fig", "ax", "title", "subtitle", "width",
                  "height", "ax_height", "axs_heights_ratios", "fontsize",
                  "title_fontsize", "figsize", "xmargin", "color",
                  "linestyles", "linescolors",
                  "showgrid", "conf_alpha", "xtitle", "ytitle"]:
        if param in params:
            plot_params[param] = params[param]
            plain_params.pop(param)
    return plain_params, plot_params


def __plot_acf_pacf__(stat_fun, *args, zero=True, plot_params=None, **kwargs):
    plot_params = init_if_none(plot_params, dict)
    kwargs, plot_kwargs = __split_plot_params__(kwargs, plot_params)
    res = stat_fun(*args, **kwargs)
    conf_intvs = None
    conf_intvs_xs = None
    if type(res) is tuple:
        assert len(res) <= 2
        values, conf_intvs = res
        conf_intvs_xs = np.arange(1, len(conf_intvs), dtype=float)
        conf_intvs = conf_intvs[1:, :]
    else:
        values = res
    xs = np.arange(not zero, len(values))
    values = values[(not zero):]
    return plot_stats(values, conf_intvs, xs=xs, conf_intvs_xs=conf_intvs_xs,
                      **plot_kwargs)


def plot_acf(*args, plot_params=None, **kwargs):
    plot_params = init_if_none(plot_params, dict)
    if "title" not in plot_params and "title" not in kwargs:
        plot_params["title"] = "Autocorrelation"
    return __plot_acf_pacf__(acf, *args, plot_params=plot_params,
                             **kwargs)


def plot_pacf(*args, plot_params=None, **kwargs):
    plot_params = init_if_none(plot_params, dict)
    if "title" not in plot_params and "title" not in kwargs:
        plot_params["title"] = "Partial Autocorrelation"
    return __plot_acf_pacf__(pacf, *args, plot_params=plot_params,
                             **kwargs)
