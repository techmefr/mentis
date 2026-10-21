# code-review-reviewer-pitfalls: origin and source stamps

> Provenance of `skills/code-review-reviewer-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from published review guidance, never run by us. No review was held and no process was
changed while writing it. Open points are listed under "Not verified".

## Attribution (CC BY 3.0)
This block adapts material from Google's engineering practices documentation
(https://github.com/google/eng-practices), which is licensed under the Creative Commons Attribution 3.0 Unported
licence (https://creativecommons.org/licenses/by/3.0/). Changes made: the text was reworded and restructured, the
Google-internal terms ("CL", "LGTM", references to Google's style guides and tooling) were replaced by neutral ones,
and the document's numbers were relabelled as examples; no sentence was copied. Google does not endorse this block.

## Sources (re-read in full 2026-10-16, rewritten in our own words, no sample code copied)

| Source | Licence | What it gave |
|---|---|---|
| google/eng-practices (commit 3bb3ec2, 2024-09-18), `review/reviewer/standard.md`, `speed.md`, `comments.md`, `pushback.md`, `looking-for.md` (all sections read; used for the standard, context, every-line and tests parts) | CC BY 3.0 (the repository LICENSE file is the Creative Commons Attribution 3.0 Unported legal code, re-checked; the README states the documents are CC-By 3.0); attribution given above | The approval bar, the principles, conflict resolution, severity labels, courtesy, guidance versus fixing, praise, explanations, response time and its example maximum, focus, approve with comments, large changes, pushback, the cleanup promised for later, strictness complaints, review of tests, context and every line |
| google/eng-practices, `review/developer/small-cls.md` (same commit, read in full) | CC BY 3.0 (as above) | Why small, what small means and its size examples, when large is acceptable, separating refactorings, tests with code, not breaking the build, splitting strategies, getting consent for an unavoidable large change |
| mgreiler/code-review-checklist, `README.md` (commit 35875e6, 2026-07-29, read in full) | MIT (repository LICENSE file, re-checked: "MIT License", Michaela Greiler) | Only the testing and testability questions (§4.5); the rest is a generic checklist with no failure mode behind each line |

## Rewrite notes
Every number is the Google document's example for one organisation: the one-business-day maximum response, the one
hundred and one thousand line sizes, the two hundred lines in one file against fifty files. They are labelled as
examples where they appear.

**Decision where the source conflicts with this repository:**
1. **Stacking changes** (small-cls, "Stacking Multiple Changes on Top of Each Other"): not carried; the repository's
   practice is one change per merge on the main line (§3.8). The other splitting strategies are carried.
2. **Comments in code** (comments.md and looking-for.md, "add a code comment" and "comments explain why"): not
   carried; this repository keeps comments out of code (§2.4). The source's point that explanations given only in the
   review tool do not help future readers is carried.
3. **Filing a bug and a TODO comment for deferred cleanup** (pushback.md, looking-for.md): the bug becomes a note in the
   change description with an owner and a date, and the TODO comment is dropped (§4.3).
4. **A reviewer writes no fix**: the source says fixing is the author's job (§2.3), which agrees with the house rule that
   a reviewer in review-only mode never edits the code under review. The rule is stated for the reviewer and is not a
   derivation from the source.

**Own guidance, not from a source:** the cross-links, the output checkpoint, and the sentence in §2.3.1 that ties the
source to the review-only rule.

## Removed from the review item
1. **Not carried, as Google tooling or organisation specific:** the terms "CL" and "LGTM", references to Google's style
   guides and documentation tool, the hiring remark in the every-line section, the link to Chromium's respect document,
   and the cross-time-zone paragraph beyond one sentence.
2. **Not carried from the checklist:** the "ethics and morality" section and the generic implementation, security and
   readability prompts; they are not about defects in a way a reviewer can check against a rule.
3. **Cross-links not made:** the review block's own reference files are not on the main line, so none is cited.

## Not verified
1. **`review/emergencies.md`** was not read; what counts as an emergency is only stated as the source's single exception
   (§1.2, §4.3).
2. **`review/reviewer/navigate.md`, `review/developer/handling-comments.md`, `cl-descriptions.md` and `index.md`** were
   not read. The advice on quick initial broad comments (§3.4) is as speed.md states it, not from navigate.md.
3. **The effect of any threshold** (response time, change size) on your team was not measured; they are the source's
   examples.
4. **The research on interruption** cited in speed.md was not looked up.

## Related blocks
`receiving-review-pitfalls`, `review`, `over-engineering-review`, `mr-conventions`, `testing-anti-patterns`.

## Section 5 (`05-agent-written-code-debt.md`), added 2026-10-20
**Status: 🟡.** One source, licence file read the same day: `wshobson/agents`,
`plugins/skill-forge-essentials/skills/ai-debt-detector/SKILL.md` (MIT, root LICENSE, copyright 2024 Seth Hobson;
the plugin manifest declares MIT for its own author). It gave the five audit questions (failure modes, orphans,
edge cases, invented dependencies, drift from patterns), the red-flag list and the "compilation is not
correctness" reminder (points 1 to 3, 4, 5, 7 to 9). Ours: the registry lookup for new packages and the
no-rate statement (points 5 and 11), deprecated interfaces (6), asking for the command run (10). Not taken:
its rate claim ("significantly higher than people"), which cites nothing, and the trigger of "20 or more lines
generated". Not run on a real review. This section is not Google material and carries no CC BY text.
