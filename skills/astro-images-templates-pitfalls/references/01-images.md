# astro-images-templates-pitfalls §1 — Images

The image component does three jobs at build time: it optimises, it writes the output attributes, and it
infers the dimensions that prevent layout shift. Which of those happen depends on where the file lives.

## 1.1 Where the file lives decides what happens
1. **`src/` images are processed and optimised.** Import them and pass the import to the component. Astro reads
   their dimensions, converts formats and produces the responsive output.
2. **`public/` images are never optimised.** Files there are copied to the build as they are, so an `<img>` or an
   `<Image>` that points at one gets nothing from the pipeline.
3. **Remote images are optimised only for authorised sources.** List the hosts in `image.domains` or the URL
   patterns in `image.remotePatterns`. Other remote images are not optimised, though the component still helps
   against layout shift.
4. **Prefer `<Image>` or `<Picture>` from `astro:assets` to a raw `<img>`.** The raw tag skips conversion,
   `srcset` and dimension inference. `<Picture>` generates several formats or sizes.

## 1.2 Dimensions
1. **Public images need `width` and `height`.** Astro cannot analyse files in `public/`, so both are required.
   A missing pair is the usual cause of layout shift on an image that looks correctly written.
2. **Remote images need the same, or `inferSize`.** `inferSize` reads the dimensions from the image when it is
   fetched at build time. Use it only for hosts you trust to be reachable at build time.
3. **Imported `src/` images need neither,** because the component infers them from the original aspect ratio.

## 1.3 The largest image above the fold
1. **The default output is lazy and asynchronously decoded.** `loading="lazy"` and `decoding="async"` are right
   for most images and wrong for the one that decides the largest contentful paint.
2. **Mark the main above-the-fold image as priority.** The component's `priority` prop sets `loading`,
   `decoding` and `fetchpriority` to values suited to above-the-fold images; where the installed version lacks
   it, set `loading="eager"` and `fetchpriority="high"` by hand.
3. **Below the fold, keep `loading="lazy"` and give explicit dimensions.**

## 1.4 Formats
1. **The default output format is WebP;** request another (`format="avif"`) when the target browsers allow it
   and the size gain is measured.

## Verification
- Build, then read the generated HTML: every image has `width`, `height` and the intended `loading` and
  `fetchpriority` (§1).
- Open the page with throttled network and watch for content jumping when images arrive (§1).
- Confirm that the hero image is not served from `public/` by accident (§1).
