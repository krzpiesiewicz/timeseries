from abc import ABC
from abc import abstractmethod

import pmdarima as pm


class Model(ABC):
    @abstractmethod
    def fit(self, train_interval):
        ...

    @abstractmethod
    def score(self, test_interval, measure=pm.metrics.smape, trans=None):
        ...

    @abstractmethod
    def predict(self, pred_interval):
        ...
