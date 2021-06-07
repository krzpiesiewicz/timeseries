import numpy as np


def ts_from_fun(n, fun_t, start=0):
    return fun_t(np.arange(start, start + n))


def transform_time(n_points, start_t, end_t, fun, x0=0, x1=None):
    if x1 is None:
        x1 = x0 + end_t - start_t
    ys = fun(np.linspace(x0, x1, n_points))
    ys -= np.min(ys)
    max_y = np.max(ys)
    return start_t + (end_t - start_t) / max_y * ys


def lin_grow(coeff):
    return lambda x: coeff * x


def exp_grow(base):
    return lambda x: np.exp(x * np.log(base))


def log_grow(base):
    return lambda x: np.log(x + 1) / np.log(base)
