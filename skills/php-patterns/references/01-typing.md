# § 1 — Typing: modern PHP (8.x) is no longer untyped PHP

> Section 1 of `skills/php-patterns`. Read it when a signature, a property or a closed set of values is
> typed. §1.1 is cited from `laravel-conventions` §5.12, which overrides it at the framework boundary.

1. **`declare(strict_types=1)` as the first line of every PHP file** — on a framework-free file, or a
   framework whose own boundary is already strictly typed. Without it, a typed signature is only
   half-enforced: PHP still coerces `"5"` to `5` or `0` to `false` across the call, and the type
   declaration from point 2 documents a contract it doesn't actually check. This is the one PSR-12 rule
   that changes runtime behaviour rather than formatting, which is why it belongs here rather than
   being left to Pint/PHP-CS-Fixer the way brace placement or line length are. **On Laravel specifically,
   this default is overridden, not just "may be overridden"**: `laravel-conventions` sits above this block
   for exactly this kind of conflict, and the framework boundary is the reason — request input, route
   parameters and config values cross it as loose scalars by design (`$request->input('age')` is `"25"`,
   not `25`), so `strict_types=1` turns Laravel's own coercion into a call-site `TypeError`, i.e. a 500 in a
   path that worked before. Laravel's own `artisan make:*` stubs omit the declaration for that reason.
   **Existing files that already declare it stay exactly as they are** — this is a default for new files,
   never a drive-by removal — and a pure domain file with no framework-boundary calls (a value object, a
   calculator) is still a reasonable place to opt in deliberately.
2. Typed function/method signatures (parameters + return), including an explicit `void`/`?type`; an
   untyped parameter is a regression, not a neutral style in PHP 8+. The declaration is checked at the
   call, so it converts a bug that surfaced later — as a null passed three frames down, or a string
   concatenated into a number — into a failure at the boundary that crossed it, with the caller in the
   trace.
3. `readonly` on properties that never change after construction (value objects, DTOs): prevents an
   accidental deep mutation. It is shallow, though — a readonly property holding an array cannot be
   reassigned but a readonly property holding an object still lets that object be mutated through it, so
   an immutable shape means immutable all the way down, not one keyword at the top.
4. Union types (`int|string`) rather than `mixed` out of reflex: `mixed` expresses no intent, an
   explicit union type documents the real contract. A union of two things the caller has to distinguish
   is also a signal worth reading — often the honest type is a small object, not the union.
5. Native PHP 8.1+ enums (`enum ... : string`) rather than class constants scattered around to
   represent a closed set of values. The gain is exhaustiveness: a `match` over an enum with a missing
   case is an error the analyser reports, where a `match` over string constants silently falls through
   to its default. Add the behaviour that belongs to the set as methods on the enum rather than as a
   `switch` repeated at each call site.
6. **A backed enum's value is stored data; its case name is code.** Renaming a case is a refactor the
   analyser follows; changing a backing value is a data migration, because rows, payloads and caches
   already hold the old string. Choose the values deliberately at the point the enum is written, and
   never "tidy" them afterwards.
7. **A typed property with no default is uninitialised, which is not the same as null.** Reading it
   before assignment throws `Error: must not be accessed before initialization` — a different failure
   from a null, and one that fires in whichever code path forgot to set it rather than at construction.
   Assign every property in the constructor, or give the type a null default and mean it.
8. **`array` as a type says nothing about what is in the array.** `array $rows` is satisfied by an empty
   array, a list of the wrong objects, or a map — so the check passes and the loop inside fails. Where
   the contents matter, the shape goes in an annotation the analyser reads (`list<Invoice>`,
   `array<string, int>`), and where it matters a lot, the honest answer is a typed collection object
   rather than an array at all.
9. **Constructor property promotion declares the object's shape once.** The version that declares the
   properties, then the parameters, then the assignments states the same three facts three times, and
   the failure is the ordinary one: someone adds a field to two of the three places.
10. **`never` as a return type for a function that always throws or exits.** It tells the analyser the
    code after the call is unreachable, which is what stops it from demanding a return value on a branch
    that cannot continue — and stops a reader from adding one.
11. **Typing pays off in static analysis, not at runtime.** The runtime check fires when the bad call
    actually happens, in whichever request reaches it; the analyser finds it before the code runs. So
    the declarations are worth writing only to the extent something reads them, and a baseline entry
    that hides a reported error is a decision to keep it, not a fix — it just moves the report.
12. **Variance goes one way, and getting it wrong is fatal at class-load time.** An overriding method may
    widen a parameter type and narrow a return type, never the reverse. The failure is a fatal error the
    first time the class is loaded — which is the first request that touches that code path, not the
    deploy, so a signature change that looks harmless can break one route and nothing else.
