---
name: web-animation-pitfalls
description: "Use when choosing a browser animation tool (CSS, Web Animations API, an animation library, a Lottie or Rive asset, a video) or reviewing animation code that stutters, replays, outlives its component, skips its exit, or loses meaning under reduced motion: pick the cheapest tool that fits, check acceleration instead of assuming it, tear down what a component created, and read what a library's reduced-motion switch really removes."
---

# web-animation-pitfalls

A pitfalls block for animation on the web, not a tutorial. `skills/webperf` §1 already says what to animate
(transform and opacity, no `transition: all`, interruptible, reduced-motion variant) and `business/interface-design`
§9 says whether a motion should exist at all. This block covers the gap between them: which tool to reach for,
what that tool costs, how an animation is stopped when its component goes away, and what the platform's newer
primitives are. It owns no library syntax and no numbers: durations, easings and springs belong to the design
system (`business/interface-design` §9.9). Related: `skills/webperf` §1 (the per-property rules), `skills/accessibility`
§7 (reduced motion, pause controls, flashes), `business/interface-design` §9 (motion as meaning),
`skills/react-nextjs-conventions` rules 15 and 27 (animate a wrapper not the SVG, View Transitions),
`skills/flutter-conventions` §9 (the native-app counterpart).

## When
- A new animation is about to be built and a tool has to be chosen.
- A library is added "for one animation", or an existing one is questioned.
- An animation janks, replays twice, keeps running after navigation, ignores its exit, or flashes at the wrong
  size.
- A reduced-motion setting is added to a project that uses an animation library.
- A designer hands over an authored animation file (Lottie, dotLottie, Rive) or asks for a looping clip.

## Steps

| Part | Covers | Read it when | File |
|---|---|---|---|
| 1 | The ladder of tools by cost: CSS, Web Animations API, library, authored asset, video; the licence line for a library | a tool is chosen or a library is proposed | [`01-choosing-the-tool.md`](./references/01-choosing-the-tool.md) |
| 2 | Acceleration is not a guarantee, `will-change` as a measured fix, how to check | an animation drops frames or someone adds a layer hint | [`02-acceleration-and-will-change.md`](./references/02-acceleration-and-will-change.md) |
| 3 | Lifecycle: teardown with the component, exit animations and presence, layout animations, asset runtimes | animation code lives inside a component, a list or a route | [`03-lifecycle-and-presence.md`](./references/03-lifecycle-and-presence.md) |
| 4 | Reduced motion beyond the media query, scroll-driven CSS as the first choice for scroll-linked effects | a reduced-motion switch is wired, or an effect follows scroll | [`04-reduced-motion-and-scroll.md`](./references/04-reduced-motion-and-scroll.md) |

## Output / checkpoint
No pipeline checkpoint. For each animation reviewed or added: the tool chosen and the rung of the ladder that
justifies it; how it is stopped when its owner goes away; what the reduced-motion path keeps; and, where the
claim is about acceleration or browser support, the evidence (a profile, or the page re-read on the date) or the
words "re-read before relying". An animation with no stated teardown is not finished.

## Guardrails
- Start from the cheapest rung that does the job, and move up only for a named reason (logic, gestures, layout,
  exit, a designer's asset). Never add a library to animate one state change that a transition handles.
- Tie every animation's lifetime to its owner: what a component starts, the same component stops. Never leave a
  timeline, trigger, listener or runtime instance to be collected by luck.
- Treat acceleration as something to check in the browser's profiler, not as a property of a CSS name. Never claim
  "this runs on the compositor" from a rule of thumb alone.
- Put the static, finished layout first and the movement on top, so a missing feature, a disabled script or a
  reduced-motion preference lands on a usable page. Never make the end state exist only as the last frame of an
  animation.
- Read a library's reduced-motion switch against the meaning the motion carries (`business/interface-design`
  §9.8) before trusting it. Never assume the switch removes everything or only the decoration.
- Record a library's licence in one sentence and re-read it when the product changes; the block cannot judge a
  licence's prohibited uses. Never state a price, a bundle size or a browser-support date from memory.
- Never put a numeric duration, easing curve or spring setting in this block or copy one from a source: they are
  values a design system owns.

## Origin
Motion, MDN, web.dev and GSAP documentation, Rive and Lottie documentation, plus the ideas of three skill
collections (two MIT, one Apache-2.0), read 2026-10-20 and rewritten. Provenance, what was removed and not verified:
[`references/origin.md`](./references/origin.md). 🟡: never run by us.
