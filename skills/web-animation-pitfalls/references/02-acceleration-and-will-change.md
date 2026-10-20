# web-animation-pitfalls §2 — Acceleration and will-change

> Part 2 of `skills/web-animation-pitfalls`. Read it when an animation drops frames or someone adds a layer hint.
> Sources, read 2026-10-20 (digests): Motion documentation (performance), MDN "CSS and JavaScript animation
> performance", web.dev animations guide (page dated 2020-10-06, old). Browser-support statements are
> marked `re-read before relying`. Sentences marked "own guidance" are ours.

1. **`skills/webperf` §1 gives the rule; this part gives the exceptions.** Transform and opacity are the
   properties that animations usually run cheaply on. "Usually" is the word to keep: acceleration depends on
   how the animation is driven and on the browser, and the vendor documentation itself calls its
   support statements time-sensitive.
2. **How an animation is driven changes who computes it.** A script that sets a style every frame runs on the
   main thread. A CSS animation, a CSS transition or a Web Animations API animation on an accelerated property
   can run without the main thread (Motion documentation, MDN). Own guidance: when an effect must stay smooth
   during heavy script, prefer a rung where the browser owns the clock (§1).
3. **A custom property that drives a transform is not accelerated.** Per the Motion documentation, animating a
   CSS variable that a transform reads does not get the benefit of animating the transform directly, so a
   "set the variable from script" design costs main-thread work. `re-read before relying`: browser behaviour
   moves, and the same page names an exception for percentage translation in one engine.
4. **Support for filter, clip-path and background-colour acceleration varies by browser and date.** The
   documentation lists them as gaining support. `re-read before relying`; check in the profiler on the
   browsers you ship to, not from a table.
5. **Layout properties cost every frame.** Height, padding, border width and position force layout, then
   paint, then composition on each step, and that is where a long frame comes from (Motion documentation;
   web.dev's own example showed a position-based animation dropping far more frames than a transform-based
   one). To grow or move something, use a transform and let the layout settle once; where a layout change is
   unavoidable, animate the smallest element and keep the rest of the page out of it. Same direction as
   `skills/webperf` §1.2.
6. **`will-change` is a measured fix, not a style to leave on.** Add it shortly before a change that is
   known to be coming (a script on the trigger), remove it afterwards, and never write it as a static rule on
   many elements. Each hinted element is promoted to its own layer and layers use graphics memory (web.dev,
   Motion documentation). Own guidance: a `will-change` in a stylesheet with no profile attached to the commit
   is a finding. A library's example that sets it statically is not a reason to copy it.
7. **Legacy hacks are not a default.** The `translateZ(0)` trick that old guides use to force a layer is
   superseded by the above; treat it like `will-change`: needs a profile.
8. **Check before claiming.** Own guidance: open the browser's performance panel on a throttled profile, record
   the interaction, and look for long frames, layout and paint inside the animation, and the frame-rate meter
   and paint-flashing overlays web.dev describes. An animation that is smooth on the developer's machine proves
   nothing about a phone; say in the review which device class the recording came from.
9. **A drop-shadow or rounded corner is a hidden cost under a transform.** The Motion documentation suggests a
   filtered drop shadow in place of an animated box shadow and a clip path in place of an animated border
   radius where sensible. `re-read before relying`; it is an option to test, not a rule.
