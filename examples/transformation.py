from datetime import datetime

import pandas as pd

from timeseries import Interval, plot_ts
from timeseries.analysis import plot_hist
from timeseries.transform.ihs import IHSTransformer


def main():
    # .csv available to download at:
    # https://www.investing.com/currencies/gbp-usd-historical-data
    gpd_usd_data = pd.read_csv("data/GBP_USD Historical Data_daily.csv")
    gpd_usd_data["Date"] = pd.to_datetime(gpd_usd_data.Date,
                                          format="%b %d, %Y")
    gpd_usd_data.set_index("Date", inplace=True)
    gpd_usd_data.sort_index(ascending=True, inplace=True)

    ts = gpd_usd_data.Price
    whole_intv = Interval(ts, datetime(2019, 1, 1))
    train_intv = Interval(ts, datetime(2020, 2, 1), datetime(2021, 4, 1))
    # whole_intv = Interval(ts)
    # train_intv = Interval(ts, datetime(2013, 1, 1), datetime(2021, 4, 1))

    plot_ts(whole_intv.view(), title="GBP/USD Daily").show()

    trans = IHSTransformer(ts, interval=train_intv, verbose=True,
                           lmb=None)
    trans_ts = trans.transform(ts)
    print(f"Differences – skewness: {trans_ts.skew()}")

    trans_ihs = IHSTransformer(ts, interval=train_intv, verbose=True,
                               save_loglikelihood_deriv=True)
    trans_ihs_ts = trans_ihs.transform(ts)
    print(f"Differences of IHS – skewness: {trans_ihs_ts.skew()}")
    fig1 = plot_ts(whole_intv.view(trans_ts),
                   title="GBP/USD Daily – IHS Transformed Diferences")
    plot_ts(train_intv.view(trans_ihs_ts), color="tab:red", name="Train",
            fig=fig1)
    fig1.show()

    trans_diff_after_ihs = IHSTransformer(
        ts, interval=train_intv, difference_first=False,
        verbose=True,
        save_loglikelihood_deriv=True
    )
    trans_diff_after_ihs_ts = trans_diff_after_ihs.transform(ts)
    print(f"IHS for differences – skewness:"
          f" {trans_diff_after_ihs_ts.skew()}")
    fig1 = plot_ts(whole_intv.view(trans_ts),
                   title="GBP/USD Daily – Differences of IHS Transformed")
    plot_ts(train_intv.view(trans_diff_after_ihs_ts), color="tab:red",
            name="Train",
            fig=fig1)
    fig1.show()

    figh = plot_hist(whole_intv.view(trans_ts),
                     label="differenced and normalized")
    plot_hist(whole_intv.view(trans_ihs_ts), fig=figh,
              label="differenced with IHS and normalized")
    figh.show()

    # figh = plot_hist(whole_intv.view(trans_ts), bins=50,
    #         title="GBP/USD Daily – Histogram of Transformed",
    #         name="differenced only")
    # plot_hist(whole_intv.view(trans_ihs_ts), fig=figh, bins=50,
    #           name="differenced with IHS")
    # figh.show()

    detrans_ts = trans.detransform(train_intv.view(trans_ts),
                                   train_intv.prev_view())
    detrans_ihs_ts = trans_ihs.detransform(train_intv.view(trans_ihs_ts),
                                           train_intv.prev_view())
    detrans_diff_after_ihs_ts = trans_diff_after_ihs.detransform(
        train_intv.view(trans_diff_after_ihs_ts),
        train_intv.prev_view())

    fig2 = plot_ts(whole_intv.view(), title="GBP/USD Daily")
    plot_ts(detrans_ts, color="tab:orange", name="Detransformed", fig=fig2)
    plot_ts(detrans_ihs_ts, color="tab:green", name="Detransformed IHS",
            fig=fig2)
    plot_ts(detrans_diff_after_ihs_ts, color="tab:red",
            name="Detransformed "
                 "Differenced After IHS",
            fig=fig2)
    fig2.show()

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

    plot_ts(ts, title=f"Covid-19 {loc}", engine="plotly",
            color="tab:blue").show()

    train_intv = Interval(ts, begin=datetime(2020, 8, 1),
                          end=datetime(2021, 3, 1))

    trans = IHSTransformer(ts, interval=train_intv, lmb=None, verbose=True)
    trans_ts = trans.transform(ts)
    print(f"differenced only – skewness: {trans_ts.skew()}")

    fig1 = plot_ts(trans_ts, engine="plotly", color="tab:blue",
                   title=f"Covid-19 New Cases in {loc} – Transformed Without IHS")
    plot_ts(train_intv.view(trans_ts), color="tab:red", fig=fig1)
    fig1.show()

    trans_ihs = IHSTransformer(ts, interval=train_intv,
                               difference_first=True, verbose=True)
    trans_ihs_ts = trans_ihs.transform(ts)
    print(f"differenced with IHS – skewness: {trans_ihs_ts.skew()}")

    fig1 = plot_ts(trans_ihs_ts, engine="plotly", color="tab:blue",
                   title=f"Covid-19 New Cases in {loc} – IHS Transformed")
    plot_ts(train_intv.view(trans_ihs_ts), color="tab:red", fig=fig1)
    fig1.show()

    figh = plot_hist(whole_intv.view(trans_ts),
                     title=f"Covid-19 New Cases in {loc} – Histogram of "
                           "IHS Transformed",
                     name="differenced only",
                     engine="plotly", color="tab:blue")
    plot_hist(whole_intv.view(trans_ihs_ts), fig=figh,
              label="differenced with IHS", color="tab:orange")
    figh.show()

    detrans_ts = trans_ihs.detransform(train_intv.view(trans_ihs_ts),
                                       train_intv.prev_view())

    fig2 = plot_ts(ts, title=f"Covid-19 {loc}", engine="plotly",
                   color="tab:blue")
    plot_ts(train_intv.view(ts), color="yellow", fig=fig2)
    plot_ts(detrans_ts, color="tab:red", name="Detransformed IHS Train",
            fig=fig2)
    fig2.show()

    # # Evil Example
    # import numpy as np
    # from timeseries import ts_from_fun
    # fun = lambda x: np.exp(x / 200 + np.power(np.sin(x/50), 2))
    # ts = pd.Series(ts_from_fun(1400, fun, start=-200),
    #                index=np.arange(-200, 1200))
    #
    # trans = IHSTransformer(ts)
    #
    # trans_ts = trans.transform(ts)
    # plot_hist(trans_ts).show()
    # detrans_ts = trans.detransform(trans_ts, ts.iloc[:trans.d])
    # print(ts)
    # print(detrans_ts)
    # print(ts - detrans_ts)
    # print(trans_ts)
    #
    # fig3 = plot_ts(trans_ts)
    # fig3.show()
    #
    # fig4 = plot_ts(ts, color="gray")
    # plot_ts(detrans_ts, fig=fig4)
    # fig4.show()


if __name__ == "__main__":
    main()
