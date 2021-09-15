import numpy as np
from matplotlib import dates as mdates
from matplotlib import pyplot as plt
from matplotlib import ticker

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
        xmargin=0,
        width=None,
        height=None,
        fontsize=13.5,
        xaxis_title=False,
        yaxis_title=False,
        ynbins=10,
        xscale="linear",
        yscale="linear",
        calc_xticks=True,
        major_xstep=None,
        minor_xticks=None,
        major_xticks_loc=None,
        minor_xticks_loc=None,
        date_fmt=None,
        datemin=None,
        datemax=None,
        round_dates=None,
        rotx=0,
        ha="center",
        title=None,
        **kwargs,
):
    plt.ioff()
    if "pandas.core." in f"{type(index)}":
        if xaxis_title == True:
            xaxis_title = index.name
        index = index.values
    if index_values is None:
        index_values = index
    if "pandas.core." in f"{type(index_values)}":
        if xaxis_title == True:
            xaxis_title = index.name
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
            plt.rcParams.update({"font.size": fontsize})
            gs_kw = {"height_ratios": axs_heights_ratios}
            fig = plt.figure(constrained_layout=True)
            axs = fig.subplots(nvars, gridspec_kw=gs_kw)
            if nvars == 1:
                axs = [axs]
            for ax in axs:
                ax.grid(True)
                ax.set_xmargin(xmargin)
            fontratio = fontsize / 13.5
            subplots_titles_height = 0
            for ax, var_name in zip(axs, vars_names):
                if var_name != "":
                    ax.set_title(var_name)
                    subplots_titles_height += 18 * fontratio
                subplots_titles_height += 18 * fontratio
            if title is not None:
                fig.suptitle(title, fontsize=26)
                title_height = 53
            else:
                title_height = 0
            if width is None:
                width = 900
            bottom = 35
            if height is None:
                if ax_height is None:
                    ax_height = 500 if len(axs) == 1 else 400
                spacing = 22
                height = (
                        bottom
                        + ax_height * len(axs)
                        + spacing * (len(axs) - 1)
                        + title_height
                        + subplots_titles_height
                )
            dpi = fig.get_dpi()
            if DEBUG:
                print(subplots_titles_height)
                print(ax_height * len(axs))
                print(spacing * (len(axs) - 1))
                print(height)
                print(dpi)
            c = 1
            fig.set_size_inches((int(width / dpi * c), int(height / dpi * c)))
        else:
            axs = fig.get_axes()

    for ax, ts in zip(axs, seq_vars):
        plot_single(ax, ts)

    for ax in axs:
        if not is_datetime_x:
            ax.set_xscale(xscale)
        if type(xaxis_title) is str:
            ax.set_xlabel(xaxis_title)
        ax.yaxis.set_major_locator(ticker.MaxNLocator(nbins=ynbins))
        ax.set_yscale(yscale)

    if yaxis_title == True:
        for ax, var_name in zip(axs, vars_names):
            ax.set_ylabel(var_name)

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
