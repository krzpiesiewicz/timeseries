import numpy as np
import pandas as pd

from timeseries import plot_ts
from timeseries.generator import transform_time, exp_grow, log_grow

ts = pd.DataFrame.from_dict(
    {
        "log": transform_time(9950, 10, 100, log_grow(2), x0=0),
        "exp": transform_time(9950, 10, 100, exp_grow(1.05), x0=0),
        "exp2": transform_time(9950, 10, 50, exp_grow(1.05), x0=0),
    }
)

ts2 = [
    transform_time(11420, 10, 200, log_grow(2), x0=0),
    transform_time(11420, 10, 20, exp_grow(1.05), x0=0),
]

ts3 = transform_time(5000, 10, 200, log_grow(2), x0=0)

ts4 = np.array([
    transform_time(1000, 100, 200, log_grow(2), x0=0),
    transform_time(1000, 100, 200, exp_grow(1.05), x0=0),
]).T


def plot_with_pyplot():
    fig = plot_ts(ts, name="maly", title="3 Plots", fontsize=21)
    plot_ts(
        ts2,
        fig=fig,
        color="tab:orange",
        linestyle="dashed",
        name="duzy",
    )
    plot_ts(ts3, fig=fig, axs=[0], subtitle="I set this subtitle (log)",
            xtitle="index axis",
            color="tab:green",
            linestyle="dotted")
    plot_ts(ts4, fig=fig, axs=[1, 2], ytitle="values axis", color="tab:red",
            linewidth=3)
    fig.show()


def plot_with_plotly():
    fig = plot_ts(
        ts,
        name="maly",
        title="3 Plots",
        engine="plotly",
        showlegend=True,
        fontsize=20,
        #     legend_pos="bottom",
        legend_pos="right",
    )
    plot_ts(ts2, fig=fig, color="orange", name="duzy", dash="dash")
    plot_ts(ts3, fig=fig, rows_and_cols=[(1, 1)], color="green", dash="dot")
    plot_ts(ts4, fig=fig, axs=[1, 2], color="red", line_width=3)
    fig.show(config={"displayModeBar": False, "displaylogo": False,
                     "staticPlot": True})


def main():
    plot_with_pyplot()
    plot_with_plotly()


if __name__ == "__main__":
    main()
