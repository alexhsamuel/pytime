from aslib.timing import call_timer
import cron
from datetime import datetime
import udatetime
import delorean
import arrow
import pendulum

TIMER = call_timer(10000)

def time(fn, label):
    result = TIMER(fn)
    print("{:6.2f} µs  {}".format(result["time"] * 1E6, label))



time(lambda: None, "null")
time(datetime.utcnow, "datetime.utcnow")
time(udatetime.utcnow, "udatetime.utcnow")
time(delorean.Delorean.utcnow, "Delorean.utcnow")
time(arrow.utcnow, "arrow.utcnow")
time(pendulum.utcnow, "pendulum.utcnow")
time(cron.now, "cron.now")

