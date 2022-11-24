from matplotlib import pyplot as plt

from timeseries.utils.init_structs import init_if_none

DEBUG = False


def fig_with_vertical_subplots(
        n_axes,
        axs_heights_ratios=None,
        ax_height=None,
        xmargin=None,
        width=None,
        height=None,
        fontsize=13.5,
        title_fontsize=26,
        title=True,
        subplots_titles=False,
        xtitle=None,
        ytitle=None,
        showgrid=None,
        grid_kwargs=None
):
    grid_kwargs = init_if_none(grid_kwargs, dict)
    plt.rcParams.update({"font.size": fontsize})
    gs_kw = {"height_ratios": axs_heights_ratios}
    fig = plt.figure(constrained_layout=True)
    axs = fig.subplots(n_axes, gridspec_kw=gs_kw)
    if n_axes == 1:
        axs = [axs]
    for ax in axs:
        if showgrid is not None:
            grid_kwargs["b"] = showgrid
        ax.grid(**grid_kwargs)
        if xmargin is None:
            xmargin = 0
        ax.set_xmargin(xmargin)

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

    fontratio = fontsize / 13.5
    subplots_titles_height = 0
    if type(subplots_titles) is bool:
        if subplots_titles:
            subplots_titles = [True] * n_axes
        else:
            subplots_titles = [""] * n_axes
    assert type(subplots_titles) is list
    for ax, subplot_title in zip(axs, subplots_titles):
        if subplot_title != "":
            if subplot_title == True:
                subplot_title = ""
            ax.set_title(subplot_title)
            subplots_titles_height += 18 * fontratio
        subplots_titles_height += 18 * fontratio
    if title is not None:
        fig.suptitle(title, fontsize=title_fontsize)
        title_height = 53 * title_fontsize / 26
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
    return fig, axs
