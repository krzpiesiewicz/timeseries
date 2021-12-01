import numpy as np
from matplotlib import dates as mdates
from matplotlib import pyplot as plt
from matplotlib import ticker

from timeseries.plotting.fig_with_vertical_subplots import (
    fig_with_vertical_subplots
)

DEBUG = False


def pyplot_vars(
        seq_vars,
        color,
        index,
        index_values=None,
        name=None,
        vars_names=[],
        fig=None,
        axs=None,
        axs_heights_ratios=None,
        ax_height=None,
        xmargin=None,
        width=None,
        height=None,
        fontsize=13.5,
        title_fontsize=26,
        xtitle=None,
        ytitle=None,
        ynbins=10,
        xscale="linear",
        yscale="linear",
        calc_xticks=True,
        major_xstep=None,
        minor_xticks=None,
        major_xticks_loc=None,
        minor_xticks_loc=None,
        showgrid=True,
        grid_kwargs=dict(),
        date_fmt=None,
        datemin=None,
        datemax=None,
        round_dates=None,
        rotx=0,
        ha="center",
        title=None,
        subtitle=None,
        **kwargs,
):
    plt.ioff()
    if "pandas.core." in f"{type(index)}":
        index = index.values
    if index_values is None:
        index_values = index
    if "pandas.core." in f"{type(index_values)}":
        index_values = index_values.values
    is_datetime_x = False
    if "datetime" in f"{index_values.dtype}":
        index_values = index_values.astype(np.datetime64)
        is_datetime_x = True

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

    for ax, ts in zip(axs, seq_vars):
        plot_single(ax, ts)

    for ax in axs:
        if not is_datetime_x:
            ax.set_xscale(xscale)
        ax.yaxis.set_major_locator(ticker.MaxNLocator(nbins=ynbins))
        ax.set_yscale(yscale)

    if subtitle is not None:
        subtitles = subtitle if type(subtitle) is list else [subtitle] * len(axs)
        assert len(subtitles) == len(axs)
        for ax, subtitle in zip(axs, subtitles):
            ax.set_title(subtitle)

    if xtitle is not None:
        xtitles = xtitle if type(xtitle) is list else [xtitle] * len(axs)
        assert len(xtitles) == len(axs)
        for ax, xtitle in zip(axs, xtitles):
            ax.set_xlabel(xtitle)

    if ytitle is not None:
        ytitles = ytitle if type(ytitle) is list else [ytitle] * len(axs)
        assert len(ytitles) == len(axs)
        for ax, ytitle in zip(axs, ytitles):
            ax.set_ylabel(ytitle)

    if calc_xticks:

        def major_steps_and_minors_ticks(ax):
            xmargin, _ = ax.margins()
            ax.set_xmargin(0)
            x_min, x_max = ax.get_xlim()
            ax.set_xmargin(xmargin)
            x_range = int(x_max - x_min)
            major_step = 1
            for new_step in (a * (10 ** exp) for exp in range(10) for a in
                             (1, 2, 5)):
                if 10 * new_step >= x_range:
                    step = new_step
                    break
            minor_ticks = 5
            return step, minor_ticks

        for ax in axs:
            if is_datetime_x:
                if datemin is None:
                    datemin = np.datetime64(min(index_values))
                if datemax is None:
                    datemax = np.datetime64(max(index_values))
                if round_dates is not None:
                    datemin = np.datetime64(datemin, round_dates)
                    if np.datetime64(datemax, round_dates) < datemax:
                        datemax = np.datetime64(datemax,
                                                round_dates) + np.timedelta64(
                            1, round_dates
                        )
                xmargin, _ = ax.margins()
                ax.set_xmargin(0)
                xmin, xmax = ax.get_xlim()
                ax.set_xmargin(xmargin)
                old_datemin = np.datetime64(
                    mdates.num2date(xmin).replace(tzinfo=None))
                old_datemax = np.datetime64(
                    mdates.num2date(xmax).replace(tzinfo=None))
                datemin = min(datemin, old_datemin)
                datemax = max(datemax, old_datemax)
                ax.set_xlim(datemin, datemax)
                if minor_xticks != 0:
                    if minor_xticks_loc is None:
                        minor_xticks_loc = mdates.AutoDateLocator()
                    ax.xaxis.set_minor_locator(minor_xticks_loc)
                if major_xticks_loc is not None:
                    ax.xaxis.set_major_locator(major_xticks_loc)
                if date_fmt is not None:
                    ax.xaxis.set_major_formatter(date_fmt)
            else:
                major_step, minor_ticks = major_steps_and_minors_ticks(ax)
                if major_xstep is None:
                    major_xstep = major_step
                if minor_xticks is None:
                    minor_xticks = minor_ticks
                if major_xticks_loc is None:
                    major_xticks_loc = ticker.MultipleLocator(base=major_xstep)
                ax.xaxis.set_major_locator(major_xticks_loc)
            if minor_xticks is None:
                ax.xaxis.grid(True, which="minor")
            else:
                if minor_xticks != 0:
                    if minor_xticks_loc is None:
                        minor_xticks_loc = ticker.AutoMinorLocator(
                            minor_xticks)
                    ax.xaxis.set_minor_locator(minor_xticks_loc)
                    ax.xaxis.grid(True, which="minor")
            ax.tick_params(which="major", length=7)
            ax.tick_params(which="minor", length=0)
            plt.setp(ax.get_xticklabels(), rotation=rotx, ha=ha)
    return fig
