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


## Memory use methodology

Computing the amount of memory used by Python objects is tricky.  Besides the
instance itself, the object may carry a `__dict__` as well as attribute values.
However, some of these attribute values may be shared singletons, such as small
integers and time zone instances.

I measure memory use under the assumption that this question is interesting in
cases where large numbers of instances are stored in a collection.  To estimate
such memory use, I check the Python process size under Linux using the VmSize
field of `/proc/self/status`, before and after constructing a list of instances.
From the increase in process size, I subtract the comparable increase for
creating a list of `None`, then divide by the number of elements.

I assume that `numpy.datetime64` will be stored in `ndarray` objects, and
`pandas.Timestamp` in Pandas datastructures, where each value occupies 8 bytes.

