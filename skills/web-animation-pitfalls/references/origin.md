# web-animation-pitfalls: origin and source stamps

> Provenance of `skills/web-animation-pitfalls`. Read it when a rule has to be traced to its source or checked
> for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from published sources, never run on a real animation by us.

## Sources (read 2026-10-20, restated in our own words, no text copied)

Every web page below was read through a fetch tool that returns a small model's digest, **not the verbatim
page**. Wording, figures and dates were not checked at the page itself.

| Source | Licence | What it gave |
|---|---|---|
| GSAP, `gsap.context()` docs and React guide (gsap.com), read this session | Vendor documentation; idea only | One collection per component and one revert; things created after the hook are outside it; development double-run exposes missing teardown; dependency changes do not revert by default; listeners need removing |
| GSAP standard licence page (gsap.com/community/standard-license), read this session | Proprietary no-charge licence, effective 30 April 2025, last modified 30 May 2025, holder Webflow; not open source | The one-sentence licence line (§1.5) |
| Motion documentation: `AnimatePresence`, layout animations (motion.dev), read this session | Vendor documentation; idea only | Wrapper stays mounted, stable keys, exit modes, nested propagation; layout animation as transforms and its caveat list |
| Motion documentation: performance and React accessibility, MDN "CSS and JavaScript animation performance", web.dev animations guide (dated 2020-10-06) | Vendor and public documentation; idea only | Carried from the same-day review digests and not re-fetched in this session (only the web.dev date was re-checked): main-thread versus compositor, variable exception, layout cost, `will-change` discipline, the global reduced-motion mode and what it skips |
| MDN Web Animations API page, read this session | Public documentation; idea only | What the API is and that `element.animate()` returns a controllable animation object; the page has no compositor, support or Baseline statement and does not describe cancel, finish or commit members |
| MDN CSS scroll-driven animations (first 100000 of 130853 characters) and `animation-timeline` (first 100000 of 150673), read this session | same | Feature-query fallback pattern; the property page carried a "limited availability" banner (not Baseline); no engine list, no Baseline date and no accessibility note were in the text read |
| Rive web runtime docs (rive.app), read this session | Vendor documentation; idea only | State machine must be named, cleanup call frees native objects, reduced motion only a demo link |
| LottieFiles documentation landing page (docs.lottiefiles.com), read this session | Vendor documentation; idea only | dotLottie exists as a delivery format next to Lottie JSON; the detail pages were not reached |
| lottiefiles/motion-design-skill (commit f9a8a041b85185ee4881b3471d3415e939aac772; LICENSE re-read: MIT, "Copyright (c) 2025 LottieFiles") | MIT | Idea source only for this block: the symptom-to-cause habit (used in `business/interface-design` §9.23). Nothing carried here |
| secondsky/claude-skills (commit 88378361314f558fb719aec0af9fd898ab36f0b2; LICENSE re-read: MIT, "Copyright (c) 2025 Claude Skills Maintainers") | MIT | The exit-needs-a-mounted-wrapper and conflicting-transition-class pitfalls, as pointers to check against the library's own page |
| heygen-com/hyperframes (commit 0693839b52306cbe35ee508f7b4c4b6f914a4fae; LICENSE re-read: Apache-2.0, full text) | Apache-2.0 | Idea only: animate from and to values fixed at setup rather than measured at tween time (§3.10). No file or text copied, so the NOTICE terms do not apply |
| W3C WCAG 2.2 Understanding 2.3.3 and 2.2.2, MDN `prefers-reduced-motion` | W3C and public documentation | Read 2026-10-19 for the sibling rules; not re-read for this block |

## Removed
1. **Every duration, easing curve, spring setting, stagger budget and bundle-size figure**: values a design system
   owns (`business/interface-design` §9.9) or volatile vendor numbers.
2. **The sampled collections' per-library tutorials and snippets**: syntax is the library's page, not a block.
3. **Remotion, video-as-code and brief workflows**: another topic, not in this block.
4. **dylantarre/animation-principles**: rejected on quality in the review (static `will-change`, uniform
   hover scale, unsourced domain claims); nothing used.
5. **Any claim that scroll-driven animation runs off the main thread or is Baseline**: not on the text read.

## Not verified
1. All web pages through digests, as stated above.
2. Browser support for scroll-driven animations, filter and clip-path acceleration, and the percentage-translation
   exception: marked `re-read before relying` in the rules.
3. dotLottie container, themes and player API; Rive play, pause and input methods; reduced-motion implementation
   of either runtime. The pages read did not cover them.
4. Web Animations API members for cancelling, finishing and committing styles, and any compositor behaviour.
5. GSAP's difference between kill and revert (the page does not explain it), and the accuracy of the digest of the
   licence's dates and prohibited-use wording; re-read the page before depending on them.
6. The "remove conflicting transition classes" pitfall comes from one third-party skill, not from the library's
   own page; it is worded as a thing to check.
7. Motion's licence and the exact current names of its React components in the version a project uses.
8. No animation was run or profiled; no frame rate was measured.

## Related blocks
`skills/webperf`, `skills/accessibility`, `business/interface-design`, `skills/react-nextjs-conventions`,
`skills/flutter-conventions`, `skills/source-freshness`.
