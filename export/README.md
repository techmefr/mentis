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

- 🟡 Never run against the tools. The Cursor `globs` spelling (a comma-separated string) is our reading of
  the format, not something we exercised.
- Two blocks and two targets. A third target, and more blocks, come only after these two have been used
  on a real project.
- The pilot blocks mention other blocks (`laravel-conventions`, `WORKFLOW.md`, rule A): an exported rule
  carries those mentions as plain text. Whether to rewrite them is open.
- Personal-repo tool: it is not part of any employer's workflow.
