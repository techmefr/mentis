# angular-conventions §3 — Signals, resources and forms

> Section 3 of `skills/angular-conventions`. Read it when state, derived state, async data or a form is
> written. The other sections and the guardrails stay in `SKILL.md`.

1. **Signals hold local component state, `computed()` derives from it.** A derived value is never copied into
   a second writable signal by hand; it is a `computed()`. Keep transformations pure.
2. **`linkedSignal()` is for state that is derived and also settable**, such as a selection that must reset when
   its option list changes. With a `source` and a `computation` it can keep the previous choice when it is still
   valid, and the generic arguments must then be written out explicitly. An optional `set` lets a write go back
   to the real source of truth instead of the linked copy.
3. **`effect()` is the last tool, never the way to propagate state.** The reach order is `computed()`, then
   `linkedSignal()`, then an effect. An effect that copies one signal into another is a sign the source of
   truth sits too low. Legitimate uses are syncing to non-signal APIs: logging or analytics, `localStorage`
   and cookies, DOM behaviour a template cannot express, canvas or third-party chart rendering. Effects run
   asynchronously during change detection and always at least once.
4. **Never call `mutate` on a signal**: use `set` or `update`, so every change is a new value that consumers
   can compare.
5. **Async data is a `resource`, not a subscription copied into a signal.** `params` is the reactive input,
   `loader` is the async function; a `params` that returns `undefined` leaves the resource `idle` and the loader
   unrun, which is the way to express "no id yet". Use `stream` for sources that emit many values (sockets,
   server-sent events), `loader` for one-shot fetches. Pass the loader's `abortSignal` to the request: a
   changed `params` aborts the in-flight load and an ignored signal leaves the stale request running.
6. **Render from the resource's `status`, not from `value` alone.** `idle`, `loading` (value empty),
   `reloading` (previous value kept), `resolved`, `error` and `local` (set by hand) are six different screens;
   a template that tests only `value()` shows a blank during load and an empty state during an error.
7. **Chain dependent resources with `chain()`**, not by reading the upstream `value` inside `params`. Reading
   the value makes the downstream resource `idle` while the upstream loads or fails, hiding the real state;
   `chain()` mirrors loading and error. Pass the chained value directly (`chain(user)?.companyId`), because
   wrapping it in an object makes `params` defined even when the inner value is `undefined` and the loader runs
   with it. If you only derive a value synchronously from a resource, use `computed()`.
8. **An `id` on a resource caches it for server rendering through the transfer state**, which serialises the
   value into the page. Never set it on data specific to the requesting user when the rendered HTML can be
   cached or shared.
9. **HTTP reads that are reactive on signals use `httpResource`**, which goes through the HTTP stack and so
   through interceptors (§4).
10. **New forms use Signal Forms** (`@angular/forms/signals`, stable from Angular 22): the source of truth is
    a writable signal model, validation is a schema, types are inferred from the model. When not using them,
    prefer Reactive forms to template-driven ones for anything beyond a trivial form. Do not mix two form
    systems inside one form.
11. **Reactive forms in a zoneless application do not schedule change detection on `setValue`,
    `patchValue` or `FormArray.push`.** Either mark the view for check from the form's observables or reflect
    the data through signals the template reads (§5.16).
12. **Build dynamic forms from data, never from a template string that carries user input** (§5).

## Mechanical checks

```
grep -rnE "\.mutate\(" src
grep -rnE "effect\(" src --include=*.ts
grep -rnE "\.subscribe\(" src --include=*.ts
grep -rnE "(value|hasValue)\(\)" src --include=*.html | grep -v "status\|isLoading\|error"
```

- Every `effect(` hit is read: if the body only writes another signal, it is a `computed()` or a
  `linkedSignal()`.
- A `subscribe` whose callback only assigns a field is a `resource`, an `httpResource` or an interop call.
