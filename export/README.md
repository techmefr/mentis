# export

Pilot of the rule exporter (`bin/export_rules.py`): it renders chosen blocks into the formats other
coding agents read, so the blocks stay harness-neutral and only this edge knows about a harness.

| File | Role |
|---|---|
| `manifest.json` | The blocks to export, with the globs a Cursor rule applies to, and `"references": "inline"` for blocks whose rules live in `references/` |
| `golden/agents-md/AGENTS.md` | What the `agents-md` target renders today |
| `golden/cursor/.cursor/rules/*.mdc` | What the `cursor` target renders today |

```bash
python3 bin/export_rules.py --target agents-md --out ./some-project
python3 bin/export_rules.py --target cursor --out ./some-project
python3 bin/export_rules.py --check          # what pre-push runs, through bin/test_export_rules.py
python3 bin/export_rules.py --write-golden   # after a deliberate change to a block or the manifest
```

## What it does and does not do

- Drops the frontmatter, keeps `description` as the "when" line, replaces the `# title` with a section
  heading, demotes the other headings one level.
- Does not rewrite links. Anything that would dangle outside this repo (other blocks, `WORKFLOW.md`, a
  `references/` file that was not inlined) is listed on stderr.
- Depends on nothing: this repo installs nothing to test itself.

## Limits of the pilot

- 🟡 Never run in a real Cursor or any other tool. Checked against the docs on 2026-10-20 only: Cursor
  rules (`.cursor/rules/*.mdc`, `description` string, `globs` comma-separated string, `alwaysApply`
  boolean, rules under 500 lines, `AGENTS.md` at the root and in subfolders) and the agents.md site
  (plain Markdown, no required fields, nearest file wins). A block with inlined references is split into
  one rule per part to stay under 500 lines.
- Open and unverified: `globs: **/*.vue` is unquoted and starts with `*`, which a strict YAML parser reads
  as an alias; the Cursor docs show globs unquoted, so we follow them. The docs say nothing on `.cursorrules`.
- `AGENTS.md` is one 870-line file; the spec sets no limit, but an agent reads it in full each session.
- Targets are Cursor and `AGENTS.md` only; Windsurf, Copilot, Gemini CLI and Aider are not claimed. The
  agents.md site lists them as readers of `AGENTS.md` (Aider and Gemini CLI need a config line to do so).
- Two blocks and two targets. A third target, and more blocks, come only after these two have been used
  on a real project.
- The pilot blocks mention other blocks (`laravel-conventions`, `WORKFLOW.md`, rule A): an exported rule
  carries those mentions as plain text. Whether to rewrite them is open.
- Personal-repo tool: it is not part of any employer's workflow.
