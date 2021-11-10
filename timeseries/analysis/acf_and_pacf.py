import numpy as np
import pandas as pd
import statsmodels.tsa.stattools as stattools


def acf(x, *args, **kwargs):
    return cross_validated_acf_or_pacf(x, *args, **kwargs,
                                       kind_of_statistics="ACF")


def pacf(x, *args, **kwargs):
    return cross_validated_acf_or_pacf(x, *args, **kwargs,
                                       kind_of_statistics="PACF")


def cross_validated_acf_or_pacf(
        x,
        *args,
        kind_of_statistics=None,
        cross_validated=False,
        return_conf_intvs=True,
        nblocks=5,
        blocks_group=3,
        debug=False,
        **kwargs):
    if kind_of_statistics == "ACF":
        stat_fun = stattools.acf
    else:
        if kind_of_statistics == "PACF":
            stat_fun = stattools.pacf
            if "method" in kwargs:
                method = kwargs["method"]
                if method == "burg":
                    return_conf_intvs = False
                    stat_fun = stattools.pacf_burg
                    kwargs.pop("method")
                    if "alpha" in kwargs:
                        kwargs.pop("alpha")
        else:
            raise Exception("kind_of_statistics must be 'ACF' or 'PACF")

    if type(x) is pd.Series:
        x = x.values

    def call_stat_fun(*args, **kwargs):
        res = stat_fun(*args, **kwargs)
        if type(res) is tuple:
            if not return_conf_intvs:
                res = (res[0], None)
        else:
            res = (res, None)
        return res

    stat_values = None
    stat_conf_intvs = None
    if not cross_validated:
        stat_values, stat_conf_intvs = call_stat_fun(x, *args, **kwargs)
    else:
        pos = np.linspace(0, len(x) - 1, nblocks + 1, dtype=int)
        n = nblocks - blocks_group + 1
        lags = None
        for i in range(0, n):
            y = x[pos[i]: pos[i + blocks_group]]
            if debug:
                print(f"{blocks_group}/{nblocks}, n={n}, i={i},"
                      f"i+blocks_group={i + blocks_group}: {pos[i]}–{pos[i + blocks_group]}")
            values, conf_intvs = call_stat_fun(y, *args, **kwargs)
            if lags is None:
                lags = len(values)
            if len(values) > lags:
                values = values[:lags]
                if conf_intvs is not None:
                    conf_intvs = conf_intvs[:lags, :]
            if len(values) < lags:
                lags = len(values)
                stat_values = stat_values[:lags]
                if conf_intvs is not None:
                    stat_conf_intvs = stat_conf_intvs[:lags, :]
            if stat_values is None:
                stat_values = values
                if conf_intvs is not None:
                    stat_conf_intvs = conf_intvs
            else:
                stat_values += values
                if conf_intvs is not None:
                    stat_conf_intvs += conf_intvs
        stat_values /= n
        if stat_conf_intvs is not None:
            stat_conf_intvs /= n
    if return_conf_intvs and stat_conf_intvs is not None:
        return stat_values, stat_conf_intvs
    else:
        return stat_values
