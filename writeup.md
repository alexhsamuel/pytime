# The packages

## Delorean

Uses pytz for time zones.

Uses [`babel.dates`](http://babel.pocoo.org/en/latest/api/dates.html) for
formatting.

Uses [`dateutil.parser`](http://dateutil.readthedocs.io/en/stable/parser.html)
for parsing.



## Pandas

Uses `datetime64` arrays, but scalars exposed as `pandas.Timestamp` 
[implemented in Cython](https://github.com/pandas-dev/pandas/blob/master/pandas/_libs/tslibs/timestamps.pyx).

```py
>>> ser = pd.Series([ datetime.datetime.now() for _ in range(10) ])
>>> ser
0   2017-11-21 22:21:26.994301
1   2017-11-21 22:21:26.994310
2   2017-11-21 22:21:26.994312
3   2017-11-21 22:21:26.994313
4   2017-11-21 22:21:26.994315
5   2017-11-21 22:21:26.994317
6   2017-11-21 22:21:26.994319
7   2017-11-21 22:21:26.994320
8   2017-11-21 22:21:26.994322
9   2017-11-21 22:21:26.994324
dtype: datetime64[ns]
>>> ser.iloc[0]
Timestamp('2017-11-21 22:21:26.994301')
>>> ser.values[0]
numpy.datetime64('2017-11-21T22:21:26.994301000')
```


# Appendices

## Benchmarking methodology

See `benchmark.py`.

1. I use a no-argument callable to represent each operation being benchmarked.
   This is usually a lambda.  I use temporary variables outside the lambda
   to minimize attribute lookup in the operation itself.

1. I sample each operation's performance 20 times.  Each sample consists of
   invoking the callable 5000 times inside a Python loop, with calls to
   `time.perf_counter` before and after. 

1. I use the 5th percentile of the 20 samples, i.e. the second smallest sample.
   I do this to measure the best-case performance of the operation, and ignore
   fluctuations due to scheduling, other system activity, etc.  I hope (without
   justification) that 20 samples is enough to obtain this.

1. Before each sampling, I similarly sample an empty loop (containing a `pass`
   statement only) 20 times and take the 5th percentil.  I subtract this
   pedestal value from the main benchmark result, to account for loop overhead.

I've run the benchmarks on my laptop (late 2013 MacBook Pro, 2.4 GHz i5, macOS
10.12.6) and a bare metal Linux desktop (Ubuntu 17.04, 3.5 GHz i7-3770K, kernel
4.10.0-24-lowlatency).  While results differ considerably, I find ratios among
different implementations of the same operations to be roughly comparable.

