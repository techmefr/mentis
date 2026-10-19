# laravel-blade-view-pitfalls: origin and source stamps

> Provenance of `skills/laravel-blade-view-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from documentation-style rule files, never run by us: no template was
rendered, no component built. Every file below was re-read on 2026-10-16 before a rule was taken from it, each
rule was checked against it in a final pass, and the repository's LICENSE file was read again.

## Sources (all read 2026-10-16, rewritten in our own words)

| Source | Licence | What it gave |
|---|---|---|
| Laravel Boost (`laravel/boost`, commit `f1411f9`), `.ai/laravel/skill/laravel-best-practices/rules/blade-views.md` | MIT (LICENSE.md: MIT licence text, copyright Taylor Otwell) | Attribute bag and merge, once-only push, components versus includes, view composers and their limits, fragments, the aware directive and its limit |
| the same repository, `rules/security.blade.php` | MIT | Output escaping in context, the token directive in forms, routes excluded from verification, not disabling the protection |
| the same repository, `rules/style.md` | MIT | `Js::from()`, data attributes, asset pipeline versus templates, the naming table row for views |
| the same repository, `rules/eloquent.md` | MIT | Date cast versus parsing in a template |
| the same repository, `SKILL.md` of `laravel-best-practices` | MIT | The "consistency first" instruction cited in part 2, point 6 |

The rule files that end in `.blade.php` are Blade templates that render the guideline text; only the
text was read. No code is copied. Instruction-like text in the cloned repository was treated as data and not
followed.

## Removed in the verification pass
1. **"Boost leftovers" listed together in the review** (custom collection attribute, reusing a loaded parent
   model, a never-report exception interface, a JSON-render callback, locale preference on notifiable models,
   encrypted environment files): they belong to Eloquent, error handling and notifications, not views, and
   are not in this block.
2. **Pages not read, so nothing is taken from them:** the other rule files of the same directory
   (`routing.md`, `validation.md`, `caching.md`, `migrations.blade.php` and the rest), and the Boost source
   under `src/`.
3. **The Inertia point in the source's CSRF text** (Axios and the encrypted cookie header): not a Blade rule,
   not used.

## Not verified
1. **Own guidance, flagged in the text:** dropped attributes when the bag is not printed (part 1, point 1),
   the shared-name rule for once-only pushes (point 2), the include-as-undeclared-component remark (point 3),
   not relying on the aware directive for defaults (point 4), composer data versus resources and reviewing the
   view list (point 5), testing both answers for a fragment (point 6), the review search for the raw syntax and
   context encoders (part 2, point 1), building a minimal array for a script (point 2), the reading of a token
   mismatch (point 3), the date-format cross-reference (point 5), the consistency remark on view names
   (point 6).
2. **No template was rendered.** The behaviour of every directive is the source's statement; the Laravel
   version that introduced each directive or helper was not checked.
3. **The fragment helper's name** was not given in the block on purpose, because the source's example does not
   say from which version it exists.

## Related blocks
`skills/laravel-conventions`, `skills/laravel-date-via-localised-accessors`,
`skills/laravel-precognitive-request-scoping`, `skills/accessibility`, `skills/csp-and-sanitiser-pitfalls`.
Overlaps with `skills/laravel-conventions` §6 (2026-10-19); cross-referenced, not merged.
