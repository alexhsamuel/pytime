# Recommendations

These are the author's personal opinions.

- Choose consistent time and date reperesentations.

  If you have no need for performing temporal operations, and just need to store
  and retrieve them, stringified representations are fine.  Otherwise, choose
  the library that best meets your project's feature and performance needs, and
  use it consistently throughout.

- For ease of use, Pendulum is a good choice.

  Pendulum has tons of features, a solid API, and clear documentation.
  Advantages over Delorean and Arrow: it provides additional types for dates,
  time of day, intervals, etc.; and its types subclass the corresponding
  `datetime` types, so can be used interchangably.

  Arrow is a solid second choice, if you don't care about date
  handling&mdash;since it does not provide a date type.  Delorean lags in
  features and performance.

- For performance and compatibility, use `datetime`.

  The implementation is highly optimized for single values.  The feature set is
  bare-bones; you'll almost certainly need additional packages to fill feature
  gaps:

  - pytz is the faster time zone implementation, but dateutil.tz is a fine
    choice if you use its other functionality.  Note the API differences.

  - udatetime accellerates some operations, most notably string parsing.

  - Babel provides locale-specific formatting.

  - Humanize provides human-friendly representations.

- For large data sets, use Pandas.

  For large datasets with times, Pandas is far more memory efficient.  Its
  `Timestamp` scalar type will provide most of the features you need; you may
  need additional libraries for special uses.

  If you already use NumPy heavily, `datetime64` is the obvious choice, though
  its features are severely lacking.  You may have to wrap or reimplement some
  of these yourself.

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

- Use geographical time zones, not fixed UTC offsets. 

  Fixed UTC offsets, _e.g._ UTC-5, are _not_ the time zones you care about.  For
  correct results, you need to use greographical/political time zones, such as
  "America/New_York" or "US/Eastern".

  For the same reason, use UTC for formatted timestamps in APIs.  Formatting a
  time as "2017-11-26T11:30:00-05:00" is a bit like formatting the number 16 as
  "11-5".  The UTC offset does not specify a time zone, and is not sufficient to
  equip the time with unambiguous localized date operations.

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



