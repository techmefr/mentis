# react-nextjs-conventions §2 — Naming

> Section 2 of `skills/react-nextjs-conventions`. Read it when a symbol or a file has to be named. The other sections and the guardrails stay in `SKILL.md`.

1. Functions declared as arrow functions assigned to a `const`, consistently. The value of the convention is
   that it is one: a file mixing declarations and expressions makes the reader wonder whether the difference
   is meaningful, and hoisting then becomes something they have to think about at every call.
2. **No abbreviations** in identifiers: `expense` not `exp`, `index` not `idx`, `error` not `err`,
   `button` not `btn`, `previous` not `prev`, `event` not `e`. The keystrokes saved cost every future reader
   a guess. They also cost the search: `err` matches nothing when you grep for `error`, so an abbreviation
   is a name that hides from the tooling used to find it.
3. A function name **starts with an action verb**: `formatAmount`, not `amount`; `fetchBills`, not `bills`.
   A noun-named function reads like a value at the call site, so `const total = amount` looks settled when
   it is a function reference that will render as `function amount() {…}` in the DOM.
4. **A name describes the value, not its type or its provenance.** `dataArray`, `userObject` and `strName`
   restate what the type already says and go stale when it changes; `usersFromApi` and `cachedList` name an
   implementation detail, so moving the fetch or dropping the cache leaves a name that actively misleads.
5. **Singular for one, plural for a collection.** `const user = await fetchUsers()` is the cheapest bug in
   any review to spot and one of the easiest to write, because the mismatch reads fine locally and only
   breaks where the value is consumed.
6. **Components are nouns; hooks and handlers are verbs.** `<RenderInvoice/>` reads as a function call in
   the JSX and `useInvoiceData` reads as a component in the import list — the casing carries the technical
   distinction, and the part of speech is what tells a reader what the thing is for.
7. **A custom hook starts with `use`, and that is not a style rule.** The linter's rules-of-hooks analysis
   keys on the prefix, so a hook named `getFormState` that calls `useState` gets no checking at all: every
   conditional-call and dependency mistake §5.1 exists to prevent becomes invisible to tooling.
8. Booleans prefixed `is`/`has`/`can`/`should`, including boolean props and JSX flags. **Phrase them
   positively**: `isHidden`, `disableSave` and `isNotReady` all end up read inside a negation, and a double
   negative in a condition is where a reviewer's attention runs out.
9. **Callback prop vs handler**: the prop is `onSomething`, the function implementing it is
   `handleSomething`. Swapping them makes it impossible to tell an incoming contract from a local
   implementation. The handler is then named for what it does rather than for the event that triggered it —
   `handleCreateInvoice` over `handleClick` — because the same click means something different on every
   screen.
10. A hook wrapping a server query is `use` + Resource + `Query`; a hook wrapping a mutation is `use` + verb +
    Subject + `Mutation`. `useBill`, `fetchBills` and `createClientVatMutation` each break it in a different
    way. The pattern is worth the rigidity because it makes the cache shape readable from the import list:
    a reviewer can see which screens read the same resource, and therefore which mutation has to invalidate
    what (§6.3).
11. The result of a mutation hook is stored as the **whole result object** under a derived name, not
    destructured into bare `mutate`/`isPending` — two mutations in one component collide immediately
    otherwise, and the collision is resolved by renaming to `mutate2`, which then means nothing.
12. **Named constants** instead of inline literals: a numeric threshold in a condition, a status code, a
    timeout, a string used as an identifier. A magic value whose meaning isn't obvious from context is a
    comment waiting to be needed. The second cost is duplication: an unnamed value gets retyped somewhere
    else, and then only one of the two copies is updated.
13. Query keys in one casing, camelCase by default, across every key segment — a mismatched key silently
    fails to invalidate, which looks like a caching bug. There is no error, no warning and no failing test;
    the screen simply keeps showing what it showed before the mutation, which is why this one is usually
    debugged in the wrong layer.
14. **One casing convention for filenames, applied everywhere.** The local filesystem is usually
    case-insensitive and CI's is not, so a file imported as `Button` while stored as `button` works on every
    developer's machine and fails only in the pipeline — and the error names a module that plainly exists.
15. **The file is named after what it exports** (§1.1). A component file whose name and export disagree
    breaks the one navigation habit everybody relies on, which is guessing the path from the symbol.
16. **The attribute tests key on has a convention too.** A suite that selects by class name or by visible
    text breaks on a restyle or a translation, and then the test failure says nothing about the behaviour it
    was protecting. A dedicated, consistently named test attribute is what makes the selector survive a
    redesign.
17. **`data`, `item` and `value` are placeholders, not names.** They survive because the first draft of a
    `map` callback only has one thing in scope; the moment a second list is nested inside the first, or a
    query result named `data` is destructured next to another one, the body becomes a puzzle about which
    `data` is meant. Name the element after what it is — and where a hook hands back a generic key, rename
    it at the destructuring rather than living with it.
