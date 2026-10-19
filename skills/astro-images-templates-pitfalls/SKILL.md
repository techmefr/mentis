---
name: astro-images-templates-pitfalls
description: "Use when an Astro page shows images or scripts: astro:assets Image or Picture instead of a raw img tag, width and height for images in public/ and remote images (inferSize, image.domains), the LCP image priority, then class:list versus string concatenation, a script tag with src or extra attributes, scripts that stop working under ClientRouter (astro:page-load), the site option for canonical URLs and sitemap, and astro check in CI."
---

# astro-images-templates-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for the Astro template mistakes that build cleanly and then show up as
layout shift, an unoptimised hero, a script that runs once and never again, or a canonical URL that is
missing. The sections share one premise: **Astro only optimises and bundles what it can see at build time**:
an image under `src/`, a script with no extra attributes. Anything else is passed through as written. Each rule
says what you see when it is missed.

**Version scope.** Astro documentation read on 2026-10-08, when the package registry showed the stable tag at
a 7.x release. The version-6 upgrade list from the review was not written, because it targets an older major
than the current one; check each rule against the installed version.

Standalone block, written because the broader Astro conventions block exists only on an unmerged branch. It is
meant to be merged into the same-named framework block when that lands (see
[`references/origin.md`](./references/origin.md)). Until then it cites only blocks present on the main branch.

## When
- A page uses `<img>`, `<Image>` or `<Picture>`, or an image comes from `public/` or from another host.
- A hero or banner image is the largest thing above the fold.
- A script is added to a layout, a component or a page, or a script stops working after the first navigation.
- A class list is built conditionally, a canonical URL or sitemap is missing, or CI has no template type check.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Images: the optimisation pipeline, dimensions, remote sources, the LCP image | an image is added or a page shifts while loading | [`01-images.md`](./references/01-images.md) |
| 2 | Templates and project: class:list, scripts, ClientRouter, site, astro check | a script, a conditional class, navigation, URLs or CI changes | [`02-templates-scripts-and-project.md`](./references/02-templates-scripts-and-project.md) |

## Output / checkpoint
Each rule was exercised, not read off the file: the built page was inspected for the `width`, `height`,
`loading` and `fetchpriority` attributes of each image (§1), the page was loaded with the network throttled
and no layout shift was seen (§1), the script was exercised after a client-side navigation (§2), and
`astro check` was run and exited 0 (§2). A page that only built is not verified.

## Guardrails
- Never put an image the build should optimise in `public/`: it is served as is (§1).
- Never leave `width` and `height` off an image from `public/`; Astro cannot read them (§1).
- Never lazy-load the largest above-the-fold image (§1).
- Never put an `addEventListener('DOMContentLoaded', ...)` initialiser behind `ClientRouter` (§2).
- Never add an attribute to a `<script>` that should be bundled without knowing it stops the bundling (§2).
- Image weight and Core Web Vitals strategy belong to `webperf`; sitemap, canonical and metadata policy belong to
  `seo`; alternative text belongs to `accessibility`.

## Origin
Rewritten from the official Astro documentation (images, assets reference, directives, client-side scripts,
view transitions, configuration and CLI references) and two MIT Astro skill sets, read 2026-10-08. 🟡: never
run by us; open points are in [`references/origin.md`](./references/origin.md).
