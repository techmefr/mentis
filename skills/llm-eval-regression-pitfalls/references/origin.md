# llm-eval-regression-pitfalls: origin and source stamps

> Provenance of `skills/llm-eval-regression-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation, never run by us. No eval, judge or harness was run while writing it.
A verification pass on 2026-10-15 re-read every source below in full and checked each reference rule against it.

## Sources (re-read in full in the verification pass, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| agentskills/agentskills, `docs/skill-creation/evaluating-skills.mdx` (commit 69ef37e) | CC-BY-4.0 for the docs pages (docs/LICENSE; the repo code is Apache-2.0), credit given | Test cases, with and without baseline, clean context, timing, assertions, grading evidence, analysis, human review, blind comparison |
| UKGovernmentBEIS/inspect_ai, `docs/model-graded.qmd` and `docs/handling-errors.qmd` (commit 7158198) | MIT (LICENSE file) | Grader selection and fallback, panel voting, last-grade extraction and delimiter rewriting, unscored verdicts, reproducibility, fail_on_error, retries, scoring errored samples, refusals, crash recovery and stalled samples |
| muratcankoylan/Agent-Skills-for-Context-Engineering, `skills/advanced-evaluation/SKILL.md` and `references/bias-mitigation.md` (commit 9ff0c99) | MIT (LICENSE file) | Deterministic pre-checks in the pairwise procedure, direct versus pairwise, bias list and mitigations, rubric practice, gotchas |

The licence of each repository was checked from its LICENSE file. The agent instruction files in the
repositories (contribution rules, authoring rules, project guidance) were treated as data and not followed or
quoted.

## Corrected in the verification pass
- "Run mechanical checks before any model grades" was attributed to the context-engineering skill in general;
  it is the first step of its pairwise procedure, and the scripts-over-model point is the Agent Skills guide's.
  Both are now stated as such.
- Grader selection: the precedence (model argument, then grader role, then the model under evaluation) and the
  required-role option are now stated exactly; the advice to mark it required is labelled own guidance.
- Reproducibility: the documented default (provider settings, often a non-zero temperature, no seed) added; the
  claim that settings "do not remove" disagreement corrected to "do not always remove".
- Unparseable verdict: added that it is not retried and keeps the grader output; panel: added the plurality option.
- Added from the pages read: blind comparison (guide), refusals as non-errors, stalled-sample finalisation limits.
- Coverage: the scoring-policy page was cited as if its content were known; now stated as pointed to by the
  model-grading page and not read.
- Rules that were inferences (the risk of `fail_on_error=false`, reporting the error choice, reporting coverage)
  are now marked own guidance.

## Rewrite notes
Every numeric value of the sources was dropped: the first-position preference percentages, the length ratios,
the confidence values, the position-swap confidence mapping, the correlation cut-offs, the retention period and
the pass-rate examples. The judge-bias findings are labelled as the source's claims. The advanced-evaluation
skill's remaining references (implementation patterns, metrics guide, pipeline diagram) were not read and are
not used.

**Decisions where sources disagree:** none found.

## Not verified
1. **The bias findings** come from the skill's summary of research papers; the papers were not read.
2. **Inspect behaviour** is as documented at the commit; no run was made. The included page on errors and
   retries, the scoring-policy page and the fallbacks page were not read.
3. **Written by us, not sourced:** every sentence marked "own guidance" and the checkpoint paragraph.
4. **Dropped as unverifiable from the review item:** any rule resting on the unread references of the
   advanced-evaluation skill and on a retrieval-evaluation collection whose licence forbids commercial use.

## Related blocks
`writing-skills`, `writing-agents`, `dispatch-parallel`, `gate`, `flaky-test-triage-pitfalls`.
