# compose-correctness: origin and source stamps

> Provenance of `skills/compose-correctness`. Read it when a rule has to be traced to its source or checked
> for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and reading, never run on a real Compose app by us. No composable
was written, no layout inspector was opened and no compiler report was read while writing it.

**Fold-in note.** This block is meant to be folded into a Compose reference of `kotlin-android-conventions`
(that block exists only on the unmerged branch) when PR 118 lands. It is standalone only so that it does not
depend on a block that is not yet on main.

## Sources (all read 2026-10-08, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| The Android developer pages on Compose state, where to hoist state, side effects, phases, performance best practices, lists, stability, fixing stability and strong skipping (pages show "last updated 2026-10-01") | Android developer content licence (prose CC-BY 4.0, code Apache-2.0, per the page footer) | §1, §2.1 point 1, §2.2, §2.3, §3 |
| Four skills from one Compose performance skill repository: choosing derivedStateOf, deferring state reads, collecting flows safely, using efficient effects | Apache-2.0 (LICENSE read) | §1.4 points 3 to 5, §2.1 points 2 to 5, §2.2 points 2 to 4 |

The MIT-licensed Compose expert skill repository was opened for this block (its modifier reference only) and
used for no phrasing: its modifier-order rule could not be confirmed on an official page. Two other
Apache-2.0 sources named in the review (a second skills repository and the sample app's agent notes) were not
read for this block.

## Rewrite notes
Rules are re-explained principle first. The stability section follows the documentation's own statement that
strong skipping changes the comparison from `equals` to instance equality for unstable types; an earlier,
common formulation ("a plain List parameter blocks skipping") is correct only before Kotlin 2.0.20 or with
strong skipping off, and is written that way.

## Not verified
1. **Compose version numbers.** The pages read carry no Compose release number. Versions named in the block
   come from the pages' own mentions: Kotlin 2.0.20 for strong skipping, Compose 1.2 for `contentType`,
   lifecycle-runtime-compose 2.6 for the lifecycle-aware collector.
2. **The lambda-provider and "do not pass a `Flow`" rules** come from one Apache-2.0 skill, not from an
   official page; the rationale about skipping that the skill gives was left out because it does not hold
   under strong skipping.
3. **Compiler reports and the layout inspector** are named only as ways to measure; their output format and
   commands were not read.
4. **Dropped from the source list:** "give `Modifier` as the first optional parameter and apply it to the
   root" and the modifier-ordering rule (not confirmed on an official page), "previews for states, not the
   happy path" and "no allocations in hot composables" (no page read states them), "use `remember { }`
   rather than `LaunchedEffect(Unit)` for a one-off" (the skill's reasoning confuses recreation with
   recomposition and was not confirmed), and "measure recomposition in a release build" (the official page
   read does not state it).
5. **Written by us, not sourced:** the checks lists.

## Related blocks
`accessibility` (touch targets and labels in a Compose UI), `testing-anti-patterns`, `webperf` (the web
counterpart of recomposition cost).
