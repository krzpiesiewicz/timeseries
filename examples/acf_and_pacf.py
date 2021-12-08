from datetime import datetime

import numpy as np
import pandas as pd

from timeseries import Interval
from timeseries.analysis import acf, plot_acf, plot_pacf, plot_stats, pacf


def main():
    # COVID
    # .csv available to download at:
    # https://ourworldindata.org/explorers/coronavirus-data-explorer
    covid_data = pd.read_csv("data/covid-data.csv")
    covid_data["date"] = pd.to_datetime(covid_data["date"], format="%Y-%m-%d")
    covid_data.set_index("date", inplace=True)
    covid_data.sort_index(ascending=True, inplace=True)

    loc = "Argentina"
    ts = covid_data[covid_data.location == loc]["new_cases"]
    ts = ts[~ts.isnull()]

    train_intv = Interval(ts, begin=datetime(2020, 8, 1),
                          end=datetime(2021, 3, 1))

    print(f"acf for whole ts: {acf(ts)}")
    print(f"acf for whole ts with conf intvs: {acf(ts, alpha=0.05)}")
    acf_values, confint = acf(train_intv.view(ts), alpha=0.05)
    plot_stats(acf_values, confint, label="train", color="green",
               showgrid=True, title="ACF manually").show()
    plot_acf(ts, zero=False, label="whole").show()

    fig = plot_pacf(ts, alpha=0.05, zero=False)
    plot_pacf(train_intv.view(ts), alpha=0.05, zero=False,
              label="train", fig=fig)
    plot_pacf(ts, alpha=0.05, zero=False,
              cross_validated=True, nblocks=7, blocks_group=5,
              label="cross validated whole", fig=fig).show()

    print(f"pacf_burg for whole ts: {pacf(ts, method='burg')}")

    plot_pacf(train_intv.view(ts), zero=True, alpha=0.1,
              label="burg method", method="burg").show()

    plot_stats(np.linspace(2, 5, 10), xs = np.arange(2, 12),
               std=np.array([a*a for a in np.linspace(0.7, 2, 10)]),
               fill_only_positive=True,
               title="Example statistics",
               subtitle="Totally unreal ;)").show()

    plot_stats(np.linspace(2, 20, 20), xs=np.arange(2, 22),
               std=np.array([a * a for a in np.linspace(0.5, 1.01, 20)]),
               fill_along_axis=False, calc_xticks=True, showgrid=True,
               title="Example statistics").show()

    plot_stats(2 ** (np.linspace(2, 3, 10) ** 4), xs=np.arange(2, 12),
               std=np.array((2 ** ((np.linspace(2, 3, 10) ** 4.011) + 1)) / 4),
               fill_along_axis=False, yscale="log",
               title="Example statistics").show()


if __name__ == "__main__":
    main()
