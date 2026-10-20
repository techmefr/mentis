# programmatic-video-pitfalls §2 — One paused timeline and the end state first

> Part 2 of `skills/programmatic-video-pitfalls`. Read it when a timeline or animation is written, or when a
> frame is blank or misplaced. Sources, read 2026-10-20: the core skill, determinism rules and layout contract
> of an Apache-2.0 HTML-to-video framework (read in the clone). The React framework's pages were not read for
> this part. Sentences marked "own guidance" are ours. Whether a timeline library may be used is §4.

## 2.1 A timeline the renderer can position
1. **Create exactly one timeline per composition, paused.** The renderer positions it at the requested time; a
   timeline that plays by itself runs on the clock, which is §1.1 again. The framework read states the shape:
   one paused timeline registered under the composition's own identifier, never started by script for
   anything the render depends on.
2. **Register it only when it is fully built.** If the build waits for something (the fonts, a measurement),
   register at the end of that step. An empty timeline registered early is treated as ready and the animation
   renders blank, and the frame stays frozen at the start when two or more are registered and one key does not
   match its composition. A blank video with no error is the usual sign.
3. **The total length is set by the composition, not by whichever timeline is longest.** In the framework read,
   a timeline that runs past the declared length is cut off and one that ends early holds its last frame, and the
   declared length is read once before scripts run. Own guidance: fix the duration where the composition is
   declared and make the timeline fit it, rather than the other way round.
4. **Do not add empty tweens only to stretch a duration**; declare the duration where durations are declared.
5. **Let the framework own what it owns.** The framework read says it shows and hides each timed element
   itself, and rejects an animation of visibility on one of them. Animate a child, or the element's opacity.
   Own guidance: whenever a renderer has taken responsibility for a property, a second writer is the bug.

## 2.2 Two writers, one property
1. **One property of one element is driven from one place.** A style set in the stylesheet and a tween that
   starts from the same property fight: the starting value of the tween and the stylesheet disagree and the
   first frame is wrong. The framework read lints this for transforms. Set the starting state inside the
   animation (animate from a stated value to a stated value), not in two places.
2. **Do not centre with the same transform you animate.** The usual case is a translate used to centre an
   element and a tween that moves the same element: centre with the layout engine (flex or inset) and keep the
   transform for the movement.

## 2.3 The end state first
1. **Lay out the finished frame in static markup and style, then animate from or to it.** The framework's layout
   contract puts it this way, and it is the same advice as `skills/web-animation-pitfalls` guardrail on the
   static layout: if the layout is right when no animation runs, a missing animation costs a motionless frame,
   not a broken one.
2. **Give the root a fixed frame size and let the contents fill it** with padding, flex and grid rather than
   hand-placed offsets. Hard-coded pixel sizes on a nested root rather than the declared canvas size are a
   silent layout bug the framework warns about.
3. **Position for the largest frame.** An element that pulses or overshoots needs room at its peak and must not
   sit on a clipping edge, or it overlaps a neighbour or is cut. Own example: a badge that scales up 20 percent
   by the middle of a scene is positioned for that size, not for its resting one.
4. **Text is laid out by wrapping, not by forced breaks.** A hard line break ignores the real width of the font
   and doubles the break when the line already wraps. Let the container wrap and give long text a maximum width
   or a fit step.
5. **Transforms need a sized block.** A scale on an inline element, or on a block whose width is zero, shows
   nothing. Give an animated bar or fill a real size first (the framework marks this as a silent failure no
   automated check may catch).

## 2.4 Measure at setup, not while it runs
1. **Compute layout constants once, before the animation, and animate between values fixed at that point.**
   The framework's layout contract provides measurement helpers that work off a canvas, so nothing reflows, and
   keeps shared caches out of reach so that one render cannot depend on what another did. The reason is §1.1:
   frames are drawn in parallel, and a value measured from the page during an animation can differ between
   workers.
2. **Wait for fonts before measuring text.** Both sources read say it: text measured before the font arrives is
   the wrong size (the framework builds its registration on a fonts-ready step; the React page lists unawaited
   fonts as a cause of a bad frame).
3. **The same rule appears in `skills/web-animation-pitfalls` §3** (values fixed at setup) for a browser
   animation; here it is a requirement rather than a preference.
