# session-retro: origin and source stamps

> Provenance of `skills/session-retro`. Read it when a rule has to be traced to its source or checked for
> freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from one skill file and its documentation page, never run by us. No session was reviewed
with it and no code from the repository was run.

## Sources (re-read in full on 2026-10-19, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| mattpocock/skills, `skills/engineering/retro/SKILL.md` (commit 49dd158) | MIT (LICENSE file, "Copyright (c) 2026 Matt Pocock") | The seven categories and their "use when" triggers, the read-the-repository's-checks-first step, the no-guardrail-is-a-finding rule, the mechanical-versus-judgement classification and the build-the-check default, standards imposed at review rather than implementation, steering files as pointers, present-in-order-of-severity |
| same repository, `docs/engineering/retro.md` | MIT | Propose-only behaviour, the one-session blind spot, the discard-what-you-cannot-trace rule, the default of the current session |

The skill's own instruction to load a separate writing-style skill was not followed (not a dependency of ours).

## What changed in the rewrite
- The source is operator-invoked only and names product files and tool names. Here the block speaks of "the
  steering files" and "the session record" (`CONVENTIONS.md` Rule D).
- The worked cases (query in a loop, a clumsy abstraction) are ours.
- The source is silent on where a pruning rule lives; the pointer to `maintaining-blocks` §4 is ours.

## Removed
Its name and persona, the reference to a hosted dictionary, its chain-position diagram, and every product-specific
filename.

## Not verified
1. **Nothing was run.** The loop was not tried on a real session; the source's usefulness claims are its author's.
2. **Written by us, not sourced:** reading from the stored record for a long session (§1.1.2), the "not a quota"
   point (§1.3.2), the blind-spot statement as a rule of the report (§2.3.4), and the boundary with
   `session-postmortem` and `review` in the block's `When`.
3. **Overlap:** `session-postmortem` diagnoses a bad session with `path:line` evidence and fixes nothing;
   `hooks/README.md` states the check-over-rule doctrine without a loop that produces it. This block is neither.
4. **Not read:** the source's `writing-for-agents` skill, which the retro skill loads, so its writing advice is
   not reflected here.
