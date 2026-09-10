# python-conventions §1 — Typing

> Section 1 of `skills/python-conventions`. Read it when a signature, an attribute or a generic is typed. The other sections and the guardrails stay in `SKILL.md`.

1. Type hints on **all new code**: parameters, return types, class attributes, module-level constants. A type
   checker in strict mode (`mypy --strict`, `pyright`) runs on the diff, not only at project setup. A checker
   that only runs locally is a suggestion: the rule is the CI job, because that is the one nobody can skip
   while in a hurry.
2. Existing untyped code stays as it is, grandfathered by a baseline. Typing is a rule for new code, not a
   licence to rewrite the codebase in passing.
3. **A baseline that grows is a broken ratchet.** The whole point of grandfathering is that the untyped set
   only ever shrinks, so the baseline is regenerated deliberately and a diff that adds entries to it is a
   diff that added untyped code. Without that check, the baseline becomes the place new debt is filed.
4. **`Any` does not fail locally — it spreads.** Every value derived from an `Any` is also unchecked, so one
   annotation retires the checker across a whole call path and the error appears nowhere near where the type
   was lost. `dict[str, Any]` and a bare `object` are the same thing wearing a container: if the shape is
   genuinely unknown say so and narrow, and if it is known, write it down.
5. **Never a bare ignore comment.** Every silencer carries the specific error code in brackets
   (`# type: ignore[arg-type]`) plus a short reason. A bare ignore hides every future error on that line too.
   Enable the unused-ignore warning while you are there: it makes a silencer remove itself once the
   underlying problem is fixed, instead of outliving its cause and hiding the next, unrelated error at the
   same spot.
6. **A checker error is information; never widen a signature to make it go away.** The error is the design
   saying the two shapes do not match, and the choices are to fix the shape or handle the case — both of
   which end up in the code. A parameter loosened to `Any`, or a return widened to a union nobody narrows,
   records only that somebody was in a hurry.
7. Explicit `T | None` rather than an untyped `None` default that leaves the real contract to guesswork. And
   a `None` default the body then treats as mandatory is a lie in the signature: either the parameter is
   optional and the body handles its absence, or it is required and says so.
8. **Accept the widest, return the narrowest.** A parameter typed `list[str]` refuses a tuple for no reason,
   while a return typed `Iterable[str]` stops the caller indexing, taking a length or iterating twice. Take
   `Sequence`/`Iterable`/`Mapping`, hand back the concrete type you actually built.
9. **A mutable class attribute needs `ClassVar` or it is an instance field.** An annotation at class level
   describes each instance's attribute, so a shared registry or cache written there is invisible until two
   instances disagree — the type-level twin of the mutable default in §5.1.
10. A dataclass or a validation model for a data structure with rules, rather than an untyped dict passed from
    function to function. `TypedDict` to type an existing dict (external API, JSON) without converting it into
    a class — but never `dict[str, Any]` out of reflex. Mark the optional keys as not-required individually
    rather than making the whole mapping partial, or every key becomes a `KeyError` waiting for a reader who
    trusted the type.
11. **Types are erased where it matters most.** A hint is not a check, so a payload annotated as a model is
    a description of what the sender promised, not a statement about what arrived — and the two diverge on
    the day the producer deploys before the consumer. Validation at the boundary is §2's business, and the
    type there is derived from the validator rather than written beside it.
12. **Deferred annotations change what the runtime sees.** With annotations evaluated lazily, a framework
    that reads them at import time — a validation model, a request handler, a dependency injector — gets
    strings and has to resolve them, which fails on a type that is only imported for checking. Know which
    mode the project is in before moving an import behind a type-checking guard.
13. On modern Python, the language's own generic syntax (PEP 695) rather than explicit `TypeVar`s, and a
    `Protocol` rather than an ABC for duck-typed collaborators. The protocol is the one that lets a test
    substitute a plain object without inheriting anything, which is what makes §8.8's seam possible.
14. **A type parameter used once is not a generic**, and a callable typed with an ellipsis is a callback with
    its arguments erased. Both look like typing and check nothing: the first is `Any` with ceremony, the
    second accepts a function of any shape and fails when it is called.
15. **Where a return type depends on an argument, overload it.** Returning a union instead pushes a
    narrowing burden onto every call site — including the ones that always pass the argument that makes the
    answer unambiguous, and which now have to assert what the signature already knew.
16. Tests are the relaxed zone: annotations optional, loose types acceptable in expressions. Holding test code
    to production typing rules buys nothing and costs momentum.
17. **A `Protocol` describes a shape; `@runtime_checkable` lets `isinstance` ask about it, and the two answer
    different questions.** A checker verifies structural conformance at every call site without the
    decorator, which is the static guarantee that matters; `runtime_checkable` only checks that the named
    methods exist, not that their signatures match, so an `isinstance` check that passes can still fail on
    the first call with a wrong argument count. Reach for it only where the check genuinely happens at
    runtime — a plugin loaded dynamically, a duck-typed value arriving from outside the type system — not as
    a substitute for the static check that already ran.
