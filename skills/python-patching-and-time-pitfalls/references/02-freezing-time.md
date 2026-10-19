# python-patching-and-time-pitfalls §2 — Freezing time

freezegun replaces the readers of the current time for the duration of a test. The traps are in what it replaces, in
the default that time then stands still, and in the libraries that need real time. Facts here are from the README of
freezegun 1.5.5; each option is as that README describes it.

## 2.1 What is frozen
1. **While a freeze is active, these return the frozen time:** `datetime.datetime.now()`, `datetime.datetime.utcnow()`,
   `datetime.date.today()`, `time.time()`, `time.localtime()`, `time.gmtime()` and `time.strftime()`.
2. **`time.monotonic()` and `time.perf_counter()` are frozen too.** The README says they carry no guarantee about their
   absolute value, only about changes over time.
3. **Ways to apply it:** a decorator on a function, a method or a class, a context manager, or `start()` and `stop()` on
   the object. A decorator on a class that is not a `unittest.TestCase` freezes around each callable and, in the README's
   words, may not work in every case; for a `TestCase` it freezes each test along with its set-up and tear-down.
4. **Default arguments are not modified.** A default argument evaluated at definition time, such as a parameter whose
   default is today's date, keeps the real value, and freezing time later does not change it. Pass the value in, or compute
   it inside the function.

## 2.2 Time stands still unless you move it
1. **By default the frozen time does not advance.** Code that measures elapsed time, waits in a loop on a deadline or
   compares two timestamps sees zero seconds pass.
2. **Three ways to advance it, as the README describes them:**
   - `tick=True` restarts time at the given value and then lets it keep running;
   - `auto_tick_seconds=N` adds N seconds each time the clock is read (the `tick` argument is ignored when it is given);
   - the object returned by the context manager has `tick()` and `move_to()` for moving time by hand, and
     `move_to` takes a string, a date or a datetime.
3. **Prefer the manual form for a test that asserts on elapsed time.** Own guidance: a clock that moves only when the test
   says so keeps the assertion exact, where a running clock reintroduces real-time jitter.

```python
import datetime

from freezegun import freeze_time


def test_thirty_seconds_pass_on_demand():
    with freeze_time("2020-01-14 10:00:00") as clock:
        started = datetime.datetime.now()
        clock.tick(datetime.timedelta(seconds=30))
        assert datetime.datetime.now() - started == datetime.timedelta(seconds=30)
```

## 2.3 Timezone offset
1. **`tz_offset` sets the local offset from UTC,** as a number of hours or a timedelta.
2. **`utcnow()` returns the frozen value as given; `now()` is shifted by the offset.**
3. **`date.today()` uses the local time,** so it can land on a different day from the frozen UTC value. The README's
   example freezes early on the 14th of January with an offset of minus four hours and gets the 13th from `today()`.
4. **Test a date boundary on purpose.** Own guidance: freeze a time just before midnight with a non-zero offset to
   exercise the code that turns a timestamp into a day.

## 2.4 asyncio and a frozen monotonic clock
1. **The event loop reads monotonic time, and monotonic time is frozen,** so `asyncio.sleep()` and other asyncio
   functions that depend on it can stop working under a freeze. The first half is the README's statement about
   `real_asyncio`; the consequence of "stops working" is our reading of its remark that the option avoids breaking them.
2. **`real_asyncio=True` lets the event loops see real monotonic time while `time.monotonic()` stays frozen** for the code
   under test.
3. **Use it on the freeze of any async test that sleeps or awaits a timeout.**

```python
import asyncio

from freezegun import freeze_time


@freeze_time("2020-01-14", real_asyncio=True)
async def test_sleep_still_returns():
    await asyncio.sleep(1)
```

## 2.5 Packages that must see real time
1. **Some libraries break when they see frozen time.** The README lets you exclude packages for one freeze with the
   `ignore` argument, naming module prefixes, for example `threading`.
2. **Defaults:** the README lists these as ignored by default: `nose.plugins`, `six.moves`, `django.utils.six.moves`,
   `google.gax`, `threading`, `Queue`, `selenium`, `_pytest.terminal.`, `_pytest.runner.` and `gi`.
3. **`freezegun.configure(default_ignore_list=[...])` replaces that list,** so the defaults are lost unless you repeat them.
4. **`freezegun.configure(extend_ignore_list=[...])` adds to the defaults.** Use it to add one library without dropping the
   others.
5. **Add a library to the ignore list when a test that works unfrozen hangs or times out under a freeze** and the library
   uses real time internally. Own guidance: confirm by adding it to `ignore` for that one test first.
