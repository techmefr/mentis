# laravel-conventions §5 — Naming, typing, style

> Section 5 of `skills/laravel-conventions`. Read it when a symbol has to be named, or a docblock written. The other sections and the guardrails stay in `SKILL.md`.

1. House casing applied per artefact kind (classes, jobs, events, listeners, commands, resources, enums,
   views, routes, variables, methods, abilities) without exception.
2. **Names reveal intent**: never `$temp`, `$data`, `$result`, `$array`, `$item`, `$value`, `$x`. The generic
   name pushes the meaning into the reader's head.
3. **No magic strings or numbers with domain meaning.** A domain value (status, type, kind, mode) becomes an
   enum; a queue name, config key or event name becomes a constant or a config entry; a threshold becomes a
   named constant.
4. **Native typed properties and signatures** over docblock-only types: the runtime enforces the former.
5. A docblock is for what the type system can't express (a collection's element type, an array shape, a union
   the signature can't state). **Skip it entirely on a fully type-hinted method** — a docblock repeating the
   signature is a second copy to keep in sync.
6. **Constructor property promotion** for a constructor that only assigns its parameters to properties.
7. String building through interpolation with braced placeholders rather than concatenation splicing quoted
   fragments.
8. **A date rendered as text goes through the date library's own localised accessors** (a month name, a
   weekday name, a translated format), never a lookup array keyed by the month number or a `match` on it.
   The hand-rolled version reinvents a catalogue the library already ships for every locale, and hardcodes
   user-facing text while doing it — two rules broken by one array (point 3 and point 11).
9. Blank lines **between logical steps** inside a method body, so the steps are visible; not between every
   pair of lines.
10. Guard clauses and early returns rather than nested branches; no brace-less single-line statement.
11. **All code in one language — English** — including class and method names, command signatures and
    descriptions, log messages, console output, exception messages, queue and config keys. User-facing text
    is the exception, and it goes through translation.
12. Whether new files declare strict types is a **project-wide decision applied uniformly**, and the
    framework's own scaffolding is the reference point: a codebase half strict and half not gets the downsides
    of both. **The default for a new Laravel file is to omit `declare(strict_types=1)`, matching what
    `artisan make:*` generates** — this overrides `php-patterns`' language-level default (see that block's
    §1.1) precisely at this framework's boundary, where request/route/config values cross as loose scalars
    on purpose. Leave an existing file's declaration exactly as it is either way; this is a default for new
    files, not a retrofit.
13. **A method that answers reads as a question; a method that acts is named for its effect.**
    `isPublished()`, `canBeCancelled()`, `hasPendingInvoices()` on one side; `publish()`, `cancel()`,
    `notifyOwner()` on the other. The mistake that costs is the middle ground — a `check…()` or
    `handle…()` that both answers and mutates, because every caller then has to read the body to know
    whether calling it twice is safe.
14. **A class named after a pattern instead of a subject is a class with no subject.** `*Service`,
    `*Manager` and `*Helper` are already banned by `skills/code-baseline`; the Laravel-specific case is
    `*Repository`, and the reason is concrete rather than stylistic — Eloquent is already the data-access
    layer, so a repository wrapper adds a class, forbids nothing, and gets bypassed by the first developer
    who needs a query it does not expose. Name the behaviour: `PublishArticle`, `MonthlyRevenue`.
15. **An enum that every caller `match`es on is an enum missing a method.** The label, the colour, the
    allowed transitions and the permission belong on the enum itself; the same `match` written in a
    controller, a resource and a Blade view is three places to forget the case you add next month. The
    compiler cannot help with a `match` that has a default arm, so the duplication is silent.
16. **A migration's file name is the only place its intent is legible.** `add_status_to_invoices` beats
    `update_invoices_table`, because the list of migrations is read as a history — and a name that says
    "update" forces the reader to open the file to know whether it is the one they are looking for.
17. **Route names, ability names and queue names are string contracts, so renaming one is a search across
    the whole repository** — Blade views, front-end code, tests, config, seeders — not just the PHP that
    declares it. Nothing fails at compile time: a stale `route('…')` throws at runtime on the one page
    nobody opened, and a stale ability name silently authorises nothing or everything depending on the
    fallback.
18. **A long collection pipeline gets named steps.** Five chained calls with inline closures cannot be read
    in a review diff, and the reviewer's only options are to trust it or to rebuild it mentally. Break it
    where the meaning changes and name the intermediate value; the performance is identical and the
    argument becomes possible.
19. **`array` and `mixed` in a signature are the absence of a type.** Where the shape is known, a typed
    object, a value object or a typed collection carries it in a way the runtime enforces; an array shape
    written only in a docblock is checked by static analysis at best and by nothing at worst (points 4 and
    5). Keep them for the genuine boundary cases — a config blob, a decoded payload about to be validated.
