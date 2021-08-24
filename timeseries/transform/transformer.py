from abc import ABC, abstractmethod

from timeseries import Interval


class Transformer(ABC):
    def __get_ts_and_interval__(self, ts, interval):
        if type(ts) is Interval:
            if interval is None:
                interval = ts
            ts = interval.ts
        if self.d is not None and interval is None:
            interval = Interval(ts, begin=ts.index[self.d])
        return ts, interval

    @abstractmethod
    def transform(self, ts):
        ...

    @abstractmethod
    def detransform(self, diffs_ts, prev_original_values, index=None):
        ...
