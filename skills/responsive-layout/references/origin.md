# responsive-layout — origin and source stamps

> Provenance of `skills/responsive-layout`. Read it when a rule has to be traced back to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

No external source: internal synthesis of long-standing CSS layout practice (fluid grids, dynamic viewport
units, safe-area insets, overflow debugging), written as a checklist. The failure shapes (the mid-range
gap, `100vh` on mobile, `overflow` concealment, keyboard cover) are the ones that recur in review. Not yet
run on real work.

Steps 13 to 29 added 2026-10-02. The viewport-unit, input-capability, small-screen table, stacked
sticky layer and clickable-text points (13 to 17) come from reading the layout-and-mobile rules of public
anti-slop and design-quality repositories (`anti-slop`, `hallmark`, both MIT, read that day); the
mechanism was rewritten and every fact checked against the CSS specifications (CSS Values, Media Queries
level 4 for `hover` and `pointer`, CSS Cascade level 5 for layers, CSS Containment for container
queries, CSS Logical Properties) and WCAG 2.2 (1.4.10, 2.5.8). Steps 18 to 29 come from the topics of
the public `Front-End-Checklist` repository (README and package metadata declare MIT; no licence file is
present, so no sentence was reused), rewritten from the same specifications and MDN. Not taken: a named
list of modern CSS features (it goes stale on arrival), a CSS reset or a stylesheet linter as a tool
requirement (project choices, rule B), minification and unused-CSS removal (owned by the bundler), and any
engine's field-zoom trigger value (read from the vendor's documentation).
