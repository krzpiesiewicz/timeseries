import numpy as np
import pandas as pd

from timeseries.plotting.plotly_vars import plotly_vars
from timeseries.plotting.pyplot_vars import pyplot_vars


def plot_ts(ts, **kwargs):
    seq_vars = None
    if type(ts) is np.ndarray:
        if len(ts.shape) == 1:
            seq_vars = [ts]
        else:
            seq_vars = [arr.reshape(ts.shape[:-1]) for arr in
                        np.array_split(ts, ts.shape[-1],
                                       axis=len(ts.shape) - 1)]
    if type(ts) is list or type(ts) is tuple:
        seq_vars = ts
    if seq_vars is not None:
        if "index" not in kwargs:
            max_len = max(len(var) for var in seq_vars)
            kwargs["index"] = pd.RangeIndex(0, max_len)
        if "vars_names" not in kwargs:
            kwargs["vars_names"] = [
                var.name if type(var) is pd.Series else "" for var in seq_vars
            ]

    if type(ts) is pd.Series:
        seq_vars = [ts]
        kwargs["index"] = kwargs.get("index", ts.index)
        kwargs["vars_names"] = kwargs.get("vars_names", [ts.name])
    if type(ts) is pd.core.frame.DataFrame:
        seq_vars = [ts[colname] for colname in ts.columns]
        kwargs["index"] = kwargs.get("index", ts.index)
        kwargs["vars_names"] = kwargs.get(
            "vars_names", [series.name for series in seq_vars]
        )

    if "fig" in kwargs and kwargs["fig"] is not None:
        engine = (
            "pyplot" if "matplotlib" in f"{type(kwargs['fig'])}" else "plotly"
        )
    else:
        engine = kwargs["engine"] if "engine" in kwargs else "pyplot"
    kwargs.pop("engine", None)

    if "color" not in kwargs:
        kwargs["color"] = "steelblue"

    if engine == "pyplot":
        return pyplot_vars(seq_vars, **kwargs)
    elif engine == "plotly":
        kwargs.pop("index_was_generated", None)
        return plotly_vars(seq_vars, **kwargs)
    else:
        raise Exception("Unknown plotting engine")
