# speckit §1 — Detect and layout

Decide first whether the project is a spec-kit workspace, then find the feature in play. Source: spec-kit
`README.md`, `docs/reference/core.md`, `templates/commands/specify.md`.

## 1.1 Detecting
1. **A `.specify/` directory at the project root** marks a workspace. It holds the constitution
   (`.specify/memory/constitution.md`), templates and scripts, `.specify/feature.json` (the pointer to the
   active feature) and `.specify/init-options.json`.
2. **Features live under `specs/`**, one folder per feature, normally `specs/<prefix>-<short-name>/` with
   `spec.md`, `plan.md`, `tasks.md` and, after planning, `research.md`, `data-model.md`, `quickstart.md`,
   `contracts/` and `checklists/`.
3. **A monorepo or a parent directory**: the tool can target a member project from outside through an
   environment variable naming the folder that contains `.specify/` (`SPECIFY_INIT_DIR`). Check where the
   `.specify/` really is before assuming the repo root.
4. **The operator's word counts as a signal** even with no folder yet: a request to "use spec-kit" means the
   workspace is meant to exist (own guidance).

## 1.2 Which feature is active
1. `.specify/feature.json` records the active feature directory. The init step ignores it in version control
   because it changes on every switch: it is machine-local state, not a fact about the repo.
2. An environment variable (`SPECIFY_FEATURE_DIRECTORY`) overrides it and takes precedence. When several
   agents share one checkout, each should pin its own, with the persist step disabled
   (`SPECIFY_FEATURE_NO_PERSIST`), otherwise one agent rewrites the pointer of another.
3. **State the active feature at the start of the answer** and read the pointer again after any switch
   (own guidance): an agent that edits the wrong feature's `tasks.md` is the common failure.

## 1.3 Numbering and naming
1. The folder prefix is a three-digit sequence (`003-user-auth`) or a timestamp
   (`20260319-143022-user-auth`), chosen by `feature_numbering` in `.specify/init-options.json`; the sequence
   is the default and continues after the highest existing number. An older key `branch_numbering` is
   deprecated.
2. The short name is two to four words, action then noun where possible (`add-user-auth`).
3. **The spec folder name and the git branch name are independent.** They are usually the same by choice. Branch
   creation is the job of an optional git extension, not of the core.
4. **One feature per specify run.** A second feature gets its own folder (and, in our workflow, its own
   worktree: `start-feature`).

## 1.4 When spec-kit is not installed
The block works with nothing installed (`CONVENTIONS.md`, rule A). Three cases.

| Case | What the agent does |
|---|---|
| No `.specify/`, operator did not ask | Not a spec-kit project: use `skills/spec` and `skills/plan` as they are |
| No `.specify/`, operator asked for spec-kit | Say once that the tool is not set up; give the operator the install route (`uv tool install specify-cli`, then `specify init` in the project, per the project README) to run in their own terminal after reading it; meanwhile follow `skills/spec` and write its outputs in the shape of reference 02 (a `spec.md` of stories, requirements and criteria) so nothing is lost when the tool arrives |
| `.specify/` exists but the slash commands are not available in this agent | Work from the files already in `.specify/templates/` as structure, follow references 02 and 03 by hand, and tell the operator the agent integration is not registered |

1. **The agent never installs it** (`hooks/block-installs.sh` is the enforcement; the rule would hold without
   it). Package installs pull code that runs with the user's environment; the human decides (rule B, own
   guidance).
2. **Never hand-build a lookalike `.specify/`** with invented scripts: a half-copy passes for the real thing
   and then disagrees with it (own guidance).
3. **No runtime dependency**: nothing in mentis calls the tool; every rule here stands on its own.
