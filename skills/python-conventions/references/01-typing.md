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
