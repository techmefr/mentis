# § 3 — Performance: Core Web Vitals

> Section 3 of `skills/seo`. Read it when a diff touches the largest element, image sizing or main interactions.

1. LCP (Largest Contentful Paint): the main above-the-fold image/block doesn't wait on a heavy JS load
   or an avoidable client-side fetch; `fetchpriority="high"` on the LCP image (on one or two images at most, or the hint stops helping), `lazy`
   on the rest, never on the LCP image, and the image present in the served HTML so the browser can discover it
   early (web.dev, optimize LCP). `loading="eager"` is the default and adds nothing. Good is 2.5 seconds or less, poor
   above 4.0, at the 75th percentile of visits.
2. CLS (Cumulative Layout Shift): explicit dimensions (`width`/`height` or `aspect-ratio`) on
   images/videos/embeds to reserve the space before loading: never content that pushes the layout
   around afterwards. Width and height attributes, or an aspect ratio, and a reserved minimum height for ads and
   embeds; good is 0.1 or less, poor above 0.25 (web.dev, optimize CLS).
3. INP (Interaction to Next Paint, covering click, tap and keyboard, not scrolling or hovering; good is 200 ms or
   less, poor above 500 ms at the 75th percentile, web.dev): no long blocking JS task on the main interactions (click, typing):
   see the perf conventions already set in
   `vue-nuxt-vuetify-conventions`/`react-nextjs-conventions`.

