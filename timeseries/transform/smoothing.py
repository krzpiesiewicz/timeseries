import numpy as np
import pandas as pd
from scipy.stats import norm


def get_smoothed(ts, std=None, weights=None, only_prevs=True):
    if weights is not None:
        assert std is None
    else:
        assert std is not None
        xs = np.arange(int(-5 * std), int(5 * std) + 1)
        weights = norm.pdf(xs, loc=0, scale=std)
        weights = weights[weights >= 0.05 * weights[len(weights) // 2]]
    assert len(weights) % 2 == 1
    m = len(weights) // 2
    x = ts.values
    n = len(x)
    y = np.zeros(n + 2 * m)
    y[:m] = x[0]
    y[-m:] = x[-1]
    y[m:-m] = x
    s = np.zeros_like(x)
    if only_prevs:
        weights[m + 1:] = 0
    weights = weights / np.sum(weights)
    for i, w in enumerate(weights):
        if w != 0:
            s += w * y[i: n + i]
    return pd.Series(s, index=ts.index)
