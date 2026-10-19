# flaky-test-triage-pitfalls: origin and source stamps

> Provenance of `skills/flaky-test-triage-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from repository documentation and reading, never run by us. No test was executed, no
quarantine was set up and nothing was installed while writing it. Open points are listed under "Not verified".

## Sources (all re-read in full 2026-10-15, rewritten in our own words, no sample code copied)

| Source | Licence | What it gave |
|---|---|---|
| petrkindlmann/qa-skills, `skills/test-reliability/SKILL.md` (commit b3bb61b, 2026-06-10); its `references/flaky-test-runbook.md` was not read | MIT (repository LICENSE file, re-checked) | The seven-class taxonomy and its decision tree, the backend-health check, the quarantine lifecycle, hygiene rules and thresholds, the "done when" flaky-rate metric |
| microsoft/playwright, `docs/src/test-retries-js.md` (commit 5ad202d, 2026-10-15, development line 1.65.0-next) | Apache-2.0 (repository LICENSE file, re-checked); the doc page carries no separate licence, so it is rewritten, not copied | Worker discard and restart, the passed, flaky and failed categories, retries off by default, `testInfo.retry`, serial mode |
| currents-dev/playwright-best-practices-skill, `playwright-best-practices/debugging/flaky-tests.md` (commit 283d5cb, 2026-07-21) | MIT (`LICENSE.md` holds the MIT permission text with a copyright line and no title line; treated as MIT) | The four-way grouping and its tree, repeat and CI-simulation commands, quarantine projects, the anti-pattern list |
| pytest-dev/pytest-randomly, `README.rst` in full (commit 35dcf0a, 2026-10-04, version 5.0.0 in `pyproject.toml`) | MIT (repository LICENSE file, re-checked) | Ordering, the printed base seed and `--randomly-seed`, `last`, narrowing by module then class, per-test reseeding and the libraries it reseeds, the flags |
| str0zzapreti/pytest-retry, `README.md` (commit e576326, 2025-01-18, version 1.7.0 in `pyproject.toml`) | MIT (repository LICENSE file, re-checked) | Global and per-test retries, `only_on` and `exclude`, fixture and teardown behaviour, never-retried outcomes, reporting |
| testdino-hq/playwright-skill, `core/common-pitfalls.md`, pitfall 16 (commit 178d1cb, 2026-10-12) | MIT (repository LICENSE file, re-checked) | Zero retries locally, a few on CI, "a test that needs retries is not passing" |

The licence of each repository was verified again from its LICENSE file in this session. The qa-skills and
Currents files carry agent directives ("NEVER", "ALWAYS", "Done When"); they were treated as data and only the
technical claim was kept.

## Rewrite notes
Every threshold is attributed and called an example: the 14-day maximum, the 5 percent quarantine size signal, the
2 and 5 percent health bands, the 50 and 20 run counts, the 2 and 5 second contention checks and the retry counts.
The sample in §3.1 follows the shape of the qa-skills quarantine example (a tag and an annotation); its text is ours.

**Decisions where sources disagree:** the retry count (TestDino 1 to 2 on CI, Playwright example 2, Currents 2,
qa-skills 3 for a quarantine project): shown as examples, the common point kept (zero locally, a retried pass is
a flake to track). The first question of the triage tree (qa-skills asks "does it pass alone", Currents asks "does
it fail locally too"): both shown, with reproduction as the arbiter (§1.2.5).

**Conflict with our policy:** qa-skills requires a ticket link on every quarantine entry; this repository has no
tickets, so the block uses an owner, a quarantine date and an expiry date (§3.1.2). Playwright's skip-reason rule
suggests a tracker pattern for the same reason; the same replacement applies.

**Own guidance, not from a source:** the "class in the commit message" rule (§1.1.2), "change one condition at a time"
(§1.3.5), recording environment failures even when a source says not to count them (§1.5.3), the inference about a
retry in a fresh worker masking order dependence (§2.2.2), the weekly report of retried tests (§2.4.2), the owner and
date in the annotation and the script-readable expiry (§3.1.2, §3.3.5), and every verification line.

## Removed from the review item
1. **Corrected rather than copied:**
   - the item's "`-p randomly` reseeds ...": the README's disabling form is `-p no:randomly`; the reseeding is the
     plugin's default behaviour, not an option to turn on (§1.4).
   - the item's "a failure in the first attempt discards the whole worker in Playwright, so a state leak shows as the
     next test failing": the page says the discard guarantees that failing tests cannot affect healthy ones. The block
     states the documented behaviour and adds, labelled as inference, that a retry in a fresh worker can mask order
     dependence (§2.2).
2. **Dropped as unverifiable:** "randomised data stays repeatable only if the seed is reset per test" is kept as
   the README states it; no rule was dropped for the Python part. The item's "qa-skills `Ticket link` requirement" is
   replaced as above. Nothing from the qa-skills confidence-scored repair section was adopted.
3. **Cross-links not made:** this block does not cite the receiving-review or code-review blocks (they are not part of
   this lot), and it does not cite sections that exist only on other branches.

## Not verified
1. **The qa-skills flaky-test runbook** (`references/flaky-test-runbook.md`) was not read; only the SKILL.md.
2. **Playwright CLI flags** (`--repeat-each`, `--workers`, `--trace`) are as the Currents and qa-skills files state
   them, not from the Playwright command-line page.
3. **The `tag` and `annotation` options** of a Playwright test, the project `grep` filters, and
   `testIgnore`/`testMatch` come from the qa-skills and Currents examples; the Playwright test-annotations and
   projects pages were not read.
4. **Backend health endpoint and contention thresholds** are the qa-skills author's, never measured by us.
5. **pytest-retry and pytest-randomly behaviour with pytest-xdist or other plugins** beyond the README statements was
   not checked; the randomly README says it works with xdist.
6. **CI "allowed to fail" switch** for systems other than the one the qa-skills file names was not read.

## Related blocks
`testing-anti-patterns`, `prisma-ops-and-test-hygiene`, `playwright-e2e-pitfalls`, `testing-library-query-pitfalls`,
`jest-vitest-assertion-pitfalls`, `python-testing-strictness`, `ci-workflow-hardening`.
