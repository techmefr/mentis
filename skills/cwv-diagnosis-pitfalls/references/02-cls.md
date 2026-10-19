# cwv-diagnosis-pitfalls §2 — CLS: who moved, and who made them move

Cumulative Layout Shift scores unexpected movement, and the element that moved is often not the element that
caused it. A fix at the victim leaves the cause in place.

## 2.1 Reading a shift
1. **The score of one shift is the impact fraction times the distance fraction, and the metric sums unexpected
   shift clusters across the page visit.** Use the shifted-node and initiator evidence from the trace.
2. **The shifted element may be the victim.** Content inserted above it is the cause, so look at what arrived
   before the move.
3. **One-session evidence has limits.** A `PerformanceObserver` on `layout-shift` entries that ignores shifts
   after recent input lists the shifted nodes with their previous and current rectangles for the current
   session; it is not the distribution of real visits (`webperf-measurement-and-budget-pitfalls` §1).
4. **Exercise the states, not only the first load.** The trace must cover the page state and the viewport where the
   shift occurs: after a click that opens a panel, after a validation error, at the narrow width.

## 2.2 Reserving space
1. **Media and embeds reserve their box.** Width and height on images, an aspect ratio on the frame of a video or
   an embed (`seo` §3.2). For advertisements and embeds whose final size varies, reserve a realistic minimum:
   a placeholder that later collapses shifts the content too.
2. **Do not insert banners, validation summaries, consent bars or notifications above visible content without a
   reserved slot.** Prefer an overlay, an insertion outside the current viewport, or a stable container that
   exists before the content does; fill the container instead of prepending to the page.

   ```js
   document.querySelector('[data-notification-slot]').replaceChildren(notification);
   ```

3. **The slot is sized for the longest content it will hold.** The reference asks to verify that responsive
   content and localisation do not overflow the reserved space. Own guidance: size it for the longest translation
   of the message, not for the source language.
4. **Font swaps are fixed with measured metrics.** When the trace attributes shifts to font replacement, use a
   fallback font with similar metrics and tune it with `size-adjust`, `ascent-override`, `descent-override` and
   `line-gap-override`. Derive the values from the actual pair of fonts and test them with representative text;
   do not copy values written for another pair.
5. **Animate with `transform` and `opacity`, then check.** Animating `height`, `width`, `top` or `left` can trigger
   layout, but replacing them mechanically is not enough: confirm that the transformed element does not cover
   content or move the hit area it should have.

## 2.3 Before saying it is fixed
1. **Run the reference's checklist.** Images and responsive media have intrinsic space, ads, embeds and
   asynchronous components have stable containers, banners and messages do not push visible content, font swaps
   use measured fallbacks where they caused shifts, and animations avoid layout work.
2. **Claim a field improvement only after new RUM or CrUX visits**, as for any vital.
