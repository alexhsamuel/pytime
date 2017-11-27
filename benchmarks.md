# Benchmarks

Below are microbenchmark results for several common time operations.

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

The usual warnings about interpreting microbenchmark results apply here.  See
the appendix for details.


