# mentis: conventions for writing the building blocks

> Governance for every block in the workflow (skills, commands, agents, tools).
> Two founding rules, then the **single writing template**.

## Rule A: test the complete approach first

We assemble the **whole pipeline** (steps 1→11 of `WORKFLOW.md`) and push **one real feature end
to end** before splitting things into projects (mentis / starfleet / FLEET / …). The split comes
*after*, once the complete approach has been validated in the field. Until the full loop has run
once, no project boundary gets frozen.

## Rule B: rewrite it "our way", never depend on it

Any block coming from outside (skill, agent, technique, tool) is **rewritten internally**, never
wired in as a runtime dependency on a third-party repo.

**Why:**
- **Nobody upstream can change or break our workflow** (no drift, no `npx skills add` that
  behaves differently overnight).
- **Auditable**: we know exactly what each block does, it's our code/our words.
- **Maintainable**: *everything is written the same way* → a dev who knows one block knows them
  all.

**We keep the idea, not the package.** We read the source, extract the mechanism, rewrite it in
the template below, and **credit the origin** (`Origin` section). We don't copy the text; we
reimplement the principle.

### Checklist for adopting an external block
1. Read the source, isolate **the mechanism** (not the prose).
2. Check that no internal block already covers it (otherwise: extend, don't duplicate).
3. Rewrite it in the **single template** (below), Xefi voice, in English.
4. Fill in `Origin` (where the idea comes from, honestly).
5. **Zero external install**: the block lives in our repo. No network dependency.

## Rule C: mentis stays publishable

`mentis/` is designed to be **extracted one day into a public repo** ("superpowers, the Xefi
version", along the lines of the equivalent frameworks opened up by independent devs on the
market). So that it's a plain copy-paste when the time comes, we hold the boundary **from the
moment we write**:

- **Inside `mentis/` (generic, publishable)**: pipeline, skills, template, conventions, generic
  agents. No secrets, no real project names, no infra reality.
- **Outside `mentis/` (internal, private)**: real project names, infra (ports, SSO, hosts, DB
  server names), `CHALLENGE.md` / `FRICTIONS.md` / `VEILLE.md`, the memory. A block **never
  references those hard-coded**, it names a role ("the Laravel backend"), not a specific project
  (an internal repo name).

Simple rule: if a sentence couldn't be read by a dev outside Xefi, it doesn't go in `mentis/`.
Publication itself is **out of agent scope** (a human decision).

---

## The single template

Every block follows the **same shape**. One block = one folder `skills/<name>/SKILL.md` (or
`commands/<NAME>.md` for a sequence trigger, see below).

```markdown
---
name: <kebab-case-name>
description: Use when <precise triggering situation>, <what the block does>. <one sentence>.
---

# <name>

<One sentence: the purpose, and which step of WORKFLOW.md it maps to.>

## When
<The explicit trigger. If a checklist exists, one todo per item.>

## Steps
<Numbered, actionable. What the dev/agent does, in order.>

## Output / checkpoint
<What gets produced + the starfleet checkpoint written (`spec_done`, `verified`, …).>

## Guardrails
<What we don't do. Agent/human boundary if relevant. Escalation if blocked.>

## Origin
<Idea taken from: native Claude Code / market tooling / internal. Honest.>
```

### Form rules (non-negotiable)
- **English**, Xefi voice. The description starts with `Use when …` (reliable triggering).
- **No comments in the code** produced; explanations go in the chat/the docs.
- One block = **one responsibility** (see the split in `WORKFLOW.md` §4).
- **Never** reimplement what's native (`/model`, `/code-review`, `/security-review`, hooks,
  memory), we invoke it, we don't duplicate it.
- **commands vs skills**: a `command` (`/SPEC`…) is a short *step trigger* that invokes the
  matching `skill(s)`. The logic lives in the skill, not in the command. Goal: a single source
  per mechanism.

---

## State of the blocks (to be consolidated under this template)

Today the blocks are scattered (`starfleet/.claude/commands`, `starfleet/.claude/skills`,
`mentis/skills`) and use different formats. Target: **everything under `mentis/skills`**, one
thin `command` per step, a single template. Step → block mapping in `WORKFLOW.md` §2.

Gaps still to write (our way): **brainstorm** (1), **archi/graphify** (3), **GATE default-FAIL +
evaluator** (7), plus reinforcements **grill→ADR** (2), **two-axis review** (8), **`{passes:false}`
contract** (5), **finish** (11, wrapper around `finish_task`).
