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
   The hand-rolled version reinvents a catalogue the library ships for every locale, and hardcodes
   user-facing text — two rules broken by one array (point 3 and point 11).
9. Blank lines **between logical steps** inside a method body, so the steps are visible; not between every
   pair of lines.
10. Guard clauses and early returns rather than nested branches; no brace-less single-line statement.
11. **All code in one language — English** — including class and method names, command signatures and
    descriptions, log messages, console output, exception messages, queue and config keys. User-facing text
    is the exception, and it goes through translation.
12. Whether new files declare strict types is a **project-wide decision applied uniformly**, and the
    framework's own scaffolding is the reference point: a codebase half strict and half not gets the downsides
    of both. **The default for a new Laravel file is to omit `declare(strict_types=1)`, matching what
    `artisan make:*` generates** (the 12.x class, job, model and factory stubs open with `<?php` and no
    declaration) — this overrides `php-patterns`' language-level default (see that block's §1.1) at this
    framework's boundary, where request/route/config values cross as loose scalars on purpose. Leave an
    existing file's declaration exactly as it is; this is a default for new files, not a retrofit.
    [laravel/framework 12.x stubs, read 2026-10-21.]
13. **A method that answers reads as a question; a method that acts is named for its effect.**
    `isPublished()`, `canBeCancelled()`, `hasPendingInvoices()` on one side; `publish()`, `cancel()`,
    `notifyOwner()` on the other. The costly mistake is the middle ground — a `check…()` or `handle…()` that both answers and
    mutates, so every caller must read the body to know whether calling it twice is safe.
14. **A class named after a pattern instead of a subject is a class with no subject.** `*Service`,
    `*Manager` and `*Helper` are already banned by `skills/code-baseline`; the Laravel-specific case is
    `*Repository`, for a concrete reason — Eloquent is already the data-access layer, so a repository
    wrapper adds a class, forbids nothing, and gets bypassed by the first developer who needs a query it
    does not expose. Name the behaviour: `PublishArticle`, `MonthlyRevenue`.
15. **An enum that every caller `match`es on is an enum missing a method.** The label, the colour, the
    allowed transitions and the permission belong on the enum itself; the same `match` written in a
    controller, a resource and a Blade view is three places to forget the case you add next month, and the
    compiler cannot help with a `match` that has a default arm.
16. **A migration's file name is the only place its intent is legible.** `add_status_to_invoices` beats
    `update_invoices_table`: the list of migrations is read as a history, and "update" forces the reader to
    open the file.
17. **Route names, ability names and queue names are string contracts, so renaming one is a search across
    the whole repository** — Blade views, front-end code, tests, config, seeders — not just the PHP that
    declares it. Nothing fails at compile time: a stale `route('…')` throws on the one page nobody opened, and a
    stale ability name silently authorises nothing or everything.
18. **A long collection pipeline gets named steps.** Five chained calls with inline closures cannot be read
    in a review diff. Break it where the meaning changes and name the intermediate value; the performance is
    identical and the argument becomes possible.
19. **`array` and `mixed` in a signature are the absence of a type.** Where the shape is known, a typed
    object, a value object or a typed collection carries it in a way the runtime enforces; an array shape
    written only in a docblock is checked by static analysis at best (points 4 and 5). Keep them for the
    genuine boundary cases — a config blob, a decoded payload about to be validated.
20. **An exception is named for the condition, not for the layer that threw it.**
    `InvoiceAlreadyPaid` tells a catch block what happened; `InvoiceServiceException` tells it where the
    code was, which the stack trace already does (§11).
21. **A value object or a DTO is `readonly` unless something legitimately mutates it after construction.**
    Combined with constructor property promotion (point 6), `readonly` turns the class into one line per
    property with no setter to forget and no accidental reassignment three methods later. Use it on a money
    amount, an address, a search filter; not on an Eloquent model, which is mutable by design and already
    guards its own attributes.
22. **A boolean property or parameter is named as a predicate, the same rule point 13 applies to methods.**
    `$isDefault`, `$hasExpired`, `$canRetry` read at the call site; `$default`, `$expired`, `$retry` on a
    parameter force the reader to check the signature to know which way `true` points. It matters most on
    a positional boolean argument — `notify($user, true)` says nothing, `notify($user, shouldQueue: true)`
    does.
