# writing-skills §11 — authoring rules from the Agent Skills guides

> Continues the numbered points of `SKILL.md` Steps (1 to 10). Append new points at the end; never renumber,
> a point cited elsewhere has to keep resolving. Every point below was checked against the guide text in
> `origin.md` before it was written; the wording is ours. 🟡: stated from documentation, not yet measured by us.

Read this file when a skill is being drafted or revised and its body or its description is the question.

## Content that earns its place

11. **A gotchas section is the highest-value content a skill can carry.** A gotcha is a concrete correction to a
    mistake the agent will make without being told: an environment fact that defies reasonable assumptions (a
    table that soft-deletes so every query needs the filter, one identifier with three names across three
    services, a health endpoint that stays green while the database is down). It is not general advice such as
    "handle errors properly". Keep it in the `SKILL.md` body, as an optional `## Gotchas` section after `Steps`:
    a reference file works only if the agent recognises when to load it, and for a non-obvious trap it will not.
    When the agent makes a mistake you have to correct, the correction becomes a gotcha.
12. **Test each paragraph with "would the agent get this wrong without it?"** If not, cut it. If unsure, test it.
    If the agent already does the whole task well with no skill, the skill adds nothing.
13. **Ground a skill in real material, not in general knowledge.** The sources that work are a hands-on task
    with its corrections and preferences, and project artefacts (runbooks, schemas, review comments, the history
    of fixes, real failures). A skill synthesised from a generic best-practice summary comes out as vague
    procedure.
14. **One skill is one coherent unit of work.** Too narrow and several skills must load for one task; too broad
    and it can no longer be activated precisely.
15. **Moderate detail beats exhaustive detail.** Concise stepwise guidance with one working example outperforms
    a full manual; edge cases the agent's own judgement handles do not need a rule.

## Calibrating control

16. **Match specificity to fragility.** Where several approaches are valid, give the freedom and the reason, so
    the agent can decide in context. Where an operation is fragile or order matters, be prescriptive: the exact
    sequence, and "do not change the command".
17. **Give a default, not a menu.** Pick one tool or approach, name the alternative once, with the condition for
    using it.
18. **Favour procedures over declarations.** Teach how to approach a class of problems, not the answer to one
    instance. Specific details stay legitimate (output templates, hard constraints, tool-specific instructions);
    the approach is what has to generalise.

## Patterns

19. **An output format is given as a template**, not described in prose; short ones inline, long or
    occasional ones in a separate file loaded on a stated condition.
20. **A multi-step workflow with dependencies carries a checklist**, so steps are not skipped.
21. **Validate before moving on.** Do the work, run a validator (a script, a reference checklist or a
    self-check), fix, repeat until it passes.
22. **A batch or destructive operation is planned, validated, then executed.** The agent writes the plan in a
    structured file, a validator checks it against the source of truth, and only then does the operation run.
    The validator's error message names what is available ("field X not found, available: A, B"), which is what
    lets the agent correct itself.
23. **Bundle a script when the agent keeps reinventing the same logic.** Compare execution traces across test
    cases; the same helper written independently every run is the signal to write and test it once.
24. **Refine from real runs, all of them, and read the traces.** Failures and successes both go back into the
    revision: what triggered wrongly, what was missed, what could be cut. Vague instructions, instructions that
    do not apply to the task, and menus without a default show up in a trace as wasted tries.

## The description

25. **A description says what the skill does and when to use it**, with the keywords that identify the task.
26. **Write it as an instruction to the agent.** "Use when ..." rather than "this skill does ...": the agent is
    deciding whether to act.
27. **Describe the user's intent, not the skill's mechanics.** The agent matches against what was asked.
28. **Be explicit about contexts, including those where the user does not name the domain.** Leaning towards
    over-listing contexts is the guide's advice; the counterweight is near-miss testing
    (`skills/skill-trigger-evals`), which shows the description that grew too broad.
29. **Keep it short, under the hard limit.** The open specification caps `description` at 1024 characters and
    `bin/test_frontmatter.py` enforces that figure. A client may list less (Step 3 states the figure measured for
    one platform); the portable cap is the one a block must never exceed.
30. **A simple one-step request may not load a skill even when the description matches.** Agents tend to consult
    skills for work beyond what they do alone, so a trigger test needs prompts that really need the skill.
