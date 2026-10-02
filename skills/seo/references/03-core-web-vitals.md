# § 3 — Performance: Core Web Vitals

> Section 3 of `skills/seo`. Read it when a diff touches the largest element, image sizing or main interactions.

1. LCP (Largest Contentful Paint): the main above-the-fold image/block doesn't wait on a heavy JS load
   or an avoidable client-side fetch; `loading="eager"`/`fetchpriority="high"` on the LCP image, `lazy`
   on the rest.
2. CLS (Cumulative Layout Shift): explicit dimensions (`width`/`height` or `aspect-ratio`) on
   images/videos/embeds to reserve the space before loading: never content that pushes the layout
   around afterwards.
3. INP (Interaction to Next Paint): no long blocking JS task on the main interactions (click, typing):
   see the perf conventions already set in
   `vue-nuxt-vuetify-conventions`/`react-nextjs-conventions`.

