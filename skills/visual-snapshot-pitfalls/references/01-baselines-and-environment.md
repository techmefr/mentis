# visual-snapshot-pitfalls §1 — Baselines and environment

> Section 1 of `skills/visual-snapshot-pitfalls`. Read it when baselines differ between machines or are created,
> updated or stored. Restated from the Playwright guide `docs/src/test-snapshots-js.md` (commit `5ad202d`,
> Apache-2.0) and the jest-image-snapshot README (commit `1a9a025`, Apache-2.0), read 2026-10-16. Option names
> and defaults are version-bound. Sentences marked "own guidance" are ours.

1. **Make and compare baselines in the same environment.** Playwright warns that rendering varies with the host
   operating system, its version and settings, the hardware, the power source (battery or adapter) and headless
   mode, and says to run tests where the baselines were generated. Own guidance: for a team that means one
   pinned CI image makes the baselines and compares them, and a developer's laptop is not a place to
   generate or update them.
2. **A baseline belongs to a platform and a browser.** Playwright names the file with the test name, the project
   (browser) and the platform, for example a Chromium-on-Mac name, because rendering, fonts and more differ.
   On the first run it reports that a snapshot does not exist, writes the actual image and, to get a stable
   one, takes screenshots until two consecutive ones match. Own guidance: a "missing snapshot" failure on a new
   platform means generate the baseline there; do not copy one across.
3. **Commit the baselines and review changes to them.** Playwright says to commit the snapshot folder and review
   any change to it; jest-image-snapshot stores baselines in a snapshot folder beside the tests or in a
   configured one.
4. **Update with the explicit flag, then look at every changed image.** Playwright updates with its update
   snapshots flag, jest-image-snapshot with Jest's update flag. Own guidance: an update that "makes the suite
   green" is a decision about what the product should look like; treat the changed images as code in the review,
   and re-run without the flag to confirm.
5. **Keep the received image when a failure happens on CI.** jest-image-snapshot's option to store received
   images separately from the composed diff image is off by default and is described as useful when updating
   baselines from CI; the README adds that where the file system does not persist you need to upload the images
   a failed run produced, and gives a reporter recipe for it. Own guidance: a pipeline that refreshes baselines
   should do it from those artefacts of the pinned image, then go through point 1.4.
6. **Obsolete baselines pile up.** jest-image-snapshot's update flag does not delete image files that are no
   longer used; its outdated-snapshot reporter does when an environment variable is set, and the README warns
   not to run it on a partial suite because snapshots of tests that did not run look obsolete.
7. **A size mismatch is a failure; leave it one.** jest-image-snapshot fails when the two images have different
   dimensions and has an option to allow it, off by default. Own guidance: a different size usually means the
   viewport or layout changed, which the test exists to catch.
8. **Retries need unique snapshot names.** The README notes that Jest's retry feature helps screenshot tests
   with frequent false positives, but then a custom snapshot identifier must be unique per snapshot, as it is the
   only reliable way to tell snapshots apart. Own guidance: a test that only passes on retry is still a flake to
   explain (see `skills/playwright-e2e-pitfalls`).
9. **Hover state is part of the picture.** Playwright says screenshots capture hover effects present at that
   moment; move the mouse to a spot that triggers none, or hover an element with no effect, before the capture.
