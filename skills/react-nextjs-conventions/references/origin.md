# react-nextjs-conventions — origin and source stamps

> Provenance of `skills/react-nextjs-conventions`. Read it when a rule has to be traced back to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

Ideas taken from: a market React skill catalogue (perf/rendering/waterfall patterns) for the Next.js
rendering rules; a market React/Node catalogue (`redux-toolkit`) for the RTK paragraph; a market shadcn
catalogue for the component-library section; a market React linter (the `oxlint-plugin-react-doctor` package,
a registry of ~780 deterministic rules, `error`-severity subset filtered for relevance outside niche
frameworks) for the effects/security section; a market open source TypeScript project (the
`typescript-review` skill) for the accessibility/bundle-weight items; **an org skill catalogue for this stack
(36 skills: file and component structure, container/presentational split, naming across identifiers, verbs,
booleans, handlers, query and mutation hooks, typing including derived types, string unions, assertions and
schema validation at boundaries, control flow, hooks discipline, immutability, memo discipline, library-owned
state, query-key factories, mutation callback split, atomic store selectors)** — rules extracted,
de-identified and rewritten generically, with everything naming an internal library or project deliberately
left out (rule C). Mechanisms rewritten, no copied text. Stamped 2026-08-06.

Re-checked directly against the public **React Doctor** tool (react.doctor, the linter this block's
effects/security section already traces to) on 2026-08-10: its documented rule set added three genuine gaps
— prop drilling across component layers (§1.6), several `setState` calls for one logical update belonging
in a `useReducer`/derived value, and a hand-rolled `isLoading` boolean where `useTransition` already applies
(§5.12-13) — plus a missing-`alt` check folded into the existing icon-label rule (§10.1). Everything else it
flags (unnecessary derived-state effects, array-index keys, hardcoded secrets, incorrect hook usage) was
already covered here under a different heading.

**Depth pass 2026-09-08 — all ten sections.** Every section stated its rules and stopped there, so this
pass kept each original point verbatim and added, per point, the mechanism and what the reader actually
sees when the rule is broken; new points were written only where a section was *silent* on a failure mode
rather than terse about one. Before → after: §4 control flow 116 → 1,005 words, §9 security 124 → 1,010,
§8 component library 145 → 944, §10 accessibility/bundle 159 → 909, §7 Next.js 193 → 922, §3 typing
210 → 912, §2 naming 275 → 940, §6 server state/stores 284 → 975, §1 components/files 300 → 952, §5
state/effects/hooks 496 → 1,207. The ten sections alone go 2,302 → 9,776 words; with the router, 3,002 → 10,476.

The additions worth naming are the ones the block had no line about at all, not the elaborations. On the
security side: a `NEXT_PUBLIC_` variable is published content, inlined into every user's bundle at build
time and impossible to un-publish (§9.3); everything a Server Component passes to a Client Component is
serialised into the HTML payload, so handing a whole model row down ships every column it has (§9.10, and
§7.9 from the other direction); a hand-written `POST` route handler authenticated only by a cookie has no
origin check, which Server Actions do carry (§9.11); identity is never read from anything the client can
set (§9.8); and a client-side role check hides a control without protecting anything (§9.9). On
correctness: changing which element wraps a subtree unmounts it, so an "optional card" around a form
destroys what the user typed (§4.9), while the same mechanism used deliberately through `key` is the honest
way to reset a form (§4.10); a cleanup runs on every dependency change and not only on unmount, which for
an unstable dependency is a socket that reconnects on every render (§5.15); state seeded from
`localStorage` or `window` renders differently on the server and makes React discard the tree (§5.19); a
query key missing one of its inputs makes two different requests share a cache entry, so changing a filter
shows the previous filter's rows (§6.4); and reading cookies or headers opts a whole route tree out of
static rendering, which makes a shared helper a rendering decision (§7.5).

Two structural notes. `§4.2` is new and resolves a real collision: the guard-first habit of §4.1 and the
rules of hooks (§5.1) disagree about where an early return goes, and neither section had said so. And the
numbering of the three points this block's 2026-08-10 React Doctor re-check had added — §1.6 prop
drilling, §5.12-13 setState-count and `useTransition`, §10.1 missing `alt` — was deliberately preserved,
since the stamp above cites them; all twenty-eight intra-block `§N.M` references were then re-checked one
by one against the current numbering, and four that the renumbering had left pointing at the wrong rule
were corrected (§3.4 → §3.9 for exhaustiveness, §3.6 → §3.15 for boundary validation, §6.2 → §6.3 for the
key factory, §7.8 → §7.13 for the exported Server Action).

Measured against the org catalogue's react plugin (36 skills, 9,302 words), this block is now the first to
cross it: 10,476 words of rules against 9,302, where it stood at x3.1 before the pass. That is a
same-subjects-same-depth statement about this stack only, and it is the cheapest of the remaining stacks to
cross — the react catalogue is the thinnest of the four the operator's plugins carry.
