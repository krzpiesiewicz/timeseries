from datetime import datetime, timedelta

import pandas as pd

from timeseries import Interval, plot_ts
from timeseries.transform import get_smoothed, get_downsampled, \
    get_interpolated


def main():
    # .csv available to download at:
    # https://www.investing.com/currencies/gbp-usd-historical-data
    gpd_usd_data = pd.read_csv("data/GBP_USD Historical Data_daily.csv")
    gpd_usd_data["Date"] = pd.to_datetime(gpd_usd_data.Date,
                                          format="%b %d, %Y")
    gpd_usd_data.set_index("Date", inplace=True)
    gpd_usd_data.sort_index(ascending=True, inplace=True)

    ts = gpd_usd_data.Price[datetime(2019, 1, 1): datetime(2019, 3, 1)]
    intv = Interval(ts, datetime(2019, 1, 5), datetime(2019, 2, 10))

    smoothed_ts = get_smoothed(ts, std=5)
    downsampled_ts = get_downsampled(smoothed_ts, timedelta(days=5))
    interpolated_ts = get_interpolated(downsampled_ts, intv)
    fig = plot_ts(ts, title="GBP/USD Daily", color="grey")
    plot_ts(smoothed_ts, fig=fig, color="darkred")
    plot_ts(downsampled_ts, fig=fig, color="green")
    plot_ts(interpolated_ts, fig=fig, color="orange")
    fig.show()


if __name__ == "__main__":
    main()
