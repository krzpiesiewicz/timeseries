from matplotlib import pyplot as plt

from timeseries.plotting.pyplot_ax_settings import ax_params, ax_settings
from timeseries.plotting.pyplot_fig_with_vertical_subplots import (
    fig_with_vertical_subplots
)
from timeseries.utils.init_structs import init_if_none


def pyplot_vars(
        seq_vars,
        color,
        index,
        index_values=None,
        name=None,
        vars_names=None,
        fig=None,
        axs=None,
        axs_heights_ratios=None,
        ax_height=None,
        xmargin=None,
        width=None,
        height=None,
        fontsize=13.5,
        title_fontsize=26,
        showgrid=True,
        grid_kwargs=None,
        title=None,
        **kwargs,
):
    vars_names = init_if_none(vars_names, list)
    grid_kwargs = init_if_none(grid_kwargs, dict)
    plt.ioff()
    if "pandas.core." in f"{type(index)}":
        index = index.values
    if index_values is None:
        index_values = index
    if "pandas.core." in f"{type(index_values)}":
        index_values = index_values.values

    def plot_single(ax, ts):
        ax.plot(index_values, ts[index], color=color, label=name, **kwargs)
        if name is not None:
            ax.legend()

    nvars = len(seq_vars)
    set_axs = None
    if axs is not None:
        assert nvars == len(axs)
        assert fig is not None
        set_axs = True
        fig_axs = fig.get_axes()
        axs = [fig_axs[i] for i in axs]
    if not set_axs:
        if fig is None:
            fig, axs = fig_with_vertical_subplots(
                nvars,
                axs_heights_ratios=axs_heights_ratios,
                ax_height=ax_height,
                showgrid=showgrid,
                grid_kwargs=grid_kwargs,
                xmargin=xmargin,
                width=width,
                height=height,
                fontsize=fontsize,
                title_fontsize=title_fontsize,
                title=title,
                subplots_titles=vars_names,
            )
        else:
            axs = fig.get_axes()

    ax_settings_kwargs = {k: v for k, v in kwargs.items() if k in ax_params}
    for k in ax_settings_kwargs:
        kwargs.pop(k)
    ax_settings_kwargs["index_values"] = index_values
    ax_settings_kwargs["showgrid"] = showgrid
    ax_settings_kwargs["grid_kwargs"] = grid_kwargs

    for ax, ts in zip(axs, seq_vars):
        plot_single(ax, ts)

    ax_settings(axs, **ax_settings_kwargs)

    return fig
