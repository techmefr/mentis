# tailwind-conventions — origin and source stamps

> Provenance of `skills/tailwind-conventions`. Read it when a rule has to be traced back to its source or checked
> for freshness (`skills/source-freshness`), never to apply a rule.

**Written 2026-10-02, new block, never run on real work (🟡, base to confront with a real project).**

Sources, all primary, read on 2026-10-02 from a shallow clone of the framework's documentation site repository
(`tailwindlabs/tailwindcss.com`, `src/docs`), at **Tailwind CSS 4.3.3** (the latest release on the package
registry that day). Pages used: detecting classes in source files, theme variables, functions and directives,
adding custom styles, styling with utility classes, dark mode, responsive design, hover/focus and other
states, preflight, compatibility, editor setup, and the upgrade guide.

**Licence, honestly.** That repository states it is not under an open-source licence and is the intellectual
property of its company ("source available as an educational resource"). Under rule B of `CONVENTIONS.md` that
makes the documentation **idea only**: only mechanisms were taken (how detection works, what a theme variable
does, which defaults changed) and every sentence and example here is our own wording. The framework's code
repository is MIT-licensed and was not needed for these rules; the facts are the framework's, the prose is not.

What is ours: the numbering, the grouping, the "never build a class name" framing as a review rule, the
`@apply` fallback order in §1.6, the mechanical-check commands. Rule 8 of §3 (editor extension and formatter
plugin) names a plugin the documentation recommends; its package name was read in the editor-setup page.

**Facts that move, with their pin.**
- Browser floor Safari 16.4, Chrome 111, Firefox 128 (§3.1): v4.0 statement, re-read at 4.3.3.
- Renamed scales and defaults (§3.6): the upgrade guide's v4.0 list; later 4.x releases may add further notes
  that were not searched in the changelog.
- Directive set (`@theme`, `@source`, `@utility`, `@variant`, `@custom-variant`, `@apply`, `@reference`,
  `@config`, `@plugin`) and functions (`--alpha()`, `--spacing()`, `theme()` deprecated), §2 and §3.
- Not read: the full default theme reference, the plugin API, the per-utility pages, the typography and forms
  plugins, and the framework's changelog. A gap, stated.

**Refresh protocol.** Re-read the upgrade guide and the "functions and directives" page of the next major;
give each pinned fact above a verdict (`skills/source-freshness` §3); stamp the date even when nothing changed.

**Not taken.** The sourcing notes listed an ESLint plugin for Tailwind; it was not read and no rule here
depends on it.

## Re-verified 2026-10-20 (🟡, nothing run)

The code repository `tailwindlabs/tailwindcss` was read through its licence file (**MIT**, "Tailwind Labs, Inc.") and its
changelog (4.3.3 released 2026-07-16 is the latest tagged section; an Unreleased section exists). The documentation
repository stays not open-licensed (above): on this pass its pages were read on the official site as product
documentation, for facts only, and nothing was copied.

| Page read | Points confirmed |
|---|---|
| upgrade guide | §3.1 (browser floor), §3.2 to §3.7 and the new §3.9: separate packages, `@import`, removed options, `@config`, renames, outline, ring, border, space and divide selectors, gradients, container, preflight changes, important and prefix shapes, Node 20 |
| detecting classes in source files | §1.1 to §1.4 (plain-text scan, ignored paths, `@source`, `not`, `source(none)`, `source()` base, `inline()`, braces and ranges) |
| functions and directives | §2.7, §2.8, §2.10, §3.4 (directive and function list, `@reference`, `theme()` deprecated, `--alpha()`, `--spacing()`) |
| theme variables | §2.1 to §2.5 |
| dark mode, responsive design, hover and states, compatibility, editor setup | §2.10 to §2.13, §3.8, §1.10 |
| styling with utility classes, adding custom styles | §1.5 to §1.7, §2.7, §2.9, §2.14 |

**Corrected:** the `@property`/`color-mix()` dependency and the Vite-plugin speed claim (both unstated, now worded as
such); the `@apply` escape attribution (§1.6); the data-type hint syntax (§1.5). **Added:** §3.9 (four silent changes).
**Still unverified:** the `@property`/`color-mix()` dependency, the Vite plugin speed advantage, the claim that variant
stacking order matters beyond the upgrade note (the states page documents no order rule), `--value()` type list
beyond the page's excerpt, the ESLint plugin remark. **Not re-opened:** preflight, the plugin API, per-utility pages.
