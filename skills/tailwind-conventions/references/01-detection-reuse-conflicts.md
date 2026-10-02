# tailwind-conventions §1 — Class detection, dynamic names, reuse and conflicts

> Section 1 of `skills/tailwind-conventions`. Read it when a class name is built in code, a class list is
> repeated, or a component accepts extra classes. The other sections and the guardrails stay in `SKILL.md`.

1. **Tailwind reads your source as plain text.** It does not parse code: it collects every token that could be
   a class and keeps those that match a utility it knows. So a class is generated only if it appears **whole,
   literally, in a scanned file**.
2. **Never build a class name by interpolation or concatenation** (`` `text-${color}-600` ``). The full string
   exists nowhere in the source, so nothing is generated and the element is silently unstyled. Map each prop
   value to a complete class name (`{ red: 'text-red-600', green: 'text-green-600' }`), which also lets two
   values differ in more than one shade.
3. **Know what is not scanned**: paths in `.gitignore`, `node_modules`, binary files, CSS files and lock files.
   A component library in `node_modules` built with Tailwind is therefore invisible: register it with
   `@source "../node_modules/the-library"`. In a monorepo where the build runs from the repository root, set
   the base with `source("...")` on the import; ignore directories that never hold classes with
   `@source not`; turn automatic detection off with `source(none)` when each stylesheet should list its own.
4. **Safelist with `@source inline("...")`, not with a content list that exists only to force classes.** It takes
   brace expansion (`{hover:,focus:,}underline`, `bg-red-{50,{100..900..100},950}`), and `@source not inline(...)`
   excludes classes. Needed for class names that reach the page from a database or a CMS and so appear in no
   source file.
5. **Prefer the value you can see.** `top-[117px]` is an inline style that still takes variants (`hover:`,
   `lg:`); use it for a genuine one-off, and a theme variable (§2.1) when the value will occur twice. A space
   inside an arbitrary value is written with an underscore; if the type is ambiguous (`text-[length:var(--x)]`
   against `text-[color:var(--x)]`), give it a data-type hint.
6. **Duplication is solved the usual way, not with `@apply`.** In order: the repeated markup is already rendered
   in a loop (one class list exists); a block of one file is edited in one pass; a repeated block across files
   becomes a component (or a template partial in a server-rendered app) with the classes inside it; only when a
   partial would be heavy for a single element, a small custom class using theme variables. `@apply` and the
   `components` layer are the escape for HTML you do not own (a Markdown renderer, a third-party widget).
7. **Never put two classes on one element that set the same property.** The one that comes later in the
   generated stylesheet wins, not the later one in the attribute, so `flex grid` yields a grid for a reason
   invisible in the markup. Choose the class you mean.
8. **A component does not take free-form extra classes from its consumers.** Outside classes conflict with the
   component's own. Expose props (size, tone, density) that select complete class names inside the component;
   if a class slot is unavoidable, document that it must not override the component's own properties.
9. **Order within the attribute is for the reader and the formatter.** Use the official formatter plugin to sort
   classes so diffs stay small; do not sort by hand.
10. **Compose with variants, not with states in JavaScript.** `hover:`, `focus-visible:`, `disabled:`,
    `aria-*`, `data-*`, `group-*` / `peer-*` (named with `group/name` when nested) and `has-*` express state in
    the markup. A class toggled by script to emulate a pseudo-class is a defect to repair, not a feature.

## Mechanical checks

```
grep -rnE "(class|className)=.*\\$\{" src
grep -rnE "['\"\`](text|bg|border|ring|p|m|w|h)-\\$\{" src
grep -rnE "@apply" src --include=*.css --include=*.vue --include=*.svelte
grep -rnE "@source" src --include=*.css
grep -rnE "!important| !" src --include=*.css
```

- An interpolation inside a class string is a finding (rule 2), unless every possible whole value is also written
  literally somewhere in the scanned files (not a pattern to rely on).
- `@apply` in a component style block needs `@reference` to the main stylesheet (§2.8).
