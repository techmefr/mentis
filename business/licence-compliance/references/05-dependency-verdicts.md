# licence-compliance §5 — Verdicts, records and the CI rule

> Section 5 of `business/licence-compliance` (the numbers 1 to 4 of that file are inline in `SKILL.md`). Read it
> when dependencies are checked in bulk, by a scanner or in CI, and a verdict must be recorded. It adds verdict
> states, records and a CI rule; the licence categories are in step 1 of `SKILL.md` and are not restated.
> Sources, read 2026-10-16: the `shcherbak-ai/licenseal` repository (Apache-2.0, commit `e2bc3b8`), files
> `docs/concepts/verdicts.md`, `licenseal.review.toml` and the "not legal advice" line of `README.md`; the
> Free Software Foundation page https://www.gnu.org/licenses/license-list.en.html (English version; the
> statements quoted below on Apache-2.0 and AGPLv3 were read); the SPDX License List page
> https://spdx.org/licenses/ (its version line read: 3.29.0, 2026-09-16). Sentences marked "own guidance" are
> ours. Not legal advice; the decision on strong or network copyleft stays with counsel.

1. **Use four verdicts, not two.** The licenseal documentation sorts each dependency into compatible, warning
   (the combination may be acceptable but the tool cannot tell, so a person decides), violation, or unknown (the
   licence is missing or cannot be classified, so a person reads it). Own guidance: adopt the four states and
   count "unknown" as never compatible; it is routed to a person who reads the licence text.
2. **Some licences cannot be auto-classified.** The same page lists source-available and use-restricted
   licences (it names SSPL, BUSL, Elastic, FSL, Parity, PolyForm, CC-BY-NC and CC-BY-ND among others) as
   "unknown", routed to manual review. Own guidance: send them to a person even when a scanner has a
   label for them.
3. **The verdict is relative to our own licence and to how we distribute.** The licenseal matrix compares each
   dependency's risk level with the project licence. Own guidance: record, with each verdict, the licence we
   ship under and the way the dependency reaches users (shipped binary, source, hosted service), because the
   same dependency can be a different case for each.
4. **Identify licences by SPDX identifier, and read the text from the official source.** The SPDX List is a
   list of commonly found licences with a standard short identifier, the full name, the licence text and a
   permanent URL for each; the version read is 3.29.0 of 2026-09-16, and the list changes, so note the version
   used. Own guidance: a deprecated or ambiguous identifier is resolved by the list, and an unrecognised
   string stays "unknown".
5. **Compatibility is stated by the licence steward, not by a tool or a blog.** Example read on the FSF page:
   Apache-2.0 is described as a free software licence compatible with version 3 of the GNU GPL and not
   compatible with GPL version 2, for stated reasons (certain patent-termination and indemnification
   provisions). The AGPL version 3 is described as the terms of GPLv3 plus an additional paragraph, in section
   13, allowing users who interact with the software over a network to receive its source. These are the
   FSF's statements, not ours, and a question about a pair not on its page goes to counsel. The pair-level
   rules in licenseal beyond the Apache-2.0 and GPL pair were not checked against the licence texts and are
   not carried.
6. **Keep a checked-in review file.** The licenseal repository holds a review file with, per dependency, the
   ecosystem, package, version, the reviewed licence and a note, generated for each flagged dependency. Own
   guidance: keep ours in the repository with package, version, accepted licence, reason, who decided and the
   date, so a warning is decided once, and re-open the entry when the version changes.
7. **A dev-only dependency is a lower-severity finding, and says so.** The licenseal page says that a violation
   on a development dependency is reported as a warning. Own guidance: label the finding "dev only" in the
   report; do not drop it, since a dev dependency can end up bundled.
8. **Resolve transitive dependencies from lockfiles.** Own guidance (it extends step 1 of `SKILL.md`): the risky
   licence is often several levels down, so read the lockfile and not only the manifest.
9. **Decide in advance what fails the build.** Own guidance: write the rule down before the first run (for
   example, violation and unknown fail the build and a warning does not, or stricter), run the check in CI, and
   re-run it when a dependency's major version changes, since licences change there (as step 2 of
   `SKILL.md` already says for upgrades).
10. **A tool verdict is an aid.** The licenseal README states that it is not legal advice and not a
    substitute for legal review. The decision on strong or network copyleft in a shipped product stays with
    counsel (`SKILL.md`, guardrails).
