from abc import ABC, abstractmethod

import numpy as np
import pandas as pd
import pmdarima as pm


class Transformer(ABC):
    @abstractmethod
    def transform(self, ts):
        ...

    @abstractmethod
    def detransform(self, diffs_ts, prev_original_values, index=None):
        ...


class AutoIHSTransformer(Transformer):
    def __init__(self, ts, d=None):
        self.d = pm.arima.ndiffs(ts) if d is None else d
        self.div = 1
        ts = self.transform(ts)
        std = np.sqrt(np.var(ts))
        self.div = 4 * std
        if self.div == 0:
            self.div = 1
        self.prev_val = 0

    def __next_val__(self, diff):
        self.prev_val = self.prev_val + diff
        return self.prev_val

    def transform(self, ts):
        x = np.arcsinh(np.diff(ts, self.d)) / self.div
        if type(ts) is pd.Series:
            index = ts.index[self.d:]
            x = pd.Series(x, index=index)
        return x

    def detransform(self, diffs_ts, prev_original_values, index=None):
        if type(prev_original_values) is not np.ndarray:
            prev_original_values = np.array(prev_original_values)
        assert len(prev_original_values) >= self.d
        if index is None:
            if type(diffs_ts) is pd.Series:
                index = diffs_ts.index
            else:
                index = pd.Index(np.arange(len(diffs_ts)))
        ts = pd.Series(diffs_ts, index=index)
        ts = (ts * self.div).apply(np.sinh)
        if self.d == 2:
            self.prev_val = prev_original_values[-1] - prev_original_values[-2]
            ts = ts.apply(self.__next_val__)
        if self.d >= 1:
            self.prev_val = prev_original_values[-1]
            ts = ts.apply(self.__next_val__)
        return ts


class Interval:
    def __init__(self, ts, begin=None, end=None):
        self.ts = ts
        if begin is not None and end is not None:
            assert begin < end
        self.begin = begin
        self.end = end

    def index(self, ts=None, begin=None, end=None, prevs=0, nexts=0):
        if ts is None:
            ts = self.ts
        if begin is None:
            begin = self.begin
        if end is None:
            end = self.end
        assert prevs >= 0
        index = ts.index
        if begin is not None:
            index = ts[begin:].index
            if prevs > 0:
                index = ts[:begin].index[-prevs:].append(index)
        if end is not None:
            index = index.intersection(ts[:end].index)
            if nexts > 0:
                index = index.append(ts[end:].index[:nexts])
        return index

    def view(self, ts=None, begin=None, end=None, prevs=0, nexts=0):
        if ts is None:
            ts = self.ts
        index = self.index(ts, begin, end, prevs, nexts)
        ts = ts[index]
        return ts

    def prev_view(self, ts=None):
        if ts is None:
            ts = self.ts
        return self.view(ts, begin=None, end=self.begin)
