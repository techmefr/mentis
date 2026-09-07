# The native platform surface

> What Claude Code itself provides, as of the stamp below, so that no block in this repo
> reimplements it and no block declares a guarantee the platform would have enforced.
>
> **Verified 2026-09-07** against the official documentation at `code.claude.com/docs`
> (the `docs.claude.com/en/docs/claude-code/*` paths now redirect there). Expiry: this is a
> version-pinned corpus and the platform ships weekly — treat anything here as unverified past
> 2026-12-07 and refresh per `skills/source-freshness` §3 before relying on a field name.

Two rules in `CONVENTIONS.md` depend on this file being current, and both fail silently when it
isn't. "Never reimplement what's native" needs an accurate list of what *is* native — a block that
reimplements a polling loop the platform grew three months ago is not wrong, it's redundant, and
nothing in a review catches redundancy. "A guarantee is enforced or it isn't a guarantee" needs the
frontmatter field list — an agent whose file says *never Write/Edit* while its frontmatter grants
every tool is a rule the operator believes and the runtime ignores.

## 1. Models and effort

The model is one axis and the reasoning budget is a second, independent one. `skills/choose-model`
owns the decision; this section owns the facts it decides against.

| Alias | Resolves to (Anthropic API) | Where it fits here |
|---|---|---|
| `haiku` | Haiku 4.5 | mechanical work: stack detection, extraction, formatting |
| `sonnet` | Sonnet 5 | the default: building, reading a diff, applying documented conventions |
| `opus` | Opus 5 | a verdict that is hard to walk back: a gate, a judge, a security audit |
| `fable` | Fable 5.1 | the longest sessions; not used by any agent here |
| `best` | Fable where available, else Opus | never pinned in a block: it moves under you |
| `opusplan` | Opus in plan mode, Sonnet in execution | not used here; our plan step is a skill, not a mode |

On third-party providers the same alias resolves to an older version (`sonnet` is Sonnet 4.5 on
Amazon Bedrock, Sonnet 4.6 on Claude Platform on AWS), so an agent pinned to an alias behaves
differently on a gateway than it does locally. That is a reason to state the alias and not a full
model ID: the alias degrades to whatever that provider has, a hardcoded ID fails outright.

**Effort levels** are `low`, `medium`, `high`, `xhigh`, `max`, available on Fable 5.x, Opus 5,
Sonnet 5, Opus 4.8 and Opus 4.7; Opus 4.6 and Sonnet 4.6 have no `xhigh`. The default is `high`.
`xhigh` buys deeper reasoning for more tokens, and `max` is documented as prone to overthinking —
so it is a thing to test on a case, not a default to reach for. `effort:` is a frontmatter field on
both skills and agents, and `/effort` sets it for a session.

The consequence for this repo: **a hard-to-undo verdict is an effort decision before it is a model
decision.** Moving a reader from Sonnet to Opus multiplies its cost on every diff it ever reads;
leaving it on Sonnet and giving the four agents whose verdict blocks a merge an explicit
`effort: xhigh` buys the depth where the cost of being wrong actually sits.

**Subagent model resolution**, in order (v2.1.251+): the per-invocation `model` parameter, then the
agent file's `model:`, then `CLAUDE_CODE_SUBAGENT_MODEL`, then the main conversation's model.
`CLAUDE_CODE_SUBAGENT_MODEL_FORCE` overrides all of it, which is worth knowing before debugging why
`galadriel` came back on Sonnet.

## 2. Skill frontmatter

The template in `CONVENTIONS.md` uses `name` and `description` because those were the only fields
that existed when it was written. The rest of the list is now load-bearing, and four of these
fields do jobs our blocks currently do in prose:

