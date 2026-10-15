# release-notes-writing-pitfalls §1 — Select and reduce

The failure this section prevents is notes written per commit: noise in, noise out, with the one breaking
change somewhere in the middle.

## 1.1 Reduce to the net outcome
1. **Collapse fixup, revert and follow-up commits into the surviving result.** Three commits that add,
   revert and re-add a flag are one entry or none.
2. **The unit of an entry is a change a reader experiences**, not a commit.

## 1.2 Select by what a consumer can observe
1. **Keep changes a consumer can observe even when they look internal**: default values, error message text
   (people match on it), timeouts and limits; runtime, engine or platform version floors; performance
   characteristics, when there is a measurement; refactors with a behavioural side effect and newly documented
   behaviour.
2. **Drop changes with no consumer surface**: development-only dependency bumps, lint and formatter
   configuration, CI workflows, test-only changes, internal renames, comment and documentation formatting churn.
3. **Never decide from a file name or directory.** A change under a documentation folder can matter to a
   release and a change under the source folder can be pure churn; read what it does.
4. **When the range is too large to write up, rank by consumer impact and set an explicit cut line**, state
   it, and list what fell below it, rather than trimming by feel.

## 1.3 Work from the diff
1. **Most real histories follow no convention.** Assume squash merges and subjects like "wip" until you see
   otherwise.
2. **Work from the diff and the pull request title and body, not the commit subjects.**
3. **Re-check each claim against the diff**: titles overstate, and an entry that trusts one contradicts the
   code.
4. **Group changed files into features by reading the code, then confirm each grouping with someone who
   knows**, before writing entries for it.
5. **Ask for anything you cannot see**: a change behind a feature flag, an infrastructure change with a
   user-visible effect.
6. **Do not propose a commit convention unless asked.** Fixing the pipeline is a different job from writing
   this release's notes.

## 1.4 Verify
For each dropped change write the reason on one line; for each kept change write the commit or pull request
that carries it (this becomes the table in §3.2). A change in neither list was not looked at.
