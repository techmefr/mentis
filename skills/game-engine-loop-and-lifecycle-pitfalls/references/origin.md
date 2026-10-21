# game-engine-loop-and-lifecycle-pitfalls: origin and source stamps

> Provenance of `skills/game-engine-loop-and-lifecycle-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from the author's own craft knowledge, with part of the engine facts checked against the Godot documentation on 2026-10-20. Never dogfooded; no engine project was built or run.

## Sources (read 2026-10-20)

| Source | Licence | What it gave |
|---|---|---|
| Godot Engine documentation: idle and physics processing, notifications and ready order, background loading, resources, saving games, node class | CC BY 3.0 (`LICENSE.txt` of the documentation repository read 2026-10-20); credit: Godot Engine documentation contributors; rewritten, nothing copied | Fixed versus per-frame callbacks and the step (§1.1, §1.2), ready order (§2.2.3), removal is not freeing (§2.2.5), threaded loading (§2.4.1), shared resources (§2.4.3), save formats (§2.4.4) |
| Unity documentation | no usable licence (NOASSERTION), not opened | Nothing |

## Removed
- Engine-specific code, API names, performance numbers, rendering, networking and shader topics: not covered.

## Not verified
1. **Checked (one engine):** fixed versus variable callbacks, ready order, threaded loading, shared resources, removal is not freeing. **Also checked 2026-10-20:** autoload lifetime and never freeing one, deferred scene removal, resource cache sharing and duplicate depth. **Unverified:** the catch-up and its cap (the settings page was too large to read), the timing of deferred free, signal ownership and one-shot connections, validity checks on freed references, web export limits, per-frame allocation and lookup cost, input, determinism. Re-read before relying.
2. **Unity and Unreal** are named only as "the same traps"; no engine-specific rule for them was written.
3. **Determinism** (§1.4) is design guidance; no lockstep project was built.

## Related blocks
`c-conventions`, `cpp-conventions`, `source-freshness`.
