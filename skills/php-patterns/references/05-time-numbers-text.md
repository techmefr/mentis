# § 5 — Time, numbers and text

> Section 5 of `skills/php-patterns`. Read it when a date, a money amount, a numeric input or a
> non-ASCII string is handled. These are the three value kinds where a plausible-looking line is wrong
> only for some of the data.

1. **`DateTimeImmutable`, never `DateTime`.** `DateTime::modify()` and `->add()` mutate the object in
   place and *also* return it, so a date passed to a helper comes back changed for every other holder of
   that object — the caller's "start of the month" quietly becomes the end of it. The immutable class
   has the same API and returns a new instance, which is why it is the default and the mutable one is the
   special case.
2. **A date with no timezone uses the ini default, which is a property of the server.** So the same code
   gives a different day in a different environment, and a container that was rebuilt with a different
   default silently shifts every boundary in the app. Store and compute in UTC, attach the intended zone
   explicitly, and convert only at the edge where a human reads it.
3. **A day and a moment are different values.** Comparing a date-only value against a timestamp puts the
   date at midnight, so "everything up to today" excludes everything that happened today, and a report
   that looks right on a small dataset is short by one day's rows in production. Decide which of the two
   a column and a parameter hold, and make the comparison inclusive on purpose.
4. **A day is not 86,400 seconds, and a month has no fixed length.** Across a DST change, adding a day's
   worth of seconds lands at the wrong hour; adding one month to 31 January gives 3 March, because
   PHP normalises the overflow rather than clamping it. Add calendar units for calendar intent, seconds
   for elapsed time, and check the month-end case explicitly — it is the one a monthly job hits four
   times a year.
5. **Floats do not hold decimal values exactly, so `0.1 + 0.2 !== 0.3`.** Never compare floats with
   `===` — compare against a tolerance, or don't use floats. The visible consequence is a total that is
   off by a cent, a sum that fails to match, and a condition that is false on the one input a human
   checked by hand.
6. **Money is an integer of minor units or a decimal string, never a float.** Whichever you pick, the
   rounding rule is a decision that has to be written down: PHP's `round()` is half-up by default, and
   the difference from banker's rounding shows up as a systematic bias over thousands of lines, not as
   a visible bug. `bcmath` is the standard-library answer for decimal arithmetic on strings.
7. **Integer overflow becomes a float silently.** `PHP_INT_MAX + 1` is a float, and a float above 2^53
   cannot represent consecutive integers — so arithmetic on large ids or accumulated cents starts
   returning values that are close and wrong, with no error anywhere. Keep large identifiers as strings
   unless they are actually being computed with.
8. **Division by zero throws in PHP 8, and there are three behaviours to choose between.** `/` and `%`
   raise a `DivisionByZeroError`, `intdiv` raises the same, and `fdiv` returns `INF`/`NAN` instead.
   Guard the denominator where zero is a legitimate input — an average over an empty set is the usual
   one — rather than letting a 500 stand in for "no data yet".
9. **A numeric string from input is not a number until it is validated.** `(int) "12abc"` is `12`,
   `"1e3"` compares equal to `1000`, and a leading `+`, a space or a locale's comma decimal separator
   all cast to something. Validate with `filter_var` or `ctype_digit` and reject, then cast — casting
   first means the invalid input has already become a plausible number.
10. **Strings are bytes, and the core string functions count bytes.** `strlen` on a UTF-8 string returns
    its byte length, and `substr` truncating a name at 20 bytes can cut a multi-byte character in half.
    The result is not just a wrong character count: an invalid UTF-8 string makes `json_encode` return
    `false`, so the response body is empty and the error is reported nowhere near the truncation. Use
    the `mb_*` functions with an explicit encoding for anything a human typed.
11. **`json_encode` and `json_decode` fail by return value unless told otherwise.** Invalid UTF-8, a
    structure deeper than the depth limit, `NAN`, or a recursive reference all produce `false`/`null` —
    which the caller then passes on as if it were an empty payload. Pass `JSON_THROW_ON_ERROR` so a
    serialisation failure is a failure, and set the depth deliberately where the data is nested.
12. **Case-insensitive comparison of non-ASCII text needs the multi-byte functions.** `strtolower` works
    byte by byte, so accented characters are left alone and two spellings that a reader would call the
    same string compare as different — which turns into a duplicate account, a failed lookup, or a
    deduplication that quietly keeps both. Normalise with an explicit encoding, and normalise on the way
    in rather than at each comparison.
13. **Comparing a secret with `===` leaks its length and its prefix through timing.** Use
    `hash_equals` for a token, a signature or an API key. And a password is never hashed with a hash
    function: `password_hash`/`password_verify` exist because the algorithm, the salt and the cost have
    to be stored with the hash and upgraded over time.
14. **Anything a person should not be able to guess comes from `random_int`/`random_bytes`.** `rand`,
    `mt_rand`, `shuffle`, `array_rand` and `uniqid` are predictable — `uniqid` is derived from the
    clock — so a token, a password-reset link, a filename that must not be enumerable or an invitation
    code built from them is guessable by anyone who watches a few of them. The cryptographic functions
    cost nothing extra here.
15. **`createFromFormat` normalises an impossible day, and reports it as a warning rather than an
    error.** `'!Y-m-d'` against `2026-02-30` does not return `false`: it returns a valid object holding
    2026-03-02, and `getLastErrors()` gives `warning_count: 1` with `error_count: 0` — so the `=== false`
    check §2.9 teaches passes it, and so does a guard on the error count. Point 4 states this
    normalisation for arithmetic; parsing is where it bites first, because an invalid day almost always
    arrives from outside. Round-trip the result — `$parsed->format('Y-m-d') !== $input` — or `checkdate`
    before parsing.
16. **A `DateInterval`'s `days` is unsigned; the direction is in `invert`.** `$from->diff($to)->days` is
    the same number whether `$to` is three days ahead of `$from` or three days behind it, so a "days
    remaining" reads correctly on every fixture built in the expected order and becomes "days overdue"
    with the same figure on the screen for the rows in the other one. Use `format('%r%a')` where the
    sign matters, or read `invert` explicitly.
