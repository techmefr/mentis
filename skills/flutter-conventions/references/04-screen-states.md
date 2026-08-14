# flutter-conventions §4 — Screen states

> Section 4 of `skills/flutter-conventions`. Read it when a screen renders async data. The other sections and the guardrails stay in `SKILL.md`.

1. **An async view renders all four states explicitly: loading, success, empty, error.** Never a blank
   screen, never stale content presented as fresh. This is the rule that makes a mobile app feel finished.
2. A useful empty state: an illustration or icon, a short explanation, and the primary action that would
   fill it. "No data" alone tells the user nothing to do.
3. A friendly error state with a **Retry** — a raw exception string on screen is a bug report shown to a
   customer.
4. Prefer content-shaped skeleton placeholders over a centred spinner for content that has a known shape:
   the layout doesn't jump when the data lands.
