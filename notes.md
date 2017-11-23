# Libraries

- no library
  - string date
  - string time
  - int date
  - int time
- standard library datetime
  - implementation ([datetime.h](https://github.com/python/cpython/blob/master/Include/datetime.h))
- dateutil: 
  [code](https://github.com/dateutil/dateutil/) 
  [docs](https://dateutil.readthedocs.io/en/stable/)
  - unlocalized vs localized
- numpy `datetime64`
  - pandas
- udatetime: 
  [code](https://github.com/freach/udatetime) 
  [pypi](https://pypi.python.org/pypi/udatetime)
  - POSIX only
- Delorean:
  [code](https://github.com/myusuf3/delorean)
  [pypi](https://pypi.python.org/pypi/Delorean)
  [docs](http://delorean.readthedocs.io/en/latest/)
- Arrow
- Pendulum
  [code](https://github.com/sdispater/pendulum)
  [pypi](https://pypi.python.org/pypi/pendulum)
  [docs](https://pendulum.eustace.io/)

## Other

- tzlocal: 
  [pypi](https://pypi.python.org/pypi/tzlocal)
- pytzdata:
  [code](https://github.com/sdispater/pytzdata)



# Criteria

## Features

- date
- time
- time of day
- time zones
  - data source
  - how recent?
    - macOS 10.12.6 `/usr/share/zoneinfo` is 2017b
    - Ubuntu 17.04 `/usr/share/zoneinfo` is 2017b
- date arithmetic
- time arithmetic
- parsing and formatting
- vector operations
- calendar

## Other

- performance
- precision and range
- conceptual clarity
- API and style



# Setup

## Software

- conda
- Python 3.6.3 (conda)
- dateutil 2.6.1 (pip)
- pytz 2017.2 (conda)
- udatetime 0.0.13 (pip)
- delorean 0.6.0 (pip)
- arrow 0.10.0 (conda)
- pendulum 1.3.2 (pip)
- pytzdata 2017.3.1 (pip) for pendulum
- babel 2.5.0 (conda) for delorean
- tzlocal 1.2 (pip) for delorean


# Exercises

1. A JSON file contains a time zone name, a date, and several times of day.  
   1. Load them.
   1. Assemble them into times.
   1. Print them, sorted, in New York time zone, in ISO format.
   1. Print the time in seconds between the earliest and latest.

1. Given an iterable of ISO-formatted times, produce a histogram of the number
   of timestamps per hour.



