# video-brief-and-storyboard §3 — The storyboard is a proposal

> Part 3 of `business/video-brief-and-storyboard`. Read it when a plan is shown to the person who approves it.
> Sources, read 2026-10-20 in the clone: the story-spine reference (its storyboard section) and the storyboard
> and final-review steps of the product workflow of an Apache-2.0 HTML-to-video framework. Its storyboard-recipe
> and review-loop references were not read. The table shown is our own example. Sentences marked "own
> guidance" are ours. Not marketing advice (`business/README.md`).

## 3.1 Shape of the proposal
1. **Open with the strategy line.** Echo "this video tells [audience] that [message]" (§1.2) before any frame,
   so the person checks the premise before the details.
2. **One row per frame, with a column that says why.** The source's proposal is a table of frame, beat, what is
   on screen and why. Own example, for a short video about a review tool:

   | Frame | Beat | On screen | Why |
   |---|---|---|---|
   | 01, Lost comments | hook | A reviewer scrolls past a thread that has vanished after a new round | Names the pain the audience already has; lands the message in the first beat |
   | 02, One thread | claim | The same thread, pinned to the same paragraph through three rounds | States the message; everything after proves it |
   | 03, Round three | evidence | The tool's real round-comparison screen | Shows the claim working on the real product |

   The "why" is the frame's job in the story, traced to the message; "to look nice" is not a why.
3. **End with the practical footer and ask.** Own guidance and the source's shape: style and length where they
   matter to the decision, then "approve, or tell me what to change". The source's remark is the reason the
   stage exists: a change at this point costs seconds; the same change after the build costs a build.
4. **Recommendations carry their receipts.** The choice of structure, the number of beats and any beat the
   person may question each give their basis (§1.3).

## 3.2 Approval before build
1. **Show the proposal and wait.** The product workflow makes the storyboard a gate: the plan is presented
   and iterated until approved, and only then is anything built. In an unattended run it posts the summary as
   a notice and proceeds, and a final preview carries the one question that remains.
2. **A rough sketch of the frames, before the polished build, is cheaper still.** The source offers a
   sketch-first option: each frame posed as a still, put on one sheet, with the person asked one layout
   question. Own guidance: offer it when the video has more than a handful of frames or when the layout is the
   risk; skip it for a short piece.
3. **Revise only the frames the person named.** Own guidance: a request about frame 4 does not reopen frames
   1 to 3; say what was changed and what was left alone.

## 3.3 The frame with no why
1. **A frame whose why cannot be traced to the message is cut.** The source says the frame is "to cut, not to
   decorate". Ask of each row: if it were removed, would the message get weaker?
2. **A frame can earn its place indirectly.** Own guidance: a pause before the main claim, a breath between two
   dense frames or a closing call to action are fine, provided the why says so. The test is that a reason
   exists, not that every frame carries a fact.
3. **Where the same element continues across a cut, say so in both frames.** The product workflow records a
   hand-off for an element that carries from one frame into the next, with the same position, size and
   direction written in both, so that two people building two frames do not invent two versions of the seam.
   Own guidance: if the same person builds everything, one line suffices.
