# typescript-patterns §2 — Async: the number one source of silent bugs

> Section 2 of `skills/typescript-patterns`. Read it when a promise is created, awaited or left running. The other sections and the guardrails stay in `SKILL.md`.

1. A `Promise` never left dangling without an `await` or an explicit `.catch`; a rejected promise
   that isn't handled is a silent crash or an unhandled rejection.
2. `Promise.all` for independent operations, never a serial `await` in a loop out of reflex when
   parallelism is possible and safe (no dependency between them).
3. `async` on a function that does nothing asynchronous is a signal to remove, not a neutral style.
4. The classic race condition: two `await`s modifying the same shared state with no logical lock
   (e.g. two calls that read then write the same variable): check the real execution order, not the
   apparent order in the code.
