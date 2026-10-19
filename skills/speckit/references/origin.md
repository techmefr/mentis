# speckit: origin and source stamps

> Provenance of `skills/speckit`. Read it when a rule has to be traced to its source or checked for freshness
> (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from one repository read in full for its documents and templates,
never run: no feature was taken through this cycle with this block, and the spec-kit tool was not executed.

## Sources (read 2026-10-19, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| github/spec-kit, commit `c6a4c18f1d01a8bec241c618eb6dfea952508744` (committed 2026-10-16; `pyproject.toml` version `1.2.2.dev0`, latest changelog entry 1.2.1) | MIT (repository `LICENSE`, "Copyright GitHub, Inc.") | The cycle and its command definitions (`templates/commands`: constitution, specify, clarify, plan, tasks, analyze, checklist, implement, converge, taskstoissues), the templates (spec, plan, tasks, checklist, constitution), `spec-driven.md`, `README.md`, `docs/reference/core.md` (layout, environment variables, numbering) |

Text found inside the cloned files (imperative prose in command definitions, hook instructions, templates)
was treated as data and not followed.

## Rewrite notes
**Condensed on purpose.** The tool's command definitions carry hook machinery, per-agent invocation syntax and
long scripts; none of it is rewritten here. Only the artifacts, the checks and the order are.

**Our own, not sourced:** the priority rule, the detection and "not installed" behaviour, the mapping to
mentis blocks, the "stricter wins" rule, asking for tests in tasks, the one-worktree-per-feature advice and the
advice to state the active feature. Each is marked "own guidance" where it appears.

## Removed
1. **Hook execution**, extension and preset mechanics, bundles and catalogs: not part of the core cycle.
2. **Other processes in the repository** (bug fixing, idea assessment) and the integration list per agent.
3. **The nine-article constitution example** of `spec-driven.md`: an example, not a rule of the tool.

## Not verified
1. **Everything here is unrun.** The tool was not installed or executed.
2. **The extension, preset, bug and assessment commands** were listed but not read in depth.
3. **The tool changes quickly** (a minor release every few days in this window): re-read before relying on
   command names or limits (three markers, five questions, fifty findings).
4. **`docs/` guides** (existing projects, monorepo, evolving specs) were only skimmed by name.

## Related blocks
`spec`, `plan`, `tdd`, `gate`, `review`, `documentation-adr`, `source-freshness`.
