<h1 align="center">How I write and govern my agents</h1>

<p align="center">
  <em>The method, not just the result: why this framework has this shape,<br>
  how an agent is born here, and the rules that apply to all of them, without exception.</em><br>
  <sub>Written for someone who knows none of my agents.</sub>
</p>

<p align="center">
  <a href="#3-the-three-founding-rules"><img alt="rules" src="https://img.shields.io/badge/founding%20rules-A%20·%20B%20·%20C-2f6feb?style=flat-square"></a>
  <a href="#4-the-single-template-how-i-write-an-agent"><img alt="template" src="https://img.shields.io/badge/template-7%20sections-8250df?style=flat-square"></a>
  <a href="#5-the-two-cross-cutting-guarantees"><img alt="guarantees" src="https://img.shields.io/badge/guarantees-fresh%20context%20%C2%B7%20default%3Dfailure-1a7f37?style=flat-square"></a>
  <a href="#6-always--ask--never"><img alt="guardrails" src="https://img.shields.io/badge/guardrails-ALWAYS%20%2F%20ASK%20%2F%20NEVER-bf8700?style=flat-square"></a>
</p>

<table>
<tr><td width="50%" valign="top">

1. [The context](#1-the-context)
2. [The problem I'm solving](#2-the-problem-im-solving)
3. [The three founding rules](#3-the-three-founding-rules)
4. [The single template](#4-the-single-template-how-i-write-an-agent)
5. [The two cross-cutting guarantees](#5-the-two-cross-cutting-guarantees)
6. [ALWAYS / ASK / NEVER](#6-always--ask--never)

</td><td width="50%" valign="top">

7. [How an agent is born here](#7-how-an-agent-is-born-here-the-sourcing-cycle)
8. [Real status, being honest about maturity](#8-real-status-being-honest-about-maturity)
9. [A loop is possible, but not on everything](#9-a-loop-is-possible-but-not-on-everything)
10. [The vision: the system should learn](#10-the-vision-the-system-should-learn-not-just-run)
11. [Why it matters](#11-why-it-matters)

</td></tr>
</table>

---

## 1. The context

I've been working on this for about a month. Built piece by piece, not in one
go: **one agent at a time, each tested on real work before I consider it
settled**. Some already have real production experience (the Nuxt/Vue and
PHP/Laravel reviewers, the final gate, the cold judge). Others are written
but not yet proven on anything real, for lack of a project on those stacks
for now (the Go/.NET agents). The detail is in the
[Real status](#8-real-status-being-honest-about-maturity) section.

> [!NOTE]
> **My baseline method**: I assemble the complete pipeline first, on a real task
> end to end, before freezing a split into separate projects. I freeze no
> boundary until the full loop has run once.

## 2. The problem I'm solving

A generic "code assistant" agent gives me three concrete problems — and each
one is answered by exactly one rule.

| | The problem | Answered by |
|---|---|---|
| 1️⃣ | **Whoever writes the code cannot be the one who judges it**, in the same session. It watched the code being written, it knows the trade-offs taken along the way, it is structurally lenient with itself. | [Fresh context](#fresh-context) |
| 2️⃣ | **"Do your best" is not verifiable.** Without a testable criterion, an agent that claims "it's done, it works" is something I can neither confirm nor contradict. I need cited evidence (file, line, test output), never a statement taken at face value. | [Default = failure](#default--failure) |
| 3️⃣ | **I take inspiration from the market without depending on it.** Good ideas exist in public repos, conventions, agent patterns, framework structures. But installing them as a dependency means exposing myself to a third party changing its behaviour overnight and breaking my pipeline without warning. | [Rule B](#rule-b-i-rewrite-it-my-way-i-never-depend-on-it) |

## 3. The three founding rules

### 🅰️ Rule A: I test the complete approach first

I assemble the whole pipeline (brainstorm → … → finish) and run it on a
real task before splitting it into separate projects. The split comes
afterwards, once the approach has proven itself in the field.

### 🅱️ Rule B: I rewrite it my way, I never depend on it

Any idea coming from outside (skill, agent, technique) gets rewritten
internally. **Never wired in as a runtime dependency.**

```mermaid
flowchart LR
    A["📖 I read<br/>the source"] --> B["🔧 I extract<br/>the mechanism<br/><i>never the prose</i>"] --> C["✍️ I rewrite it<br/>in my template"] --> D["🏷️ I credit the origin<br/>in CATALOG.md"]
    D --> E["<b>What I keep is the idea,<br/>never the package</b>"]
    classDef s fill:#f6f8fa,stroke:#8c959f,color:#0d1117
    classDef o fill:#dafbe1,stroke:#1a7f37,color:#0d1117
    class A,B,C,D s
    class E o
```

Why I work that way: **nobody upstream can break my workflow.** I know exactly
what each block does, it's my code, my words. And everything is written the
same way, so anyone who knows the template can find their way around.

### 🅲 Rule C: the framework stays publishable

I write it from the start so it can be extracted one day into a public repo:
no secrets, no real project names, no infra reality in this folder. A block
names a role ("the Laravel backend"), never a specific project.

> [!TIP]
> My simple rule: **if a sentence couldn't be read by someone from outside, it doesn't go here.**

## 4. The single template: how I write an agent

All my agents follow the same **7-section structure**, never improvised case by
case.

```mermaid
flowchart TD
    R["<b>1 · ROLE</b><br/>a single responsibility,<br/>what the agent NEVER does"]
    M["<b>2 · MEMORY</b><br/>what persists, where,<br/>what is re-read on every call"]
    B["<b>3 · LOOP</b><br/>action → verification → decision,<br/>explicit exit condition"]
    O["<b>4 · TOOLS &amp; SCOPE</b><br/>allowed / forbidden, hard-coded"]
    G["<b>5 · GUARDRAILS</b><br/>ALWAYS / ASK / NEVER"]
    C["<b>6 · FRESH-CONTEXT REVIEW</b><br/>how freshness of judgement<br/>is guaranteed by construction"]
    T["<b>7 · TRACE</b><br/>what is returned,<br/>readable and verifiable after the fact"]
    R --> M --> B --> O --> G --> C --> T

    classDef what fill:#ddf4ff,stroke:#0969da,color:#0d1117
    classDef how fill:#fff8c5,stroke:#bf8700,color:#0d1117
    classDef proof fill:#dafbe1,stroke:#1a7f37,color:#0d1117
    class R,M what
    class B,O,G how
    class C,T proof
```

ROLE is what this agent's single responsibility is, and what it never does.
MEMORY is what persists between two invocations and where it lives. LOOP is
the exact cycle, action then verification then decision, and how it stops.
TOOLS & SCOPE lists what is allowed and what is forbidden, hard-coded, not
just verbally. GUARDRAILS is what must always happen, what I want asked
rather than guessed, what is off limits. FRESH-CONTEXT REVIEW explains how I
guarantee that judgement isn't polluted by the session that produced the
work. TRACE, finally, is what the agent returns at the end, so that someone
else can verify it after the fact.

> [!IMPORTANT]
> **"Hard-coded, not just verbally" was a claim I hadn't earned until 2026-09-07.**
> All 25 agents carried `name`, `description` and `model` in their frontmatter and nothing else, so
> twelve of them stated *"Never Write/Edit: you fix nothing, you report"* while the runtime handed
> them every tool. The prohibition was real in the prose and absent in the config: it held exactly
> as long as the model chose to honour it, which is the shape of guarantee this whole framework
> exists to refuse from anyone else.
>
> Twenty of them now declare `disallowedTools`, so the forbidden tools are gone before the first
> turn. What the field cannot express is a **path-scoped** rule — my eight readers do write, inside
> their scratch directory and nowhere else — so each of those now says which half the runtime holds
> and which half is still trust, rather than implying it's all covered.

<details>
<summary><b>One exception, added 2026-08-14</b> — a uniform family may hoist sections 1–7 into one reference</summary>

It is the same rule pushed one step further. When several agents do the same job on different
stacks, those seven sections end up identical, and **identical text in eight files stops being
identical the first time one of them is fixed**. My eight review readers had drifted to 93–96 %
similar for 92 KB.

So a uniform family may hoist sections 1 to 7 into a single `references/` doc: their contract now
lives in `references/review-core.md`, each reader reads it first, and its own file carries only what
actually differs — its calibration, its scope, its default mode, where its rules come from, what it
looks for, its style delta.

**The contract isn't weaker, it's written once**, which is the only way it stays identical. Any
agent outside such a family still carries all seven itself.

</details>

<details>
<summary><b>A concrete example</b> — <code>galadriel</code>, the cold judge</summary>

| Section | For `galadriel` |
|---|---|
| **ROLE** | Return a binary PASS/NEEDS_WORK verdict, nothing else — no fixes, no code suggestions |
| **MEMORY** | Nothing persists between two invocations; the input must explicitly contain the diff, the acceptance criteria and the evidence |
| **Main guardrail** | Missing or inconclusive evidence means automatic `NEEDS_WORK`, **never** the benefit of the doubt |

</details>

## 5. The two cross-cutting guarantees

### Fresh context

**Whoever judges never watched the code being written.**

```mermaid
sequenceDiagram
    autonumber
    participant Dev as 🛠️ Production session
    participant Code as 📄 Code produced
    participant Judge as 🧊 Judge agent (fresh context)
    Dev->>Code: writes the code, knows the trade-offs taken
    Note over Judge: invoked separately,<br/>no memory of the Dev session
    Code->>Judge: diff + cited evidence only
    Judge-->>Dev: PASS / NEEDS_WORK — never negotiated in the same session
```

This isn't an option I switch on now and then, **it's structural**. The judge
agent is invoked as a separate subagent, with no access to the history of
the conversation that produced the work.

### Default = failure

A claim along the lines of *"I tested it, it works"* without cited evidence is
not evidence, I ignore it. If the scope given is too incomplete to assess
anything, the default verdict is `NEEDS_WORK`, never `PASS` out of optimism.

> [!NOTE]
> I found this rule in **none** of the public sources I consulted on agent design.
> It's the part I had to invent myself.

### Short output by default

An agent's answer isn't billed like a human's answer — every output word has a
real token cost. By default, an agent returns the bare minimum: a status, a
verdict, a list of findings with file + line + one sentence. Never a wall of
justification or context that duplicates what I can already see. The detail
(full reasoning, alternatives explored) stays available if I ask for it
again, it isn't given by default.

I had explored a lead while sourcing, a "Caveman" agent in output-compression
mode. The fully telegraphic style I ruled out, unreadable on a second pass.
But the principle — short output by default rather than verbose — I keep as a
cross-cutting guarantee, on the same footing as fresh context and default-failure.

Until 2026-08-14 that guarantee was stated and enforced nowhere, so a review
that found four things still came back as two pages. It now has a mechanism,
[`references/terse-reporting.md`](../references/terse-reporting.md), cited from the TRACE section of
the **seventeen** agents that hand back a report and from `review-core.md`.

| ✅ The report is | ❌ Never in it |
|---|---|
| Verdict on the first line | Preamble |
| One line per item: file, fact, consequence | Restatement of my own instruction |
| Then the artefact paths | Method narrative, count of files read |

**Three things are exempt**, and they are where a terse register actually breaks, not on length:

| Exempt | Why |
|---|---|
| 🔁 **Negation and polarity** | *"nothing found on the parsing path"* compressed to *"parsing"* inverts a verdict, and a gate reporting the opposite of what it found is worse than a gate saying nothing |
| 🔤 **The verdict word itself** | Spelled out — not an emoji, not a colour |
| 📊 **The confidence level** | Flattening confirmed, worth-digging-into and speculative into one list is a loss, not a saving |

And **evidence stays quoted in full**: under default = failure a paraphrased proof is not a proof.

> [!WARNING]
> **The boundary matters as much as the rule.** This governs the **report** — what I read once and
> act on. It never governs the **artefact** — what someone else reads later: an MR comment, an ADR,
> a commit message. Those keep their own register, which for an MR comment is already short and
> direct for a different reason: it has to pass as written by me in a public thread.

## 6. ALWAYS / ASK / NEVER

The most robust guardrail format I found in external research (analysing more
than **2,500 public agent configuration files**) is a three-tier rule rather than
a flat list of prohibitions:

| Tier | Means |
|---|---|
| 🟢 **ALWAYS** | What must happen systematically |
| 🟡 **ASK** | The cases where the agent must stop and ask me rather than choose on my behalf |
| 🔴 **NEVER** | The absolute red lines |

A real example with `elrond`, my orchestrator that detects a diff's stack and
routes it to the right reviewer. When the stack is ambiguous (monorepo,
contradictory signatures), the rule isn't *"do your best"* but explicitly **ASK**.
Never guess, even at the cost of interrupting the flow.

## 7. How an agent is born here: the sourcing cycle

```mermaid
flowchart LR
    V["🔭 <b>Scouting</b><br/>a repo/idea spotted<br/>along the way"] --> T["📋 <b>Triage</b> in CATALOG.md<br/>status 🔎 to mine"]
    T --> D{"Does an internal block<br/>already cover the idea?"}
    D -->|yes| X["✕ <b>Ruled out</b><br/>reason noted honestly"]
    D -->|no| E["🔧 <b>Extract the mechanism</b><br/>never copied prose"]
    E --> W["✍️ <b>Rewrite</b> in the single<br/>template, in English"]
    W --> O["🏷️ <b>Origin credited</b><br/>in CATALOG.md"]
    O --> DF["🍽️ <b>Dogfood</b> on real work"]
    DF --> S["📈 <b>Status updated</b><br/>🟡 written → 🟢 proven"]

    classDef scout fill:#f6f8fa,stroke:#8c959f,color:#0d1117
    classDef out fill:#ffebe9,stroke:#cf222e,color:#0d1117
    classDef work fill:#fff8c5,stroke:#bf8700,color:#0d1117
    classDef done fill:#dafbe1,stroke:#1a7f37,color:#0d1117
    class V,T,D scout
    class X out
    class E,W,O work
    class DF,S done
```

I adopt nothing because it sits in a popular repo. Every line of
`CATALOG.md` carries an explicit decision of mine — adopted or ruled out, with
its reason noted. **A good part of the backlog I deliberately rule out**, and
that is precisely what proves the triage is real, not just a pile-up.

## 8. Real status, being honest about maturity

No overselling here. Some of my agents have real production experience,
others are written but not yet confronted with a real project. The table is
kept up to date in `CATALOG.md`, and **its maturity column is the source of
truth, not this document**.

| Marker | Means |
|---|---|
| 🟢 | It **ran on real work** |
| ✅ | Only that the **rewrite is finished** |
| 🟡 | Written, never run — **most of the repo**, and saying so is the point of the column |

Two consequences of the same honesty:

- **A second layer exists with a weaker contract.** The `business/` blocks
  (legal, marketing, sales, communication, product) are written *without*
  internal expertise in those functions, they never gate anything, and 🟡 is
  their ceiling until someone who owns that function reviews them. They live in
  a separate folder precisely so the dev core's claims aren't diluted by
  association — the reasoning is in [`business/README.md`](../business/README.md).
- **Where someone else already owns a rule, I don't.** The org skill catalogue
  (211 skills, versioned, installed org-wide) is the authority on per-stack style
  and structure. **Two sources for one rule is the same failure as a producer
  judging its own work**: nobody knows which holds. The boundary is drawn block by
  block in `CATALOG.md` §0.

## 9. A loop is possible, but not on everything

My pipeline can run in a loop without supervision **up to the gate**: brainstorm
→ spec → archi → plan → code → debug can chain together without a human
validating each step.

```mermaid
flowchart LR
    subgraph AUTO["🔁 can loop unsupervised"]
      direction LR
      A["brainstorm → spec → archi → plan → code → debug"]
    end
    subgraph HUMAN["🛑 deliberate human stops, non-negotiable"]
      direction LR
      B["<b>gate — galadriel</b><br/>returns a verdict,<br/>merges nothing"] --> C["<b>the merge</b><br/>always 2 human approvals"]
    end
    AUTO --> HUMAN
    classDef auto fill:#dafbe1,stroke:#1a7f37,color:#0d1117
    classDef stop fill:#ffebe9,stroke:#cf222e,color:#0d1117
    class A auto
    class B,C stop
```

This isn't a technical limitation on my side. End-to-end autonomy in the
style of the market's fully agentic autonomy frameworks I explicitly ruled
out as a counter-example while sourcing (`CATALOG.md`): **an agent that merges
code on its own without validation is exactly the counter-example I don't
want to become.** The loop speeds up production, never the decision to merge.

### Which native loop — three answers, and I had only been using two

| Shape | Use it when | Here |
|---|---|---|
| 🎯 **`/goal`** | The exit condition is a **verdict I produce** | The gate: step 6 back to 7 until `PASS` |
| ⏱️ **`/loop`** | The exit condition is **somebody else's state**, and has to be sampled | A queue of incoming bug reports |
| 📡 **`Monitor`** | There is a **stream to tail** rather than a state to sample | A build, a log, a test watcher |

`Monitor` streams the output lines into the conversation as they arrive, where a `/loop` spends a
whole turn per sample to ask *"is it done yet"*. **Nothing in this repo named it until 2026-09-07**,
which means the shape my own `dispatch-parallel` block would have blessed — agents dispatched to
poll something — was the expensive one. The mechanics, and the seven-day expiry that bounds a
`/loop` I forget about, are in
[`references/claude-code-platform.md`](../references/claude-code-platform.md) §5.

## 10. The vision: the system should learn, not just run

My goal isn't to have a frozen set of agents. It's a system that gets smarter
with use, **without ever touching the fixed rules** (fresh context, default =
failure). What improves is the accumulated domain knowledge, not the doctrine.

Three feedback loops are in place, even if only partially:

```mermaid
flowchart LR
    W["🛠️ real work"] --> C["📊 <b>Calibration</b><br/>every review logged:<br/>findings kept, false positives disproved"]
    W --> M["🧠 <b>Persistent memory</b><br/>corrections and confirmations<br/>become durable rules"]
    W --> X["🔄 <b>extract-conventions</b><br/>conventions generated from<br/>the real existing code"]
    C & M & X --> F["⚡ faster, better-aimed triage next time"]
    F -.-> W

    classDef in fill:#f6f8fa,stroke:#8c959f,color:#0d1117
    classDef loop fill:#ddf4ff,stroke:#0969da,color:#0d1117
    classDef out fill:#dafbe1,stroke:#1a7f37,color:#0d1117
    class W in
    class C,M,X loop
    class F out
```

> [!WARNING]
> **What I still lack** for this to be systematic rather than ad hoc: a periodic review that
> re-reads those three sources and updates `CATALOG.md` (maturity, refined guardrails).
> Not automated yet — to be set up as the next step.

## 11. Why it matters

- 🧊 **The review doesn't flatter**, because the reviewer is never the one who wrote the code — it
  runs in a separate cold session.
- 🧾 **Nothing is taken on trust.** *"It's done"* is never enough; concrete evidence is.
- 🔓 **It grows richer without depending on anything.** The market evolves, I dip into it, but
  nothing can break my pipeline by changing from the outside.
- 🎯 **It's adapted to my reality**, not to a fiction of uniform competence: an agent phrases its
  remarks as honest questions on a stack I haven't mastered yet (PHP/Laravel), and as clear-cut
  statements on a stack where I have real expertise (JS/TS). **The style follows my reality, not a
  generic tone.**
