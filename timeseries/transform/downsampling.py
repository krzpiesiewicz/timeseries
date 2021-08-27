from datetime import datetime, timedelta
import pandas as pd


def downsample_ts(ts, time_delta, intv=None):
    intv_ts = intv.view(ts) if intv is not None else ts
    begin_date_time = intv_ts.index[0]
    last_date_time = intv_ts.index[-1]
    total_seconds = (
        begin_date_time - datetime.fromtimestamp(0) - timedelta(hours=24)
    ).total_seconds()
    total_seconds -= int(total_seconds) % time_delta.seconds
    date_time = datetime.fromtimestamp(0) + timedelta(seconds=total_seconds)
    index = []
    while date_time < begin_date_time:
        date_time += time_delta
    while date_time <= last_date_time:
        index.append(date_time)
        date_time += time_delta
    index = pd.DatetimeIndex(index)
    index = index.intersection(intv_ts.index)
    return intv_ts.loc[index]
