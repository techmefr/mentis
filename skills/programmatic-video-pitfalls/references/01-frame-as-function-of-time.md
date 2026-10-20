# programmatic-video-pitfalls §1 — Every frame a pure function of time

> Part 1 of `skills/programmatic-video-pitfalls`. Read it when any frame depends on something besides the time
> it is asked for. Sources, read 2026-10-20: the determinism rules and core contract of an Apache-2.0
> HTML-to-video framework (read in the clone), and, as digests not verbatim text, the fundamentals, flickering
> and random pages of a frame-based React framework. Sentences marked "own guidance" are ours.

## 1.1 What a frame may read
1. **The renderer asks for a time (or a frame number) and draws that picture; the picture must not depend on
   anything else.** Both frameworks read say this in their own terms: one states that the same input time must
   give the same pixels; the other says an animation should depend purely on the current frame value. The
   consequence is the same for any frame-by-frame renderer, so treat it as the contract of the approach, not
   of one tool.
2. **List what each frame reads, and make the time the only entry.** Own guidance: write the list in the
   review. The usual extra entries, each of which makes two renders differ:
   - the wall clock or a high-resolution timer;
   - a random number with no seed;
   - the answer to a network request;
   - hover, focus, pointer or scroll state, because a renderer produces none of those events;
   - a loop with no end;
   - the order in which frames happen to be drawn.
3. **Frames are drawn in parallel, so state shared between frames is a defect.** The React framework's
   flickering page gives the reason: a render runs across several tabs that share nothing, so an animation that
   advances on its own, or a component that relies on the previous frame having run, shows different things in
   different tabs. The HTML framework's rules likewise forbid two timelines driving the same property of the
   same element at the same time, because which one wins can change between renders. Own example: a counter
   that adds one each time the draw function is called gives a different number per worker; a counter computed
   from the requested time does not.
4. **Preview is a live player and the render is not.** Something that looks right in a preview that plays in
   real time can still break in the file. Check the render's own frames (§3), not only the preview.

## 1.2 Randomness and loops
1. **If something has to look random, derive it from a seed.** A generator seeded with a fixed value, or seeded
   from the element's index, gives the same layout in every worker. The React framework ships its own seeded
   `random()` for this and warns on the unseeded one; the HTML framework tells authors to use a seeded
   generator. A single unseeded call is enough to make two renders differ.
2. **A loop must end at a count worked out from the duration.** An unbounded repeat is acceptable only where
   the renderer clips to a fixed total length, and even then it is the total length that makes it safe, not the
   repeat. When the loop must stop before the video does, compute the count from the duration and the length of
   one cycle and round down: rounding up overshoots the end. Guard the arithmetic so a negative count cannot
   turn into "forever". (One of the frameworks lints for exactly the round-up case; the arithmetic is the same in
   any.)
3. **Randomness that is deliberately fresh per render is a separate decision.** Own guidance: if a variant of
   the video should differ each time, pass the difference in as an input value recorded with the render, so the
   result can still be reproduced.

## 1.3 Assets and waiting
1. **Bundle what the render needs.** Fonts, images, audio and data that a frame requires are local files
   present before the render starts. A required asset fetched at render time makes the result depend on the
   network and the moment.
2. **Where a frame truly must wait for something, say so to the renderer.** The React framework's page names a
   wait call for data and fonts: without it the renderer can capture a half-loaded state, and text measured
   before the font arrives is measured wrong. Own guidance: a frame that is blank in the file and fine in the
   preview is first suspected of drawing before an asset was ready.
3. **Do not hide the symptom.** Rendering with a single worker can make a flicker disappear (the React page
   says so), but it is much slower and does not fix the dependence. Find the shared state or the unseeded value
   instead.

## 1.4 Quick test
Own guidance. Render the same few frames twice, on a clean run each time, and compare them byte for byte or by
a difference image. Frames that differ name the culprit: look at what changed between the runs. This was not
run for this block; it is the cheapest check the contract above suggests.
