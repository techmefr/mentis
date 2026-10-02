# § 4 — Schema-first RPC: protobuf and gRPC

> Section 4 of `skills/api-design`. Read it when the contract is a `.proto` file and the transport is gRPC (or
> any protobuf-over-HTTP): a message or service is added, a field is changed or removed, a deadline or a retry
> policy is chosen, or a status code has to be picked. The general rules (contract-first §1, what an interface
> exposes §2, extension rather than breakage §3) apply unchanged; this section is what they become when the
> schema is also a wire format. Stamped against sources read 2026-10-02 (see `references/origin.md`).

## Evolving a schema

1. **A tag number is spent forever.** Never reuse one, even for a field "nobody ever used": a serialized
   message from a log, a queue or an old binary still carries the old meaning, and the new reader will
   decode it as the wrong thing without any error. A tag is identity on the wire, the field name is only a
   label for humans.
2. **When a field or an enum value is deleted, reserve its number and its name.** The reservation costs one
   line, needs no type (so it can even trim a dependency) and turns the later accidental reuse into a compile
   error instead of a data-corruption incident. Reserving the name too stops a re-added field from silently
   inheriting the JSON key of the deleted one.
3. **Do not change the type of a field.** Some pairs happen to parse each other's bytes, and that is exactly
   why it looks safe; the generated code changes, the rollout is two-sided (clients and servers are never
   updated at the same instant, and one of them can be rolled back), and the day it breaks is the day of the
   rollback. The move is a new field with a new number and a migration.
4. **Do not change a default, and do not go from repeated to scalar.** A changed default makes a client and a
   server whose builds straddle the change read the same unset field differently. Repeated to scalar loses
   data: in a JSON mapping a mismatch of repeatedness drops the whole message, in the binary form the last
   value wins or the whole field vanishes depending on the type.
5. **No required fields.** A field that is obviously mandatory today may have to become absent in four years
   (an id that migrates to a structured type), and a schema-level `required` turns that into an unparseable
   message, especially for a middle server that only forwards what it does not read. Say "required" in the
   field's documentation, validate it at the boundary (§1.2), and keep the wire format permissive.
6. **Every enum starts with a zero value named `*_UNSPECIFIED`, and that value carries no meaning.** It is what
   an old reader sees when a new value arrives and what an unset field reads as; if it means something real
   ("standard", "active") then "I do not know" and "standard" are the same bytes. Prefix every value with the
   enum's name in upper snake case: enum values are scoped by their parent, not by the enum, so two enums in
   one package that both define `SET` do not compile, and when the collision spans files the compiler may not
   catch it at all. Number values densely, and leave a gap only where a value was removed (and reserved).
7. **Add a new enum alias last, and remove the old name in three steps.** Add the new name under the old one
   and deprecate the old; once every parser knows the new name, swap the order so serializers start emitting
   it; once every serializer has that version, delete the old one. Anything shorter has a window where one
   side writes a name the other cannot read. Better still: do not put the name on the wire at all (point 10).
8. **A boolean is only for something that will be two-valued for all time.** A flag that is "is it a GIF" today
   is "which format" next year, and a bool cannot grow. An enum with two values costs nothing now and spares a
   breaking migration later.
9. **Use the shared types for time, duration, money, dates and field masks.** A `timeout_millis` integer or a
   `seconds_since_epoch` integer is a unit and an epoch every consumer has to guess (§1.9); the timestamp,
   duration, date, time-of-day, money, interval and field-mask types exist so that nobody has to. The
   well-known ones ship with the compiler; the "common types" (money, date, postal address) come from a
   separate schema repository and need a declared dependency.
10. **Binary on the wire, text only for humans.** Text format and the JSON mapping carry field and enum names as
    strings, so a rename or an addition breaks an old parser, and a protobuf exposed as JSON to the public can
    never rename anything. Keep JSON as an edge translation if consumers need it, and treat every name in it
    as permanent (§2.2).
11. **Never rely on byte-for-byte serialization.** The encoding is not canonical and is not stable across
    builds of the same binary, so it must not be hashed into a cache key, a signature or a deduplication id.
    Derive those from the fields.
12. **Prefer extensions to `Any` where the set of types is known to you.** `Any` is for infrastructure that
    must carry arbitrary messages it cannot enumerate; for anything else it trades type information for
    flexibility nobody asked for, and moves the error from the compiler to the consumer.
