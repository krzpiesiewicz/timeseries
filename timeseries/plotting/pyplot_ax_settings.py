import numpy as np
from matplotlib import dates as mdates
from matplotlib import pyplot as plt
from matplotlib import ticker

from timeseries.utils.init_structs import init_if_none

ax_params = [
    "axs",
    "fig",
    "index_values",
    "xtitle",
    "ytitle",
    "ynbins",
    "xscale",
    "yscale",
    "calc_xticks",
    "major_xstep",
    "minor_xticks",
    "major_xticks_loc",
    "minor_xticks_loc",
    "showgrid",
    "calc_grid",
    "grid_kwargs",
    "date_fmt",
    "datemin",
    "datemax",
    "round_dates",
    "rotx",
    "ha",
    "subtitle",
]


def ax_settings(
        axs=None,
        fig=None,
        index_values=None,
        xtitle=None,
        ytitle=None,
        ynbins=None,
        xscale=None,
        yscale=None,
        calc_xticks=False,  # default: do not change xticks
        major_xstep=None,
        minor_xticks=None,
        major_xticks_loc=None,
        minor_xticks_loc=None,
        calc_grid=False,
        showgrid=None,
        grid_kwargs=None,
        date_fmt=None,
        datemin=None,
        datemax=None,
        round_dates=None,
        rotx=None,
        ha=None,
        subtitle=None,
):
    grid_kwargs = init_if_none(grid_kwargs, dict)
    if axs is None:
        assert fig is not None
        axs = fig.get_axes()
    else:
        if type(axs) is not list and type(axs) is not np.ndarray:
            axs = [axs]

    def not_nones(*args, **kwargs):
        for arg in args:
            if arg is None:
                return False
        for key, val in kwargs:
            if val is None:
                return False
        return True

    is_datetime_x = None
    if not_nones(index_values):
        is_datetime_x = False
        if "datetime" in f"{index_values.dtype}":
            index_values = index_values.astype(np.datetime64)
            is_datetime_x = True

    if not_nones(subtitle):
        subtitles = subtitle if type(subtitle) is list else [subtitle] * len(
            axs)
        assert len(subtitles) == len(axs)
        for ax, subtitle in zip(axs, subtitles):
            ax.set_title(subtitle)

    if not_nones(xtitle):
        xtitles = xtitle if type(xtitle) is list else [xtitle] * len(axs)
        assert len(xtitles) == len(axs)
        for ax, xtitle in zip(axs, xtitles):
            ax.set_xlabel(xtitle)

    if not_nones(ytitle):
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
            for new_step in (a * (10 ** exp) for exp in range(10) for a in
                             (1, 2, 5)):
                if 10 * new_step >= x_range:
                    step = new_step
                    break
            minor_ticks = 5
            return step, minor_ticks

        for ax in axs:
            if not_nones(is_datetime_x, index_values) and is_datetime_x:
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
                if showgrid is not None and calc_grid:
                    ax.xaxis.grid(showgrid, which="minor")
            else:
                if minor_xticks != 0:
                    if minor_xticks_loc is None:
                        minor_xticks_loc = ticker.AutoMinorLocator(
                            minor_xticks)
                    ax.xaxis.set_minor_locator(minor_xticks_loc)
                    if showgrid is not None and calc_grid:
                        ax.xaxis.grid(showgrid, which="both")
            ax.tick_params(which="major", length=7)
            ax.tick_params(which="minor", length=0)
            if not_nones(rotx):
                plt.setp(ax.get_xticklabels(), rotation=rotx)
            if not_nones(ha):
                plt.setp(ax.get_xticklabels(), ha=ha)

    for ax in axs:
        if not_nones(is_datetime_x, xscale) and not is_datetime_x:
            ax.set_xscale(xscale)
        if not_nones(ynbins):
            ax.yaxis.set_major_locator(ticker.MaxNLocator(nbins=ynbins))
        if not_nones(yscale):
            ax.set_yscale(yscale)
        if showgrid is not None:
            grid_kwargs["b"] = showgrid
        ax.grid(**grid_kwargs)