18. **A `TypedDict` key is required by default; mark the exceptions, not the rule.** `total=False` on the
    whole mapping makes every key optional, including the ones the boundary always sends, which is §1.10's
    `KeyError`-waiting-to-happen one level up. `Required`/`NotRequired` per key says exactly which fields a
    partial payload is allowed to omit and leaves the rest checked.
19. **`ParamSpec` types a decorator that forwards its wrapped function's exact signature, where a bare
    `Callable[..., T]` erases it.** A decorator typed with `...` accepts a call with the wrong arguments and
    only fails at the call the decorator wraps, far from the decoration site; `Callable[P, T]` with
    `*args: P.args, **kwargs: P.kwargs` keeps the checker validating the original signature through the
    wrapper, which is the whole reason to decorate rather than duplicate.
20. **`Self` types a method that returns the calling class, including a subclass, without hand-writing a
    `TypeVar` bound to it.** A builder or fluent-interface method returning the base class by name breaks
    the chain the moment it is called on a subclass — the checker sees the base type back and every further
    chained call resolves against the wrong class's methods. `-> Self` keeps the return type tied to
    whatever was actually called.
21. **`@overload` signatures are read top to bottom, and the first match wins.** A narrower overload placed
    after a broader one that would also match is dead: the checker picks the first one whose parameter
    types accept the call, so a `str`-specific overload following a general `object` one is never selected
    and the general branch's return type is what every caller sees, silently.
22. **A dataclass and a validation model answer different questions, and picking the wrong one shows up at
    the boundary.** A dataclass is a typed container that trusts its caller — nothing rejects a value built
    directly with the constructor — while a validation model checks its input as it is built and is what
    §2.11 means by deriving the type from the validator. Internal, already-trusted data is a dataclass;
    anything arriving from outside the process is validated first and only then handed around as one.
23. **`Literal` types a value to its exact allowed members, not merely to `str`.** A parameter typed
    `Literal["asc", "desc"]` rejects `"ascending"` at the call site, before the function runs, where a
    parameter typed `str` accepts anything spellable and only fails — if it fails at all — the first time
    the value is compared against one of the two it actually understands. It is the typed alternative to
    §3.7's magic string for a set of values too small or too call-site-local to warrant a full `Enum`.
24. **`@override` states that a method is meant to replace one from a superclass, and the checker verifies
    it.** Without it, renaming or removing the base method silently turns the subclass's method into a new,
    unrelated one that nothing calls the way the author intended — the checker has no way to tell "this was
    supposed to override something" from "this is a new method that happens to share a name". `@override`
    makes that intent checkable instead of assumed.
25. **`TypeIs` narrows both branches; `TypeGuard` narrows only the positive one.** A function returning
    `TypeIs[int]` lets the checker treat the value as `int` after a true check and as the original type minus
    `int` after a false one, matching how `isinstance` already behaves — `TypeGuard` narrows only the `if`
    branch and leaves the `else` branch at the original, wider type, which is right only for the rarer case
    where the predicate does not partition the input cleanly. Reach for `TypeGuard` deliberately, not as the
    default because it came first.
26. **A closed `TypedDict` (`closed=True`, or a per-field `extra_items` type) says no other key can appear**,
    where a plain `TypedDict` only constrains the keys it names and silently accepts anything else a caller
    adds. A payload validated against an open `TypedDict` can carry a typo'd key alongside the correct one and
    the checker will not flag it, because nothing said the shape was exhaustive.
27. **A stub-only detail — `.pyi` files, third-party stubs, `typeshed` overrides — is still part of the
    contract your code type-checks against**, even though it never runs. A local stub that lags the library's
    actual signature passes the checker while calling code breaks at runtime, which is a more confusing
    failure than no stub at all: the checker vouched for a shape the library stopped providing.
28. **A generic bound (`class Repo[T: HasId]`) is a promise the checker enforces, not documentation.**
    `class Repo[T]` alone says nothing about what `T` supports, so any method needing `.id` on the stored
    value has to fall back to `Any`-shaped access or an `# type: ignore`; the bound lets the checker verify
    every instantiation actually satisfies it and lets the repository's own methods use `.id` without
    narrowing first.
29. **`NewType` distinguishes two values with the same runtime type but different meaning**, at zero runtime
    cost. `UserId = NewType("UserId", int)` stops a plain `int` — a page number, a quantity, another entity's
    id — from being passed where a user id is expected, a mistake `int` alone cannot catch because both sides
    of the call are "just an int" to the runtime; the checker is the only place the distinction exists, which
    is exactly where the bug would otherwise go unnoticed.
30. **A `Callable` protocol is more than one method wearing a function's shape.** `Protocol` with a
    `__call__` signature types "anything callable this way" — a plain function, a bound method, a class with
    `__call__` — without forcing a caller into a base class, which is what makes it the right shape for a
    pluggable strategy or hook where a lambda is often the natural first implementation and a `Protocol`
    inheritance requirement would rule it out.
