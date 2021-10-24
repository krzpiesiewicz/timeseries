from datetime import datetime

import pandas as pd

from timeseries import Interval
from timeseries.analysis import acf, plot_acf, plot_pacf, plot_stats


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
               showgrid=True).show()
    plot_acf(ts, zero=False, label="whole").show()

    fig = plot_pacf(ts, alpha=0.05)
    plot_pacf(train_intv.view(ts), alpha=0.05, zero=False,
              label="train", fig=fig)
    plot_pacf(ts, alpha=0.05, zero=False,
              cross_validated=True, nblocks=7, blocks_group=5,
              label="cross validated whole", fig=fig).show()


if __name__ == "__main__":
    main()
