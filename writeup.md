# Preliminaries


## Time

Time at its core is conceptually fairly simple.  It's kind of like space, except
one dimension instead of three, and history proceeds&mdash;basically by
definition&mdash;monotonically in one direction.


## Date

Date is a much more complicated, human concept.  We divide time into recurring
periods of 24 hours (usually), and represent a time by specifying which day
period (the date) and how far into this day (the time of day, or sometimes just
"time" for short).


## Time zones

To complicate things further, we don't agree on when each day starts.  Each
government is free to specify this for its territory or subterritories, and to
change this at its leisure.  A government will generally specify this to
coordinate the time of day with the rising and setting of the sun in its
territory.  A geographical region with a consistent association of time to date
and time of day is a "time zone".  

Many governments modify the associations over the year for social or economic
policy; this is "daylight savings time" (DST).

The mapping between time and (date, time of day) is a political creation and not
tied to any physical reality.  As such, the past, current, and projected future
mapping needs to be encoded as data, and this data needs to be updated whenever
governments change their minds.  

Basically all systems uses the "Olson" [time zone
database](https://en.wikipedia.org/wiki/Tz_database) as the source of this
information.  On UNIX/Linux/macOS systems, it's generally installed in
`/usr/share/zoneinfo`.

In the past, some systems did not include up-to-date copies of the database,
though it seems nowadays mostly up-to-date.  At the time of writing, Ubuntu
17.04 and macOS 10.12.6 both provide the "2017b" version; the latest version is
"2017c".

FIXME: Windows

### UTC

UTC is sort of a time zone associated with no territory.  It provides a
non-varying association between physical time and (date, time of day), and is
the reference against which other time zones are specified.

### Naming

Time zones in the time zone database are named by major cities or other
geographical features contained in them, for example "America/New_York",
"Europe/London", and "Asia/Tokyo".  The time zone database is just a directory
with one file (or symlink) for each zone, so poke around to see what's there.

Usually you don't want to use EST and EDT as a time zone; each is honored in the
Eastern U.S. for only half the year.  The combined time zone is "Eastern time",
specified as "US/Eastern" or "America/New_York" in the time zone database.

Avoid using GMT (Greenwhich Mean Time) as a synonym for UTC; it's not quite the
same thing.  Among other things, GMT is wintertime part of the United Kingdom's
time zone.  UK is on GMT in the winter and BST (British Summer Time) in the
summer, just as the U.S. Eastern time zone is on EST in the winter and EDT in
the summer.


# Formatting

There are countless ways to format dates and times as strings in use, for both
human and machine consumption.  Historically, many computer programs used
existing or invented formats to suit the developers' or users' preferences.

Even standard formats are language-, culture-, and country-specific.  [POSIX
_locales_](http://pubs.opengroup.org/onlinepubs/009695399/basedefs/xbd_chap07.html)
(not to be confused with _localization_, described below) specify standard date
and time formats for specific regions and languages.

The [ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html) standard
specifies a family of standard formats for machine-readable dates and times.
[RFC 3339](https://tools.ietf.org/html/rfc3339) recommends a particular subset
of ISO 8601 formats for use in Internet protocols.  These are examples of RFC
3339 timestamps:

```
1937-01-01T12:00:27.87+00:20
1990-12-31T23:59:60Z
```

The 'Z' suffix stands for UTC; it derives from the "Zulu" [military time
zone](https://en.wikipedia.org/wiki/List_of_military_time_zones), which has a
zero UTC offset.  This can be used interchangably with explicit "+00:00".

_Note that a UTC offset does not unambiguously specify a time zone!_ The time
"2017-11-26T11:06:08.465019-05:00" has a UTC offset of &ndash;5 hours.  It may
be the current time in America/New_York... but also in America/Toronto,
America/Havana, America/Lima, and others.  These time zones coincide at this
given instant, but may vary in their UTC offsets over the year and over history.


# Primitive representations

Several _ad hoc_ representations are widely used for times and dates.

1. Stringified dates and times, for example "2017-11-25" and "2017-11-25
   10:29:46.531286-05:00".  Two major advantages: these are easy for humans to
   read and write, and essentially any language, framework, and format
   (particularly: CSV, JSON, XML) can represent them.  

   The major disadvantage is that no time/date operations are naturally
   available, e.g. "2017-12-31" + 1 day.  

2. Dates and times stringified without punctuation and re-encoded in integers,
   _e.g._ 20171127 (today), 123000 (lunchtime).  These too can be represented in
   most systems, but operations are similarly unavailable.

3. Dates represented as dates since a specific "epoch" date, and times
   represented as ticks (seconds, or afixed fractions of a second) since a
   specific "epoch" instant.  On UNIX, traditional epoch is
   1970-01-01T00:00:00+00:00.

The first two have the advantages of being readily interpreted in human-friendly
time units (year, month, day, hour, minute, second).  Further, all languages,
frameworks, and formats (such as JSON, XML, and CSV) can represent them.
However, few operations are available; for example, adding a day to a date
correctly is not possible.  

The third representation, days or ticks since an epoch, is the opposite.  Date
and time operations are just ordinary additions and subtractions; however it's
not possible to extract human-friendly units or format dates and times for
humans.

Various time and date packages exist to bridge this feature gap: to provide
human-friendly representations that also support temporal operations.


# The packages

## dateutil

`dateutil.tz` provides an implementation of `tzinfo` that, by default, uses
your system's copy of the Olson time zone database.

`dateutil.zoneinfo` uses its own copy of the database (2017b in the PyPI/conda
2.6.1 package).


## pytz

pytz combines a copy of the Olson time zone database with an implemntation of
`tzinfo` built on top of it.  

**A pytz time zone object needs to be used properly in order to produce correct
results.**  This code does _not do the right thing_:

```py
tz = pytz.timezone("America/New_York")
t = datetime(2017, 11, 23, 15, 16, 46, tzinfo=tz)   # WRONG!
```

Instead, you _must_ use the time zone's `localize()` method to convert from
a naive to an aware datetime.

```py
tz = pytz.timezone("America/New_York")
t = tz.localize(datetime(2071, 11, 23, 15, 16, 46))  # right
```


## Delorean

The `delorean` package provides a `Delorean` time type, implemented in Python,
that wraps `datetime` to provide a more convenient API.  Only localized times
are supported; naive times and dates are not.

Delorean uses pytz for time zones, and allows you to specify the time zone by
name in its APIs.

```py
>>> Delorean(timezone="Africa/Timbuktu")
Delorean(datetime=datetime.datetime(2017, 11, 25, 22, 28, 31, 394419), timezone='Africa/Timbuktu')
```

Delorean uses
[`dateutil.parser`](http://dateutil.readthedocs.io/en/stable/parser.html) for
parsing.  It's reasonably smart and can guess the time format in many cases.

Delorean doesn't support any Python `format()` specifiers at all, but does
provide a `format_datetime()` method based on the
[Babel](http://babel.pocoo.org/en/latest/index.html) localiztion library.  Babel
doesn't use the POSIX strftime pattern syntax; instead, it has its own [pattern
synxtax](http://babel.pocoo.org/en/latest/dates.html#pattern-syntax).

```py
>>> d.format_datetime("YYYY-MM-dd hh:mm:ssZZ")
'2017-11-25 05:25:07-0500'
```

Delorean also builds in an interface to the
[humanize](https://pypi.python.org/pypi/humanize) library, for converting times
to human-friendly descriptions like "an hour ago".



## Arrow

The `arrow` package provides an `Arrow` time type, implemented in Python, that
wraps the `datetime` type to provide a more convenient API.

Has its own from-scratch localization implementation, with support for about 50
languages.


## Pendulum

The `pendulum` package provides classes that subclass those in the `datetime` to
extend their APIs.  Because Pendulum uses subclassing, its instances are drop-in
replacements for the standard `datetime` types'.

- `pendulum.Pendulum` extends `datetime.datetime`
- `pendulum.Date` extends `datetime.date`
- `pendulum.Time` extends `datetime.time`
- `pendulum.Interval` extends `datetime.timedelta`
- `pendulum.Timezone` extends `datetime.tzinfo`

Pendulum uses the pytzdata package for time zone data, but implements the time
zone data format itself.

Pendulum supports strftime-style formatting and its own JODA-style formatter for
dates and times.  It also provides a "humanized" formatting for time intervals.


## NumPy


## Pandas

Pandas is built on top of NumPy, and uses `datetime64` arrays to represent time
and date values.  Pandas extends NumPy's functionality in two major ways:

First, even though NumPy datetime64 arrays are always naive, Pandas's datetime
indexes and series can carry a time zone; all index values are localized to that
time zone.  Naive datetime indexes are also allowed.

`DatetimeIndex` instances have time zone methods `tz_localize()` and
`tz_convert()`.

```py
>>> di = pd.DatetimeIndex([ datetime.now() for _ in range(4) ]).tz_localize("America/New_York")
```

`Series` instances have these methods on a `dt` proxy attribute.

```py
>>> ser = pd.Series([ datetime.now() for _ in range(4) ]).dt.tz_localize("America/New_York")
```

A number of other time-specific functions, such as rounding and (year, month,
...) component access are also available.
   

Second, while NumPy's datetime64 arrays produce scalar values of the
`np.datetime64` type, Pandas's time series indexes and series use a custom
`Timestamp` type to represent individual values.  This type extends
`datetime.datetime` and is [implemented in
Cython](https://github.com/pandas-dev/pandas/blob/master/pandas/_libs/tslibs/timestamps.pyx).

```py
>>> ser = pd.Series([ datetime.now() for _ in range(4) ])
>>> ser
0   2017-11-26 10:29:15.875552
1   2017-11-26 10:29:15.875560
2   2017-11-26 10:29:15.875562
3   2017-11-26 10:29:15.875564
dtype: datetime64[ns]
>>> ser[0]
Timestamp('2017-11-26 10:29:15.875552')
>>> ser.values[0]
numpy.datetime64('2017-11-26T10:29:15.875552000')
```

`Timestamp` is a subclass of `datetime.datetime`; it augments the resolution to
1 ns and adds a number of convenience methods.



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
|locales            |✘       |✘       |custom  |custom  |✘       |✘       |
|humanizing         |✘       |✔       |✔       |✔       |✘       |✘       |
|memory use<sup>3</sup>|40   |220     |512     |448     |40 (single)<br>8 (bulk)|120 (single)<br>8 (bulk)|
|implementation     |C       |Python  |Python  |Python  |C       |Cython  |
|interal repr       |components|`datetime`|`datetime`|`datetime`|ticks|`datetime`+ns|

<sup>1</sup> For NumPy, we consider "datetime64[ns]" for times and "datetime64[D]" for dates.

<sup>2</sup> NumPy and Pandas represent dates as "datetime64[D]", _i.e._ times
with 1 day precision.

<sup>3</sup> **Estimates** of memory use in bytes for single time values.  See
appendix for details.  NumPy and Pandas store times as 8-byte values in
collections (NumPy arrays; Pandas indexes, series, dataframes), but single
objects consume more memory.


# Recommentations

- Choose consistent time and date reperesentations.

  If you have no need for performing temporal operations, and just need to store
  and retrieve them, stringified representations are fine.  Otherwise, choose
  the library that best meets your project's feature and performance needs, and
  use it consistently throughout.

  - For ease of use, Pendulum and Arrow are good choices.

  - For performance and compatibility, use `datetime` and `pytz`, with
    `dateutil` for additional functionality if you need it.

  - For large datasets with times, NumPy and Pandas are far more memory
    efficient.  If you use NumPy, `datetime64` is the obvious choice, though you
    will find the features to be lacking.  If you use Pandas, `Timestamp` will
    provide most of the features you need.  You may need additional libraries
    for special uses.

- Prefer UTC for stored times.

  Store UTC times whenever you wish to represent when an event happened, for
  example timestamps of log events or transactions.

- Use localized time objects.

  In almost all cases, use explicitly localized times.  If the entire
  application uses UTC only, and never converts to other time zones, this is
  optional, but still recommended for clarity.

- Use RFC 3339 formatting.

  The point of standards is that everyone should use them, despite personal
  preference.  This makes life easier for everyone.

- Use UTC for formatted timestamps in APIs. 

  Formatting a time as "2017-11-26T11:30:00-05:00" is like formatting the number
  12 as "17-5".  The UTC offset does not specify a time zone, and is not
  sufficient to equip the time with unambiguous localized date operations.

- Use time zone- and locale-aware times in UIs.

  Nontechnical users expect localized times presented in their local time zones
  and formatted to their language- and culture-specific conventions.

- Don't use times to represent dates.

  A date is a different animal; it represents a geographically specific interval
  of (usually) 24 hours.  It often has additional domain-specific meaning,
  particularl in finance.  Use a proper date representation, if available.

  Despite what some libraries may have you believe, a date is not a time, and a
  time is not a date.

- Learn how to use `datetime`, even if it's not your primary representation.

  This is the _lingua franca_ for date and time representations in Python,
  supported by nearly every library and framework that needs them, e.g. APIs,
  database drivers, and formatting tools.

- Use geographical time zones, not fixed UTC offsets. 

  Fixed UTC offsets, _e.g._ UTC-5, are _not_ the time zones you care about.  For
  correct results, you need to use greographical/political time zones, such as
  "America/New_York" or "US/Eastern".



# Benchmarks

```
get current UTC time
  0.11 µs =  1    datetime.utcnow
  0.12 µs =  1.1  udatetime.utcnow
  4.45 µs = 40.0  Delorean.utcnow
  2.38 µs = 21.4  arrow.utcnow
  7.31 µs = 65.8  pendulum.utcnow
  0.33 µs =  2.9  ns.datetime64('now', 'ns')
  5.03 µs = 45.3  pd.Timestamp.utcnow

convert time to string
  0.89 µs =  1    datetime.datetime.__str__
  0.58 µs =  0.6  udatetime.to_string
 43.05 µs = 48.2  Delorean.format_datetime
  1.79 µs =  2.0  Arrow.__str__
  2.12 µs =  2.4  Pendulum.__str__
  0.30 µs =  0.3  np.datetime64.__str__
  2.79 µs =  3.1  pd.Timestamp.__str__

convert from one time zone to another
  5.25 µs =  1    datetime.astimezone pytz
 20.61 µs =  3.9  datetime.astimezone dateutil.tz
 13.69 µs =  2.6  Delorean.shift
 20.68 µs =  3.9  Arrow.to pytz
 27.68 µs =  5.3  Arrow.to dateutil.tz
 15.46 µs =  2.9  Pendulum.in_timezone pytz
  7.47 µs =  1.4  pd.Timestamp.astimezone pytz
  7.56 µs =  1.4  pd.Timestamp.astimezone dateutil

get minute of local time
  0.13 µs =  1    datetime.minute
  0.21 µs =  1.6  Delorean.datetime.minute
  0.83 µs =  6.5  Arrow.minute
  0.16 µs =  1.3  Pendulum.minute
  0.07 µs =  0.5  Timestamp.minute

parse UTC time
 13.73 µs =  1    datetime.strptime
  1.02 µs =  0.1  udatetime.from_string
111.62 µs =  8.1  delorean.parse
 73.06 µs =  5.3  arrow.get
 23.63 µs =  1.7  pendulum.from_format
 20.64 µs =  1.5  pendulum.strptime
 16.27 µs =  1.2  pendulum.parse
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

