---
name: extract-conventions
description: Use when starting on a project or when the reference docs need refreshing, generates from the REAL CODE a draft of the observed conventions, instead of writing them by hand.
---

# extract-conventions

**Setup / maintenance** block (not a pipeline step). Makes the agents stronger by giving them
references **anchored in the real code**, and automates the recovery of a project's *internal*
knowledge. Complements `SOURCING-INBOX` (which collects *external* knowledge).

## When
When starting on a project, or to refresh the references before `review`/`code`/`archi` rely on
them. Always at a human's request.

## Steps
1. Read the real code — a structural index first where one is installed (an AST search such as
   `claude-mem`'s `smart-explore`, or a graph artefact such as `graphify`), and targeted reading
   in every case: structure, recurring patterns, naming, backend responses, frontend components,
   design tokens actually used, test patterns. The index only tells you where to look; a
   convention is observed in the code, never inferred from a symbol list. On a small codebase
   with no index installed, direct targeted reading of every file is the primary path, not a
   fallback to apologise for — don't spend time installing an index just to satisfy this step.
2. Extract the **observed conventions** by domain (frontend / backend / tests / design) — only
   the domains actually present; an empty or single-file domain isn't worth its own section, fold
   it into the nearest one instead. For each convention, count how many independent places show
   it: a pattern seen in one file only is a candidate, not yet a convention — mark it "single
   occurrence, unconfirmed" rather than stating it with the same confidence as a pattern repeated
   across three or more files. This matters most on small codebases, where most patterns *are*
   single-occurrence and the draft otherwise reads as more settled than the evidence supports.
3. Emit a **draft** `references/observed/<project>.md`, marked **INTERNAL** (it contains project
   specifics).
4. **Human ratification**: the dev validates / corrects. What is validated **and generic** is
   distilled (by hand) into the publishable conventions (`references/conventions-*.md`); the rest
   stays internal.
5. Replayable: running it again produces a diff against the previous version (drift becomes
   visible).

## Output / checkpoint
`references/observed/<project>.md` (internal) + a possible update of the generic conventions after
ratification. No pipeline checkpoint.

## Guardrails
- **The automation proposes, the human ratifies**: the output has no authority until it's
  validated. We extract what the code *does* (good AND bad habits) ≠ what it *should* do.
- **Internal by default** (rule C): generated from a real project → the publishable version is a
  human distillation, with no project/colleague name.
- **Read-only** on the project: we read, we never edit the code.
- **On demand**, never an automatic hook (the auto "doc-freshness" was removed on purpose).

## Origin
Internal `graphify` + a recognised market skill author (improve-codebase-architecture) + a market
generalist dev skill catalogue (source-driven-development / context-engineering), rewritten our
way.

Dogfooded, 2026-09-10: ran steps 1-3 for real against a small standalone NestJS project
(`/tmp/dogfood-nestjs`, 14 source files: `UsersModule` with controller/service/repository/DTO, a
`WelcomeEmailQueue` job, unit tests — the same project `nestjs-node-conventions` dogfooded
earlier the same day), no structural index installed, direct file reading only. Extracted 11
backend conventions, output kept as `/tmp/dogfood-nestjs/EXTRACTED_CONVENTIONS.md` (outside this
repo, per rule C). Compared against `skills/nestjs-node-conventions/SKILL.md`: found the same
core patterns already documented there (module/DI/DTO/exception/repository rules in
`nestjs-node-conventions` §1-2, the ESM `.js`-extension and `import type`/`TS1272` rule already
folded into `nestjs-node-conventions` §1.6 from the earlier pass), plus two the existing skill
doesn't mention — a plain `interface` for the entity/model (no class, no behavior needed on it)
and a discriminated union used for a job/queue result (not just an API response, which is the
only case `nestjs-node-conventions` §3.2 covers). Nothing obvious was missed. Two
real method gaps found and fixed above: step 1 didn't say what to do when no structural index is
installed on a small project (added: read directly, that's the primary path here, not a fallback
to apologise for); step 2 had no way to flag a pattern seen in exactly one file as less certain
than one repeated across several — on a small codebase most patterns are single-occurrence, and
without that flag the draft reads as more settled than the evidence supports. Step 4 (human
ratification) and step 5 (replay diff) weren't exercised — no second run happened, and no dev
ratified the draft into the generic conventions.
