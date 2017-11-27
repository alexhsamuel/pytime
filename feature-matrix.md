# Feature matrix

|                   |datetime|Delorean|Arrow   |Pendulum|NumPy<sup>1</sup>|Pandas  |
|-------------------|:------:|:------:|:------:|:------:|:------:|:------:|
|naive time         |✔       |✘       |✘       |✘       |✔       |✔       |
|localized time     |✔       |✔       |✔       |✔       |✘       |✔       |
|date               |✔       |✘       |✘       |✔       |✔<sup>2</sup>|✔<sup>2</sup>|
|time of day        |✔       |✘       |✘       |✔       |✘       |✘       |
|time range         |1-9999  |1-9999  |1-9999  |1-9999  |1678-2262|1678-2262|
|time resolution    |1 µs    |1 µs    |1 µs    |1 µs    |1 ns    |1 ns    |
|date range         |1-9999  |        |        |1-9999  |huge    |huge    |
|rounding           |✘       |✔       |✔       |✔       |✘       |✔       |
|parsing            |strptime|udatetime|strptime<br>custom|strptime<br>custom|limited|strptime<br>custom|
|formatting         |strftime|Babel   |custom  |strftime<br>custom|✘|strftime|
|locales            |POSIX<sup>3</sup>|✘|custom|custom  |✘       |✘       |
|humanizing         |✘       |✔       |✔       |✔       |✘       |✘       |
|memory use<sup>4</sup>|40   |220     |512     |448     |40 (single)<br>8 (bulk)|120 (single)<br>8 (bulk)|
|implementation     |C       |Python  |Python  |Python  |C       |Cython  |
|interal repr       |components|`datetime`|`datetime`|`datetime`|ticks|`datetime`+ns|

<sup>1</sup> For NumPy, we consider "datetime64[ns]" for times and "datetime64[D]" for dates.

<sup>2</sup> NumPy and Pandas represent dates as "datetime64[D]", _i.e._ times
with 1 day precision.

<sup>3</sup> datetime's strftime formatting honors the POSIX locale, but this
must be set globally in the process, and locales may not be set up on all
computers.

<sup>4</sup> **Estimates** of memory use in bytes for single time values.  See
appendix for details.  NumPy and Pandas store times as 8-byte values in
collections (NumPy arrays; Pandas indexes, series, dataframes), but single
objects consume more memory.


