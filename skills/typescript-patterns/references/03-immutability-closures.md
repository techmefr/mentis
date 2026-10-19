# typescript-patterns §3 — Immutability and closures

> Section 3 of `skills/typescript-patterns`. Read it when a variable is declared, an argument is modified, a callback is created in a loop or an enum is considered. The other sections and the guardrails stay in `SKILL.md`.

1. `const` by default, `let` only if reassignment is genuinely necessary: never `var`.
2. A closure inside a loop captures the reference, not the value at creation time: a classic trap
   with `var`, less so with `let`/`const` but worth checking if an array of callbacks is built
   dynamically.
3. Mutating an object/array received as a parameter = a side effect invisible to the caller: return a
   copy (spread, `structuredClone`) if the contract isn't explicitly "I mutate in place".
4. Native TS `enum` avoided in favour of an `as const` object + a derived type
   (`typeof X[keyof typeof X]`): the native enum generates superfluous runtime JS and behaves
   differently under `isolatedModules`.
