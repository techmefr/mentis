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
