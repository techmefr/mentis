---
name: visual-snapshot-pitfalls
description: "Use when tests compare screenshots or stored snapshots against a baseline (Playwright toHaveScreenshot, jest-image-snapshot, text and DOM snapshots): which environment makes and compares baselines, the two different thresholds (per pixel colour and whole-image failure), masking dynamic regions instead of widening them, updating baselines and reviewing the diff, received images on CI, retries, and keeping text snapshots short and inline."
---

# visual-snapshot-pitfalls

A block for the tests whose assertion is "this looks like the file we stored". Two things make them fail for the
wrong reason: the baseline was made in an environment the comparison does not run in, and the tolerance was
widened until the test could no longer fail. Both sections come from tool documentation (Playwright and
jest-image-snapshot) and one best-practice list, read at the commits in `references/origin.md`; option names and
defaults are version-bound. Locators, waits and test isolation are in `skills/playwright-e2e-pitfalls`; weak
assertions in general are in `skills/testing-anti-patterns`. Visual review by a person (design QA) is a
different job and is not covered.

## When
- A suite adds screenshot assertions or a baseline folder, or its screenshot tests fail on CI and pass locally.
- A threshold or a retry count is raised "to stop the flakes".
- A baseline update is about to be committed, or a pipeline has to refresh baselines.
- A test stores a large text, DOM or JSON snapshot.

## Steps

**Read the part for the failure you see.**

| Part | Covers | Read it when | File |
|---|---|---|---|
| 1 | Baselines and environment: where they are made, naming per platform, committing, updating, CI artefacts, obsolete files, retries | baselines differ between machines, or are created, updated or stored | [`01-baselines-and-environment.md`](./references/01-baselines-and-environment.md) |
| 2 | Thresholds and noise: the two thresholds, defaults, shared config, masking, blur, small inline text snapshots | a comparison is flaky, or a tolerance is about to be raised | [`02-thresholds-and-noise.md`](./references/02-thresholds-and-noise.md) |

## Output / checkpoint
For each visual test: the environment that makes the baseline and the one that compares it (they are the same
image), both thresholds with the reason for any non-default value, what is masked or hidden and why, and how a
baseline update is reviewed. Evidence is two runs on the CI image with no change that both pass, and one
deliberate small change (a moved element or a changed word) that fails with a diff image you opened.

## Guardrails
- Never make baselines on a developer machine for a suite that compares on CI (point 1.1).
- Never copy a baseline made on one platform to another; generate it there (point 1.2).
- Never raise the whole-image threshold to hide a dynamic region; mask the region (point 2.2, point 2.3).
- Never commit a baseline update without opening the changed images (point 1.4).
- Never allow a size mismatch to pass (point 1.7).
- Never keep a large external text snapshot nobody reads (point 2.5).
- Do not paste a real customer's screen into a baseline; use made-up data.

## Origin
Rewritten from the Playwright visual comparison guide (Apache-2.0), the jest-image-snapshot README
(Apache-2.0) and one item of a JavaScript testing best-practice list (MIT), read 2026-10-16. The full provenance,
what was removed and what is our own guidance are in [`references/origin.md`](./references/origin.md). 🟡: never
run by us.
