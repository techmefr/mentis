---
name: programmatic-video-pitfalls
description: "Use when a video is rendered from code (a frame-by-frame renderer driven by HTML, React or a script) or such a project is reviewed: two renders differ, a frame is blank or flickers, an animation is written to play on its own, a render is started before anyone has looked at a frame, an approach is chosen before the need is clear, or a framework is adopted without reading its licence. Every frame a pure function of time, one paused seekable timeline, the end state laid out first, a lint, snapshot, preview, render-after-approval sequence, and a licence gate."
---

# programmatic-video-pitfalls

A pitfalls block for video produced by code, not a tutorial and not a tool manual. A renderer that captures a
page or a component one frame at a time asks something a browser animation never does: that the picture at time
`t` be the same on every run, on every machine and in every worker that draws it. Most of what goes wrong
follows from forgetting that. The block owns no framework syntax, no encoder settings and no number for duration
or easing (durations and easings belong to a design system, `business/interface-design` §9.9). It owns four
things: the determinism contract, the shape of a timeline a renderer can seek, the order in which a render is
checked before it is paid for, and how to choose an approach and a framework.

What the video says and how it is storyboarded is `business/video-brief-and-storyboard`. Animation inside a
live web page is `skills/web-animation-pitfalls`. Captions, audio descriptions and flashing in the finished
video are `skills/accessibility` §7; delivering a short clip on a page instead of an animated GIF is
`skills/webperf` §5. Whether and how the finished video may be used in advertising, including any test of it, is
not covered here.

## When
- A video is going to be built from code: HTML, React components, a script that draws frames.
- Two renders of the same project differ, a frame is blank, an element flickers or sits in a different place in
  the preview and in the file.
- An animation is written with a play call, a timer, a hover handler or a random number.
- A render is about to be started and nobody has looked at a single frame yet.
- A framework is proposed, or a template is copied from one, and its licence has not been read.

## Steps

**Read only the part the task meets.** Part 1 first when two renders differ.

| Part | Covers | Read it when | File |
|---|---|---|---|
| 1 | Every frame a pure function of time: what may not be read at render time, seeded randomness, finite loops, assets bundled not fetched | any frame depends on something other than the time it is asked for | [`01-frame-as-function-of-time.md`](./references/01-frame-as-function-of-time.md) |
| 2 | One paused seekable timeline, registered only when built; the static end state laid out first; setup-time constants instead of measuring during the animation | a timeline or animation is written, or a frame is blank or misplaced | [`02-timeline-and-end-state.md`](./references/02-timeline-and-end-state.md) |
| 3 | The sequence before a render: lint, snapshot at chosen times, preview, render after approval; a check that reports zero checks | a render is about to start, or a check output is read | [`03-check-before-render.md`](./references/03-check-before-render.md) |
| 4 | Choose the production approach before the tool; the licence gate for a framework and for what it ships | an approach, a framework or a template is being chosen | [`04-approach-and-licence.md`](./references/04-approach-and-licence.md) |

## Output / checkpoint
No pipeline checkpoint. For a project reviewed or started: the production approach chosen and why (§4.1); the
list of things each frame reads, with the time as the only one (§1); where the single timeline is registered
and that it is paused (§2); the checks that ran and what each one reported, including the number of items it
actually examined (§3.3); the frames looked at before the render; the framework's licence conditions with the
date they were read, and the licences of the fonts and media in any template used (§4.3). A render that was
started before the frames were seen is reported as such.

## Guardrails
- Make every frame a function of the requested time and nothing else. Never read the wall clock, an unseeded
  random number, a network response, a pointer or scroll position, or an unbounded loop while drawing a frame
  (§1.1, §1.2).
- Bundle every asset the render needs before it starts. Never fetch a required font, image or data file during
  the render (§1.3).
- Register one timeline per composition, created paused, and register it only after it is fully built. Never
  start it with a play call or leave an early empty registration standing (§2.1, §2.2).
- Lay out the finished frame in static markup first and animate from and to it. Never measure the page while an
  animation runs and feed the result into the animation (§2.3, §2.4).
- Run the checks, look at frames, preview, and render only after the person approves. Never render first to see
  what it looks like (§3.1, §3.2).
- Read a check that reports zero items as "nothing ran". Never read it as a pass (§3.3).
- Choose the production approach for the need before choosing a tool. Never ask a generative video model for
  readable text or a product's real interface (§4.1).
- Read the licence of a framework and of every font, sound and image a template ships, and write the
  conditions with the date. Never call a source-available framework open source, never copy a price into a block
  and never assume bundled media is free to reuse (§4.2, §4.3).
- This block is a method written from documentation and repositories and never run by us: no video was rendered
  and no determinism claim was tested. Sources and open points are in
  [`references/origin.md`](./references/origin.md).

## Origin
Rewritten in our words from the contract and workflow skills of an Apache-2.0 HTML-to-video framework, the video
skill of an MIT marketing skills repository, and the documentation of a second, source-available frame-based
framework (read as digests), 2026-10-20. 🟡: never run by us. Details and licence record:
[`references/origin.md`](./references/origin.md).
