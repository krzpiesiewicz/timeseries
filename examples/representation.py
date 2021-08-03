from datetime import datetime

import pandas as pd

from timeseries import Interval, AutoIHSTransformer
from timeseries.plotting import plot_ts


def main():
    # .csv available to download at:
    # https://www.investing.com/currencies/gbp-usd-historical-data
    gpd_usd_data = pd.read_csv("data/GBP_USD Historical Data_daily.csv")
    gpd_usd_data["Date"] = pd.to_datetime(gpd_usd_data.Date,
                                          format="%b %d, %Y")
    gpd_usd_data.set_index("Date", inplace=True)
    gpd_usd_data.sort_index(ascending=True, inplace=True)

    ts = gpd_usd_data.Price
    trans = AutoIHSTransformer(ts)
    print(f"d = {trans.d}")
    print(f"div = {trans.div}")
    diffs = trans.transform(ts)
    summed = trans.detransform(diffs, ts[: trans.d])

    date1 = datetime(2020, 5, 1)
    date2 = datetime(2021, 4, 1)
    intv = Interval(ts, date1, date2)

    fig1 = plot_ts(diffs)
    plot_ts(intv.view(diffs), color="black", fig=fig1)
    fig1.show()

    fig2 = plot_ts(ts)
    plot_ts(summed, color="red", fig=fig2)
    plot_ts(intv.view(), color="black", fig=fig2)
    fig2.show()


if __name__ == "__main__":
    main()
