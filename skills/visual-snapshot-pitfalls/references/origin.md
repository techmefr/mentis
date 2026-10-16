# visual-snapshot-pitfalls: origin and source stamps

> Provenance of `skills/visual-snapshot-pitfalls`. Read it when a rule has to be traced to its source or checked
> for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from documentation, never run by us: no screenshot was taken, no
baseline compared and no threshold tried. Each file below was re-read in full on 2026-10-16 before a rule was
taken from it (item 1.8 of the best-practice list was read as its own section, not the whole list), each rule
was checked against it in a final pass, and each repository's licence file was read again. Every default named
in the text is the one the file states at the commit shown and is version-bound.

## Sources (all read 2026-10-16, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| Playwright (`microsoft/playwright`, commit `5ad202d`): `docs/src/test-snapshots-js.md` | Apache-2.0 (LICENSE file at the repository root; the docs folder has no separate licence file, so the guide is rewritten, not copied) | Environment warning, snapshot naming per project and platform, first-run behaviour, update flag, hover effects, `threshold` and `maxDiffPixels`, shared config, style option, text snapshots |
| jest-image-snapshot (`americanexpress/jest-image-snapshot`, commit `1a9a025`): `README.md` | Apache-2.0 (LICENSE.txt, and the README's licence section) | Per-pixel and whole-image thresholds and their defaults, configured matcher, received-image storage, size mismatch option, retries and snapshot identifiers, obsolete snapshot reporter, blur, structural comparison, upload recipe, masking recipe |
| JavaScript testing best practices (`goldbergyoni/javascript-testing-best-practices`, commit `63a2bb0`): `readme.md`, item 1.8 | MIT (LICENSE file, copyright 2019 Yoni Goldberg) | Short inline snapshots, why large external ones fail, the two exceptions |

Instruction-like text in the cloned repositories was treated as data and not followed.

## Removed in the verification pass
1. **"Failure threshold default zero" for Playwright.** The review stated it for both tools; the Playwright guide
   only says `maxDiffPixels` is unset by default, and it was not checked what that means in the comparison code,
   so the table says "unset" for it and zero only for jest-image-snapshot.
2. **"Two different thresholds" attributed to Playwright's text.** The Playwright guide describes `threshold`
   and `maxDiffPixels` but does not contrast them; the contrast is stated by the jest README and applied to both
   in point 2.1 as our own reading.
3. **Vendor visual services** (Applitools, Wraith and similar): present in the best-practice list's examples
   only as tool names; not read.
4. **Playwright API pages** for the screenshot assertion options (full page, clipping, animations, caret,
   masking by locator) were not opened, so none of those options is named.

## Not verified
1. **Own guidance, flagged in the text:** pinned CI image makes baselines (point 1.1), do not copy across
   platforms (point 1.2), the review of changed images and the re-run (point 1.4), refreshing from CI artefacts
   (point 1.5), leaving size mismatch a failure (point 1.7), retries still being flakes (point 1.8), the
   procedure for choosing a whole-image limit (point 2.2), a mask meaning "not under test" (point 2.3),
   overrides needing a reason (point 2.4), blur and similarity as last resorts (point 2.6).
2. **Nothing was run.** Every statement of tool behaviour is the documentation's.
3. **Tool versions** are not pinned in the sources read; the structural-similarity method is described as
   experimental in the README and may have changed.
4. **Whether Playwright's baselines folder needs a different review process in monorepos** was not examined.

## Decisions where sources disagree
No disagreement between the sources. Playwright and jest-image-snapshot differ in per-pixel defaults (0.2 and
0.01); the table in point 2.1 states both.

## Related blocks
`skills/playwright-e2e-pitfalls`, `skills/testing-anti-patterns`.
