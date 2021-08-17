from abc import ABC, abstractmethod


class Transformer(ABC):
    @abstractmethod
    def transform(self, ts):
        ...

    @abstractmethod
    def detransform(self, diffs_ts, prev_original_values, index=None):
        ...
