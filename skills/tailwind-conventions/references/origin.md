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
