# typescript-patterns §4 — Errors, narrowing and exhaustiveness

> Section 4 of `skills/typescript-patterns`. Read it when an error is caught, a union is branched on, a type
> predicate is written, an identifier or validated string needs its own type, or optional and missing values
> are modelled. The other sections and the guardrails stay in `SKILL.md`.

1. **A caught value is `unknown` until narrowed.** Anything can be thrown, including a string or `undefined`,
   so the catch variable is typed `unknown` (the strict mode does this) and narrowed with an `instanceof`
   check on the error class before reading `message`. A small helper that turns an unknown thrown value into an
   `Error` keeps the narrowing in one place. Reading `error.message` on an untyped catch variable is a latent
   crash in the error path, the one that runs least often and is tested least.
2. **A wrapped error keeps its cause.** Rethrowing with a new message passes the original through the
   standard `cause` option, so the stack of the real failure survives into the report. A rethrow that drops it
   leaves the monitoring tool with a message and no origin.
3. **Custom errors are classes with a stable discriminator.** A class extending `Error` with a `code` (or a
   `name`) is recognised with `instanceof` inside one bundle, but `instanceof` is unreliable across realms,
   duplicated packages and serialisation boundaries. When an error crosses one of them, branch on the code.
4. **A closed set of variants is matched exhaustively.** In a `switch` over a discriminated union, the
   default branch assigns the value to `never` through a small assertion function, or uses `satisfies never`,
   so adding a variant makes every unhandled switch a compile error. A plain default that returns something
   plausible turns the same addition into silent behaviour (the compile-time equivalent of a catch that
   swallows).
5. **`satisfies` checks a value against a type without widening it.** For a configuration table, a route map
   or a lookup object, `satisfies` verifies the shape and keeps the literal keys and values, so later code
   gets precise types. An `as` annotation on the same object discards that precision and silences missing
   keys.
6. **A type predicate is a promise the compiler cannot check.** A function declared `value is User` that
   returns `true` after looking at one field narrows every caller to a lie when the other fields are wrong.
   It checks every field it claims, or the boundary uses a schema parse (§7); an assertion function is the
   same promise with a throw.
7. **A branded type separates values that share a representation.** A user id and an order id are both
   strings, and swapping them compiles. Give each an opaque type (the base type intersected with a
   phantom marker property) created only by a function that validates it, so the compiler rejects the swap
   (`skills/code-baseline` §5 states the principle: distinct concepts, distinct types).
8. **Absence has one representation per layer.** Choose between a missing property, `undefined` and `null`
   and say which, rather than accepting all three. The optional-property-exactness setting distinguishes a
   property that is absent from one set to `undefined`, which matters when a patch object means "leave
   unchanged" versus "clear". Use `??` for defaults (it replaces only `null` and `undefined`), never `||`,
   which also replaces `0`, the empty string and `false`.
9. **An index lookup can miss.** With the unchecked-indexed-access setting an array element and a record
   value are typed `T | undefined`, which is the truth. Handle the miss with `at()`, a destructuring default or
   a guard; for a dynamic set of keys use a `Map`, which has no prototype keys and no key-type pun.
10. **`Object.keys` and `Object.entries` return strings.** Casting the result to the key union asserts that
    the object has no other keys, which an object with extra properties from structural typing violates. Keep
    the cast in one named helper, used where the object is known to be exact, and nowhere else.
11. **Read-only is stated in the type.** A function that must not modify its argument takes `readonly T[]` or
    `Readonly<T>`, a constant table is declared `as const`, and a method returning internal state returns a
    read-only view. The compiler then enforces what §3 asks for by discipline.
12. **A boolean parameter is a flag the reader cannot decode at the call site.** `render(item, true, false)`
    says nothing. Take an options object with named members, or two functions, or a union of named modes. More
    than three parameters become an object for the same reason.
13. **Generics are constrained and earn their parameter.** A type parameter appears at least twice in the
    signature (input and output, or two inputs that must agree); otherwise a concrete type or a union is
    simpler. Constrain with `extends`, never default a parameter to `any`, and prefer overloads to a long
    conditional type when there are two or three cases.
14. **Suppression directives are findings.** `@ts-expect-error` is preferred to `@ts-ignore` because it fails
    when the error disappears, so a stale suppression is found; both are justified in the review and counted,
    and a file-wide suppression is never added.
