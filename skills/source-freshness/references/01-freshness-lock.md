# source-freshness §5 — The freshness lock

> Reference of `skills/source-freshness`, step 5. Read it when adding a package to the lock, when the sync
> check reports a move, or when wiring the check into a pipeline. The rules of stamping and refreshing stay in
> `SKILL.md`. This mechanism is ours; it has no external source.

## Files
- `references/tracked.json`: one key per package name, `blocks` (the blocks that pin a fact to it, at least
  one) and an optional `note`. A package is tracked when a block states a version-dependent fact about it.
- `references/freshness.lock.json`: one key per tracked package, `version` (a full `x.y.z`) and `generatedAt`
  (`YYYY-MM-DD`, the day the facts were last verified against that version). Keys are sorted.
- `bin/check_freshness_lock.py`, tested by `bin/test_freshness_lock.py`.

## Rules
1. **Add a package in the same change as the block that pins it**: an entry in `tracked.json`, then
   `--stamp`. A block citing a version with no lock entry is invisible to the check.
2. **The lock says what was verified, not what is installed.** Do not bump it to the registry's latest to make
   the check pass; re-read the block's facts for the new version, then stamp.
3. **Stamping is a verification event**, in the sense of `SKILL.md` step 1.4: an edit to the block that does
   not re-read the source does not touch the lock.
4. **The window is 120 days.** Past it the offline check fails, which is the prompt to re-verify or, if the
   block is no longer maintained, to untrack it and say so in its `Origin`.
5. **Moves are major or minor.** A patch release does not fail the sync check; a team that pins patch-level
   facts (a security fix, a bug workaround) records them as dated facts with their own expiry (step 2).
6. **The sync check reads the registry and nothing else.** It runs `npm view <package> version` for each
   tracked package, so it only covers packages published there. A tracked source that is not an npm package
   (a standard, a regulation, a language release) is dated in its `Origin` and out of this lock.
7. **No block, hook or pipeline step depends on the lock** (`SKILL.md` step 4.3): it is an authoring-time
   aid, and a network failure leaves the blocks exactly as fresh as their stamps.

## Mechanical checks

```
python3 bin/check_freshness_lock.py
python3 bin/test_freshness_lock.py
python3 bin/check_freshness_lock.py --sync-check
```

- The first two run offline and belong in the targeted tests; the third needs the network and a person.