13. **Keep API messages and storage messages apart**, even when they are identical on day one. The needs of a
    live contract and of a stored record diverge, and one shared type means a storage migration is an API
    change (§2.1). The translation layer is a cost that pays back the first time storage changes.
14. **One top-level entry point per file.** A file that exports one message, enum, service or extension moves
    when the code does and drags in few transitive imports; a file with twenty messages cannot be moved
    without extracting them. Types meant for reuse outside the project get their own dependency-free file;
    nested types are private to their parent and are not vocabulary for others.

## Names and files

15. Files are `lower_snake_case.proto`. Messages, enums and services are `TitleCase`; fields and oneofs are
   `lower_snake_case`; enum values are `UPPER_SNAKE_CASE`; methods are `TitleCase`. Repeated fields take a
   plural name. Abbreviations count as one word (`GetDnsRequest`, not `GetDNSRequest`).
16. **An underscore is followed by a letter, never by a digit or a second underscore, and never starts or ends
   a name.** Generated code converts the same identifier to the local style of each language, and two names
   that differ only by an underscore before a digit collapse into one in some of them. `XYZ_V2`, not `XYZ_2`.
17. **The proto package is short, lowercase, dotted, and independent of the directory and of the language.**
   Do not write a Java-style reverse-domain package in the schema; set the language-specific package option
   separately, and derive it from the proto package so that two files with different packages can never map
   to the same generated namespace.
18. **Avoid field and oneof names that clash with generated accessors:** the prefixes `has_`, `get_`, `set_`,
   `clear_`, the suffix `_value`, `descriptor`, and the keywords of any language that reads the schema. The
   failure is a build break in one language, found by the team that adopts the schema last.
19. **Service methods follow a request/response pair per method**, named for the operation, with distinct
   message types even when two methods currently take the same fields: reusing one request type across methods
   welds their evolution together.

## Calls: deadlines, cancellation, retries, errors

20. **Every client call sets a deadline.** The default is none, which means a client can wait forever for a
   server that is gone, holding a thread, a connection and whatever sits behind them. Pick the value from what
   you know of the system, then confirm it under load; a deadline nobody measured is a guess with a timeout's
   authority.
21. **The server stops working when the call is cancelled or its deadline passes.** The library cancels the call
   but cannot interrupt the handler: a long-running handler checks for cancellation at its own loop boundaries
   and cancels the downstream calls it started, or it keeps consuming resources for a result nobody will read.
22. **A deadline propagates down a call chain, as a remaining timeout and not as a wall-clock time.** Passing
   the absolute instant across machines makes it depend on their clocks; the transport converts it into the
   time left, and a service that calls another one should inherit that rather than invent a fresh one per hop.
   Some stacks do it by default and some need it switched on: check which yours is.
23. **Pick the status code by what the caller should do next.** `INVALID_ARGUMENT` is wrong whatever the state of
   the system; `FAILED_PRECONDITION` is wrong until the state is fixed and must not be retried until then;
   `OUT_OF_RANGE` is a problem that a state change can cure (reading past the end of what exists); `ABORTED`
   means retry at a higher level (a failed test-and-set, a transaction to restart); `UNAVAILABLE` means retry
   this very call. The three-way split between `UNAVAILABLE`, `ABORTED` and `FAILED_PRECONDITION` is the one
   most often collapsed into `INTERNAL`, and the collapse removes the only information a client has.
24. **`PERMISSION_DENIED` is for authenticated callers who may not do this; `UNAUTHENTICATED` is for missing or
   invalid credentials; neither is for quota** (`RESOURCE_EXHAUSTED`). When a whole class of callers must not
   learn that a resource exists, `NOT_FOUND` is the correct answer for the class, while denial to some members
   of a class that can see the resource is `PERMISSION_DENIED`.
25. **The library generates a subset of the codes; user code owns the rest.** Codes like `INVALID_ARGUMENT`,
   `NOT_FOUND`, `ALREADY_EXISTS`, `FAILED_PRECONDITION`, `ABORTED`, `OUT_OF_RANGE` and `DATA_LOSS` are produced
   only by application code, which is why seeing one at a client means the application said it. Return a
   library-generated code (such as `UNAVAILABLE`) from the application only when it is true.
