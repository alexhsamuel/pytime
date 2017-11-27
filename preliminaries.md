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


