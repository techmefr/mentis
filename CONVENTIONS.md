# mentis: conventions for writing the building blocks

> Governance for every block in the workflow (skills, commands, agents, tools).
> Two founding rules, then the **single writing template**.

## Rule A: test the complete approach first

We assemble the **whole pipeline** (steps 0→11 of `WORKFLOW.md`) and push **one real feature end to
end** before splitting anything out into a separate project or tool. The split comes *after*, once the
complete approach has been validated in the field. Until the full loop has run once, no boundary gets
frozen — and **no block may depend at runtime on a tool that split off**, which is where rule A meets
rule B (see `start-feature`, corrected for exactly that).

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
3. Rewrite it in the **single template** (below), the house voice, in English.
4. Fill in `Origin` (where the idea comes from, honestly).
5. **Zero external install**: the block lives in our repo. No network dependency.

## Rule C: mentis stays publishable

Rule C carries two loads, and the nearer one is the company, not the public. **Sharing inside a company
means many teams**: a block hard-coding one team's project name is useless to the others and leaks to
everyone. The second load is that `mentis/` should stay **extractable into a public repo** one day. Both
are served by holding the same boundary **from the moment we write**:

- **Inside `mentis/` (generic, publishable)**: pipeline, skills, template, conventions, generic
  agents. No secrets, no real project names, no infra reality.
- **Outside `mentis/` (internal, private)**: real project names, infra (ports, SSO, hosts, DB
  server names), `CHALLENGE.md` / `FRICTIONS.md` / `VEILLE.md`, the memory. A block **never
  references those hard-coded**, it names a role ("the Laravel backend"), not a specific project
  (an internal repo name).

Simple rule: if a sentence couldn't be read by a dev outside the company, it doesn't go in `mentis/`.
Publication itself is **out of agent scope** (a human decision).

A block that can't pass this test isn't rewritten to be vaguer — it's **kept out and stays local**. That
has already happened, and the mechanism for deciding is in `skills/distributing-blocks` §1.

## The second layer: `business/`

Blocks for the company's other functions (legal, UI/UX, marketing, sales, communication, product) live in
`business/`, follow the **same template**, and carry an **explicitly weaker contract**: no fresh-context
judge, no cited evidence, they never gate anything, and 🟡 is their maturity ceiling. Rules A/B/C apply
unchanged. The reasoning, and the honesty rule specific to that layer, are in `business/README.md` — read
it before adding one.

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
<What gets produced + the pipeline checkpoint written (`spec_done`, `verified`, …), see `WORKFLOW.md` §5.
A `business/` block has no checkpoint and says so.>

## Guardrails
<What we don't do. Agent/human boundary if relevant. Escalation if blocked.>

## Origin
<Idea taken from: native Claude Code / market tooling / internal. Honest.>
```

## The agent template

An agent is not a skill: a skill describes a step, an agent is a persona with a scope and a loop. It has its
own shape, and **the same one for all of them** — `.claude/agents/<name>.md`:

```markdown
---
name: <name>
description: <what it reviews or builds, on which stack, when to pick it over its siblings, which model>
model: <sonnet | opus>
---

<One or two sentences: who this agent is and what it produces.>

## 1. ROLE          <what it is responsible for, and the calibration that changes its register>
## 2. MEMORY        <what persists between two invocations, and what explicitly does not>
## 3. LOOP          <action → verification → decision, with an explicit exit condition>
## 4. TOOLS & SCOPE <allowed / forbidden, named; the scope of files it may produce findings on>
## 5. GUARDRAILS    <what it never does; the default mode; what it does when in doubt>
## 6. FRESH-CONTEXT REVIEW <what guarantees it judges the artefact and not its own memory>
## 7. TRACE         <what its final message must contain, and what it writes where>
## 8+ …             <agent-specific sections, numbered on, free titles>
## Origin           <only when the idea came from outside; omitted when the agent is ours>
```

**Sections 1 to 7 are mandatory, in that order, numbered.** They are the contract every agent honours; an
agent with nothing to say under one of them still says so in a line, because "nothing persists here" is
information. Sections 8+ carry what makes that agent worth having — the eight review readers, for instance,
all share the same four: `8. Where the rules come from`, `9. What you're looking for`, `10. Comment style`,
`11. Transport and review mechanism`.

Two consequences worth stating, because both have already been violated once:
- **A family is uniform or it isn't a family.** When several agents do the same job on different stacks, they
  carry the same sections in the same order with the same titles, and only the content differs. A reader that
  drifts into its own shape is a reader nobody can compare, and the duplication hides in the gap.
- **What is shared lives in `references/`, cited once.** An agent never re-explains a mechanism another agent
  also uses — that is how ~150 identical lines of forge plumbing ended up in eight files.

### Form rules (non-negotiable)
- **English**, the house voice. The description starts with `Use when …` (reliable triggering).
- **Agent naming = two families, and the family carries meaning.** A Lord of the
  Rings name means the agent only **watches**: review or gate, a verdict and a
  report, never Write/Edit on the repo under review. A Matrix name means the
  agent takes part in the **dev cycle**: implementers, and auditors that probe a
  running app or a repo. Picking the family is therefore not decoration: it
  commits the agent's `TOOLS & SCOPE` section. An agent that gains the right to
  write changes family, or it doesn't gain the right.
- **No comments in the code** produced; explanations go in the chat/the docs.
- One block = **one responsibility** (see the split in `WORKFLOW.md` §4).
- **Never** reimplement what's native (`/model`, `/code-review`, `/security-review`, hooks,
  memory), we invoke it, we don't duplicate it.
- **commands vs skills**: a `command` (`/SPEC`…) is a short *step trigger* that invokes the
  matching `skill(s)`. The logic lives in the skill, not in the command. Goal: a single source
  per mechanism.

---

## State of the blocks

Consolidation is done: **every block lives under `mentis/skills` or `mentis/business`**, one folder per
block, one template, no other format left. Step → block mapping in `WORKFLOW.md` §2, registry and maturity
in `CATALOG.md` §1.

What remains open is validation, not structure: most blocks are 🟡 — written, never run on real work. A
block only earns 🟢 by being used, and `skills/testing-blocks` is the cheap check in the meantime.

That list of gaps is closed: every step 0→11 has its block, the gate has its default-FAIL hook pair, and
the business layer exists. The live backlog is in `CATALOG.md` §2 — and the top item there is no longer
writing, it's **running**.
