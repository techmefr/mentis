# react-nextjs-conventions §4 — Control flow

> Section 4 of `skills/react-nextjs-conventions`. Read it when conditional rendering, lists, early returns. The other sections and the guardrails stay in `SKILL.md`.

1. **Early returns** for guards: check null/undefined/invalid at the top and return, rather than wrapping the
   entire body in one `if` and burying the happy path under an indent.
2. Never a short-circuit (`condition && sideEffect()`) purely for control flow: `if` states the intent, and
   an expression whose value is discarded reads like a mistake.
3. In JSX, `&&` only on a real boolean. `array.length && <List/>` renders a literal `0` when the array is
   empty — the classic stray zero on screen. Compare explicitly (`array.length > 0`).
