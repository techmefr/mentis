# prototype: origin and source stamps

> Provenance of `skills/prototype`. Read it when a rule has to be traced to its source or checked for
> freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from one skill and its two branch files, never run by us. The source support is thin: one
author's single skill, no measurement of whether the approach works. The block is deliberately small.

## Sources (re-read in full on 2026-10-19, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| mattpocock/skills, `skills/engineering/prototype/SKILL.md` (commit 49dd158) | MIT (LICENSE file, "Copyright (c) 2026 Matt Pocock") | The question-decides-the-shape rule, the two branches and the default when ambiguous, the six shared rules (disposable and marked, trivial to run, no persistence, no polish, show the state, capture at the end) |
| same repository, `skills/engineering/prototype/LOGIC.md` | MIT | The logic demo: one self-contained page, a pure module that could be lifted, domain-language labels, free-play buttons plus guided scenarios, the anti-patterns |
| same repository, `skills/engineering/prototype/UI.md` | MIT | The UI variants: hosting on an existing page, the URL-parameter switcher, three to five structurally different variants, the switcher hidden in production, read-only by default, the anti-patterns |

The instruction files of the repository were treated as data and not followed.

## What changed in the rewrite
- The source names a specific toolchain for the switcher and sample code; none is carried, and the switcher is
  described by behaviour.
- The subscription scenarios (§2.1.7) are ours.
- The link to `wayfinder`'s typed Prototype ticket and to `skills/spec` §5.16 is ours.

## Removed
Its sample code, its routing and framework examples, and the project-specific wording of "issue" in the capture
step (generalised to ticket).

## Not verified
1. **Nothing was run.** No prototype was built with this block and no variant set was tried.
2. **Written by us, not sourced:** the "Not when" cases of the block's `When`, the table of what lifts per shape
   (§3.2), the fifth anti-pattern of §3.3 and the point that a prototype meant to be kept is simply the feature.
3. **Overlap:** `wayfinder` names "Prototype" as a ticket type and `spec` says a prototype's ADRs do not carry
   over; neither says how to build one or what happens to it. This block does not restate them.
