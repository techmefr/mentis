# vue-nuxt-vuetify-conventions §13 — The data-access client

> Section 13 of `skills/vue-nuxt-vuetify-conventions`. Read it when the front end talks to the backend and the
> project ships a typed client for it. The other sections and the guardrails stay in `SKILL.md`.

Conditional like §8: it applies where the project has a **typed client over its REST API** — an
active-record-style model layer, a generated SDK, a query-builder wrapper. Where there is none, only point 6
holds and the rest is not a gap to fill by hand.

1. **Where a model exists for the resource, every call to it goes through the model** — never a raw
   `$fetch`/`useFetch`/`axios` call to the same endpoint next to it. Two access paths to one resource means
   the URL, the field list and the pagination limit are declared twice and drift once.
2. **Never hand-build the query payload the client generates.** A REST package with a search envelope
   (`lomkit/laravel-rest-api` and its `{ filters, includes, scopes }` shape is the case in reach here)
   exposes a builder precisely because the envelope is easy to get subtly wrong, and hand-writing it also
   throws away the typing. If a resource has no model yet, declare one before writing the call rather than
   after the second copy.
3. **Don't carry another ORM's surface over by muscle memory.** A client that reads like Eloquent or Prisma
   is not that ORM: a method that doesn't exist is a runtime error, and one that exists with different
   semantics (an eager-load helper that filters instead of includes) is worse, because it returns something.
   Read the client's own API for find-by-key, eager loading and relation filtering.
4. **A list is not the same type on both sides of hydration.** A client that wraps collections typically
   returns a plain array during SSR and its own list object once hydrated, so a ref holding one is typed for
   both. Typed as the array alone it type-checks on the server and breaks in the browser — the failure that
   only shows up after a real page load, never in the editor.
5. **Two handles on the same record are one record.** Where the client caches by identity, a field
   assignment is local dirty state on that handle until it is persisted; other components holding the record
   keep seeing the last applied values. Persist through the client's save path. A local-apply escape hatch,
   where one exists, advances the shared copy without a round trip — reach for it only with a stated reason,
   never as a cheaper save. Don't hand-patch a list after a delete either: a self-filtering collection
   already dropped the row, and a manual `splice` on top removes a second one.
6. **A response is untrusted input, whatever produced it.** Validate at the boundary, and never render a
   client object straight into the template (`{{ instance }}`): a non-serialisable handle either prints
   internals or breaks hydration, and the field you meant is the one to interpolate.

## Where the org catalogue governs
A house client is the authority on its own API surface, its decorators and its config. This section is the
generic shape of the rule — go through the model, don't rebuild its payload, type for both sides of
hydration — so the rules survive on a project with no such package, and so an agent recognises a house
override as an override.
