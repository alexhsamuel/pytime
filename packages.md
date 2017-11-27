# The packages

## datetime

The datetime package, in the Python standard library, provides the standadrd
Python implementations time type:
- `datetime.datetime` for (full) time
- `datetime.date` for date
- `datetime.time` for time of day
- `datetime.timedelta` for time/date interval

While `datetime.tzinfo` specifies the interface for time zone objects, it
provides no concrete implementations.  Other packages are required for time zone
support.

Under the hood, these types are implemented as C extension functions, and
perform very well.  The time and date types reprent values as year, month, date,
hour, minute, second, microsecond components.


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



