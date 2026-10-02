# tailwind-conventions §2 — Theme variables, directives, custom CSS, variants, dark mode

> Section 2 of `skills/tailwind-conventions`. Read it when a token, a custom utility or variant, a dark theme
> or a stylesheet directive is written. The other sections and the guardrails stay in `SKILL.md`.

1. **Design tokens are theme variables declared with `@theme`.** A variable in a namespace (`--color-*`,
   `--font-*`, `--text-*`, `--breakpoint-*`, `--spacing-*`, `--radius-*`, `--animate-*`, and the other
   namespaces in the default theme) creates the matching utility or variant: `--color-mint-500` makes
   `bg-mint-500`, `text-mint-500`, `fill-mint-500`. Tokens are not written in a config file or in `:root` when
   they should drive utilities.
2. **`@theme` versus `:root`.** `@theme` for a value that must become a utility or variant; `:root` for a plain
   custom property that is not meant to be one. Theme variables are top-level only, never inside a selector or
   a media query. The values also exist as ordinary CSS variables, so custom CSS, arbitrary values and inline
   styles read `var(--color-mint-500)`, and script reads them with `getComputedStyle`.
3. **Override one token by redefining it; remove a whole namespace by setting `--color-*: initial;`** and then
   defining yours (only your colors exist afterwards, and every utility that used the old ones is gone).
   `--*: initial;` removes the default theme entirely. Do this for a design system that must not offer
   off-palette values, and say so in the review.
4. **A token that references another token uses `@theme inline`.** Without `inline`, the utility resolves a
   variable where the *using* element is, not where it was defined, and can fall back to a wrong value (a
   font stack defined on the root but resolved on a child that defines its own variable).
5. **Only used variables are emitted.** `@theme static` forces all of them out, needed when script or another
   stylesheet reads tokens that no utility uses. Put `@keyframes` for an `--animate-*` token inside `@theme`;
   keyframes outside it are always emitted.
6. **Share tokens as a CSS file** imported by each project, or published as a package; do not copy tokens
   between repositories.
7. **Custom utilities are `@utility`, not a hand-written class in the `utilities` layer.** An `@utility` works
   with every variant (`hover:`, `lg:`), supports nesting for complex output, and can be functional, with
   `--value()` resolving a theme key, a bare number, ratio or percentage, a literal, or an arbitrary value of
   a declared type. Custom variants are `@custom-variant`; apply a variant inside custom CSS with `@variant`.
8. **`@apply` and `@variant` in a component's own style block (Vue, Svelte, CSS modules) need the theme in
   scope**: `@reference` the main stylesheet there. It imports the definitions without duplicating any CSS in
   the output. Each separately processed CSS module makes Tailwind run again, so a project with many CSS
   modules builds slowly; the framework itself does not recommend mixing CSS modules and Tailwind.
9. **Custom base styles go in `@layer base`; component classes in `@layer components`**, where a utility can still
   override them. Set page defaults (text color, font) with classes on `html` or `body`, so the decision stays
   in the markup.
10. **Tailwind is the preprocessor.** Do not combine it with Sass, Less or Stylus: imports are bundled, variables
    and nesting are native, vendor prefixes are added, loops are replaced by on-demand utilities, and
    `color-mix()` and native math functions replace colour and math helpers. Use `--alpha()` and `--spacing()`
    in CSS for opacity and the spacing scale.
11. **Mobile first.** An unprefixed utility applies at every size; `md:uppercase` applies from the `md`
    breakpoint up. Style the smallest layout with unprefixed classes and layer `sm:`, `md:` on top; `sm:` does
    not mean "on phones". Use container query variants (`@container` on the parent, `@sm:` on the child) for a
    component that must adapt to the space it is given rather than to the viewport.
12. **Dark mode is a variant, not a second set of classes.** `dark:` follows `prefers-color-scheme` by default;
    to follow a user toggle, override the variant with a selector (a `.dark` class or a data attribute on the
    root), and drive the three-way light, dark, system choice with `matchMedia` and a stored preference. A
    single utility never carries both themes, so write the light and dark classes side by side. Initialise the
    theme before first paint to avoid a flash (`skills/html-document`).
13. **Respect the user's environment with variants**: `motion-reduce:` to remove non-essential motion,
    `forced-colors:` and `not-forced-colors:` where colours are overridden by the system, `focus-visible:`
    for keyboard focus. These complement `skills/accessibility`; they do not replace its checks.
14. **Prefixes and the important modifier have fixed shapes in v4**: a prefix is written like a variant at the
    start (`tw:flex`) and theme variables are still declared unprefixed (the generated variables carry the
    prefix); `!` goes at the end of the class (`bg-red-500!`), and the old leading position is deprecated.

## Mechanical checks

```
grep -rnE ":root *\{[^}]*--(color|font|spacing|radius|text)-" src --include=*.css
grep -rnE "@theme" src --include=*.css
grep -rnE "@apply|@reference" src
grep -rnE "dark:|@custom-variant dark" src | head -20
grep -rnE "\.(scss|sass|less|styl)$|from 'sass'" package.json src 2>/dev/null
```

- A token under `:root` that is meant to drive a utility is rule 1.
- `@apply` in a framework style block without `@reference` fails or emits nothing; the build log says which.
