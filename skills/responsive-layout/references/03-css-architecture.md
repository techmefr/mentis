# Steps 20 to 29 — CSS architecture: specificity, layers, naming, themes, print

> Steps 20 to 29 of `skills/responsive-layout`. Read them when a stylesheet is added to, a third-party
> style is brought in, a naming scheme or a theme is introduced, or a page has to be printed. They
> continue the numbering of steps 1 to 19 and are about how the CSS is organised, not how a layout is
> shaped. Pixel, ratio and breakpoint figures are not stated: tokens or the cited standard
> (`skills/source-freshness`).

20. **Specificity stays low and flat.** Style with single class selectors. A selector built on an `id`, on
    an element qualified by a long ancestor chain, or on deep nesting wins today and forces a heavier
    selector tomorrow, until the only way to override is `!important`. Reserve `!important` for a named
    utility or override layer where its job is stated, and count its occurrences against a baseline in the
    pipeline.
21. **Cascade layers separate whose rules they are.** Declare the layer order once at the top of the entry
    stylesheet (reset, third-party, base, components, utilities), and put vendor CSS in an early layer so
    our rules win by position rather than by specificity. Unlayered styles beat layered ones whatever
    their specificity, so decide on purpose which side the project's own rules sit on and keep that
    consistent. Layer support is a compatibility fact; read the current table when the audience
    includes old engines.
22. **One naming scheme, decided once.** Block-element-modifier, utility classes, scoped styles or CSS
    modules: the project picks one and says so in the repository's conventions, so a new class is named by
    rule and not by taste (`vue-nuxt-vuetify-conventions` §4.5 states the Vue choice). Classes name what a
    thing is, not how it looks, so a redesign does not rename the HTML.
23. **A component responds to its container.** Page-level changes use media queries; a component that
    lives in a sidebar in one place and a wide column in another uses a container query
    (`container-type: inline-size` on the wrapper, `@container` rules inside), so its layout follows the
    room it has, not the window. A containment context affects layout and has side effects on sizing,
    which is why it is set on the wrapper and not everywhere.
24. **Themes honour the system, then the user.** The initial theme follows `prefers-color-scheme`; a
    visible control stores an explicit choice that overrides it. Declare `color-scheme` so native
    controls and scrollbars match, and apply the stored choice before first paint so the page does not
    flash the wrong theme. Every shipped theme is a second palette whose contrast is measured on its own
    (`skills/accessibility` §3.1, §3.11).
25. **Print styles only for pages people print.** An invoice, a ticket, a document or an article gets an
    `@media print` block: the chrome (navigation, banners, controls) is hidden, the content flows at full
    width in readable type, rows and figures avoid breaking across pages (`break-inside: avoid`), links
    show their destination where it matters, and the result is checked in the browser's print preview.
    Other pages get none.
26. **Reflow is a stated criterion, so it is a test.** Content must reflow without two-dimensional scrolling
    at the width and zoom WCAG 1.4.10 names; read the figures there and put them in the test, not here.
    The test loads the page at that width and compares the document's scroll width to its client width.
    Text spacing and larger default fonts (`skills/accessibility` §3.3, §3.4) are tested alongside.
27. **Form fields have a readable base size.** Some mobile engines zoom the page when a field with a small
    font is focused. The cure is a field font size at or above the engine's documented trigger (read from
    its documentation or checked on a device), usually the base body size, expressed in `rem`. It is not
    `maximum-scale` or `user-scalable=no`, which take zoom away from people who need it (Guardrails).
28. **Direction-aware properties.** Use logical properties (`margin-inline-start`, `padding-block`,
    `inset-inline-end`, `text-align: start`) rather than left and right, so a right-to-left language does
    not need a second stylesheet (`skills/html-document` for `dir`).
29. **Units follow what should scale.** Type and the spacing that belongs to it in `rem` or `em`, borders
    and hairlines in `px`, layout in fractions, percentages and container-relative units. A fixed pixel
    font size is a decision to ignore the reader's setting (`skills/accessibility` §3.3).

## Mechanical checks

```
grep -rnE '^\s*#[A-Za-z_-][A-Za-z0-9_-]*[^;]*\{' src --include=*.css --include=*.scss
grep -rn '!important' src | wc -l
grep -rnE '@layer' src
grep -rnE '@media[^{]*print' src
grep -rnE 'prefers-color-scheme|color-scheme' src
grep -rnE '(margin|padding|border)-(left|right)\s*:' src
grep -rnE 'font-size:\s*[0-9]+px' src
```

- The `!important` count is compared with a recorded baseline and may not grow without a reason in the
  pull request.
- Each `#id` selector, physical left/right property and pixel font size is a place to read, not an
  automatic fix; generated and vendor files are excluded.
- A theme toggle with no `prefers-color-scheme` or `color-scheme` anywhere in the styles is a finding.
- Reflow: a headless browser at the criterion's width, then `document.documentElement.scrollWidth >
  window.innerWidth` is a failure.
