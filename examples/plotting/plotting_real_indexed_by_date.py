import pandas as pd
from matplotlib import dates as mdates

from timeseries import plot_ts
from timeseries.plotting import ax_settings


def main():
    # .csv available to download at:
    # https://www.investing.com/currencies/gbp-usd-historical-data
    gpd_usd_data = pd.read_csv("../data/GBP_USD Historical Data_monthly.csv")
    gpd_usd_data["Change %"] = gpd_usd_data["Change %"].apply(
        lambda s: float(s[:-1]))
    gpd_usd_data["Date"] = pd.to_datetime(gpd_usd_data.Date, format="%b %y")
    gpd_usd_data = gpd_usd_data.reindex(
        index=gpd_usd_data.index[::-1]).set_index(
        gpd_usd_data.index
    )
    gpd_usd_data

    plot_ts(
        gpd_usd_data["Change %"],
        index_values=gpd_usd_data.Date,
        name="GPB in USD",
        title="GPB/USD Exchange Rates",
    ).show()

    plot_ts(
        [gpd_usd_data.Price, gpd_usd_data["Change %"]],
        index=range(100),
        index_values=gpd_usd_data.Date[range(100)],
        title="GPB/USD Exchange Rates",
        round_dates="Y",
        color="darkred",
        major_xticks_loc=mdates.YearLocator(base=1),
        date_fmt=mdates.DateFormatter("%Y"),
    ).show()

    plot_ts(
        gpd_usd_data["Change %"],
        index=gpd_usd_data.Date,
        name="GPB in USD",
        title="GPB/USD Exchange Rates",
        engine="plotly",
        #     legend_pos="bottom",
        legend_pos="top",
    ).show()

    plot_ts(
        [gpd_usd_data.Price, gpd_usd_data["Change %"]],
        index=range(200),
        index_values=gpd_usd_data.Date[range(200)],
        title="GPB/USD Exchange Rates",
    ).show()

    plot_ts(
        [gpd_usd_data.Price, gpd_usd_data["Change %"]],
        index=gpd_usd_data.Date[range(200)],
        title="GPB/USD Exchange Rates",
        engine="plotly",
    ).show()

    plot_ts(
        gpd_usd_data[["Price", "Change %"]],
        index=gpd_usd_data.Date[range(100)],
        title="GPB/USD Exchange Rates",
        name="GPB in USD",
        color="darkred",
        engine="plotly",
        showlegend=True,
    ).show()

    # COVID
    # .csv available to download at:
    # https://ourworldindata.org/explorers/coronavirus-data-explorer
    covid_data = pd.read_csv("../data/covid-data.csv")
    covid_data["date"] = pd.to_datetime(covid_data["date"], format="%Y-%m-%d")
    covid_data.set_index("date", inplace=True)
    covid_data.sort_index(ascending=True, inplace=True)

    loc = "Argentina"
    ts = covid_data[covid_data.location == loc]["new_cases"]
    ts = ts[~ts.isnull()]
    ts = ts[~(ts == 0)]

    fig = plot_ts(ts, title=f"Covid-19 {loc}", color="tab:blue")
    ax_settings(fig=fig, yscale="log")
    fig.show()


if __name__ == "__main__":
    main()
