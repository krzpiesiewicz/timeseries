from datetime import datetime

import pandas as pd

from timeseries import Interval


def main():
    # .csv available to download at:
    # https://www.investing.com/currencies/gbp-usd-historical-data
    gpd_usd_data = pd.read_csv("data/GBP_USD Historical Data_daily.csv")
    gpd_usd_data["Date"] = pd.to_datetime(gpd_usd_data.Date,
                                          format="%b %d, %Y")
    gpd_usd_data.set_index("Date", inplace=True)
    gpd_usd_data.sort_index(ascending=True, inplace=True)

    ts = gpd_usd_data.Price
    whole_intv = Interval(ts, datetime(2020, 1, 1), datetime(2020, 1, 20))
    intv = Interval(ts, datetime(2020, 1, 7), datetime(2020, 1, 15),
                    from_intv=whole_intv)

    dt = datetime(2020, 1, 8)
    for shift in [-3, -2, -1, 0, 1, 2, 3]:
        print(
            f"{dt} shifted by {shift} is {whole_intv.shifted_idx(dt, shift)}")

    print(f"whole_intv: {whole_intv}")
    print(f"intv: {intv}")

    print(f"intv.prev(): {intv.prev()}")
    print(f"intv.next(): {intv.next()}")

    print(f"whole_intv.view(): {whole_intv.view()}")
    print(f"intv.view(): {intv.view()}")
    print(f"intv.prev_view(): {intv.prev_view()}")
    print(f"intv.next_view(): {intv.next_view()}")

    print(f"intv.prev_view(nexts=2): {intv.prev_view(nexts=2)}")
    print(f"intv.prev_view(nexts=-2): {intv.prev_view(nexts=-2)}")
    print(f"intv.next_view(prevs=2): {intv.next_view(prevs=2)}")
    print(f"intv.next_view(prevs=-2): {intv.next_view(prevs=-2)}")


if __name__ == "__main__":
    main()
