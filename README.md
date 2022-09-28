# timeseries
`timeseries` is a Python package which provides tools for transformation, analysis, visualization and multistep forecasting of univariate time series. It is build on top of: `numpy`, `pandas`, `statsmodels`, `pmdarima`, `scikit-learn`, `matplotlib`, and `plotly`.

See a sample [notebook](https://students.mimuw.edu.pl/~kp385996/timeseries/example.html) for basic usage.

More examples which employ `timeseries` package:
- [An autoregressive analysis of EEG signals](https://students.mimuw.edu.pl/~kp385996/ba/ba-thesis/ar/html/eeg_ihs_ar_psd_experiments_stats-eeg_features_raw.html),
- [Wind speed prediction – A comparison of models](https://students.mimuw.edu.pl/~kp385996/wind-speed/).

## Interval representation

The key concept of this package is the class `timeseries.Interval`, which carries more information than simple `pandas.Index`. It works with integer, date, time indices, and others which have defined arithmetic operations and linear orders. Furthermore, it gives simple operations that help one manipulate time series and intervals, e.g., you may restrict the view of any time series, you may get earlier / further measurements, or extend the interval in custom way.

```python
Inteval(ts=None, begin=None, end=None, as_dataframe=False, from_intv=None)
```

## Transformation

### Inverse Hyperbolic Sine (IHS) 

The class `timeseries.transform.IHSTransformer` is a model that fits to standardize a time series on a given interval. It uses the S-shaped single parameter Inverse Hyperbolic Sine transformation. The aim of using the IHS transformation is to alter the data distribution so that it is less skewed and less heavy-tailed, and the ranges of values are narrowed. The parameter is estimated to obtain the Gaussian distribution by using the concentrated log-likelihood.

<img src="https://user-images.githubusercontent.com/36455846/178771837-71feb689-7883-49aa-9dc3-f3ae03407fab.jpg" width="70%">

See: *Terence C Mills. Applied time series analysis: A practical guide to modeling and forecasting. Academic press, 2019, pp. 16–18*.

```python
IHSTransformer(
    ts,
    interval=None,
    d="auto",
    lmb="auto",
    difference_first=True,
    save_loglikelihood_deriv=False,
    verbose=False
)
```

`IHSTransformer` has methods: `transform(ts, interval=None)` and `detransform(diffs_ts, prev_original_values, index=None)`.

### Others transformations

In `timeseries.transform` there are also: `get_smoothed`, `get_downsampled`, `get_interpolated`.

## Visualization

The most significant feature is function `timeseries.plotting.plot_ts` which uses engines: `pyplot` and `plotly`. It allows plotting univariate or multivariate time series stored in `numpy.ndarray`, `pandas.Series`, `pandas.DataFrame`.

`plot_ts(ts, **kwargs)` calls `timeseries.plotting.pyplot_vars` or `timeseries.plotting.plotly_vars` depending on the value of `kwargs["engine"]`, which can be `pyplot` (default) or `plotly`. Function `plot_ts` return `fig` object, which can be provided as an argument to another `plot_ts` call. The type of the `fig` object depends on the engine, and it is compatible with functions from `pyplot` or `plotly` packages, respectively.

The following customizations are available:

```python
pyplot_vars(
    seq_vars,
    color,
    index,
    index_values=None,
    name=None,
    vars_names=[],
    fig=None,
    axs=None,
    axs_heights_ratios=None,
    ax_height=None,
    xmargin=None,
    width=None,
    height=None,
    fontsize=13.5,
    title_fontsize=26,
    showgrid=True,
    grid_kwargs=dict(),
    title=None,
    **kwargs,
):
```

```python
plotly_vars(
    seq_vars,
    index,
    color,
    name="",
    vars_names=[],
    showlegend=None,
    legend_pos="top",
    fig=None,
    nrows=None,
    ncols=None,
    rows_and_cols=None,
    axs=None,
    ax_height=None,
    width=None,
    height=None,
    yscale=None,
    yticks=None,
    xticks=None,
    xaxis_title=False,
    yaxis_title=False,
    title=None,
    subtitle=None,  # unused currently
    fontsize=14,
    line_width=1.5,
    dash=None,  # None, "dash", or "dot"
)
```

## Analysis

There are the following functions from `timeseries`: `analysis.acf`, `analysis.pacf`, `plotting.plot_acf`, `plotting.plot_pacf`, and generic `plotting.plot_stats`.

## Forecasting

The available forecasting models are: SARIMA and seasonal median of medians. The package also contains a framework for hyperparameter search and cross-validated performance measurement, with saving the results.

## Pytorch extension
A pytorch extension to `timeseries` package: [`timeseries-pytorch`](https://github.com/krzpiesiewicz/timeseries-pytorch) provides facades for pytorch models and datasets.
