# release-changelog-pitfalls: origin and source stamps

> Provenance of `skills/release-changelog-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation, never run by us: no release tool was run, no workflow executed and
no attestation created or verified while writing it. Every file below was re-read in full on 2026-10-16 before
a rule was taken from it, and each repository's licence file was read again.

## Sources (all read 2026-10-16, rewritten in our own words)

| Source | Licence | What it gave |
|---|---|---|
| googleapis/release-please (commit `fa67225`), `README.md` | Apache-2.0 (LICENSE file: Apache License text) | What the tool does and does not do, labels, squash-merge advice, footers, the version override, releasable units, the force-run route |
| the same repository, `docs/troubleshooting.md` | Apache-2.0 | Dry-run and log levels, testing on a branch of the real repository, components, how the previous release is found, the closed-label recipe |
| olivierlacan/keep-a-changelog (commit `08d0df5`), `source/en/2.0.0/index.html.md` | MIT (LICENSE file: MIT licence text, copyright Olivier Lacan 2014) | Curation versus drafting, type order and the Fixed versus Changed test, Security and breaking entries, link structure, changelog versus release notes, the role of CI, conflicts, monorepos |
| actions/attest-build-provenance (commit `9d57eef`), `README.md` | MIT (LICENSE file: MIT licence text, copyright GitHub) | What an attestation binds, signing instance by visibility, plan limits, the version 4 wrapper |

The pages come from repositories whose licence file is the repository's licence; no separate licence for the
documentation text is stated, so the pages were rewritten, not copied. Release-please's Apache-2.0 notice is
kept here as attribution. The two code samples in the sources (commit footers, the override section) are
described in prose.

The Conventional Commits specification text and semantic-release were not read, and the specification's repo
licence does not state a licence for the text, so nothing is drawn from either.

## Version bounds stated in the sources
1. release-please: label names and the releasable-prefix list are the files' own at the commit above; the
   language strategies add prefixes (the one example is `docs` for Java and Python).
2. Keep a Changelog: the text is version 2.0.0, which differs from the 1.1.0 text the baseline block was written
   from (part 4 of `release-notes-writing-pitfalls`): the urgency order of the types, the Fixed versus
   Changed test, the CVE lead, the breaking marker and the CI guidance are 2.0.0 statements.
3. Attestation action: version 4 is the wrapper; earlier behaviour is at the v3 tag the README links.

## Removed in the verification pass
1. **"Release-please opens no release PR on rebase and merge commits"** (from the brief) was narrowed: the
   README recommends squash-merge strongly and says merge commits and squash both work for merging the release
   pull request itself; the risks it names for other merge styles are wrong-looking notes, failing points on
   main and the override section not working.
2. **"Attestation silently cannot be created"** (from the brief) was dropped: the README states the plan
   limits and nothing about how the action fails.
3. **Workflow permissions for attestation** were not stated: the README read does not list them.
4. **The strategy table, the Node.js support policy and the Java snapshot pages** of the release-please files
   were left out as tool-specific.
5. **The rest of the Keep a Changelog text** (the contribution and adoption sections) carries no rule.

## Not verified
1. **Nothing was run.** Every behaviour is the sources' claim.
2. **Whether the release pull request's changelog can be edited by hand before merging** was not checked in
   release-please; the text calls it own guidance.
3. **The action `actions/attest`** (usage, inputs, permissions) was not read.
4. **The Conventional Commits text** was not read; the footer and `!` rules are as the release-please README
   gives them.
5. **Written by us, not sourced:** the advice to publish from the tag, recording label state before changing
   it, the checks sections, the plan check before adding the step, pinning and migrating the wrapper, and
   running verification from a machine that did not build.

## Related blocks
`release-notes-writing-pitfalls`, `deprecation-migration`, `ci-workflow-hardening`, `mr-conventions`,
`helm-chart-pitfalls`, `source-freshness`.
