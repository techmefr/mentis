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

## Levers from a second source (points 31 to 38)

> Added 2026-10-19 from `mattpocock/skills` `writing-for-agents` (MIT), wording ours. 🟡: the source's claims
> restated, none measured by us. Overlap with points 12, 15 and 25 to 30 was checked by reading them; where a
> point extends one of those it says which.

31. **Every step ends on a completion criterion.** The condition that tells the agent the step is done has two
    properties. *Clarity*: can the agent tell done from not done? A vague bound ("understanding reached") invites
    stopping early, because the steps still ahead pull attention towards being finished. *Demand*: how much it
    requires. "Every modified model accounted for" forces more work than "produce a change list". The strongest
    criteria are checkable and exhaustive. When a bound cannot be made sharper and the rush is observed, the later
    steps can be hidden by splitting the sequence, which works only across a real context boundary (a hand-off or
    a delegated worker); an inline call leaves them in view. Sharpen the bound first.
32. **Steer by the positive, and keep the `Never` beside it where failure is costly.** A prohibition alone puts the
    forbidden behaviour into the agent's context and makes it more available, not less. So every guardrail carries
    its positive form (what to do instead), and where the failure is costly, or a hook enforces it, the `Never ...`
    line stays beside it; the two are not alternatives. Worked example: "Run the project's own suite and name every
    failure, even one this change did not cause. Never loosen an assertion or lower a coverage threshold to close a
    gap." A guardrail with only a prohibition gets a positive target added when it is next edited; existing blocks
    are not bulk-rewritten.
33. **Hunt no-ops, and delete the whole sentence.** An instruction the agent already follows by default costs
    load and changes nothing. This is point 12 seen from the other side, with two additions: the test is relative
    to the model in use (two people who disagree about whether a sentence is a no-op disagree about the default,
    and the way to settle it is to run the block, not to argue), and a failing sentence is deleted rather than
    trimmed. A word too weak to beat the default ("be thorough" when the agent already is) is a no-op as well; the
    fix is a stronger word, not another technique.
34. **A pointer's wording decides when its target is reached.** A skill description, a router row and a line in a
    project instruction file are all pointers: they state what the material is and the branches that should send
    the agent to it. Front-load the leading word; give one trigger per distinct branch (synonyms that rename one
    branch are one branch written twice); cut identity the body already carries; remember that every word of an
    always-loaded pointer is paid on every turn. A must-have target behind a weak pointer is a source of
    run-to-run variance: sharpen the wording first and inline the material only if that fails. Extends points
    25 to 29.
35. **The environment is a source of truth, and a block that restates it is a cache.** Package scripts, config
    files, the directory layout and a command's help output can be looked up. Write down what looking cannot find:
    the unwritten convention, the reason behind a choice, the gotcha no config confesses (point 11). Leave one-file,
    one-command lookups to the environment, where they cannot go stale.
36. **Prune against sediment.** Stale layers settle in a block because adding feels safe and removing feels
    risky, until what is still live has to be dug out from under them. Check each line for relevance: does it
    still bear on what the block does, or did the behaviour or the world it describes move on? A shorter block is
    easier to keep relevant. Complements `SKILL.md` step 7, which orders what stays and does not remove anything.
37. **One meaning, one place; one concept, one heading.** Keep each meaning in a single authoritative place so a
    behaviour change is a one-place edit (duplication also inflates a meaning's prominence beyond its real rank).
    The opposite fault is scattering: keep a concept's definition, rules and caveats under one heading so reading
    one brings its neighbours. A block that is simply too long, even when every line is live and unique, thins the
    agent's attention; the cure is to move reference behind pointers and split by branch or sequence, which is the
    router form of `CONVENTIONS.md`.
38. **A leading word can replace a spelled-out phrase.** A compact concept the model already knows ("tight",
    "red") repeated as a token, never as a sentence, recruits what the model already holds about it; a made-up
    word recruits nothing and costs its definition. A triad written out in three places, or a pointer spending a
    sentence to gesture at one idea, is a candidate. The source's claim, not measured here: check that the
    shorter word still triggers the behaviour by running the block.

