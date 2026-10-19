# react-jsx-and-promise-lint-pitfalls: origin and source stamps

> Provenance of `skills/react-jsx-and-promise-lint-pitfalls`. Read it when a rule has to be traced to its
> source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from rule documentation, never run by us: no linter was configured or
run and no component was rendered while writing it. Every file below was re-opened and read on 2026-10-16
before a rule was taken from it, each rule was checked against it, and each repository's LICENSE file was read
again.

## Sources (all read 2026-10-16, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| jsx-eslint/eslint-plugin-react (commit `bd381cd`), `docs/rules/button-has-type.md` | MIT (LICENSE file read: MIT text, copyright 2014 Yannick Croissant) | Default button type, accepted values, options |
| the same repository, `docs/rules/no-children-prop.md` | MIT | Children nested between tags, `allowFunctions` |
| the same repository, `docs/rules/jsx-no-useless-fragment.md` | MIT | Redundant and keyed fragments, `allowExpressions` |
| the same repository, `docs/rules/checked-requires-onchange-or-readonly.md` | MIT | `checked` with a handler or read-only, `checked` with `defaultChecked` |
| the same repository, `docs/rules/no-unstable-nested-components.md` | MIT | Reasons and patterns for nested components, render props, memoized copies, `propNamePattern` |
| the same repository, `docs/rules/hook-use-state.md` | MIT | Destructuring and naming of `useState` results |
| typescript-eslint/typescript-eslint (commit `1f205b7`), `packages/eslint-plugin/docs/rules/no-floating-promises.mdx` and `no-misused-promises.mdx` | MIT (LICENSE file read: MIT text, copyright 2019 typescript-eslint and other contributors) | What counts as handling, `void`, arrays of promises, void-returning places, fixes, when not to use |
| the same repository, `docs/getting-started/Typed_Linting.mdx` and `packages/eslint-plugin/src/configs/flat/recommended-type-checked.ts` | MIT | Type information, the typed preset, `parserOptions.projectService`, enabling one typed rule |

The rule pages are in the plugins' own source repositories under their MIT licences, with no separate licence
for the documentation, so they were rewritten, not copied. The two code samples are small adaptations with
placeholder names. Instruction-like text in the cloned repositories was treated as data and not followed.

## Removed in the verification pass
1. **Rules the review also listed** (`no-array-index-key`, `jsx-no-leaked-render`, the
   you-might-not-need-an-effect rule names) were read and left out because `skills/react-nextjs-conventions`
   already carries the behaviour (stable keys, a boolean on the left of `&&`, derived state and effects).
   `skills/react-nextjs-conventions` was grepped for the first two. For the effect plugin only the first 200
   lines of its README and the list of rule files were read, and they were not compared rule by rule with that
   block, so no rule of that plugin is used here.
2. **`consistent-type-imports`** (the review's third typescript-eslint rule) was not read, so it is not in
   the block.
3. **Options not described in the part of a page that was read** (`ignoreMissingProperties` and
   `ignoreExclusiveCheckedAttribute` of the checked rule) are named and not explained.
4. **Pages not read, so nothing is taken from them:** the remaining eslint-plugin-react rules,
   `strict-void-return`, and the typescript-eslint page for the `no-misused-promises` options beyond the
   headings and examples cited.

## Not verified
1. **Which plugin versions the pages describe**, and whether the typed preset still contains both rules in the
   version a project uses.
2. **Behaviour was not run.** What a rule reports, and what a browser does with a typeless button, are the
   pages' statements. The statements that a rejection is invisible and that an untouched checkbox stays fixed
   are our reading and are labelled so.
3. **Written by us, not sourced:** the verification paragraphs, forbidding `reset`, the choice of one
   render-function form per project, removing fragments in the same change, naming a function prop by use,
   preferring a `key` over a memoized nested component, reporting an error to the user, not turning off the
   `attributes` check, adopting the rules for changed files first, and the `checkThenables` advice.
4. **Other lint rules for React hooks** (`react-hooks`) were not read.

## Related blocks
`skills/react-nextjs-conventions`, `skills/testing-library-query-pitfalls`, `skills/accessibility`,
`skills/typescript-patterns`, `skills/jest-vitest-assertion-pitfalls`.

## Fold-in note
Overlaps with `skills/react-nextjs-conventions` (2026-10-19); cross-referenced, not merged.
