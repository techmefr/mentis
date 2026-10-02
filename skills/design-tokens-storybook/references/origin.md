# design-tokens-storybook — origin and source stamps

> Provenance of `skills/design-tokens-storybook`. Read it when a rule has to be traced back to its source or checked
> for freshness (`skills/source-freshness`), never to apply a rule.

**Written 2026-10-02, new block, never run on real work (🟡, base to confront with a real project).**

Sources, all primary, read on 2026-10-02 from shallow clones of public repositories:

- **Style Dictionary 5.5.5** (the latest release on the package registry that day; repository `style-dictionary`,
  Apache-2.0), its documentation sources: design tokens, architecture, configuration, transforms and transitive
  transforms, predefined transform groups, formats and references in output, logging, the DTCG utilities, the
  version 5 migration page, and the changelog entries on the structured colour and dimension forms.
- **Design Tokens Format Module 2025.10** (repository of the Design Tokens Community Group, reports licensed under the
  W3C Software and Document License): file format, design token, groups, aliases, types and the colour type; the
  resolver module's introduction only. This is a community-group draft. The copy in the repository's main branch
  carries a notice calling itself a preview draft not to be implemented directly; the rules here therefore
  describe the structure the pinned build tool reads, not a conformance claim.
- **Storybook v10.6.1** (latest on the registry that day; repository `storybook`, MIT). The documentation was read at
  the repository's main branch, which is the 11.0.0 alpha line: the pages on args, tags, naming and hierarchy,
  play functions, autodocs, themes, accessibility tests, testing in CI and visual tests, plus the migration notes
  for 9 to 10.

**Licence, honestly.** Style Dictionary and Storybook are Apache-2.0 and MIT: mechanisms rewritten with credit.
The format report's licence does not permit republishing the text as ours, so only the structure (what makes a
token, how types are inherited, what an alias may target) was taken and every sentence here is our own. No example
from any source is copied.

What is ours: the two-tier rule (§1.6), the "one notation per source" and "forbid case-only names" review rules, the
layered theme build (§2.8), warnings-as-errors in CI with the specific log levels (§2.12, from the logging page),
the severity policy for the accessibility parameter (§3.9), and all numbering.

**Facts that move, with their pin.**
- Format draft 2025.10, structured colour and dimension values, `$root`, `$deprecated`, `$extensions` (§1): the draft
  is changing; re-read on each new report.
- Build tool 5.x: Node 22 minimum, fixed reference syntax, strict references, both token notations accepted but not
  mixed (§1, §2.11).
- Storybook 10.x: Node 20.19 or 22.12, ESM configuration, the tag names and the three accessibility test levels
  (§3.5, §3.9, §3.12). The themes page in the docs is marked draft; decorator names are from its snippets and the
  addon README (§3.7).

**Not read, stated.** The format's gamut-mapping and interpolation colour modules, the composite types (shadow,
border, typography) beyond the build tool's shorthand transforms, the build tool's per-transform reference, the
Storybook CSF reference, the Vitest addon pages, the mocking pages and the visual-testing alternatives. The design
tool plugins (design-file to token exporters) were not read; no rule depends on them.

**Not in the freshness lock.** The two packages are not yet in `skills/source-freshness/references/tracked.json`; adding
them is a change to files outside this block and is listed in the writer's notes.

**Refresh protocol.** On a new major of either tool, re-read its migration page and the token format's changelog; give
each pinned fact above a verdict (`skills/source-freshness` §3); stamp the date even when nothing changed.