| Field | What it does | Where it matters here |
|---|---|---|
| `name`, `description` | routing; `description` + `when_to_use` are truncated at 1,536 characters in the listing | the sizing rule in `README.md` is a platform limit, not a style preference |
| `when_to_use` | trigger phrases appended to `description` in the listing | our `## When` section duplicates this; keep the section, it is what the invoked block reads |
| `allowed-tools` | pre-approves tools for the turn that invoked the skill; clears on the next user message | a block that runs a gate command no longer needs the operator to approve each one |
| `disallowed-tools` | removes tools from the pool while the skill is active | the documented use is exactly ours: deny `AskUserQuestion` in an autonomous loop |
| `disable-model-invocation` | `true` keeps the description out of context and makes the block operator-only | the right setting for a destructive step; also blocks preloading and scheduled firing |
| `user-invocable` | `false` hides it from the `/` menu; Claude-only background knowledge | the convention blocks are closer to this than to a command |
| `model`, `effort` | override for the rest of the turn, not saved to settings | `choose-model` applies to a skill invocation, not only to an agent |
| `context: fork` + `agent:` + `background:` | runs the skill in a subagent (background by default; `background: false` waits) | this is the native version of "hand this step to an agent", and it inverts the `skills:` field below |
| `paths` | globs that gate automatic activation | the per-stack convention blocks are the textbook case: a `.vue` file should not load the Laravel block |
| `hooks` | hooks registered on invocation, kept for the session | `skills/gate` wires its hook pair by hand today |
| `arguments`, `argument-hint` | named positional arguments and autocomplete hint | |
| `metadata` | free-form map for our own tooling; Claude Code does not act on it | where a maturity or catalogue field could live machine-readably |
| `shell` | `bash` (default) or `powershell` for inline command blocks | |
| `license`, `compatibility` | spec fields, accepted and not acted on | |

Only `name`, `description`, `license`, `compatibility`, `metadata` and `allowed-tools` are portable
outside Claude Code; the rest break an upload to claude.ai. That matters for rule C: the day
`mentis/` is extracted publicly, a block leaning on `paths` or `context: fork` is Claude Code-only,
and that is a deliberate choice to record rather than discover.

Skill precedence: enterprise, then personal (`~/.claude/skills/`), then project
(`.claude/skills/`), then plugin and nested, then bundled. A skill at any level overrides a bundled
skill of the same name. Plugin skills are namespaced `plugin:skill`, which is why nothing here
collides with an installed catalogue.

## 3. Agent frontmatter

Every agent in `agents/` carries `name`, `description`, `model` and nothing else. These are the
fields it could carry, and the first two are the ones that turn a stated prohibition into an
enforced one:

| Field | What it does |
|---|---|
| `tools` | allowlist; inherits everything available to subagents when omitted |
| `disallowedTools` | denylist, subtracted from the inherited or declared list |
| `model`, `effort` | per §1 |
| `permissionMode` | `default`/`manual`, `acceptEdits`, `auto`, `dontAsk`, `bypassPermissions`, `plan` |
| `maxTurns` | hard stop; the output comes back marked partial and is resumable |
| `skills` | skills preloaded whole into the agent's context at startup, not just their description |
| `memory` | `user`, `project` or `local`; a real memory directory with `MEMORY.md` auto-loaded |
| `isolation: worktree` | the agent runs in a throwaway git worktree, branched from the default branch, cleaned up if it changed nothing |
| `background` | `true` keeps it in the background even when the caller wants the result inline |
| `mcpServers`, `hooks` | per-agent wiring; both ignored for plugin-scoped agents |
| `color`, `initialPrompt`, `experimental.cacheTtl` | display, `--agent` entry prompt, 5m/1h prompt cache |

Four of these change how this repo should be written, not just what it can say:

**`disallowedTools` is the mechanism the naming convention was missing.** The Lord of the
Rings/Matrix split in `CONVENTIONS.md` commits an agent's tool scope — a LOTR name means it only
watches. That was prose in twelve files and a runtime that granted Write anyway. It maps onto the
field directly, with one nuance worth keeping: *"never Write/Edit on the repo under review"* is
path-scoped, and the field is not. The eight readers legitimately write their payload file inside
the scratch directory, so they deny `Edit`, `NotebookEdit` and `Agent` and keep `Write` with the
path rule still stated in prose. The auditors that write nothing at all deny `Write` too, and for
them the guarantee is now enforced rather than declared.