23. **A backed enum's backing type is chosen for what reads the value, not for what's shortest to type.**
    A `string` backing (`'draft'`, `'published'`) survives a database dump, a log line and an API payload as
    something a human recognises without the enum's source open; an `int` backing saves a few bytes and
    forces a lookup table in every reader's head. Reserve `int` for a genuinely ordinal case (a severity
    level compared with `<`) — a status is a label.
24. **A class closed to extension by default is `final`, and the exception is deliberate, not an oversight.**
    A job, a listener, a single-purpose action is rarely meant to be subclassed — leaving it open
    invites an override that silently drifts from the parent. Where extension is the design (a shared base for a family of report exporters),
    that base is the one class allowed to skip `final`, and says so by being abstract.
25. **A native `readonly` property (point 21) and PHPStan's own strictness are two different guarantees,
    and levelling up the analyser is a project-wide ratchet, not a per-file preference.** A codebase
    declares the level it targets once, and every new file is written to satisfy it rather than adding to
    a baseline meant to shrink. A baseline entry from six months ago is not a precedent for the next one.
26. **Larastan's own model of Eloquent — magic `find`, relation methods, query-builder macros — is taught
    to the analyser through its bundled extension, not through a docblock repeated on every model.** A
    project hand-writing `@property` blocks for every column duplicates what the extension can infer from
    `$casts` and, when configured to read them, the migrations; use an explicit `@property` only for a
    computed accessor the extension cannot see, never for the raw columns. See `skills/laravel-larastan`.
27. **A named argument beats a comment explaining a positional one.** `retry(times: 3, sleep: 100)` reads
    on its own; `retry(3, 100)` next to `// 3 attempts, 100ms apart` duplicates in prose what the call site
    could say for free, and the prose goes stale first. Reserve this for calls whose parameters are not
    already obvious from a single well-named argument.
28. **First-class callable syntax (`strtoupper(...)`, `$this->publish(...)`) replaces the
    `Closure::fromCallable`/string-callback indirection** wherever a method reference is passed as a
    value — to `array_map`, a collection pipeline (point 18), an event listener registration — because the
    reference is resolved where it is written, so a typo'd method name fails there instead of when the
    callable is later invoked, and the analyser can follow it.
29. **A union type in a signature states every shape the caller may pass, not just the common one** —
    `int|string $id` on a lookup that genuinely accepts either is a contract; `mixed` covering the same two
    cases is point 19's absence of a type. Past two or three unrelated shapes, split the parameter into two methods.
30. **An intersection type (`Countable&ArrayAccess`) declares a parameter needs both capabilities**, not
    one class that happens to implement both today; where only one capability is used inside the method,
    requiring the intersection ties every future caller to a coincidence. Prefer the single interface naming
    the one capability actually called.
31. **A named enum case that stands for one specific record ("the default warehouse", "the admin role")
    is a symptom the enum modeled a row, not a category.** An enum's cases are exhaustive and fixed at
    compile time; a category a future admin screen must extend belongs in a database table with a foreign
    key, not in a `match` arm waiting for the next deploy to add a case.
32. **A typed class constant (`const string STATUS = 'active';`) states the type the same way a typed
    property does, and PHP enforces it at declaration** — a mismatched value fails immediately rather than
    three files away where the constant is read as the wrong shape. Type every new class constant that
    carries a scalar or object value, as point 4 asks for properties and signatures.
33. **A whole-class `readonly` declaration (`final readonly class Money`) says every property is immutable
    without repeating the keyword on each one** — the class-level form point 21 recommends for a value
    object, applied where every property qualifies. Use the per-property form only where one property needs to stay mutable — usually a field
    belonging on another class.
34. **A method that never returns — it always throws or exits the request — is typed `never`, not `void`.**
    `void` still permits an implicit return and tells a caller nothing about reachability; `never` on an
    `abort()`-only helper or a guard clause's terminal branch lets the analyser see the code after the call
    is unreachable, the guarantee a guard clause (point 10) gives the reader by its shape alone.
