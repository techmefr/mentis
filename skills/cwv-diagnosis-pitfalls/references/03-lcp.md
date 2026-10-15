# cwv-diagnosis-pitfalls §3 — LCP: which subpart is late

Largest Contentful Paint is a sum of a server wait, a resource load and a render, and the usual fixes each
address one of them. A preload added to a page whose time goes elsewhere costs bandwidth and fixes nothing.

## 3.1 What counts and what to measure
1. **Know the candidates.** The largest element can be an `img`, an image inside an `svg`, a `video` with a
   poster, an element with a `url()` background image, or a block-level element holding text nodes. Name the
   actual element from the trace before reasoning about it.
2. **Measure the relevant subpart before and after, under equivalent conditions.** The reference says not to
   attach generic millisecond savings to any of these fixes. Own guidance: write the savings in the change
   description only as the two measured values.

## 3.2 The usual causes and the evidence that confirms them

| Cause | Evidence to confirm | Typical fix |
|---|---|---|
| The LCP resource is discovered late | A long resource load delay in the LCP breakdown or discovery insight | Put it in the initial HTML, give it priority, preload only if still necessary |
| A large image transfer | Resource load duration and response bytes dominate | Resize and compress, choose a suitable format |
| Render-blocking CSS | The render-blocking insight and a long render delay | Remove unused rules, split non-critical CSS, inline only CSS proven critical |
| Slow server response | The document latency insight or the server-response subpart dominates | Caching, fewer redirects, less server work |
| The LCP element is rendered on the client | The element is absent from the initial HTML and render delay dominates | Server rendering, static rendering or earlier rendering |

1. **Preload an image only when the trace shows it is found late.** The reference marks its own preload example
   with that condition; the first fix for a late discovery is to have the element in the initial HTML with the
   right priority (`seo` §3.1 for the priority attributes), and the preload comes after, if still needed.
2. **Read the table from the evidence side.** Own guidance: each row starts with the trace finding and the fix
   follows from it; a fix with no finding on its left is a guess.
3. **Inline critical CSS only once the trace has proved which CSS is critical.**
