# inertia-conventions — origin and source stamps

> Provenance of `skills/inertia-conventions`. Read it when a rule has to be traced back to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

Sourced from the official Inertia.js documentation (shared data via `HandleInertiaRequests`, `useForm`,
partial reloads, lazy/deferred props, asset versioning, the visit lifecycle, history state) and current
Laravel+Inertia integration practice (typed props generated from the same DTO/resource the backend
returns, Laravel Precognition for real-time validation reusing the submission's own FormRequest rules).
Mechanisms rewritten, no copied text. Stamped 2026-08-11.

**§4 is ours.** The override boundary against `laravel-conventions` and the Nuxt/Next-specific blocks was
written after a real conflict surfaced: an Inertia repo was reviewed against REST/lomkit and Nuxt-runtime
expectations that don't hold for that architecture. No existing skill named the boundary, in this repo or
in the installed org catalogue (its Laravel and Nuxt plugins), which don't cover Inertia either.

**§4.5/§4.6 went through two revisions the same day.** A first pass checked only whether the REST package
was a project dependency at all — too coarse for a project using **both** Inertia (for its pages) and a
REST package (for a genuinely separate API surface), which is a real, coherent architecture, not a
contradiction. The current version checks the specific controller — what it returns, where it's routed —
rather than the project as a whole, which is the only version of the test that gets the mixed case right.

**§4.7 was added 2026-08-11**, after a CdP running the already-fixed version still had their own session
report "a conflict between mentis and the house rules" and deleted their whole setup over a case that was
resolved. Every stack block's override paragraph now says explicitly to apply the resolution and move on.

**Sectioned and deepened 2026-09-08.** The block was a single `SKILL.md` of 1,705 rules words — the
`laravel` row of `CATALOG.md`'s depth table is the widest deficit in the repo, and this was one of the
three blocks in it. The five inline sections became six files under `references/` with a router table in
`SKILL.md`; the depth pass then went through each of them the way the `laravel`, `react`, `flutter`,
`code-baseline` and `python` blocks were done, one numbered point per real failure mode, mechanism plus
what the reader actually sees. Every original point was kept verbatim and its number preserved, because
§4 is cited from three other blocks (`laravel-conventions` §6, and the intros of
`vue-nuxt-vuetify-conventions` and `react-nextjs-conventions`) and §4.5/§4.6 are cited from this block's
own guardrails. §5 is the only genuinely new section: the original block said nothing about the visit
lifecycle — scroll and state across a visit, cancelled visits, asset versioning after a deploy, the page
data that lives in the browser's history entry, prefetching, SSR being optional — which is where most of
an Inertia app's observable behaviour actually comes from. Tests moved from §5 to §6 as a result; nothing
outside the block cited that number.

**No dedicated in-house Inertia production experience yet.** A solid base from the framework's own
documentation, not proven doctrine — which is why the block's status in `CATALOG.md` stays 🟡 regardless
of its depth. Depth is not dogfooding: the sections now state the failure modes the documentation and the
framework's own mechanics imply, and a real project is what would confirm which of them actually bite.
