---
name: writing-skills
description: Use when a new skill has to be created (or an existing skill revised) for this framework, applies the single template, checks that no existing block already covers the need, and credits the source if the idea comes from elsewhere.
---

# writing-skills

Cross-cutting (meta) block: this is the skill that explains how to write the other skills.
Applies as soon as a gap is identified in the pipeline or a sourced idea deserves to be
rewritten our way (Rule B).

## When
- A gap is spotted in the pipeline (e.g. "we're missing a model router" → `choose-model`).
- An idea seen elsewhere (market repo, article, aitmpl.com, superpowers) looks useful but doesn't
  exist here yet.
- An existing skill no longer matches real usage and needs revising.

## Steps
1. **Check that no existing block already covers the need**: read `CATALOG.md` and the skills
   table in `README.md` before writing anything. A duplicate costs more than a gap (Rule B,
   adoption checklist).
2. **Isolate the real mechanism**, not the packaging: if the skill is sourced from an external
   repo, read the concept until you can explain it without the source file in front of you.
3. **Write to the single template** (`CONVENTIONS.md`):
   - frontmatter `name` + `description` starting with "Use when..."
   - `# name`
   - `## When`
   - `## Steps`
   - `## Output / checkpoint`
   - `## Guardrails`
   - `## Origin`: never empty: either an external source credited honestly, or "no external
     source, internal synthesis".
4. **Place the skill in the pipeline** if it has a numbered step (see the `README.md` table), or
   mark it "cross-cutting" if it applies everywhere without being a sequential step (e.g.
   `choose-model`, `dispatch-parallel`).
5. **Update `CATALOG.md`** (registry + source traceability) and the skills table in `README.md`
   in the same move; a skill not referenced in both becomes invisible and gets rewritten twice
   later.
6. **Stay publishable** (Rule C): no real project name, no secret, a generic role ("the Laravel
   backend") never an internal repo name: except in an internal MR-review implementation, which has a different
   status (production evidence, real names owned).

## Output / checkpoint
A complete `skills/<name>/SKILL.md` file following the template, referenced in `CATALOG.md` and
in the `README.md` table, with a non-empty `Origin` section.

## Guardrails
- Never a skill without `## Origin`: honesty about the source (internal vs sourced from the
  market vs rewritten from a specific repo) is structural, not optional.
- Never install an external repo as a dependency: we read, we rewrite, we credit (Rule B): never
  a `git submodule` or a runtime import to a third-party repo.
- A skill that duplicates an existing block is a regression, not an addition: check step 1 before
  writing, not after.

## Origin
Rewrite of the `writing-skills` skill from a market skill/agent framework; there it documents
their own template, here it documents ours (the single template in `CONVENTIONS.md`), plus the
Rule B adoption checklist (check for duplicates, credit the source) which doesn't exist as such
on the superpowers side.
