class Interval:
    def __init__(self, ts, begin=None, end=None):
        self.ts = ts
        if begin is not None and end is not None:
            assert begin < end
        self.begin = begin
        self.end = end

    def __index__(self, ts=None, begin=None, end=None, prevs=0, nexts=0):
        if ts is None:
            ts = self.ts
        index = ts.index
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

    def index(self, ts=None, begin=None, end=None, prevs=0, nexts=0):
        if begin is None:
            begin = self.begin
        if end is None:
            end = self.end
        return self.__index__(ts, begin, end, prevs, nexts)

    def view(self, ts=None, begin=None, end=None, prevs=0, nexts=0):
        if ts is None:
            ts = self.ts
        index = self.index(ts, begin, end, prevs, nexts)
        ts = ts.loc[index]
        return ts

    def prev_view(self, ts=None, prevs=0):
        if ts is None:
            ts = self.ts
        index = self.__index__(ts, end=self.begin, nexts=prevs)
        ts = ts.loc[index]
        return ts
