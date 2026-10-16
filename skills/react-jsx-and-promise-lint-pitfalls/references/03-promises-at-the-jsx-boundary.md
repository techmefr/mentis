# react-jsx-and-promise-lint-pitfalls §3 — Promises at the JSX boundary

> Part 3 of `skills/react-jsx-and-promise-lint-pitfalls`. Read it when an `async` function reaches an event
> handler or an array method, or when a promise is dropped. Sourced from the rule pages `no-floating-promises`
> and `no-misused-promises` and the typed-linting page of typescript-eslint (commit `1f205b7`), read 2026-10-16.
> The rule names are the plugin's, written here without its prefix. Sentences marked "own guidance" are ours.

## 3.1 A floating promise
1. **A promise is floating when nothing is set up to handle its error.** The rule lists what counts as
   handling: `await`, `return`, a `.then()` with two arguments, a `.catch()` with one argument, or `void`.
   The rule page lists `.catch()` and `.finally()` called with no callback among the reported cases.
2. **`void` is a marker, not a handler.** The rule page warns that voiding a promise does not change what
   happens at run time: the result is ignored, as with a disable comment, and a rejection is still unhandled.
   Own guidance: use `void` only where you have decided that a failure is acceptable and have said so, and
   otherwise attach a `.catch` that reports the error.
3. **An array of promises is reported too.** `[1, 2, 3].map(async x => ...)` creates promises nobody handles.
   Combine them with `Promise.all`, `Promise.allSettled`, `Promise.any` or `Promise.race`, then handle that one
   promise.
4. **The rule also has options:** `ignoreVoid` (marking with `void` is allowed), `ignoreIIFE`, `checkThenables`
   (treat any object with a `then` method as a promise) and `allowForKnownSafePromises`. Own guidance: turn on
   `checkThenables` only if the project really uses a promise-like that is not `Promise`.

## 3.2 An async function where nothing is expected back
1. **TypeScript lets a function that returns a promise stand in for one that returns nothing.** That is why
   `onClick={async () => { ... }}` compiles. The rule `no-misused-promises` exists for these places and its
   page says they often come from a missing `await` or a misunderstanding of how async functions are awaited.
2. **The result is a rejection nobody sees** (own reading of the rule). The caller ignores the returned promise, so an error thrown in
   the handler is an unhandled rejection and the user sees nothing. Own guidance: in an event handler, that
   usually means a button that appears to do nothing.
3. **Wrap the call in a function that returns nothing and handle the promise:**

```tsx
<button type="button" onClick={() => { save().catch(reportError) }}>
  Save
</button>
```

4. **Or name an async function and call it with its own handling.** The page's pattern is an inner `async`
   function whose call ends with `.catch(handleError)`, so synchronous work around it can use its own
   `try`/`catch`.
5. **Own guidance:** `reportError` should show the user something (a toast, an error state) and log the error;
   the rule only checks that a handler exists.

## 3.3 The places the rule checks
1. **`checksVoidReturn` covers six places** where a function that returns nothing is expected: arguments to a
   call, JSX attributes, object properties, return values, variables, and methods inherited from an interface.
   Each can be switched off separately (`arguments`, `attributes`, `properties`, `returns`, `variables`,
   `inheritedMethods`).
2. **The `attributes` check is the one that covers `onClick` and `onSubmit` in JSX.** Turning it off, as the page
   shows, accepts that an async function can be passed to such a JSX attribute and become a floating promise.
   Own guidance: do not turn it off to silence a few reports; fix the handlers.
3. **Array methods that ignore the result are the other common case.** The page reports `forEach(async ...)`,
   `new Promise(async (resolve) => ...)` and `addEventListener('click', async () => ...)`.
4. **The fixes the page gives:** a `for...of` loop with `await` inside an async function; `Promise.all(array.map(
   async ...)).catch(handleError)` when the calls can run in parallel; an immediately called async function
   marked with `void` inside a promise executor; and, for a class method implementing a synchronous interface,
   making the interface return a promise.
5. **Conditionals and spreads are checked too.** `if (somePromise)` is always true; `{ ...asyncFn() }` spreads
   nothing useful. Await first.
6. **The rule has a stricter sibling,** `strict-void-return`, which the page says also checks non-promise
   values returned where nothing is expected. Not read beyond that line.

## 3.4 Fit with the rest of the project
1. **These rules are hard to switch on in a large existing project** that already has many such cases, the page
   says, and it suggests disabling the rule on specific lines rather than everywhere. It also says the rules
   matter less if global unhandled-rejection handlers are registered.
2. **Own guidance:** switch them on for new and changed files first, with a count of existing reports in the
   pull request description, and aim for zero; a global handler reports the symptom, it does not give the user
   feedback.

## 3.5 These rules need type information
1. **They are type-aware rules.** typescript-eslint says such rules ask TypeScript to analyse the whole project,
   so they are slower than ordinary rules. Both rules are part of its `recommended-type-checked` preset.
2. **Enable typed linting with two changes:** use the `TypeChecked` form of the preset (for example
   `recommendedTypeChecked`) and set `languageOptions.parserOptions.projectService: true`.
3. **To add one typed rule to a project that does not use the preset,** add the rule and the same
   `parserOptions`; the page's example does this for `no-floating-promises`.
4. **Verify** by adding `Promise.resolve(1);` as a statement in a file the project lints and reading the
   report. The page says typed rules still need the `parserOptions` set for the files they run on; own
   guidance: if the rule is listed but no report appears, check that setting first.

## 3.6 Verify
In a clickable component, throw inside an async handler and see the console report an unhandled rejection;
wrap it as in part 3.2 item 3 and see the handler's message instead; run the linter with the typed
configuration and read the count of reports for each of the two rules.
