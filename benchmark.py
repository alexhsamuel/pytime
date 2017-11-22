from time import perf_counter
from datetime import datetime
import pytz
import dateutil.tz
import numpy as np
import pandas as pd
import udatetime
import delorean
import arrow
import pendulum
import cron

def time(fn, label, n=100000, warmup=1000):
    for _ in range(warmup):
        fn()

    start = perf_counter()
    for _ in range(n):
        fn()
    elapsed = perf_counter() - start
    
    print("{:6.2f} µs  {}".format(elapsed / n * 1E6, label))


def time(fn, label, samples=20, n=1000, quantile=0):
    elapsed = []
    for _ in range(samples):
        start = perf_counter()
        for _ in range(n):
            fn()
        elapsed.append(perf_counter() - start)
    
    elapsed = np.percentile(elapsed, 100 * quantile, interpolation="nearest")
    print("{:6.2f} µs  {}".format(elapsed / n * 1E6, label))


#-------------------------------------------------------------------------------

if True:
    print("get current UTC time")

    time(lambda: None, "null")

    time(datetime.utcnow, "datetime.utcnow")

    time(udatetime.utcnow, "udatetime.utcnow")

    time(delorean.Delorean.utcnow, "Delorean.utcnow")

    time(arrow.utcnow, "arrow.utcnow")

    time(pendulum.utcnow, "pendulum.utcnow")

    time(lambda: np.datetime64("now", "ns"), "ns.datetime64('now', 'ns')")

    time(pd.Timestamp.utcnow, "pd.Timestamp.utcnow")

    time(cron.now, "cron.now")

    print()


if True:
    print("convert time to string")

    def none():
        pass
    time(lambda: none(), "null")

    x = datetime.utcnow()
    f = x.__str__
    time(lambda: f(), "datetime.datetime.__str__")

    f = udatetime.to_string
    time(lambda: f(x), "udatetime.to_string")

    x = delorean.Delorean.utcnow()
    f = x.format_datetime
    time(lambda: f("YYYY-mm-ddTHH:MM:SSZ"), "Delorean.format_datetime")

    x = arrow.utcnow()
    f = x.__str__
    time(lambda: f(), "Arrow.__str__")

    x = pendulum.utcnow()
    f = x.__str__
    time(lambda: f(), "Pendulum.__str__")

    x = np.datetime64("now", "ns")
    f = x.__str__
    time(lambda: f(), "np.datetime64.__str__")

    x = pd.Timestamp.utcnow()
    f = x.__str__
    time(lambda: f(), "pd.Timestamp.__str__")

    x = cron.now()
    f = x.__str__
    time(lambda: f(), "cron.Time.__str__")

    print()


if True:
    print("convert from one time zone to another")

    def none():
        pass
    time(lambda: none(), "null")
    
    z0 = pytz.timezone("America/New_York")
    x = z0.localize(datetime.now())
    z1 = pytz.timezone("Asia/Tokyo")
    f = x.astimezone
    time(lambda: f(z1), "datetime.astimezone pytz")

    z0 = dateutil.tz.gettz("America/New_York")
    x = datetime.now().replace(tzinfo=z0)
    z1 = dateutil.tz.gettz("Asia/Tokyo")
    f = x.astimezone
    time(lambda: f(z1), "datetime.astimezone dateutil.tz")

    x = delorean.Delorean.now("America/New_York")
    f = x.shift
    time(lambda: f("Asia/Tokyo"), "Delorean.shift")

    x = arrow.now()
    z1 = pytz.timezone("Asia/Tokyo")
    f = x.to
    time(lambda: f(z1), "Arrow.to pytz")

    x = arrow.now()
    z1 = dateutil.tz.gettz("Asia/Tokyo")
    f = x.to
    time(lambda: f(z1), "Arrow.to dateutil.tz")

    x = pendulum.now()
    z1 = pytz.timezone("Asia/Tokyo")
    f = x.in_timezone
    time(lambda: f(z1), "Pendulum.in_timezone pytz")
    
    # x = pendulum.now()
    # z1 = dateutil.tz.gettz("Asia/Tokyo")
    # f = x.in_timezone
    # time(lambda: f(z1), "Pendulum.in_timezone dateutil.tz")
    
    x = pd.Timestamp.now("America/New_York")
    z1 = pytz.timezone("Asia/Tokyo")
    f = x.astimezone
    time(lambda: f(z1), "pd.Timestamp.astimezone pytz")

    x = pd.Timestamp.now("America/New_York")
    z1 = dateutil.tz.gettz("Asia/Tokyo")
    f = x.astimezone
    time(lambda: f(z1), "pd.Timestamp.astimezone dateutil")

    x = cron.now()
    z = cron.TimeZone("Asia/Tokyo")
    f = cron.to_local
    time(lambda: f(x, z), "cron.to_local")

    x = cron.now()
    z = cron.TimeZone("Asia/Tokyo")
    time(lambda: x @ z, "cron.__matmul__")

    print()


if True:
    print("get minute of local time")

    z = pytz.timezone("America/New_York")
    x = z.localize(datetime.now())
    time(lambda: x.minute, "datetime.datetime.minute")

    x = delorean.Delorean.now("America/New_York")
    time(lambda: x.datetime.minute, "Delorean.datetime.minute")

    x = arrow.now("America/New_York")
    time(lambda: x.minute, "Arrow.minute")

    x = pendulum.now("America/New_York")
    time(lambda: x.minute, "Arrow.minute")

    x = cron.now()
    z = cron.TimeZone("America/New_York")
    time(lambda: (x @ z).daytime.minute, "cron @ .daytime.minute")

    print()


