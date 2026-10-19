# a11y-lint-wiring-pitfalls: origin and source stamps

> Provenance of `skills/a11y-lint-wiring-pitfalls`. Read it when a rule has to be traced to its source or checked
> for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from plugin documentation and reading, never run by us. No ESLint configuration was
executed, no rule was triggered and no plugin was installed while writing it. Option names and defaults are as the
repositories state them on the read date.

## Sources (re-read 2026-10-16, rewritten in our own words, no text copied)

Every page below was read in full, including the long README of the JSX plugin; its closing background sections
on the accessibility tree were read and are not relied on.

| Source | Licence | What it gave |
|---|---|---|
| jsx-eslint/eslint-plugin-jsx-a11y, `README.md` (commit 8f75961, version 6.10.2) | MIT (repository file `LICENSE.md`, Copyright 2016 Ethan Cohen) | Static-only scope, settings (`components`, `attributes`, `polymorphicPropName`, `polymorphicAllowList`), flat and legacy usage, shareable configs that do not set `files` or globals, the rule table with its preset marks, the options of five rules in `recommended` |
| jsx-eslint/eslint-plugin-jsx-a11y, `docs/rules/label-has-associated-control.md` (same commit) | MIT (same file) | The two association ways, label and control component options, `depth`, `assert`, two labels for one input, deterministic ids |
| jsx-eslint/eslint-plugin-jsx-a11y, `docs/rules/anchor-is-valid.md` (same commit) | MIT (same file) | Invalid `href` values, anchors as buttons, keyboard activation, button restyled as a link, `components`, `specialLink`, `aspects` |
| vue-a11y/eslint-plugin-vuejs-accessibility, `README.md` (commit b616194, version 2.6.2) | MIT (repository LICENSE file, Copyright 2020 to present Kevin Newton) | Only that the README holds no configuration section and points to a website |
| vue-a11y/eslint-plugin-vuejs-accessibility, `docs/rules/form-control-has-label.md`, `label-has-for.md`, `no-autofocus.md`, `click-events-have-key-events.md`, `no-onchange.md`, `no-aria-hidden-on-focusable.md` (same commit) | MIT (same file) | Label and control options, nesting versus id and its default, `allowChildren`, autofocus, click and key handlers, the deprecation notice, the passing examples that hide focusable elements |

The licence of each repository was verified again from its LICENSE file in this session. The Vue rule pages are
the plugin's source documents, not its website, which was not cloned.

## Rewrite notes
**Decisions where sources disagree.** The JSX page says wrapping a control in its label is enough for modern
browsers and assistive technology; the Vue page says to require both nesting and id for full coverage, and
defaults to both. Neither claim was tested; the block makes the choice a recorded project decision. The Vue
`no-aria-hidden-on-focusable` passing examples conflict with `accessibility` §2.7: the repository's rule wins.

**Corrected against the sources.** The review's re-read note named the configuration sections of both READMEs;
only the JSX README has one. The Vue options (`labelComponents`, `controlComponents` and the others) come from the
rule pages, not from its README.

**Not carried (per the review).** The Vue `no-onchange` rule (deprecated in its own page). The Vue
`no-aria-hidden-on-focusable` passing examples. The Next.js workaround options of `anchor-is-valid` (framework
specific and dated). The rules of the Vue plugin whose pages were not read (`anchor-has-content`,
`no-static-element-interactions`, `interactive-supports-focus` and the others in its docs directory).

**Version-bound.** eslint-plugin-jsx-a11y 6.10.2 (settings, preset marks, rule table), eslint-plugin-vuejs-accessibility
2.6.2 (option names and defaults).

## Not verified
1. **Nothing was run.** No ESLint run, no rule failure and no preset was observed.
2. **The Vue plugin's presets and its configuration format** are not described by any file read; its website was
   not read, so the block says nothing about its recommended configuration.
3. **The assistive technology claims** (what wrapping alone covers, what nesting plus id covers) are the plugins'
   own statements and were not tested.
4. **The JSX rules that appear only as rows of the README table** (`no-aria-hidden-on-focusable`, `prefer-tag-over-role`,
   `lang`, `control-has-associated-label`, `anchor-ambiguous-text`, `no-autofocus`) were read as one-line
   descriptions and preset marks; their own pages were not opened.
5. **The legend of the README table** (marks for enabled, disabled, deprecated) was read as written; the plugin
   source was not read to confirm it.
6. **Written by us, not sourced:** the "record which rules ran" advice, the remark on a config that omits files
   or globals, the "write the same shape" advice, the on or off with a reason advice, the `both` versus `either`
   leaning, the raise `depth` advice, the question to the designer, the native `button` advice for click handlers,
   the code-after-view-change advice for focus, and the checkpoint paragraph.
7. **Dropped as unverifiable from the review item:** none beyond the two carry-nots above; the "files and globals",
   "wrapper", "label association", "anchor" and "click handler" rules are all carried.

## Related blocks
`accessibility`, `nuxt-semantic-element-first`, `nuxt-no-hydration-nondeterminism`, `vue-nuxt-vuetify-conventions`,
`react-nextjs-conventions`.
