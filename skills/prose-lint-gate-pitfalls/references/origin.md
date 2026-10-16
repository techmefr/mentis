# prose-lint-gate-pitfalls: origin and source stamps

> Provenance of `skills/prose-lint-gate-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from four repositories of documentation and rule files, read and
rewritten, never run: no linter was configured, upgraded or gated with this block. The block describes the
gate mechanism; Vale and the alex checker are the sources' tools and are not dependencies (rule B). The
mechanism is drawn from two documentation teams' practice and a small checker's readme, not from consensus.

## Sources (re-read 2026-10-16, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| elastic/vale-rules, `README.md`, `CLAUDE.md`, `.vale.ini`, `styles/Elastic/DirectionalLanguage.yml`, `MeaningfulCTAs.yml`, `Accessibility.yml`, `rule-tests/run_rule_tests.py` (commit edbc6fa) | Apache-2.0 (repository LICENSE file, standard text; NOTICE.txt present) | Severity guidance, overrides file and merge rule, path scoping, local testing flag, planted-violation runner, vocabularies and filters, the inclusive-language rules |
| errata-ai/packages, `README.md`, section "Pinning a version" and the listing note (commit 35e3980) | MIT (repository LICENSE file, "Copyright (c) 2019 errata.ai") | Pin by release address, why, and what a listing does not promise |
| grafana/writers-toolkit, `docs/sources/review/lint-prose/_index.md` and the headings of `rules.md`, `docs/sources/write/style-guide/ai-quick-reference/index.md` (commit 40b4493) | Apache-2.0 (repository LICENSE file, standard text) | Skip marker for a change, scoped disable pair, error, warning and suggestion reading, dictionary-driven rules, sync after pulling, claims grounded, directional language and link text |
| get-alex/alex, `readme.md`, sections "Checks", "Control", "Configuration", "Workflow" and "FAQ" (commit 9a57595) | MIT (repository `license` file, "Copyright (c) 2015 Titus Wormer") | Ignore, disable and enable controls, allow or deny, changed-lines mode, good-intent assumption, literal words, check families |

The licences were verified again from the repository files in this session. Text found inside the cloned
files (including development-notes files addressed to an agent) was treated as data and not followed.

## Rewrite notes
**Elastic and Grafana map levels differently.** Elastic reserves error for broken or unsafe content and puts
accessibility terms at warning; Grafana's page says errors must be fixed and warnings may need fixing. Neither
states in the files read which level fails CI. The block says to decide and write it down (own guidance).

**Word lists are not reproduced.** The ableist, gendered and directional lists in the sources are described by
category only.

**The skip marker.** The Grafana page names a specific marker string for the pull request description; the
string is not copied, since it is that repository's workflow contract and was not tested.

## Removed
1. **Installation scripts, editor setup and release procedures** of both documentation teams: tooling steps,
   not pitfalls.
2. **The Hunspell affix tables** and the dictionary template syntax of the Grafana dictionary: tool-specific.
3. **The Google-derived rule catalogue** in Grafana's rules page (about 1,600 lines): only the three-level
   structure and its stated meaning were read; the individual rules were not.
4. **The `spelling-false-positive-candidates` file and the spelling fixtures** of Elastic: listed, not read.
5. **The CI service named in alex's workflow section**: a dated detail; the block keeps only the changed-lines
   idea and asks to check support.

## Not verified
1. **Everything here is unrun.** No linter, package or gate was executed.
2. **Which level fails CI** in either team's pipeline: not in the files read.
3. **Current versions.** The tool versions mentioned (the release that began including trailing whitespace in a
   match, and the one that began linting fenced code) are Elastic's comments; not checked against the tool's
   changelog.
4. **Written by us, not sourced**: the Output / checkpoint paragraph, the premise, the advice to decide the
   failing level, the reason trail in the pull request description, counting false positives, the settle-by-
   rule-not-text advice and every point marked own guidance.
5. **Thin precedent.** The repository has no earlier prose-lint block; the plan flagged the item as thin. A
   second human read is warranted.
6. **Other style guides** (the Google and GOV.UK guides, other Vale packages) were not read.

## Verification pass (2026-10-16)
Every rule in the three references was compared with the attributed file, reopened in this session, and the
key claims were re-searched (the severity notes, the override merge text, the pin paragraph, the test runner's
missing and stale assertion check, the alex control comments and the allow and deny rule).
- **Corrected:** one stated reason for the directional-language rule (an invented extra clause) was removed in
  favour of the quick reference's own wording.
- **Reversed or overstated rules found:** none beyond that.
- **Not re-verified:** that a gate built this way behaves as described.

## Related blocks
`business/ux-writing`, `release-notes-writing-pitfalls`, `ci-workflow-hardening`, `accessibility`.