**`memory` replaces pillar 2 for any agent that needs one.** Pillar 2 (MEMORY) says what persists
between two invocations; on every agent here the honest answer is "nothing, the artefact is re-read
cold", which is the fresh-context guarantee and must stay that way for the readers and the gate.
Where an agent would genuinely benefit from cross-session learning, the field is the way to get it,
and pillar 2 then names the scope instead of asserting amnesia.

**`isolation: worktree` overlaps step 0.** `start-feature` creates a worktree by hand because that
was the only way to isolate an implementer. For a single delegated agent the field does it, with
cleanup, and branches from the default branch rather than the caller's `HEAD`. It does not replace
step 0 — a human-driven feature still wants a worktree the operator can open, and `finish` still
owns the merge — but an audit or an experiment handed to one agent no longer needs one.

**`skills` and `context: fork` are inverses.** `skills:` on an agent preloads knowledge it needs
before it starts; `context: fork` on a skill sends a step to an agent. Preload when the skill is a
prerequisite, fork when it is the destination. A skill with `disable-model-invocation: true` cannot
be preloaded.

Agent precedence: managed settings, `--agents` flag, `.claude/agents/`, `~/.claude/agents/`, plugin
`agents/`. Names cannot contain `:`.

## 4. Delegation: subagents, forks, teams

**Fork mode is on by default in interactive sessions** since the week of 2026-08-10. Two
consequences: Claude can hand a side task to a subagent that inherits the whole conversation, and
the subagents it spawns run in the background rather than blocking the turn. Background subagents
get a reduced built-in tool set — `Read`, `Grep`, `Glob`, `Bash`, `PowerShell`, `Edit`, `Write`,
`NotebookEdit`, `WebFetch`, `WebSearch`, `TodoWrite`, `Skill`, `ToolSearch`, `EnterWorktree`,
`ExitWorktree`, `Monitor`, `TaskStop`, `SendMessage`, `Artifact` — and lose the rest. An agent whose
loop depends on a tool outside that list needs `background` handled deliberately, not assumed.

**Limits worth knowing before designing a fan-out**: 20 concurrent subagents by default
(`CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`), and a spawn depth of 3 below the main conversation
(`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`). At the depth limit the `Agent` tool is withheld. That is
the mechanical reason a chain like operator → `gandalf` → `elrond` → reader is the last layer that
can itself delegate, and it is why `elrond`'s contract forbidding a further fan-out is a design
choice rather than a limitation.

**`SendMessage` resumes a completed subagent** with its context intact, addressed by name or agent
ID; a fresh `Agent` call starts over. Built-in `Explore` and `Plan` return no ID and are one-shot.
Since v2.1.199 a message from another agent is delivered as task direction and explicitly cannot
approve a permission prompt or change the recipient's configuration — an approval relayed by an
agent is untrusted input, not consent. Both properties matter for our review flow: a reader can be
re-asked about one finding instead of re-reading the whole dump, and a reader cannot be talked into
posting by a sibling.

**Agent teams** are a separate, experimental mechanism, off unless
`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`. Teammates are full independent sessions with a shared
task list and direct messaging, they cost significantly more than subagents, and — the part that
surprises people — with teams enabled, *any* subagent Claude names launches as a teammate, so a
team can form during ordinary delegation. Teammates cannot nest, cannot be promoted to lead, and
in-process teammates do not survive `/resume`. For this repo's fan-outs, subagents are the right
tool; teams earn their cost only where the workers need to argue with each other, which is the
competing-hypotheses shape, not the per-stack review shape.

**Cross-session messaging** (macOS and Linux) lets separate sessions pass findings without a team,
and `@` in the prompt mentions another session by name.

## 5. Loops and scheduling

Four distinct mechanisms, and picking the wrong one is the usual mistake:

| Mechanism | Shape | Use it when |
|---|---|---|
| `/goal` | keeps working turn after turn until a completion condition holds | the exit is a verdict — this is the step 6→7 loop in `WORKFLOW.md` |
| `/loop` | re-runs a prompt on an interval, or self-paced | the exit is external and has to be polled |
| `Monitor` tool | streams a background script's output lines into the conversation | there is something to tail; it replaces polling entirely |
| Routines / Desktop scheduled tasks | durable, outside any session | the work must run without the session open |

