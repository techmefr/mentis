# astro-images-templates-pitfalls §2 — Templates, scripts and project setup

## 2.1 Class lists
1. **Use `class:list` for conditional classes** instead of building a string. It accepts strings, objects (truthy
   keys are added), arrays (flattened) and skips `false`, `null` and `undefined`, so no stray spaces and no
   `"undefined"` class. Example: `<div class:list={["btn", { active: isActive }, variant]} />`.

## 2.2 Scripts
1. **A bare `<script>` is processed.** Astro bundles it, treats it as a TypeScript module, resolves imports,
   includes it once even if the component appears many times, and may inline a small one. A module script is
   deferred by nature, so it does not block parsing.
2. **Any attribute other than `src` turns processing off.** The tag is then emitted as written, the same as
   `is:inline`, so attributes that control loading of an external file only work in that mode.
3. **An unprocessed external script blocks parsing unless it says otherwise.** A `<script src>` that passes
   through untouched with no `defer`, `async` or `type="module"` stops the HTML parser until it downloads and
   runs. Add `defer` or `async` (or `type="module"`) to such a tag, or move the code into a bare script that
   Astro bundles.
4. **Bundled scripts run once under `ClientRouter`.** Client-side navigation does not reload the document, so a
   `DOMContentLoaded` listener initialises only the first page. Use the `astro:page-load` event, which fires at
   the end of every navigation once the new page is visible, to set up listeners that would otherwise be lost.
   For an inline script that must run again after each transition, add `data-astro-rerun`.
5. **The component is `ClientRouter`.** Older code that imports `ViewTransitions` is on the removed name.

## 2.3 Project configuration
1. **Set `site`.** Astro builds the sitemap and the canonical URLs from it and exposes it as `Astro.site`.
   Without it those features are missing or relative. Canonical and metadata policy is in `seo`.
2. **Run `astro check` in CI.** It type-checks `.astro` files and reports errors to the console, and the process
   exits with code 1 if any are found. A build can succeed while a template has a type error that `astro check`
   would catch.
3. **Keep secrets out of the public prefix.** Variables with the `PUBLIC_` prefix are exposed to browser code,
   so a secret-looking name behind it is a leak; see `security-hardening`.
4. **`set:html` is raw HTML.** It skips escaping, which is an injection risk when the value comes from user
   input; an expression in braces is escaped. Sanitise first if raw HTML is required.

## Verification
- Navigate between two pages with `ClientRouter` and confirm each page's behaviour still initialises (§2).
- Inspect the built HTML for each external script tag and confirm it is bundled or carries `defer`, `async` or
  `type="module"` (§2).
- Run `astro check` and confirm exit code 0 (§2).