26. **Retry only what is safe to repeat, and say so per method.** There is no retry policy by default, and gRPC
   only retries the failures it can prove never reached the application. A policy is configured per method with
   a maximum number of attempts, an exponential backoff (jittered by the library) and the set of retryable
   codes, normally `UNAVAILABLE` alone. `DEADLINE_EXCEEDED`, `CANCELLED`, `INVALID_ARGUMENT` and `DATA_LOSS` are
   never retried; `ABORTED` is retried by restarting the whole transaction, not the single call; `INTERNAL`
   and `UNKNOWN` surface to the application. A call whose repetition would change state does not get an
   automatic retry at all unless it is made idempotent (point 27).
27. **Make a mutating call idempotent with a request id, and answer a repeat with the first response.** The id is
   a field on the request message, not on the resource, optional, a UUID by convention, and honoured for a
   documented time window. When the resource has since changed, returning its current state in place of the
   historical response is acceptable and should be documented as such. The retry policy of point 26 is only as
   safe as this is real.
28. **Retries need a throttle and a budget.** A retry policy without throttling turns one slow dependency into a
   storm of repeated calls; the token-bucket throttle (failed calls spend tokens, successes refill a fraction)
   pauses retries when the backend is unhealthy. Once the response headers have arrived the call is committed
   and no further retry happens, so a stream that fails after its first message is the application's to
   resume. Observe attempts, not just calls: a retry hides failures from the call-level metric.
29. **A rich error carries a machine-readable reason.** A status code and a message are too little to branch on;
    the richer model attaches typed detail messages (an error info with a stable reason and a domain, a list of
    violated fields, a precondition failure, a retry delay) in the trailing metadata. Every error response that
    a client may act on includes the error-info detail, with dynamic values in its metadata and not baked into
    the message (§1.7, §1.8). The costs are real and should be chosen knowingly: proxies and loggers cannot see
    the detail, the trailers weaken header compression and head-of-line behaviour, and a large detail can hit
    the header size limit and lose the original error.
30. **The message is for the developer, in one language; localized text travels as a typed detail.** Keep it
    short and actionable, never assume the reader knows the implementation, and never change the text of an
    existing error that clients may already match on.
31. **Collections paginate from the first release.** Adding pagination later is a breaking change (clients that
    assumed completeness silently get the first page). A list request has an optional `page_size` (documented
    default and maximum, over-large values clamped, negative values `INVALID_ARGUMENT`, fewer results than
    asked allowed even mid-collection) and an opaque `page_token`; the response carries `next_page_token`,
    absent at the end. Changing any other argument between pages is `INVALID_ARGUMENT`. The response of a list
    is not a stream.
32. **Expose health, and drain on shutdown.** Implement the standard health service, set per-service status to
    not-serving when the service cannot accept work, and tell the health library about shutdown so connected
    clients hear it. Stop gracefully: ask the server to stop accepting new calls and let in-flight ones finish,
    with a hard stop on a timer as the safety net, so a stuck call cannot hold the process forever.
33. **Wait-for-ready is a choice, not a default.** Without it a call on a channel that cannot connect fails at
    once; with it the call queues until the channel is ready or the deadline hits. It suits batch work that can
    wait, and does not remove the need to handle other failures.
34. **Keepalive is agreed with the service owner.** Pings keep a connection from being dropped by an idle-timeout
    on a proxy and detect dead peers, but a client that pings too eagerly looks like an attack: do not enable it
    without active calls, and do not set a client interval much below a minute; the server decides what it
    tolerates and answers abusive pings by closing the connection.

## Checking it

35. **Lint and breaking-change detection run in CI against the previous release's schema**, not against memory
   (§3.9). A tool that understands protobuf rules (the buf CLI is the open-source one that does both) turns
   points 1 to 5 into a failing build. Wire compatibility, source compatibility (the
   generated code still compiles for callers) and semantic compatibility (callers still receive what they
   reasonably expect) are three separate checks, and only the first two are mechanical.
36. **A resource name never changes, even across major versions,** and the set of valid names should not
   narrow or widen: clients store names, validate them with the documented pattern and compare them as
   strings.
37. **Moving a message to another file, or a field into or out of a oneof, is breaking** for generated code even
   though the wire format survives.
