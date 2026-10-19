# tailwind-conventions §3 — Build wiring and the v3 to v4 traps

> Section 3 of `skills/tailwind-conventions`. Read it when the build is set up, a project upgrades, or v3
> idioms appear in a v4 project. The other sections and the guardrails stay in `SKILL.md`.

1. **Check the browser floor before adopting v4.** It targets Safari 16.4, Chrome 111 and Firefox 128 and relies
   on `@property` and `color-mix()`. A project that must support older browsers stays on v3.4; this is a
   product decision, not a build setting.
2. **Import it with plain CSS.** `@import "tailwindcss";` replaces the three `@tailwind` directives. Imports
   and vendor prefixing are handled by the framework, so remove the import plugin and the prefixer from the
   PostCSS setup.
3. **Use the dedicated build integration.** The PostCSS plugin and the command-line tool live in their own
   packages in v4, and the dedicated bundler plugin for Vite is recommended over the PostCSS route for speed.
   A package that is missing is named and the person installs it (`pnpm add -D <package>`).
4. **Configuration is CSS.** A JavaScript config is loaded only through `@config`, and legacy plugins through
   `@plugin`, as a bridge while migrating. The `corePlugins`, `safelist` and `separator` options are not
   supported in v4 (use `@source inline()`), and the `theme()` function is deprecated in favour of the
   variables.
5. **Run the official upgrade tool on a branch, then review the diff and test in the browser.** It automates
   dependency, configuration and template changes and needs a recent Node. Read the breaking-change list
   anyway: the tool does not catch everything.
6. **Renamed and removed utilities** that fail silently if left in markup:
   - deprecated opacity utilities (`bg-opacity-*` and kin) → opacity modifiers (`bg-black/50`);
   - the shadow, radius and blur scales gained named steps, so v3's `shadow-sm` is `shadow-xs` and `shadow`
     is `shadow-sm` (same for `rounded` and `blur`): look for visual shifts, not errors;
   - `outline-none` (it never set `outline-style: none`) → `outline-hidden`, which keeps a forced-colours
     outline, while the new `outline-none` really removes it: **never** use the new one on a focusable element
     without a replacement focus indicator;
   - `ring` is 1px, not 3px, and `currentColor`, not blue: use `ring-3` and name the colour;
   - `border-*` and `divide-*` default to `currentColor`, no longer to a grey: name the colour;
   - `space-*` and `divide-*` changed selector for performance and may behave differently on inline elements
     or with extra margins: prefer flex or grid with `gap`;
   - a variant overriding part of a gradient no longer resets the whole gradient (`via-none` to unset a stop);
   - the `container` utility lost its `center` and `padding` options: extend it with `@utility`;
   - the buttons' cursor is `default`, `dialog` margins are reset, placeholders use the current text colour at
     half opacity, and a `hidden` attribute now wins over `block` or `flex`.
   The upgrade guide gives compatibility snippets; they exist for migration and are not idiomatic v4.
7. **Do not hand-write the v3 `!` at the start** (still accepted, deprecated) and do not use the v3 prefix
   shape (`tw-flex`).
8. **Editor and formatting support are part of the setup.** Install the official editor extension for
   completion and lint, and the official Prettier plugin to sort classes (`pnpm add -D prettier-plugin-tailwindcss`);
   a project with its own formatter either uses it or accepts unsorted classes, but does not hand-sort.
9. **After any upgrade, compare rendered pages in each theme and breakpoint** (`skills/frontend-testing`, visual
   layer): most of the traps above are visual and produce no error.

## Mechanical checks

```
grep -rnE "@tailwind (base|components|utilities)" src
grep -rnE "bg-opacity-|text-opacity-|border-opacity-|ring-opacity-|placeholder-opacity-|flex-grow-|flex-shrink-" src
grep -rnE "outline-none" src
grep -rnE "(^|[ \"'])(shadow|rounded|blur|ring)([ \"']|$)" src --include=*.html --include=*.tsx --include=*.vue --include=*.svelte
grep -rnE "tailwind\.config\.(js|ts|cjs|mjs)|@config|@plugin" . --include=*.css --include=*.js --include=*.ts -l 2>/dev/null | head
```

- Every `outline-none` hit is checked for a visible replacement focus style.
- The bare `shadow`, `rounded`, `blur`, `ring` hits are the renamed-scale and ring-width candidates of rule 6.
