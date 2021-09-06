from datetime import datetime

import numpy as np
import pandas as pd

from timeseries import Interval


def get_downsampled(ts, delta, intv=None, index_values=True):
    intv_ts = intv.view(ts) if intv is not None else ts
    if index_values:
        begin = intv_ts.index[0]
        last = intv_ts.index[-1]
        index = []
        point = begin
        while point <= last:
            index.append(point)
            point += delta
        if type(begin) is datetime:
            index = pd.DatetimeIndex(index)
        else:
            index = pd.Index(index)
        index = index.intersection(intv_ts.index)
        return intv_ts.loc[index]
    else:
        return intv_ts.iloc[np.arange(0, len(intv_ts.index), delta)]


def get_interpolated(ts, intv, original_ts=None):
    original_ts = intv.view() if original_ts is None else intv.view(
        original_ts)
    index = original_ts.index
    interpolated_ts = pd.Series(np.full(len(index), np.nan), index=index)
    ts = Interval(ts, intv.begin, intv.end).view(ts, prevs=1, nexts=1)
    j = 0
    n = len(interpolated_ts)
    for i in range(0, len(ts) - 1):
        a = ts.index[i]
        b = ts.index[i + 1]
        while j < n and interpolated_ts.index[j] < a:
            interpolated_ts.iloc[j] = ts[a]
            j += 1
        while j < n and interpolated_ts.index[j] <= b:
            idx = interpolated_ts.index[j]
            interpolated_ts.iloc[j] = \
                ts[a] + (ts[b] - ts[a]) * (idx - a) / (b - a)
            j += 1
    while j < n:
        interpolated_ts.iloc[j] = ts[b]
        j += 1
    return interpolated_ts
