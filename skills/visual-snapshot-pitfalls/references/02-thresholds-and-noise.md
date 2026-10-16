# visual-snapshot-pitfalls §2 — Thresholds and noise

> Section 2 of `skills/visual-snapshot-pitfalls`. Read it when a comparison is flaky or a tolerance is about to
> be raised. Restated from the Playwright guide `docs/src/test-snapshots-js.md` (commit `5ad202d`, Apache-2.0),
> the jest-image-snapshot README (commit `1a9a025`, Apache-2.0) and item 1.8 of the JavaScript testing best
> practices list (`goldbergyoni/javascript-testing-best-practices`, commit `63a2bb0`, MIT), read 2026-10-16.
> Defaults are the tools' at those commits and version-bound. Sentences marked "own guidance" are ours.

1. **There are two different thresholds; do not mix them up.** One decides which pixels count as different,
   the other decides how many different pixels fail the test.

   | Tool | Per-pixel colour sensitivity | Whole-image failure limit |
   |---|---|---|
   | Playwright | `threshold`, 0 (strict) to 1 (lax), default 0.2 | `maxDiffPixels`, unset by default |
   | jest-image-snapshot | `customDiffConfig.threshold`, default 0.01 | `failureThreshold`, default 0, in pixels or in percent through `failureThresholdType` |

   Both build on the same pixel-comparison library. The jest README says plainly that its failure threshold is
   not the per-pixel one. The two tools' per-pixel defaults differ by a factor of twenty, so a number copied
   from one tool's example does not mean the same thing in the other.
2. **Tune the whole-image limit on purpose, and write the reason down.** Own guidance: the first value is the
   strictest one that passes two unchanged runs on the pinned image; a larger one needs the observed difference
   that justified it next to it in the code, and is revisited when it is touched. A limit widened until nothing
   fails turns the test into decoration.
3. **Mask a dynamic region instead of widening a threshold.** Playwright's style option applies a custom
   stylesheet during the capture, so volatile elements can be hidden (its example hides iframes), and it can be
   set once in the config. The jest README's Puppeteer recipe removes or modifies the elements before the
   screenshot, and suggests hiding with `visibility` when removal breaks the layout. Animations, dates and ads
   are the usual regions. Own guidance: a mask is a statement that the region is not under test; say so in the
   test name.
4. **Share the defaults in configuration; override per call only with a reason.** Playwright takes `threshold`,
   `maxDiffPixels` and the style option in the config, globally or per project; jest-image-snapshot builds a
   configured matcher with shared defaults. Own guidance: a per-call override without a comment of why is the
   place thresholds creep.
5. **Keep text snapshots short and inline.** The best-practice list says to use only short, focused snapshots
   (it suggests 3 to 7 lines) inside the test, not in external files: a snapshot of a thousand lines gives a
   thousand reasons to fail, changes with every space or minor markup tweak, and tempts the author to accept a
   document nobody read. Its exceptions: asserting on a schema rather than on data, or a document that rarely
   changes. Playwright also compares text through its snapshot matcher and stores it beside the test, to be
   committed and reviewed like an image.
6. **Blur and structural comparison are noise tools, not defaults.** jest-image-snapshot can blur both images
   (a radius of 1 or 2 pixels is suggested for scaling noise) and has an experimental structural-similarity
   method for which it suggests a 1 percent failure limit. Own guidance: try masking and a pinned environment
   first; use these only when the remaining noise is documented, and expect to re-read the README for the
   current status of the experimental method.
