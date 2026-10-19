---
name: angular-signals-rxjs-ssr-pitfalls
description: "Use when Angular code mixes RxJS with signals (toSignal, toObservable, takeUntilDestroyed, rxResource), when an Angular app is server-rendered or hydrated (RenderMode per route, hydration mismatches, event replay, HTTP transfer cache, browser-only code), when it runs zoneless (NgZone stability hooks, PendingTasks, reactive forms), when reviewing signal and template mistakes that lint rules catch (uncalled signals, computed that returns nothing, async lifecycle hooks, negated async pipe, impure pipes, outerHTML), or when configuring DI tokens, app initializers, typed forms and major-version updates."
---

# angular-signals-rxjs-ssr-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for the Angular failure modes that compile, render once, and then
leak, flicker, double-fetch or go stale. The sections share one premise: **a signal is a function, an
Observable is a subscription, and the server render is a different runtime from the browser one; each
rule below names what you see when it is missed**.

Standalone block, written because the broader Angular conventions block exists only on an unmerged branch.
It is meant to be merged into the same-named framework block when that lands (see
[`references/origin.md`](./references/origin.md)). Until then it stands alone and cites only blocks present
on the main branch.

## When
- A component or service turns an Observable into a signal, a signal into an Observable, or subscribes by hand.
- Server rendering, prerendering or hydration is being set up, or a hydration mismatch, a flicker on load or a
  doubled request appears.
- The app is, or is becoming, zoneless.
- Reviewing signal-based components and templates, or a diff that adds an `effect`, a `computed` or an async pipe.
- Adding an injection token, a startup task, a form, or planning an Angular major update.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | RxJS interop: toSignal, toObservable, takeUntilDestroyed, rxResource | an Observable meets a signal, or a manual subscription is added | [`01-rxjs-interop.md`](./references/01-rxjs-interop.md) |
| 2 | SSR and hydration: render mode per route, hydration constraints, event replay, transfer cache | the app is server-rendered or prerendered, or hydration misbehaves | [`02-ssr-and-hydration.md`](./references/02-ssr-and-hydration.md) |
| 3 | Zoneless: removing zone.js, stability hooks, PendingTasks, forms, tests | the app is zoneless or loses zone.js | [`03-zoneless.md`](./references/03-zoneless.md) |
| 4 | Signal and template mistakes a linter catches | a component, effect, computed, pipe or template is written or reviewed | [`04-signal-and-template-mistakes.md`](./references/04-signal-and-template-mistakes.md) |
| 5 | DI tokens, app initializers, route inputs, typed forms, major updates | a token, a startup task, a route-bound input, a form or an Angular update is touched | [`05-di-forms-updates.md`](./references/05-di-forms-updates.md) |

## Output / checkpoint
Each rule was exercised, not read off the file: the page was loaded with the server render and the browser
console showed no mismatch error (§2), the app was started with zone.js removed and the screen still
updated after an async result (§3), the component was destroyed and the subscription stopped (§1), the
lint rules named in §4 were run on the diff by the project's own tooling. A change that only compiled is
not verified.

## Guardrails
- Never call `toSignal` repeatedly for the same Observable: each call is a subscription (§1).
- Never put `takeUntilDestroyed()` in a lifecycle method or a plain method without passing a `DestroyRef` (§1).
- Never use `ngSkipHydration` as the fix: it is a last resort that removes hydration for that component (§2).
- Never branch the rendered content on the platform in a template (§2).
- Never remove `NgZone.run` and `runOutsideAngular` just because the app is zoneless (§3).
- This block states Angular facts as of the documentation on the date in the Origin section; Angular moves
  fast, so check an API or a default against the version in use. Nothing was built or run while writing it.
- Accessibility and image performance points that a template rule touches belong to `accessibility` and
  `webperf`.

## Origin
Rewritten from the Angular repository's documentation (MIT), the angular-eslint rule documentation (MIT)
and one MIT Angular skill set, read 2026-10-08. 🟡: never run by us; open points are in
[`references/origin.md`](./references/origin.md).