20. **An exception is named for the condition, not for the layer that threw it.**
    `InvoiceAlreadyPaid` tells a catch block what happened; `InvoiceServiceException` tells it where the
    code was, which is what the stack trace is already for (§11).
21. **A value object or a DTO is `readonly` unless something legitimately mutates it after construction.**
    Combined with constructor property promotion (point 6), `readonly` turns the class into one line per
    property with no setter to forget and no accidental reassignment three methods later — the compiler
    enforces the immutability a docblock comment used to merely promise. Reach for it on a money amount, an
    address, a search filter; not on an Eloquent model, which is mutable by design and already guards its
    own attributes.
22. **A boolean property or parameter is named as a predicate, the same rule point 13 applies to methods.**
    `$isDefault`, `$hasExpired`, `$canRetry` read at the call site; `$default`, `$expired`, `$retry` on a
    parameter force the reader to check the signature to know which way `true` points. This matters most on
    a positional boolean argument passed at a call site with no named-argument hint — `notify($user, true)`
    says nothing back, `notify($user, shouldQueue: true)` does, and the fix costs nothing once the parameter
    is already named as a predicate.
23. **A backed enum's backing type is chosen for what reads the value, not for what's shortest to type.**
    A `string` backing (`'draft'`, `'published'`) survives a database dump, a log line and an API payload as
    something a human recognises without the enum's source open next to it; an `int` backing saves a few
    bytes and forces every one of those to carry a lookup table in their head. Reserve `int` for a case that
    is genuinely ordinal (a severity level compared with `<`) rather than a label — a status is a label.
24. **A class closed to extension by default is `final`, and the exception is deliberate, not an oversight.**
    A framework base class, a job, a listener, a single-purpose action class is rarely meant to be
    subclassed — leaving it open invites a second implementation that overrides one method and silently
    drifts from the first the next time the parent changes. Where extension is the actual design (a shared
    base for a family of report exporters), that base is the one class allowed to skip `final`, and it says
    so by existing as an abstract class rather than a concrete one nobody expected to be extended.
25. **A native `readonly` property (point 21) and PHPStan's own strictness are two different guarantees,
    and levelling up the analyser is a project-wide ratchet, not a per-file preference.** A codebase
    declares the level it targets once — commonly the level that catches type-juggling and dead branches
    without drowning in false positives on framework magic — and every new file is written to satisfy it
    rather than adding to a baseline meant to shrink. A baseline entry from six months ago is not a
    precedent for the next one.
26. **Larastan's own model of Eloquent — magic `find`, relation methods, query-builder macros — is taught
    to the analyser through its bundled extension, not through a docblock repeated on every model.** A
    project that still hand-writes `@property` blocks for every column duplicates what the extension
    already infers from `$casts` and the migrations; reach for an explicit `@property` only where a model
    genuinely adds a computed accessor the extension cannot see, never for the raw columns.
27. **A named argument beats a comment explaining a positional one.** `retry(times: 3, sleep: 100)` reads
    on its own; `retry(3, 100)` next to `// 3 attempts, 100ms apart` duplicates in prose what the call site
    could have said for free, and the prose is the copy that goes stale first. Reserve this for calls whose
    parameters are not already obvious from a single well-named argument.
28. **First-class callable syntax (`strtoupper(...)`, `$this->publish(...)`) replaces the
    `Closure::fromCallable`/string-callback indirection** wherever a method reference is passed as a
    value — to `array_map`, a collection pipeline (point 18), an event listener registration — because it
    is checked by the parser at the call site instead of resolved by name at call time, catching a typo'd
    method name before the code ever runs.
29. **A union type in a signature states every shape the caller may pass, not just the common one** —
    `int|string $id` on a lookup that genuinely accepts either is a contract; `mixed` covering the same two
    cases is point 19's absence of a type wearing a shorter name. Where the union grows past two or three
    unrelated shapes, that is usually the signal the parameter should have been split into two methods
    instead of documented with a longer union.
30. **An intersection type (`Countable&ArrayAccess`) declares a parameter needs both capabilities**, not
    one class that happens to implement both today; where only one capability is actually used inside the
    method, requiring the intersection ties every future caller to a coincidence the method body doesn't
    need. Prefer the single interface that names the one capability actually called.
31. **A named enum case that stands for one specific record ("the default warehouse", "the admin role")
    is a symptom the enum modeled a row, not a category.** An enum's cases are meant to be exhaustive and
    fixed at compile time; a category that a future admin screen must extend belongs in a database table
    with a foreign key, not in a `match` arm waiting for the next deploy to add a case.
