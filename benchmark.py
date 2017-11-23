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

def time(fn, label, samples=20, n=5000, quantile=0.05, unit=None):
    # Loop pedestal calculation.
    # FIXME: Do this outside?
    elapsed = []
    for _ in range(samples):
        start = perf_counter()
        for _ in range(n):
            pass
        elapsed.append(perf_counter() - start)
    null = np.percentile(elapsed, 100 * quantile, interpolation="nearest")
    # print("pass elapsed: {:6.2f} µs".format(elapsed / n / 1E-6))
    
    elapsed = []
    for _ in range(samples):
        start = perf_counter()
        for _ in range(n):
            fn()
        elapsed.append(perf_counter() - start)
    
    elapsed = np.percentile(elapsed, 100 * quantile, interpolation="nearest")
    elapsed -= null
    print("{:6.2f} µs ".format(elapsed / n / 1E-6), end="")
    if unit is None:
        print("         ", end="")
    else:
        mult = 1 if unit is True else elapsed / unit
        print("= {:5.2f}  ".format(mult), end="")
    print(label)
    return elapsed


#-------------------------------------------------------------------------------

if True:
    print("get current UTC time")

    time(lambda: None, "null")

    u = time(datetime.utcnow, "datetime.utcnow", unit=True)

    time(udatetime.utcnow, "udatetime.utcnow", unit=u)

    time(delorean.Delorean.utcnow, "Delorean.utcnow", unit=u)

    time(arrow.utcnow, "arrow.utcnow", unit=u)

    time(pendulum.utcnow, "pendulum.utcnow", unit=u)

    time(lambda: np.datetime64("now", "ns"), "ns.datetime64('now', 'ns')", unit=u)

    time(pd.Timestamp.utcnow, "pd.Timestamp.utcnow", unit=u)

    time(cron.now, "cron.now", unit=u)

    print()


if True:
    print("convert time to string")

    def none():
        pass
    time(lambda: none(), "null")

    x = datetime.utcnow()
    f = x.__str__
    u = time(lambda: f(), "datetime.datetime.__str__", unit=True)

    f = udatetime.to_string
    time(lambda: f(x), "udatetime.to_string", unit=u)

    x = delorean.Delorean.utcnow()
    f = x.format_datetime
    time(lambda: f("YYYY-mm-ddTHH:MM:SSZ"), "Delorean.format_datetime", unit=u)

    x = arrow.utcnow()
    f = x.__str__
    time(lambda: f(), "Arrow.__str__", unit=u)

    x = pendulum.utcnow()
    f = x.__str__
    time(lambda: f(), "Pendulum.__str__", unit=u)

    x = np.datetime64("now", "ns", unit=u)
    f = x.__str__
    time(lambda: f(), "np.datetime64.__str__", unit=u)

    x = pd.Timestamp.utcnow()
    f = x.__str__
    time(lambda: f(), "pd.Timestamp.__str__", unit=u)

    x = cron.now()
    f = x.__str__
    time(lambda: f(), "cron.Time.__str__", unit=u)

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
    u = time(lambda: f(z1), "datetime.astimezone pytz", unit=True)

    z0 = dateutil.tz.gettz("America/New_York")
    x = datetime.now().replace(tzinfo=z0)
    z1 = dateutil.tz.gettz("Asia/Tokyo")
    f = x.astimezone
    time(lambda: f(z1), "datetime.astimezone dateutil.tz", unit=u)

    x = delorean.Delorean.now("America/New_York")
    f = x.shift
    time(lambda: f("Asia/Tokyo"), "Delorean.shift", unit=u)

    x = arrow.now()
    z1 = pytz.timezone("Asia/Tokyo")
    f = x.to
    time(lambda: f(z1), "Arrow.to pytz", unit=u)

    x = arrow.now()
    z1 = dateutil.tz.gettz("Asia/Tokyo")
    f = x.to
    time(lambda: f(z1), "Arrow.to dateutil.tz", unit=u)

    x = pendulum.now()
    z1 = pytz.timezone("Asia/Tokyo")
    f = x.in_timezone
    time(lambda: f(z1), "Pendulum.in_timezone pytz", unit=u)
    
    # x = pendulum.now()
    # z1 = dateutil.tz.gettz("Asia/Tokyo")
    # f = x.in_timezone
    # time(lambda: f(z1), "Pendulum.in_timezone dateutil.tz", unit=u)
    
    x = pd.Timestamp.now("America/New_York")
    z1 = pytz.timezone("Asia/Tokyo")
    f = x.astimezone
    time(lambda: f(z1), "pd.Timestamp.astimezone pytz", unit=u)

    x = pd.Timestamp.now("America/New_York")
    z1 = dateutil.tz.gettz("Asia/Tokyo")
    f = x.astimezone
    time(lambda: f(z1), "pd.Timestamp.astimezone dateutil", unit=u)

    x = cron.now()
    z = cron.TimeZone("Asia/Tokyo")
    f = cron.to_local
    time(lambda: f(x, z), "cron.to_local", unit=u)

    x = cron.now()
    z = cron.TimeZone("Asia/Tokyo")
    time(lambda: x @ z, "cron @", unit=u)

    print()


if True:
    print("get minute of local time")

    def none():
        pass
    time(lambda: none(), "null")
    
    z = pytz.timezone("America/New_York")
    x = z.localize(datetime.now())
    u = time(lambda: x.minute, "datetime.minute", unit=True)

    x = delorean.Delorean.now("America/New_York")
    time(lambda: x.datetime.minute, "Delorean.datetime.minute", unit=u)

    x = arrow.now("America/New_York")
    time(lambda: x.minute, "Arrow.minute", unit=u)

    x = pendulum.now("America/New_York")
    time(lambda: x.minute, "Pendulum.minute", unit=u)

    x = cron.now()
    z = cron.TimeZone("America/New_York")
    time(lambda: (x @ z).daytime.minute, "cron @ .daytime.minute", unit=u)

    print()


