---
name: flutter-conventions
description: Use when writing or reviewing Flutter/Dart: BuildContext across async gaps, disposal, widget decomposition, rebuild scope, layout and overflows, the four async UI states, navigation, state management, storage, tests.
---

# flutter-conventions

Step 6 of the pipeline (`WORKFLOW.md`). Frames the writing and review of Flutter/Dart code. **Special
status**: no production mobile experience behind this block — content comes from the framework's own
documentation, its analyzer lints and an org catalogue for the stack. The matching reviewer (`faramir`) asks
questions rather than asserting, for the same reason.

**Relation to an org skill catalogue.** Where a company ships its own versioned catalogue and a shared UI
kit, both are the authority — **its** components, its SDK, its structure — and override this block wherever
they differ. A shared UI kit in particular inverts several rules below: where one exists, its component is
preferred over the raw framework widget, and the generic advice here applies only to what the kit doesn't
cover. Internal package names are deliberately absent (rule C).

**Applying an override is silent.** Write the code the governing rule actually requires and move on — never
report "a conflict between mentis and the house catalogue" to whoever's watching. That framing reads as
broken to a non-technical stakeholder even when the case is a normal, resolved one, and has already caused a
real project to get abandoned and restarted over nothing. Surface it as a specific, named question only when
no rule anywhere actually resolves the case — never as a general alarm.

## When
As soon as a widget, a screen, a state holder, a repository or a route is written or modified, during
`code` (6) or `tdd` (5).

## Steps

**Read only the sections the task actually touches.** The rules live one file per section under
`references/`; loading all of them for a change that only renames a variable is waste, and a section
read is a section that has to be applied. If you are reviewing a whole diff, pick the rows whose
trigger the diff meets, not the whole table.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | The two mistakes that crash in production | always, before anything else on this stack | [`01-two-mistakes-crash.md`](./references/01-two-mistakes-crash.md) |
| 2 | Widgets and rebuilds | a widget is written, or a rebuild looks too wide | [`02-widgets-rebuilds.md`](./references/02-widgets-rebuilds.md) |
| 3 | Layout | a screen is laid out, or an overflow shows up | [`03-layout.md`](./references/03-layout.md) |
| 4 | Screen states | a screen renders async data | [`04-screen-states.md`](./references/04-screen-states.md) |
| 5 | Navigation | a route, back handling, a deep link | [`05-navigation.md`](./references/05-navigation.md) |
| 6 | Lists and forms | a list, a pagination, a form, the keyboard | [`06-lists-forms.md`](./references/06-lists-forms.md) |
| 7 | State management | a cubit, a bloc, any state holder | [`07-state-management.md`](./references/07-state-management.md) |
| 8 | Data, storage, permissions | persistence, a secret, a platform permission | [`08-data-storage-permissions.md`](./references/08-data-storage-permissions.md) |
| 9 | Text, motion, monitoring | user-visible text, an animation, crash reporting | [`09-text-motion-monitoring.md`](./references/09-text-motion-monitoring.md) |
| 10 | Naming, structure, tests | a file is placed or named, or tests are written | [`10-naming-structure-tests.md`](./references/10-naming-structure-tests.md) |

## Output / checkpoint
Code compliant with the sections above, analyzer clean, no new lint introduced by the diff. Checked by
`gate` (7) and by `faramir` at review time in the `review` step (8).

## Guardrails
No comments in the code produced. Where a shared UI kit exists, **its component wins over a raw framework
widget** — and over the generic advice here. This block has never been confronted with a real production
Flutter project: if a rule diverges from a real observed need, fix this block rather than treating it as
settled, and prefer a question to an assertion when reviewing (that's `faramir`'s register too). Where an org
catalogue is installed and disagrees, **it wins**.

## Origin
Rules mined from market catalogues, linters and internal review feedback, rewritten in the house
voice; the full provenance, the source stamps and the refresh log are in
[`references/origin.md`](./references/origin.md). Read it when checking whether a rule is still
current, not when applying one.
