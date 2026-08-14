# react-nextjs-conventions §2 — Naming

> Section 2 of `skills/react-nextjs-conventions`. Read it when a symbol or a file has to be named. The other sections and the guardrails stay in `SKILL.md`.

1. Functions declared as arrow functions assigned to a `const`, consistently.
2. **No abbreviations** in identifiers: `expense` not `exp`, `index` not `idx`, `error` not `err`,
   `button` not `btn`, `previous` not `prev`, `event` not `e`. The keystrokes saved cost every future reader
   a guess.
3. A function name **starts with an action verb**: `formatAmount`, not `amount`; `fetchBills`, not `bills`.
   A noun-named function reads like a value at the call site.
4. Booleans prefixed `is`/`has`/`can`/`should`, including boolean props and JSX flags.
5. **Callback prop vs handler**: the prop is `onSomething`, the function implementing it is
   `handleSomething`. Swapping them makes it impossible to tell an incoming contract from a local
   implementation.
6. A hook wrapping a server query is `use` + Resource + `Query`; a hook wrapping a mutation is `use` + verb +
   Subject + `Mutation`. `useBill`, `fetchBills` and `createClientVatMutation` each break it in a different
   way.
7. The result of a mutation hook is stored as the **whole result object** under a derived name, not
   destructured into bare `mutate`/`isPending` — two mutations in one component collide immediately
   otherwise.
8. **Named constants** instead of inline literals: a numeric threshold in a condition, a status code, a
   timeout, a string used as an identifier. A magic value whose meaning isn't obvious from context is a
   comment waiting to be needed.
9. Query keys in one casing, camelCase by default, across every key segment — a mismatched key silently
   fails to invalidate, which looks like a caching bug.
