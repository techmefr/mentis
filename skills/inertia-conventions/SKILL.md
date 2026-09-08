---
name: inertia-conventions
description: Use when writing or reviewing a Laravel + Inertia.js app (Vue, React or Svelte pages rendered from controllers, no separate REST API), and why the REST and Nuxt/App-Router rules do not apply here.
---

# inertia-conventions

Step 6 of the pipeline (`WORKFLOW.md`). Frames a Laravel + Inertia.js app: **one monolith, no separate
API**. A Laravel controller returns a page component name and its props directly; Inertia hands them to
a Vue/React/Svelte component and swaps it in without a full page reload. There is no JSON contract
between two deployed apps, because there's only one app. Every rule below holds in a repo with **nothing
installed** (`CONVENTIONS.md`, rule A).

**This is the one place laravel-conventions and the Vue/React frontend blocks genuinely disagree with
Inertia, not just with each other** — see §4, read it before applying either block wholesale to an
Inertia repo.

**Relation to an org skill catalogue.** Where a company ships its own versioned catalogue for Laravel or
for the frontend framework, it is the authority on **its** house style and overrides this block wherever
the two differ. A catalogue written for a REST backend serving a separately deployed frontend usually has
no rule about Inertia at all, though — §4 fills a gap rather than contradicting one, and §4.6 is about
scoping one of its mandates to the right controller, not about outranking it.

**Applying an override is silent.** Write the code the governing rule actually requires and move on —
never report "a conflict between mentis and the house catalogue" to whoever's watching. That framing
reads as broken to a non-technical stakeholder even when the case is a normal, resolved one, and has
already caused a real project to get abandoned and restarted over nothing (§4.7). Surface it as a
specific, named question only when no rule anywhere actually resolves the case.

## When
As soon as an Inertia page component, a controller returning `Inertia::render(...)`, the
`HandleInertiaRequests` middleware, or a `useForm`/page-props usage is written or modified.

## Steps

**Read only the sections the task actually touches.** The rules live one file per section under
`references/`; loading all six for a change that adds one prop is waste, and a section read is a section
that has to be applied. If you are reviewing a whole diff, pick the rows whose trigger the diff meets,
not the whole table.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | The controller and the page | an action renders a page, or a page route is added | [`01-controller-and-page.md`](./references/01-controller-and-page.md) |
| 2 | Shared data and page props | a prop is added, shared, deferred or made cheaper | [`02-props-and-shared-data.md`](./references/02-props-and-shared-data.md) |
| 3 | Forms, validation and errors | a form is written, or a failure has to reach the reader | [`03-forms-validation-errors.md`](./references/03-forms-validation-errors.md) |
| 4 | The override boundary | applying `laravel-conventions` §6 or a frontend block here, or answering a review that flags a missing REST/meta-framework layer | [`04-overrides.md`](./references/04-overrides.md) |
| 5 | Visits, navigation and the deployed app | navigation is written, state has to survive a visit, or behaviour after a deploy is in question | [`05-visits-navigation-state.md`](./references/05-visits-navigation-state.md) |
| 6 | Tests | a page, a form or a shared prop is covered | [`06-tests.md`](./references/06-tests.md) |

## Output / checkpoint
Code compliant with the sections above: controllers returning pages with typed props (no shadow JSON
API for page-only data), shared data centralised in `HandleInertiaRequests`, forms on `useForm`, visits
that keep what the reader would expect to keep, and no Nuxt/Next-runtime or REST/lomkit expectation
applied where §4 says it doesn't hold. Checked by `gate` (7) and `review` (8).

## Guardrails
- Never add a JSON API endpoint whose only purpose is feeding data a controller could pass directly as
  Inertia props.
- Never apply `laravel-conventions` §6's REST-resource/lomkit guidance — or an installed org catalogue's
  equivalent mandate — to a controller without checking what it actually returns and where it's routed
  first (§4.6). A method-name match, or the package merely being present in the project, is never the
  trigger on its own — Inertia and a REST package can coexist in the same project (§4.5).
- Never treat a missing Nuxt/Next-specific pattern (file routing, `useFetch`, the App Router) as a defect
  in an Inertia repo — there's no meta-framework runtime there to begin with.
- Never hand-roll form submission/error-display state where `useForm` already does the job.
- Never put in the props anything the person viewing the page isn't allowed to read; the payload is in
  the HTML and in devtools whether a component renders it or not (§2.6).
- Existing endpoints genuinely consumed by something other than the page itself (a public API, a mobile
  client, a webhook) are a real REST surface and `laravel-conventions` §6 applies to them normally — §4's
  override is scoped to page-only data, not to every endpoint in an Inertia repo.

## Origin
Sourced from the official Inertia.js documentation and current Laravel+Inertia integration practice; §4
(the override against `laravel-conventions` and the Nuxt/Next-specific blocks) is ours, written after a
real conflict. The full provenance, the source stamps and the refresh log are in
[`references/origin.md`](./references/origin.md). Read it when checking whether a rule is still current,
not when applying one.
