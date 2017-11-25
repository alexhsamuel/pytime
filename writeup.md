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

Intead, you _must_ use the time zone's `localize()` method to convert from
a naive to an aware datetime.

```py
tz = pytz.timezone("America/New_York")
t = tz.localize(datetime(2071, 11, 23, 15, 16, 46))  # right
```


## Delorean

Uses pytz for time zones.

Uses [`babel.dates`](http://babel.pocoo.org/en/latest/api/dates.html) for
formatting.

Uses [`dateutil.parser`](http://dateutil.readthedocs.io/en/stable/parser.html)
for parsing.



## Arrow

Has its own from-scratch localization implementation, with support for about 50
languages.


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


# Feature matrix

|                           |datetime|Delorean|Arrow   |Pendulum|numpy   |Pandas  |
|---------------------------|:------:|:------:|:------:|:------:|:------:|:------:|
|naive time                 |✔       |?       |?       |?       |?       |?       |
|localized time             |✔       |?       |?       |?       |?       |?       |
|date                       |✔       |?       |?       |?       |?       |?       |
|time of day                |✔       |?       |?       |?       |?       |?       |
|time range                 |1-9999  |?       |?       |?       |?       |?       |
|date range                 |1-9999  |?       |?       |?       |?       |?       |
|time resolution            |1 µs    |1 µs    |1 µs    |1 µs    |1 ns    |1 ns    |
|rounding                   |        |?       |?       |?       |?       |?       |
|locales                    |        |?       |?       |?       |?       |?       |
|humanizing                 |        |?       |?       |?       |?       |?       |
|TEMPLATE                   |?       |?       |?       |?       |?       |?       |

For numpy, we consider "datetime64[ns]" for times and "datetime64[D]" for dates.


# Recommentations

- Choose consistent time and date reperesentations.

  If you have no need for performing temporal operations, and just need to store
  and retrieve them, stringified representations are fine.  Otherwise, choose
  the library that best meets your project's feature and performance needs, and
  use it consistently throughout.

  - For ease of use, Pendulum and Arrow are good choices.

  - For performance and compatibility, use `datetime` and `pytz`, with
    `dateutil` for additional functionality if you need it.

  - If you use numpy heavily, `datetime64` is the obvious choice, though you
    will find the features to be lacking.

  - If you use Pandas, `Timestamp` will provide most of the features you need.
    You may need additional libraries for special uses.

- Prefer UTC for stored times.

  Store UTC times whenever you wish to represent when an event happened, for
  example timestamps of log events or transactions.  

- Use RFC 3339 formatting.

  The point of standards is that everyone should use them, despite personal
  preference.  This makes life easier for everyone.

- Use localized times in UIs.

  Nontechnical users expect localized times formatted to their language- and
  culture-specific conventions.

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


