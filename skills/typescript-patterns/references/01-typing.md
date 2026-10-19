# typescript-patterns §1 — Typing: avoid the fake-typed

> Section 1 of `skills/typescript-patterns`. Read it when a type is written, an `any` or an assertion is tempting, or a union could replace optional fields. The other sections and the guardrails stay in `SKILL.md`.

1. `any` never used to avoid thinking about the real type: `unknown` + narrowing if the type really
   is unknown at that point in the code.
2. Type assertion (`as`) only when TypeScript structurally cannot infer (e.g. the result of
   `JSON.parse`, and §7 replaces even that with a schema parse at the boundary), never to silence a
   legitimate type error.
3. Derived types (`ReturnType`, `Parameters`, `Pick`/`Omit`, mapped types) rather than duplicating a
   data shape already declared elsewhere: a duplicated type diverges silently from the first one at
   the first refactor.
4. `interface` for an extensible shape (object, public contract), `type` for a
   union/intersection/alias: no rule that opposes them out of dogma, but no random choice either.
5. Discriminated unions (`{ type: 'a', ... } | { type: 'b', ... }`) rather than one object with all
   fields optional and nullable to represent mutually exclusive states.
