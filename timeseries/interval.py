import numpy as np
import pandas as pd


class Interval:
    def __init__(self, ts=None, begin=None, end=None, as_dataframe=False,
                 from_intv=None):
        assert ts is not None or from_intv is not None
        if ts is None:
            ts = from_intv.ts

        if from_intv is not None:
            ts = from_intv.view(ts)

        ts = Interval.__to_pandas__(ts, as_dataframe)

        if begin is not None and end is not None:
            assert begin < end

        self.ts = ts
        self.begin = begin
        self.end = end
        self.as_array = as_dataframe

    def __str__(self):
        return f"[{self.begin}, {self.end})"

    def __to_pandas__(ts, as_dataframe=False):
        if type(ts) is np.ndarray:
            if len(ts.shape) > 1 or as_dataframe:
                ts = pd.DataFrame(ts)
            else:
                ts = pd.Series(ts)
        if type(ts) is pd.Series and as_dataframe:
            ts = pd.DataFrame(ts)
        return ts

    def __index__(self, ts=None, begin=None, end=None, prevs=0, nexts=0):
        if ts is None:
            ts = self.ts
        else:
            ts = Interval.__to_pandas__(ts)
        index = ts.index
        if prevs == "all":
            begin = None
            prevs = 0
        if nexts == "all":
            end = None
            nexts = 0
        if begin is not None and begin >= ts.index[0]:
            index = ts.loc[begin:].index
            if prevs > 0:
                index_prevs = prevs + 1 if begin in ts.index else prevs
                index = ts.loc[:begin].index[-index_prevs:].append(index)
        if prevs < 0:
            index = index[-prevs:]
        if end is not None and end <= ts.index[-1]:
            index = index.intersection(ts.loc[:end].index)
            if len(index) > 0 and index[-1] == end:
                index = index[:-1]
            if nexts > 0:
                index = index.append(ts.loc[end:].index[:nexts])
        if nexts < 0:
            index = index[:nexts]
        return index

    def __call__(self, ts=None, begin=None, end=None, prevs=0, nexts=0,
                 as_array=None):
        ts = ts if ts is not None else self.ts
        begin = begin if begin is not None else self.begin
        end = end if end is not None else self.end
        if prevs == "all":
            begin = None
            prevs = 0
        if nexts == "all":
            end = None
            nexts = 0
        as_array = as_array if as_array is not None else self.as_array
        index = self.__index__(ts, begin, end, prevs, nexts + 1)
        if begin is not None:
            begin = index[0]
        if end is not None:
            index2 = self.__index__(ts, begin, end, prevs, nexts)
            if index[-1] == index2[-1]:
                end = None
            else:
                end = index[-1]
            
        return Interval(ts, begin, end, as_array)

    def prev(self, ts=None, nexts=0):
        return self.__call__(ts=ts, end=self.begin, prevs="all", nexts=nexts)

    def next(self, ts=None, prevs=0):
        return self.__call__(ts=ts, begin=self.end, prevs=prevs, nexts="all")

    def index(self, ts=None, begin=None, end=None, prevs=0, nexts=0):
        if begin is None:
            begin = self.begin
        if end is None:
            end = self.end
        return self.__index__(ts, begin, end, prevs, nexts)

    def shifted_idx(self, idx, shift, ts=None):
        index = self.__index__(ts, end=idx, nexts=shift + 1)
        return index[-1]

    def view(self, ts=None, begin=None, end=None, prevs=0, nexts=0):
        if ts is None:
            ts = self.ts
        else:
            ts = Interval.__to_pandas__(ts)
        index = self.index(ts, begin, end, prevs, nexts)
        ts = ts.loc[index]
        return ts

    def prev_view(self, *args, **kwargs):
        return self.prev(*args, **kwargs).view()

    def next_view(self, *args, **kwargs):
        return self.next(*args, **kwargs).view()

    # def prev_view(self, ts=None, prevs=0):
    #     if ts is None:
    #         ts = self.ts
    #     index = self.__index__(ts, end=self.begin, nexts=prevs)
    #     ts = ts.loc[index]
    #     return ts
