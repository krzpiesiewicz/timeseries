import sys

import numpy as np
import pandas as pd
import pmdarima as pm

from timeseries.transform.transformer import Transformer


class IHSTransformer(Transformer):
    def __init__(self, ts, interval=None, d="auto", lmb="auto",
                 difference_first=True,
                 save_loglikelihood_deriv=False, verbose=False):
        self.verbose = verbose
        self.d = d
        if lmb is not None and lmb != "auto":
            lmb = float(lmb)
        self.lmb = lmb
        self.ihs_after_diff = difference_first
        self.save_loglikelihood_deriv = save_loglikelihood_deriv
        self.std = None
        self.mean = None
        self.transform(ts, interval)

    def __next_val__(self, diff):
        self.prev_val = self.prev_val + diff
        return self.prev_val

    def transform(self, ts, interval=None):

        def difference(x):
            if self.d >= 1:
                x = np.diff(x, 1)
            if self.d >= 2:
                x = np.diff(x, self.d - 1)
            return x

        def ihs_trans(x):
            if self.lmb == "auto":
                if self.save_loglikelihood_deriv:
                    self.lmb, self.loglikelihood_deriv = \
                        calc_mle_of_lmb(x, get_loglikelihood_deriv=True)
                else:
                    self.lmb = calc_mle_of_lmb(x)
                if self.verbose:
                    if self.lmb is None:
                        print(f"MLE of IHS lambda cannot be found",
                              file=sys.stderr)
                    else:
                        print(f"MLE of IHS lambda: {self.lmb:e}",
                              file=sys.stderr)
            if type(self.lmb) is float:
                x = np.arcsinh(x * self.lmb) / self.lmb
            return x

        original_ts_type = type(ts)

        ts, interval = self.__get_ts_and_interval__(ts, interval)
        if np.any(ts.isnull()):
            raise Exception("Series has missing value")

        if not self.ihs_after_diff:
            # if self.d == "auto":
            #     x = interval.view(x) if interval is not None else x
            #     x, interval = self.__get_ts_and_interval__(x, interval)
            ts = ihs_trans(ts)

        if self.d == "auto":
            ts = interval.view(ts) if interval is not None else ts
            try:
                self.d = pm.arima.ndiffs(ts)
            except:
                self.d = 2
            if self.verbose:
                print(f"Order of differencing: {self.d}", file=sys.stderr)
            ts, interval = self.__get_ts_and_interval__(ts, interval)
        assert (interval is not None)
        ts = interval.view(ts, prevs=self.d)
        x = difference(ts)

        if self.ihs_after_diff:
            x = ihs_trans(x)
        if self.mean is None:
            self.mean = np.mean(x)
        x = x - self.mean
        if self.std is None:
            self.std = np.sqrt(np.var(x))
            if int(self.std) == 0:
                self.std = 1
        x /= self.std

        if original_ts_type is np.ndarray:
            x = np.array(x)
        else:
            index = ts.index[self.d:]
            if original_ts_type is pd.Series:
                x = pd.Series(x, index=index, name=ts.name)
            if original_ts_type is pd.DataFrame:
                x = pd.DataFrame(x, index=index)
                x.columns = ts.columns
        return x

    def detransform(self, diffs_ts, prev_original_values, index=None):

        def dedifference(ts, prev_original_values):
            if self.d == 2:
                self.prev_val = prev_original_values[-1] - \
                                prev_original_values[-2]
                ts = ts.apply(self.__next_val__)
            if self.d >= 1:
                self.prev_val = prev_original_values[-1]
                ts = ts.apply(self.__next_val__)
            return ts

        def ihs_trans(x):
            if type(self.lmb) is float:
                x = np.arcsinh(x * self.lmb) / self.lmb
            return x

        def ihs_detrans(ts):
            if type(self.lmb) is float:
                ts = (ts * self.lmb).apply(np.sinh) / self.lmb
            return ts

        if type(prev_original_values) is not np.ndarray:
            prev_original_values = np.array(prev_original_values)
        assert len(prev_original_values) >= self.d
        if index is None:
            if type(diffs_ts) is pd.Series:
                index = diffs_ts.index
            else:
                index = pd.Index(np.arange(len(diffs_ts)))
        ts = pd.Series(diffs_ts, index=index)
        ts = (ts * self.std)
        ts += self.mean

        if self.ihs_after_diff:
            ts = ihs_detrans(ts)
            ts = dedifference(ts, prev_original_values)
        else:
            prev_original_values = ihs_trans(prev_original_values)
            ts = dedifference(ts, prev_original_values)
            ts = ihs_detrans(ts)

        return ts


def calc_mle_of_lmb(x, get_loglikelihood_deriv=False):
    lmbs = pd.Series(dtype=np.float64)
    for v in np.power(10., np.arange(-8, 30)):
        lmbs = lmbs.append(pd.Series(np.arange(v, 10 * v, 0.1 * v)))
    lmbs = lmbs.values
    derivs = []
    used_lmbs = []
    for i, lmb in enumerate(lmbs):
        try:
            d = derivative_of_concentrated_loglikelihood(x, lmb)
            if not np.any(np.isnan(d)):
                used_lmbs.append(lmb)
                derivs.append(d)
        except:
            pass

    used_lmbs = np.array(used_lmbs)
    derivs = np.array(derivs)
    differential_quotients = []
    for i in range(len(used_lmbs) - 1):
        d = np.abs(derivs[i + 1] - derivs[i])
        if np.sign(derivs[i + 1]) * np.sign(derivs[i]) < 0 \
                and np.abs(d) > 1e-4:
            d /= (used_lmbs[i + 1] - used_lmbs[i])
            differential_quotients.append(
                (d * used_lmbs[i], used_lmbs[i], used_lmbs[i + 1]))

    if len(differential_quotients) > 0:
        differential_quotients = sorted(differential_quotients)[:10]
        _, a, b = differential_quotients[0]

        def f(lmb):
            return derivative_of_concentrated_loglikelihood(x, lmb)

        best_lmb = bisection(f, a, b, 1e-4)
    else:
        best_lmb = None

    if get_loglikelihood_deriv:
        derivs_table = pd.Series(derivs.reshape(derivs.shape[0]),
                                 index=pd.Index(np.log10(used_lmbs),
                                                name="log10(lambda)"),
                                 name="derivative of log-likelihood(lambda | x) with respect to lambda"
                                 )
        return best_lmb, derivs_table
    else:
        return best_lmb


def bisection(f, a, b, tol):
    if int(np.sign(f(a))) == int(np.sign(f(b))):
        raise Exception("the scalars a and b do not bound a root")
    m = (a + b) / 2
    if float(np.abs(f(m))) < tol:
        return float(m)
    elif int(np.sign(f(a))) == int(np.sign(f(m))):
        return bisection(f, m, b, tol)
    elif int(np.sign(f(b))) == int(np.sign(f(m))):
        return bisection(f, a, m, tol)


def derivative_of_concentrated_loglikelihood(x, lmb):
    a = lmb * x
    a = a[~np.isnan(a)]
    b = a * a + 1
    a = a[~np.isnan(a)]
    c = np.sqrt(b)
    d = a + c
    d[d < 1e-12] = 1e-12
    d = np.log(d)
    d_mean = np.mean(d)
    d_minus_d_mean = d - d_mean
    e = a / c
    e_minus_e_mean = e - np.mean(e)
    A = np.mean(d_minus_d_mean * e_minus_e_mean)
    B = np.mean(d_minus_d_mean * d_minus_d_mean)
    C = np.mean(1 / b)
    return A / B - C