**`/loop` in detail.** With an interval and a prompt (`/loop 5m check the deploy`) it becomes a
cron job. With a prompt and no interval it self-paces: after each iteration Claude picks a delay
between one minute and one hour and prints it with its reason. With neither, it runs a built-in
maintenance prompt — finish unfinished work, tend the branch's PR, then cleanup passes — or
`.claude/loop.md` / `~/.claude/loop.md` if one exists, project file winning, edits taking effect on
the next iteration, truncated past 25,000 bytes. A skill can be the prompt (`/loop 20m /review-pr
1234`), but a scheduled fire only runs skills Claude may invoke itself: anything with
`disable-model-invocation: true`, a built-in command, or a `Skill` deny rule arrives as plain text
instead of executing.

Three properties that bite: **recurring tasks expire 7 days after creation**, firing one last time
before deleting themselves; the scheduler adds **deterministic jitter** (up to 30 minutes for a
recurring task, or half the interval below hourly — so pick minute `3` over minute `0` when timing
matters); and there is **no catch-up** for a fire missed while Claude was busy. Tasks are
session-scoped, restored by `--resume` if unexpired, and cleared by a fresh conversation. A session
holds at most 50. `Esc` clears a pending self-paced wakeup; `CronCreate`, `CronList`, `CronDelete`
are the underlying tools, and `CLAUDE_CODE_DISABLE_CRON=1` removes the whole thing.

The rule for this repo: **a loop whose exit condition is a verdict we produce is `/goal`, a loop
whose exit condition is somebody else's state is `/loop`, and a loop that exists to watch a stream
is `Monitor`.** The gate already states the first. What was missing is the third — `Monitor` is
strictly better than polling a log with `/loop`, both in tokens and in latency, and no block here
named it. And a daemon that must outlive the session is neither: it is a routine, a Desktop
scheduled task, or plain cron, which is the honest reason the `claude-mem` keepalive in
`CATALOG.md` is a cron entry and not a native loop.

## 6. Native blocks not to reimplement

`/code-review` (effort-scaled, runs as a background subagent, `--comment` posts inline, `--fix`
applies), `/security-review`, `/simplify`, `/doctor` (alias `/checkup`), `/model`, `/effort`,
`/fast`, `/usage`, `/rewind`, `/fork`, `/cd`, `/run`, `/verify`, `/loop`, `/goal`, `/schedule`,
hooks, auto memory, checkpointing, worktrees, artifacts, `claude ultrareview`, and dynamic
workflows via the `Workflow` tool. Two of these are direct competition for blocks in this repo and
the answer is not the same in both cases:

- **`/simplify` and `skills/simplify`**: the native one applies quality fixes to the changed code,
  ours is the step-9 slot in the pipeline plus `over-engineering-review`'s deletion angle. Ours
  invokes, it does not duplicate — and that is already what its `Steps` say.
- **`claude plugin eval` and `skills/testing-blocks`**: the platform now runs scored eval cases
  against a plugin or a skills directory, with a no-plugin baseline arm. `testing-blocks` asks for
  proof that a block changes behaviour under pressure and offers a manual protocol for it. The eval
  runner is that proof, mechanised, and `testing-blocks` should be pointing at it rather than
  describing a hand-rolled A/B. That is a real gap, recorded here and in `CATALOG.md` §2 rather
  than closed in the same pass.

## Origin

Not an idea taken from outside: this is a stamped read of the platform's own documentation, which
is what `skills/source-freshness` §3 asks for in place of refreshing from memory. Read 2026-09-07
from `code.claude.com/docs` — `skills`, `sub-agents`, `scheduled-tasks`, `agent-teams`,
`model-config`, and the weekly digests for weeks 32 to 34 of 2026 (August 3–21). Version numbers
are quoted where the documentation quotes one; where it does not, the fact is stated without a
version and expires with this file.

The reason it exists as a reference rather than as additions inside each block: every block that
touches delegation, model choice or looping was about to repeat the same facts, and the eight
readers already taught this repo once that a mechanism explained in eight places drifts in seven of
them.
