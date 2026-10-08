# python-hygiene-pitfalls §2 — Logs and error messages

A log line and an exception message are read at the worst moment, by someone who was not there. Both rules
below are about what that reader can trust and search for.

## 2.1 Log with a literal pattern and arguments
1. **Call the logging function with a string literal as the first argument and the values as further
   arguments:** `logger.info("Current path is: %s", path)`. Do not pass an f-string or the result of
   `.format()`.
2. **Two reasons, both from the sources.** Formatting is deferred until a handler actually emits the
   record, so a message below the configured level costs no formatting (the Ruff documentation, G004, makes
   the same point about eager formatting). And some logging systems collect the unexpanded pattern as a
   queryable field, which lets you group every occurrence of one message regardless of its values.
3. **Prefer the structured form your logger offers for values you will filter on** (the `extra` mapping, or
   key-value fields in a structured logger), over interpolating them into text.

## 2.2 An error message states the true condition
Applies to messages on exceptions and messages shown to a user. Three requirements, from the Google style
guide: the message matches the actual error condition, interpolated pieces are clearly identifiable as such,
and it supports simple automated processing such as `grep`.

1. **The condition tested is the condition reported.** The guide's example: a probability check written as
   `p < 0 or p > 1` is false for NaN, so NaN passes it; `not 0 <= p <= 1` rejects it. Write the positive
   range and negate it.
2. **Do not assert a cause you did not observe.** After catching an `OSError` from a delete, a message
   saying the directory "already was deleted" assumes a reason the exception did not give; report the
   operation, the object and the actual error.
3. **Mark interpolated values** (`{p=}`, `%r`, or quotes) so a value that is empty, contains spaces or reads
   like part of the sentence is still recognisable. A directory called `deleted` in "The %s directory could
   not be deleted" produces a sentence that misleads.
4. **Keep the fixed text greppable:** one stable sentence per failure, with the variable parts after it,
   not woven through it.
5. **Catching `Exception` to log and continue is a separate rule** (`python-no-bare-except`).

## Verification
- A test calls the check with NaN, the boundary values and a value just outside, and the message names the
  value received.
- A grep for the fixed part of a message finds exactly one raise site.
- No log call in the diff passes an f-string or `.format()` result as its first argument.
