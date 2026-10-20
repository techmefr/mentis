# web-animation-pitfalls §4 — Reduced motion and scroll-driven animation

> Part 4 of `skills/web-animation-pitfalls`. Read it when a reduced-motion switch is wired, or an effect follows
> scroll. Sources, read 2026-10-20 (digests): MDN `prefers-reduced-motion`, MDN scroll-driven animations and
> `animation-timeline` pages, Motion documentation (accessibility), WCAG 2.2 Understanding pages 2.3.3 and
> 2.2.2 (read 2026-10-19 for `business/interface-design` §9.19). Browser-support statements are marked
> `re-read before relying`. Sentences marked "own guidance" are ours.

1. **`reduce` means remove, reduce or replace, not "stop everything".** MDN describes the preference as asking
   for less motion, with a gentler substitute such as a fade in place of a scale. The mechanics of the media
   query are in `skills/webperf` §1.1 and `skills/accessibility` §7.8; the meaning that must survive is
   `business/interface-design` §9.8.
2. **A library's global switch decides for you; read what it decides.** Motion's configuration for following the
   system preference skips transform and layout animations while opacity and colour changes still play (its
   accessibility page); forced "always" and "never" modes override the system. Own guidance: if a design uses
   a slide or a scale to say where something went, that meaning disappears silently in this mode, so give that
   element an explicit reduced variant that keeps the information (a highlight, a label, an instant move with a
   marker). This is vendor behaviour for one library; read the page for the one in use.
3. **Autoplaying media follows the preference too.** The same page names turning off background video as a use of
   the preference hook. Own guidance: a looping Lottie, Rive or video asset is moving content: pause it under
   the preference and give it a stop control when it runs beside content (`skills/accessibility` §7.7).
4. **Separate "triggered by the visitor" from "starts by itself".** The two WCAG criteria answer different
   questions (`business/interface-design` §9.19); one animation can fall under both. Do not close the issue by
   honouring the media query alone.
5. **For a scroll-linked effect, try CSS scroll-driven animation first.** The CSS feature ties an animation's
   progress to a scroll or element-visibility timeline (`animation-timeline`, with `scroll()` and `view()`)
   instead of time, so no scroll listener runs. Own guidance: it replaces scroll listeners and
   per-frame position reads for progress bars, reveal-on-scroll and parallax-like effects, and it extends the
   "observe intersections, do not listen to scroll" rule of `skills/accessibility` §7.9 and
   `business/interface-design` §9.16 with the CSS primitive.
6. **Gate it, and design the unsupported case.** MDN's `animation-timeline` page carried a "limited availability"
   banner (not Baseline) when read on 2026-10-20, and its examples use a feature query for the unsupported
   case. `re-read before relying`: the status, the engines and any Baseline date were not on the page text
   read, so check MDN or the Baseline listing for the date of use. Own guidance: write the static, finished
   layout as the default, wrap the movement in a feature query and in the no-preference condition, and test the
   page with the feature query forced to fail.
7. **Do not promise off-thread scroll animation.** What the pages read say about which scroll-driven animations
   run off the main thread was not on the text read; do not assert it. Measure (§2).
8. **Smooth scrolling and scroll effects share the opt-in.** Put them behind the no-preference condition with the
   static layout as default (`skills/accessibility` §7.9).
9. **View Transitions have their own rule.** Same-document and cross-document transitions are a platform
   primitive for navigation and list changes; the uniqueness, feature-detection and reduced-motion points are
   in `skills/react-nextjs-conventions` rule 27, and this session did not re-verify them from a primary page.
   Do not restate them here.
