# § 5 — Images, vector graphics and moving pictures

> Section 5 of `skills/webperf`. Read it when a page ships a raster image, an icon set, an illustration,
> an animated clip, or a video that stands in for one. Explicit dimensions, the largest-element image and
> lazy-loading stay in `skills/seo` §3 and are referred to here, not repeated. Alternative text is
> `skills/accessibility`, and an image that carries text is `skills/accessibility` §6.

## Rules

1. **Choose the format by what the image is.** A photograph is a lossy raster; a flat illustration, a
   logo or an icon is a vector; a screenshot with sharp text edges and few colours compresses best
   losslessly. The newer raster formats compress better than the old ones at the same visual quality, and
   the choice is made by capability, not by fashion: serve the newer format to a browser that declares it
   and keep the universally supported one as the last fallback (point 3). Which formats a browser decodes
   changes; read the current support table when choosing (`skills/source-freshness`), and do not keep a
   list of formats in this block.
2. **Serve a size the screen can use.** An image displayed at a small size and shipped at the source
   resolution wastes most of its bytes; one upscaled looks soft. Give the browser several widths and the
   rule for picking one: `srcset` with width descriptors plus `sizes` describing how wide the slot is at
   each layout. For a fixed-size slot on screens of different pixel density, density descriptors suffice.
   `sizes` is a statement about layout and is wrong the day the layout changes, so it is reviewed with the
   CSS that sets the slot width, not apart from it.
3. **Switch format or art direction with `picture`.** A `picture` holds `source` elements, each with a
   `type` (to offer a format by capability) or a `media` condition (to offer a different crop at a
   different layout), and a final `img` that is both the fallback and the element carrying `alt`,
   dimensions and `loading`. A `picture` with no `img` renders nothing.
4. **Weight is a budget decided per project.** Compression level, a ceiling per image and a ceiling per
   route are set once from the audience's connection and the design's need, written down, and checked
   mechanically in the pipeline. The number is the project's, not this block's (`skills/source-freshness`).
   Strip metadata that is not needed (a camera's location data is also a privacy leak, see
   `business/data-protection`), and run the compression in the build rather than by hand, so a new
   image cannot skip it.
5. **Vector graphics: pick the embedding by what must change.** A static graphic goes in as an `img` (it
   is cached, and cannot be styled from outside). Inline it only when its parts need CSS or script, such
   as a theme colour, a hover state or an animation of one path. A decorative inline SVG is hidden from
   the accessibility tree and a meaningful one has a title (`skills/accessibility` §2). Run vector files
   through an optimiser in the build; editors export a lot of dead data. An icon set is imported by
   icon, not wholesale (§2.6).
6. **A GIF is not a video format.** An animated GIF is larger than the equivalent muted looping video by a
   wide margin, and cannot be paused by a reader. Replace it with a `video` that autoplays muted, loops,
   plays inline on small screens and carries a `poster`; keep user controls, or a reachable pause, where
   the clip lasts (`skills/accessibility` §7). For a short, tiny, decorative animation, an animated
   vector or a CSS animation costs less than either.
7. **Video that matters is served as video.** Offer a compressed format with a fallback, do not load the
   media until it is near the viewport or the visitor asks (`preload="none"` or `metadata` with a
   poster), and let a streaming protocol handle long content. A background video is optional chrome:
   skipped on a data-saving or reduced-motion context.
8. **A broken image is a bug found before users do.** Detect missing files at build time by checking that
   every referenced image path resolves. A runtime fallback (an `error` handler swapping in a
   placeholder) is a safety net for user-supplied URLs, never the answer for our own assets, and it sits
   beside, not instead of, alternative text.
9. **A CDN or image-resizing service is infrastructure.** Its configuration belongs to
   `skills/devops-conventions`; this block states what the markup must offer it (widths, formats,
   dimensions), not how it is set up.

## Mechanical checks

```
find public src -type f \( -name '*.png' -o -name '*.jpg' -o -name '*.jpeg' -o -name '*.gif' \) -size +${BUDGET}k
grep -rnP '<img\b(?![^>]*\bsrcset=)' src
grep -rnE '<picture' src
grep -rnE '\.gif\b' src public
grep -rnP '<img\b(?![^>]*\bwidth=)(?![^>]*aspect-ratio)' src
```

- `BUDGET` is read from the project's budget file. The `img` lists are read by a person: a decorative or
  fixed-size image legitimately has no `srcset`.
- For each `picture`, confirm the closing `img` exists with `alt`.
- Resolve every `src` found in the built output: request it and expect a success status; fail the build
  otherwise.
- Compare the intrinsic size of each shipped file (`identify -format '%w %h'`) with the largest width at
  which the page displays it.
- Run the vector optimiser in dry-run mode in the pipeline over the repository's `.svg` files and fail on
  a difference.
