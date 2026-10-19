# typescript-patterns §7 — Trust boundaries, serialisation and dates

> Section 7 of `skills/typescript-patterns`. Read it when data arrives from the network, storage, the URL,
> the environment, a message or a file; when a value is copied or serialised; or when a date, an instant or a
> time zone is handled. The other sections and the guardrails stay in `SKILL.md`.

1. **Data from outside is `unknown` until a schema has parsed it.** Anything that crosses a trust boundary
   (a response body, a stored value, a query parameter, an environment variable, a message from another
   window or worker, a file) has the type the sender promised, not the type it has. It is parsed once, at the
   edge, by a schema validator, and the rest of the code receives the typed result. The schema is the single
   source: the static type is inferred from it, so the validator and the type cannot disagree.
2. **An assertion on boundary data is a lie told to the compiler.** `as User` on a parsed response compiles
   and does nothing; the first missing field fails somewhere far from the cause. A hand-written type guard is
   the same promise (§4, point 6). The assertion this block permits for `JSON.parse` (§1, point 2) is a
   transition state: the parse result is then handed to the schema immediately.
3. **Configuration is read once, at startup, into a typed object.** The environment is parsed and validated
   in one module that fails the process with the names of the missing or malformed variables, and the rest of
   the code imports the typed object instead of reading the environment. A variable read ad hoc in the middle
   of a function fails in production on the path nobody exercised.
4. **A failed operation signals failure one way per layer.** Either it throws a typed error that a boundary
   catches, or it returns a result union with the success and the failure as variants; mixing both in one
   layer makes callers handle each function differently. Whichever the layer picks, the failure carries a
   code a caller can branch on, and a default value is never returned in place of an error
   (`skills/gate`, step 6).
5. **Request and response types derive from one source.** The type of what the client sends and the type of
   what it receives come from the same schema or the same generated definitions as the server's (§6,
   point 11); a hand-copied interface drifts at the first field rename.
6. **Copying is shallow unless said otherwise.** The spread operator and `Object.assign` copy one level, so
   a nested object is still shared. A deep copy uses `structuredClone`, which handles dates, maps, sets and
   cycles but not functions or class prototypes; a state update that replaces only the changed path
   (§3) is usually what is wanted, not a deep copy.
7. **Serialisation is a conversion, with a defined format.** A date goes over the wire as an ISO-8601 string
   in UTC and is parsed back at the edge into a date type; a large integer as a string; a map or set as an
   array of entries; a class instance as a plain object built by an explicit method. The default JSON
   behaviour for these types is lossy or throws.
8. **Dates use the Temporal types where the runtime has them.** The legacy `Date` object is mutable,
   counts months from zero, interprets a date-only string as UTC and a date-time string as local time, and
   cannot represent a named time zone. The Temporal types separate an instant, a calendar date, a wall-clock
   time and a zoned date-time, make arithmetic explicit and immutable, and take the time zone as a parameter.
   Where the target runtime lacks them, use the standard polyfill and keep the code written against its
   API, so the polyfill can be dropped; reach for a date library only when neither is possible.
9. **The user's time zone is explicit.** An instant is stored and compared in UTC; a calendar date with no
   time (a birthday, a due date) is stored as a date, not as midnight in some zone; display converts to the
   user's zone and locale at the last moment; "today", "start of day" and "the next 24 hours" are computed
   in the zone of the person asking. A server computing "today" in its own zone is wrong for the user for
   several hours a day.
10. **The current time is a dependency.** Code that decides on "now" takes a clock as a parameter or a
    module-level provider that tests can replace; a function that calls the system clock inside is tested by
    luck or at midnight.
11. **Equality of dates compares values.** Two date objects are equal when their instants are, which the
    strict-equality operator never says; compare through the type's own comparison method or the underlying
    numeric value, and never use a date as a map key without converting it.
