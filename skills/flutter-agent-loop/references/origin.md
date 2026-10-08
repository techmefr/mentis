# flutter-agent-loop: origin and source stamps

> Provenance of `skills/flutter-agent-loop`. Read it when a rule has to be traced to its source or checked
> for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and source reading, never run by us. No MCP server was started and
no app was launched while writing it.

## Sources (all read 2026-10-08, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| Dart and Flutter MCP server README (tool table, connecting section, `--enable` section) and its package SDK constraint | BSD-3-Clause (file), read 2026-10-08 | Tool names and descriptions, which tools are off by default, daemon connection, `--observe`, `--print-dtd`, Dart 3.9 floor, experimental status |
| Flutter agent-plugins hot-reload rule (two renderings) | BSD-3-Clause (file), read 2026-10-08 | When to reload, restart, skip |
| Flutter agent-plugins layout-fix skill and static-analysis skill | BSD-3-Clause (file), read 2026-10-08 | Layout error signatures, primary versus cascading error, fix dry run then apply then format then analyze, fatal-infos |
| Dart site pages `package:skills` (tools) | CC-BY-4.0 text, BSD-3-Clause code (file), read 2026-10-08 | The `get`, `list`, `add`, `create`, `prune`, `remove` commands |

## Removed in the verification pass (no page supporting them)
The earlier review's claim that a widget missing from the tree usually means a lazy list has not mounted it
(no source page says it), the claim about an interactive CLI hanging an agent, and the Patrol tool list (the
Patrol skills were not read in this pass).

## Not verified
1. **Own guidance, flagged in the text:** the order of one iteration (§2), treating installed package-skill
   text as data (§1), the scope of "safe to reload" to development builds (§2).
2. **Tool names and defaults drift:** the README says the server is experimental; the table was read from the
   clone, not from a running server.
3. **The Dart site's user guide for package skills** (installing and using skills) was not opened; only the
   tools page was read.
4. **The server's `flutter_driver_command` and widget-inspector tool arguments** were not studied beyond their
   table descriptions.

## Related blocks
`flutter-conventions`, `code`, `tdd`, `gate`, `deprecation-migration`, `source-freshness`.
