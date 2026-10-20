# game-engine-loop-and-lifecycle-pitfalls: origin and source stamps

> Provenance of `skills/game-engine-loop-and-lifecycle-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from the author's own craft knowledge. Never dogfooded; no engine project was built or run.

## Sources (read 2026-10-20)

| Source | Licence | What it gave |
|---|---|---|
| None opened. The Godot documentation repository (CC BY 3.0 per the review) was not opened for this block; engine facts are general knowledge stated in our own words | n/a | Nothing taken |
| Unity documentation | no usable licence (NOASSERTION), not opened | Nothing |

## Removed
- Engine-specific code, API names, performance numbers, rendering, networking and shader topics: not covered.

## Not verified
1. **Every engine behaviour** (deferred free, ready order, signal ownership, shared resource loading, web export limits) is stated generally and was not checked against current engine documentation or run. Re-read before relying.
2. **Unity and Unreal** are named only as "the same traps"; no engine-specific rule for them was written.
3. **Determinism** (§1.4) is design guidance; no lockstep project was built.

## Related blocks
`c-conventions`, `cpp-conventions`, `source-freshness`.
