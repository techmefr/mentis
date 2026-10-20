# programmatic-video-pitfalls §3 — Check before you render

> Part 3 of `skills/programmatic-video-pitfalls`. Read it when a render is about to start or a check output is
> being read. Sources, read 2026-10-20: the validation list and first-pass notes of an Apache-2.0 HTML-to-video
> framework's core skill and the final steps of its product-video workflow (read in the clone). Command names
> are that tool's and are not carried here. Sentences marked "own guidance" are ours.

## 3.1 The order
1. **Static checks, then frames, then a preview, then the render.** The framework's own list runs in that
   order: a lint of the structure, a browser-based check of runtime errors, layout, motion and contrast, stills
   taken at chosen times and looked at, a preview for the person to review, and the render last, only after
   approval. Own reasoning, and the reason the order is cheap: a mistake caught on a still costs a few seconds,
   the same mistake caught in a finished file costs a full render and a second approval.
2. **Choose the times for the stills on purpose.** Own guidance: the middle of every scene, and for every cut
   one moment just before and one just after it. The middles show layout and text fit; the pair around a cut
   shows whether an element that is meant to carry on actually does. The workflow read does this and compares
   the two images at each cut for a visible jump in position, scale, opacity or direction.
3. **Look at the stills, do not only run the tools.** A tool cannot see a caption sitting over the face it
   should not cover or text that is technically inside its box but unreadable. Put the stills side by side in
   one sheet and read them.
4. **The render waits for the person.** The preview is the one question to the person: render now, or what
   changes. A render started before that answer is spending time and compute on a version nobody has approved.
   Where the work runs without a person present, post the same summary and the sheet of stills as a notice and
   say so; do not present it as an approval.
5. **Do not rerun every check after the render unless asked.** The render is the last step; if the file is
   wrong, the cause is in the source and the loop starts again from the check.

## 3.2 Failing cleanly
1. **If a command fails, show its error and stop.** The workflow read says not to pile recovery commands on a
   failure. Make the smallest edit to the file that the error names, then rerun the command that failed.
2. **A failed capture of source material is a stop, not a prompt to invent.** The reasoning belongs to the brief, in `business/video-brief-and-storyboard` §5. The same point holds in a
   build: do not carry on with what a failed step left half-written.

## 3.3 A gate that examined nothing
1. **Read the count of items a check examined, not only its verdict.** The framework's core skill warns that an
   error in the lint also switches off the layout and contrast checks, and those then report zero samples and
   zero text checks. The output looks like a clean file and means nothing ran.
2. **A check that reports zero items has not passed.** Own generalisation: a gate that examined nothing is
   missing, whatever its exit code says. Clear the error that disabled it, rerun, and report how many items it
   saw.
3. **Put the number in the report.** Own guidance: "layout check: 38 samples, 0 findings" is evidence; "checks
   pass" is not.

## 3.4 What this does not cover
No check here replaces a person watching the finished video, and none of the automated checks read covers the
accessibility of the result (`skills/accessibility` §7: captions, descriptions, flashing).
