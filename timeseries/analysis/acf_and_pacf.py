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
        nlags=None,
        nblocks=5,
        blocks_group=3,
        **kwargs):
    if kind_of_statistics == "ACF":
        stat_fun = stattools.acf
    else:
        if kind_of_statistics == "PACF":
            stat_fun = stattools.pacf
        else:
            raise Exception("kind_of_statistics must be 'ACF' or 'PACF")

    if type(x) is pd.Series:
        x = x.values

    if not cross_validated:
        return stat_fun(x, *args, **kwargs)
    else:
        stat_values = None
        stat_conf_intvs = None
        pos = np.linspace(0, len(x) - 1, nblocks + 1, dtype=int)
        n = nblocks - blocks_group + 1
        for i in range(0, n):
            y = x[pos[i]: pos[i + blocks_group]]
            values, conf_intvs = stat_fun(y, *args, nlags=nlags, **kwargs)
            if nlags is None:
                nlags = len(values)
            if len(values) > nlags:
                values = values[:nlags]
                conf_intvs = conf_intvs[:nlags, :]
            if len(values) < nlags:
                nlags = len(values)
                stat_values = stat_values[:nlags]
                stat_conf_intvs = stat_conf_intvs[:nlags, :]
            if stat_values is None:
                stat_values = values[:nlags]
                stat_conf_intvs = conf_intvs[:nlags]
            else:
                stat_values += values
                stat_conf_intvs += conf_intvs
        stat_values /= n
        stat_conf_intvs /= n
        return stat_values, stat_conf_intvs
