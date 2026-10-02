# § 7 — Media, motion and orientation

> Section 7 of `skills/accessibility`. Read it when a diff adds audio or video, an autoplaying or moving
> element, scroll-driven effects, or anything that depends on screen orientation. The general
> reduced-motion rule is §3.9; this section names the cases it does not spell out. Success-criterion
> numbers are cited so the exact conditions are read at the standard (WCAG 2.2), never from memory.

## Prerecorded and live media

1. **Video with speech or meaningful sound has synchronised captions** (1.2.2). Use a `track` element of
   kind `captions` with a language, on the native `video`; auto-generated captions are a draft to correct,
   not a deliverable. Captions carry speaker changes and non-speech sound that matters.
2. **Meaningful visuals are described.** A video whose visuals carry information that the soundtrack does
   not gets an audio description track or a text alternative that covers it (1.2.3, 1.2.5). Audio-only
   content gets a transcript (1.2.1); live content gets live captions where the criterion at the target
   level asks for them (1.2.4).
3. **Controls are real and reachable.** The native `controls` attribute is keyboard-operable and named.
   A custom player owes the whole contract (§1, §2.8): play, pause, volume, captions toggle, progress,
   fullscreen, all focusable with visible state.
4. **No sound starts by itself.** Audio that plays automatically is a barrier for anyone using a screen
   reader, who cannot hear their reader over it; the criterion (1.4.2) requires a way to stop or control it
   independently of system volume. Autoplay on the web is also gated by the browser; a muted, looping
   background clip is the allowed form, and it still needs a visible pause when it lasts (2.2.2).
5. **A video has a poster.** The `poster` attribute shows a frame before playback; it also reserves the
   space and gives a still image to the reader (and prevents a layout shift, `skills/seo` §3.2). Lazy
   media is covered in `skills/webperf` §5.7.

## Flashes and moving content

6. **Nothing flashes past the limit.** Content that flashes more than the standard allows can trigger
   seizures (2.3.1); the exact general-flash and red-flash thresholds are read from the criterion, never
   from a recalled number. Animated GIFs, video clips, canvas effects and CSS animations all count; the
   simplest policy is no flashing at all, and a tool that analyses a recording is the check.
7. **Moving, scrolling or auto-updating content can be paused, stopped or hidden** when it starts without
   the visitor's action and continues past the criterion's duration (2.2.2). Carousels, tickers,
   background videos and live feeds are the cases; the control is the first thing in the component
   (§8.11).
8. **Large motion follows the preference.** `prefers-reduced-motion: reduce` is honoured for parallax,
   zoom, large translation and scroll-triggered animation, not only for transitions (§3.9; 2.3.3 at the
   higher level). The reduced variant keeps the information and the feedback and removes the movement.
9. **Smooth scrolling is opt-in by preference.** `scroll-behavior: smooth` is applied inside a
   `prefers-reduced-motion: no-preference` condition, so anchor jumps are instant for people who asked for
   less motion. Scroll-linked and parallax effects are built the same way, with the static layout as the
   default and the movement as the enhancement (`skills/webperf` §2.8 for the cost side). A scroll
   behaviour that replaces the native one is §1.14.

## Orientation and input modality

10. **The layout does not lock the orientation.** Content works in portrait and landscape unless one
    orientation is essential, as for a piano keyboard or a cheque scan (1.3.4). Do not call the
    orientation-lock API, do not set an orientation in an installed-app manifest without that need, and
    do not hide content with an `orientation` media condition.
11. **Do not assume a modality.** A feature that needs a gesture, a hover or a physical keyboard has an
    alternative (§1.7, §1.12); `pointer` and `hover` media features describe the primary input and are
    used for layout adaptation in `skills/responsive-layout`, never to remove a capability.

## Mechanical checks

```
grep -rnP '<video\b(?![^>]*\bposter=)' src
grep -rL '<track' $(grep -rl '<video' src)
grep -rnE '\bautoplay\b' src
grep -rnE 'scroll-behavior:\s*smooth' src
grep -rLE 'prefers-reduced-motion' $(grep -rlE 'scroll-behavior:\s*smooth|@keyframes' src)
grep -rnE 'screen\.orientation\.lock|"orientation"\s*:|@media[^{]*orientation' src public
```

- Each `autoplay` hit is read for `muted`, `loop`, `playsinline` and a reachable pause.
- A count of `@keyframes` is a reading list, never a verdict.
- Captions, descriptions and flashes are judged on the media itself, by a person, on the real file.
