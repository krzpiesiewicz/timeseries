import random
import sys
from io import StringIO

import numpy as np
from matplotlib import colors as mcolors
from plotly.subplots import make_subplots

from timeseries.utils.init_structs import init_if_none


def plotly_vars(
        seq_vars,
        index,
        color,
        alpha=1.0,
        name="",
        vars_names=None,
        hide_label=False,
        showlegend=None,
        legend_pos="top",
        hovermode="x unified",
        scatter_kwargs=None,
        fig=None,
        nrows=None,
        ncols=None,
        rows_and_cols=None,
        axs=None,
        ax_height=None,
        width=None,
        height=None,
        yscale=None,
        yticks=None,
        xticks=None,
        xaxis_title=False,
        yaxis_title=False,
        title=None,
        subtitle=None,  # unused currently
        fontsize=14,
        line_width=1.5,
        dash=None,  # None, "dash", or "dot"
):
    def plot_single(fig, ts, row_and_col, color, legendgroup, showlegend):
        row, col = row_and_col
        fig.add_scatter(
            x=index,
            y=ts,
            name=name,
            legendgroup=legendgroup,
            showlegend=showlegend,
            row=row,
            col=col,
            opacity=alpha,
            line=dict(color=color, width=line_width, dash=dash),
            **scatter_kwargs
        )
        if hide_label:
            for trace in fig["data"]:
                if trace["name"] == name:
                    trace["showlegend"] = False
                    break

    vars_names = init_if_none(vars_names, list)
    scatter_kwargs = init_if_none(scatter_kwargs, dict)
    nvars = len(seq_vars)

    if axs is not None:
        assert rows_and_cols is None

    if fig is None:
        if ncols is None:
            if nrows is None:
                ncols = 1
            else:
                ncols = int(np.ceil(nvars / nrows))
        if nrows is None:
            nrows = int(np.ceil(nvars / ncols))
        if showlegend is None:
            showlegend = True

        vertical_space = 83
        if width is None:
            width = 1030
        if height is None:
            if ax_height is None:
                ax_height = 500 if nrows == 1 else 400
            height = ax_height * nrows + vertical_space * (nrows - 1)
        font_ratio = fontsize / 14
        bottom = 55 * font_ratio
        subplot_title_height = 35
        first_subplot_title_height = (
            subplot_title_height if len(vars_names) > 0 and vars_names[
                0] != "" else 0
        )
        title_height = 18 * font_ratio if title is not None else 0
        legend_top = 20 * font_ratio if showlegend and legend_pos == "top" else 0
        legend_bottom = 40 * font_ratio if showlegend and legend_pos == "bottom" else 0
        height += bottom + first_subplot_title_height + legend_top + legend_bottom
        vertical_spacing = vertical_space / (
                height - vertical_space * (nrows - 1))
        fig = make_subplots(
            rows=nrows,
            cols=ncols,
            subplot_titles=vars_names,
            horizontal_spacing=0.05,
            vertical_spacing=vertical_spacing,
        )
        fig.update_layout(showlegend=showlegend)
        if showlegend and legend_pos == "top":
            y = 1.0 + (0.5 * legend_top + first_subplot_title_height) / height
            fig.update_layout(
                legend=dict(
                    xanchor="left", yanchor="middle", x=0, y=y,
                    orientation="h"
                )
            )
        if showlegend and legend_pos == "bottom":
            y = -legend_bottom / height
            fig.update_layout(
                legend=dict(xanchor="left", yanchor="top", x=0, y=y,
                            orientation="h")
            )
        if yscale is None:
            yscale = "linear"
        fig.update_yaxes(type=yscale)
        if yticks is None:
            yticks = 10
        fig.update_yaxes(nticks=yticks)
        if xticks is None:
            xticks = 20
        fig.update_xaxes(nticks=xticks)
        fig.update_yaxes(showgrid=True)
        fig.update_xaxes(showgrid=True)

        if xaxis_title == True:
            xaxis_title = index.name
        if type(xaxis_title) is str:
            fig.update_layout(xaxis_title=xaxis_title)

        if yaxis_title == True:
            yaxis_title = name
        if type(yaxis_title) is str:
            fig.update_layout(yaxis_title=yaxis_title)

        width = int(width * 0.9)
        height = int(height * 0.9)
        fig.update_layout(
            width=width,
            height=height,
            font_size=fontsize,
            hovermode=hovermode,
            title=title,
            title_x=0.5,
            title_y=1 - 0.1 * title_height / height,
            title_yanchor="top",
            template="simple_white",
            margin=dict(
                l=0,
                r=0,
                t=title_height + first_subplot_title_height + legend_top,
                b=legend_bottom,
            ),
        )
    if yscale is not None:
        fig.update_yaxes(type=yscale)
    if yticks is not None:
        fig.update_yaxes(nticks=yticks)
    if xticks is not None:
        fig.update_xaxes(nticks=xticks)
    if showlegend is not None:
        fig.update(layout_showlegend=showlegend)

    def get_rows_and_cols():
        old_stdout = sys.stdout
        out = StringIO()
        sys.stdout = out
        fig.print_grid()
        sys.stdout = old_stdout
        grid_str = out.getvalue()
        for c in ["\n", "]", "(", ")", " "]:
            grid_str = grid_str.replace(c, "")
        rows_and_cols = []
        for string in grid_str.split("[")[1:]:
            i = string.find("x")
            nums = string[:i].split(",")
            rows_and_cols.append((int(nums[0]), int(nums[1])))
        return rows_and_cols

    if rows_and_cols is None:
        rows_and_cols = get_rows_and_cols()
    else:
        assert len(rows_and_cols) == nvars
    if axs is not None:
        rows_and_cols = [rows_and_cols[i] for i in axs]

    legendgroup = name if name is not None else f"unnamed{random.randint()}"

    def plot_first():
        plot_single(fig, seq_vars[0], rows_and_cols[0], color, legendgroup,
                    showlegend)

    try:
        plot_first()
    except ValueError as _:
        color = mcolors.to_hex(color)
        plot_first()
    for ts, (row_and_col) in zip(seq_vars[1:], rows_and_cols[1:]):
        plot_single(fig, ts, row_and_col, color, legendgroup, False)

    return fig