35. **An enum implementing an interface makes every case commit to the interface's methods, a stronger
    promise than a trait mixed into the enum.** Where point 15 puts the label, the colour and the
    transitions on the enum, an interface (`HasColour`, `HasLabel`) shared by several enums lets a Blade component or a
    resource accept "any enum that has a colour" while keeping the compile-time check.
36. **The nullsafe operator (`$user?->address?->city`) replaces a chain of `isset()` or `?? null` checks for
    reading through a possibly-null relationship**, but it only answers "is this null", not "should this be
    null here" — a chain swallowing a relationship that was supposed to be loaded (a missing `with()`) hides the
    N+1-shaped bug (§4) a loud failure would surface in development. Reserve it for a legitimately
    optional relationship.
37. **Asymmetric visibility (`public private(set) string $status`) states that every caller may read a
    property while only the class itself may write it, in the property declaration instead of a getter with
    no setter.** The middle ground between `readonly` (points 21, 33) and a fully public property: use it on
    a property that changes only through the class's own methods, such as a status with a `transitionTo()`.
38. **A PHP 8.4 property hook (`public string $status { get => ...; set => ...; }`) replaces a
    get/set-Attribute pair for a plain object the way §3 point 18's `Attribute::make` does for an Eloquent model,
    and the two are not interchangeable.** `Attribute::make` serves Eloquent's own attribute pipeline — it
    runs through `$casts` and the model's dirty-tracking; a property hook is a language feature that works
    on any class, including a value object or a DTO with no model machinery. A hook on an Eloquent
    attribute bypasses the cast pipeline (§3 point 17), while `Attribute::make` on a plain PHP class does
    nothing. [PHP 8.4 property hooks
    RFC, wiki.php.net/rfc/property-hooks, read 2026-09-10.]
39. **A property hook's `set` clause validates or normalises on assignment, which moves a guard out of the
    constructor and out of every place the property is later reassigned.** A value object validating only in
    its constructor (point 21's `readonly` case) still lets a mutable sibling property drift into an invalid
    state after construction; a `set` hook enforces the invariant on every assignment, the gap a
    constructor-only guard leaves open on any property that is not `readonly`.
40. **PHP 8.4's lazy objects (`ReflectionClass::newLazyGhost()`) defer constructing the object itself until
    something first touches it, a different mechanism from `once()` (§1 point 24) even though both defer
    work.** `once()` memoises the *result of a callback* for the life of the request; a lazy object runs its
    initialiser on first access to its state, so a hand-rolled "build it on first access" property duplicates
    what the language now ships. [PHP 8.4 lazy objects RFC, wiki.php.net/rfc/lazy-objects, read 2026-09-10;
    not re-read in the 2026-10-21 pass.]
41. **`UnitEnum::cases()` is the source of truth for "every value this enum has," and a parallel array
    maintained beside it is the two-sources-of-truth failure §3 point 1 names for a DB-level enum, in PHP
    instead of SQL.** A validation rule, a seeder, or a test data provider listing
    `['draft', 'published', 'archived']` by hand instead of mapping over `Status::cases()` silently stops
    covering a case the day someone adds one to the enum and forgets the parallel list — nothing reads from
    the enum to tell them. [PHP enumerations documentation, php.net/manual/en/language.
    enumerations.backed.php, read 2026-09-10.]
42. **The short nullable notation (`?Type`) states the same contract as `Type|null` in fewer characters, and
    mixing the two styles across a codebase is the inconsistency point 32 warns against for a different
    construct.** Use the full union form only where the nullable case is one among several unrelated shapes
    (point 29) — `?int` for "an int or absent," `int|string|null` only where the value can arrive as either
    scalar and also be missing.
43. **A codebase's formatting standard is declared once and enforced by a tool, not by review comments.**
    Laravel's own formatter, Pint, needs no configuration and uses the `laravel` preset by default; the
    docs show `psr12` as an alternative preset, set in `pint.json` or with `--preset`. Pick one and record
    it, so bracket placement and import ordering are settled before they start — §10 point 7's "a tool
    enforces it, not a paragraph" applied to formatting. [Laravel Pint docs 12.x, "Presets", read
    2026-10-21.]
