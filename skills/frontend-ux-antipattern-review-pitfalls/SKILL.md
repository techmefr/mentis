---
name: frontend-ux-antipattern-review-pitfalls
description: "Use when frontend UI code (components, pages, forms, interactive flows) is reviewed or written and the review should catch state and recovery defects: layout that shifts under the pointer, no feedback within 100 ms, optimistic updates that silently revert, errors with no way forward, disabled controls with no reason, blocked paste, required fields marked only after failure, hostile input formatters, focus stolen mid-typing, duplicate toasts, modals that cannot be dismissed, destructive actions with no confirmation or undo, redirects that drop the target, state missing from the URL, lost scroll position, double submits, stale responses overwriting newer input, session expiry mid-task, z-index chaos, updates that reset preferences, stale feature flags."
---

# frontend-ux-antipattern-review-pitfalls

Not a step of the pipeline: a craft block for reviewing the behaviour of a user-facing interface. The checklist
shares one premise: **most UX defects that survive review are not about how a screen looks but about what
happens when something goes wrong or happens twice** (a slow response, a failed request, a double click, a
refresh, an expired session), so each category is read as a question about state and recovery. Responsive
layout, touch, viewport and on-screen keyboard rules are in `webperf`; keyboard access, focus indicators,
contrast and ARIA are in `accessibility`; this block does not repeat them and covers the rest.

## When
- Reviewing a pull request or a new feature that touches a component, a form, a flow or a page.
- A user complaint reads "it did nothing", "I lost my data", "it forgot where I was" or "it ordered twice".
- Building a form, a modal, a list with filters, an optimistic update or a wizard.
- Writing the review checklist for a frontend team.

## Steps

**Read the reference once, then scan the code against the categories that apply.** The six axioms in the
reference decide what counts as a finding: every action is acknowledged, user input is never destroyed, state
survives the unexpected, the most recent intent wins, every constraint is explained, and the platform is not
fought.

| Ref | Covers | Read it when | File |
|---|---|---|---|
| 01 | Layout stability, feedback, errors, forms, focus stealing, notifications and dialogs, navigation and URL state, scroll, timing and races, layering, cumulative decay, review discipline | any frontend change is reviewed | [`01-state-and-recovery-defects.md`](./references/01-state-and-recovery-defects.md) |

Symptom to category:

| What the user says | Look at |
|---|---|
| "The button does nothing" | feedback |
| "I clicked the wrong thing, it moved" | layout stability |
| "I lost my form data" | forms, wizard back-navigation, session expiry |
| "Something went wrong" and nothing else | errors |
| "The page jumped while I was typing" | focus stealing |
| "Same notification five times" | notifications |
| "I logged in and it forgot where I was going" | redirects |
| "My order was placed twice" | duplicate submit |
| "I clicked delete and it just deleted it" | destructive actions |
| "The dropdown is behind the modal" | layering |
| "The app gets slower over time" | cache and storage decay |

Routed to the existing blocks, not carried here:

| Topic | Where |
|---|---|
| Touch target sizes, hover as the only affordance, `100vh` versus `dvh`, `autofocus`, horizontal overflow, on-screen keyboard, overscroll containment | `webperf` (`references/01-responsive-touch-interface.md`) |
| Focus indicators removed, keyboard traps, colour as the only indicator, contrast, hover-only content for keyboard users | `accessibility` |

## Output / checkpoint
A review is done when each finding names the pattern, the harm to the user and a concrete fix, tied to a place
in the code; when the categories that did not apply are not reported; and when a clean result says the code is
clean instead of inventing findings. Read the findings once looking for a style preference reported as a
defect, and for a fix that removes keyboard or screen-reader access to cure a visual problem. Nothing here was
verified on a real codebase: the check is a read of the text.

## Guardrails
- Never flag a style preference; flag only what harms the user under the axioms (reference 01, review discipline).
- Never report before reading the implementation: an abort controller, an error boundary or a framework
  loading state may already handle it (reference 01, review discipline).
- Never accept an optimistic update without a visible rollback and a retry path (reference 01, feedback).
- Never rely on a client-side guard alone against duplicate submission; the server needs idempotency for
  critical operations (reference 01, timing).
- Never move focus programmatically while the user is typing somewhere else (reference 01, focus).
- Never ship a destructive action with neither a confirmation naming the consequence nor an undo window
  (reference 01, notifications and dialogs).
- Never carry numeric thresholds as law: the source's 100 ms, 5 second and viewport-share figures are its own
  heuristics (reference 01).
- Never propose a fix that trades one violation for another, such as a visual cue that removes keyboard access.

## Origin
Rewritten from cassiozen's UX-antipatterns, `SKILL.md` and `references/antipatterns.md` (MIT), read 2026-10-16.
A young 2026 repository, one author's practice and not consensus. 🟡: never run by us; open points are in
[`references/origin.md`](./references/origin.md).
