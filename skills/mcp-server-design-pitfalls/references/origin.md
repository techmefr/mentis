# mcp-server-design-pitfalls: origin and source stamps

> Provenance of `skills/mcp-server-design-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from repository documentation, never run by us. No server was built or called. A
verification pass on 2026-10-15 re-read every source below in full and corrected the references against it.

## Sources (re-read in full in the verification pass, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| modelcontextprotocol/modelcontextprotocol, `docs/specification/2026-07-28/server/tools.mdx` (commit 86f6e0c) | LICENSE file states a transition from MIT to Apache-2.0 with a per-contribution mix; attribution and idea-level facts only | Name rules, annotations untrusted, list varies by authorisation not connection, deterministic order, structured content plus text, output schema, stateful-handle guidance, two error channels, security section |
| PrefectHQ/fastmcp, `docs/servers/tools.mdx`, `tool-fingerprinting.mdx`, `transforms/tool-search.mdx` (commit e2fcc41) | Apache-2.0 (LICENSE file) | Timeouts and side effects, error masking, visibility and allowlist mode, fingerprint recipe and CI manifest, tool search, duplicate policy, list-changed notifications |
| github/github-mcp-server, `docs/scope-filtering.md`, `tool-renaming.md`, `server-configuration.md` (commit 796afb7) | MIT (LICENSE file) | Read-only and exclude precedence, lockdown mode limits, scope filtering for classic tokens and its fail-open behaviour, deprecation aliases |
| muratcankoylan/Agent-Skills-for-Context-Engineering, `skills/tool-design/SKILL.md` (commit 9ff0c99) | MIT (LICENSE file) | Description structure, namespacing, consolidation and its limit, actionable errors; every numeric threshold dropped |

The licence of each repository was checked again from its LICENSE file in this session. The tool-design skill's
references and its claim IDs were not read; no rule rests on them.

## Corrected in the verification pass
- "A timeout may mean no default" was stated vaguely; now exactly as FastMCP says (opt-in, no server default,
  no undo of side effects, sync workers not interruptible, not applied to background tasks).
- Fingerprinting: FastMCP provides a recipe, not a built-in fingerprint that changes automatically; rewritten.
- Scope filtering: the GitHub server filters only for classic tokens, at start-up, and fails open on error by
  design; the earlier text implied a decision to test and has been replaced by the real behaviour plus own
  guidance.
- Visibility: the protocol's rule (list varies by authorisation, not by connection) added; the earlier
  "decide per caller from identity" sentence was ours and is now labelled.
- "One tool, one purpose" was softened to the skill's consolidation principle and its over-consolidation
  warning; the 1-128 character name rule and the aggregation advice were added.
- Added the protocol's stateful-handle guidance, the security section's MUSTs and the lockdown-mode caveat.
- "Announce a removal before it happens" is now labelled own guidance; the alias lifetime is not claimed to
  come from GitHub.

## Rewrite notes
No numeric threshold from the tool-design skill (parameter counts) is quoted. FastMCP's experimental
model-based search is mentioned only for its warning about descriptions.

**Decisions where sources disagree:** none found.

## Not verified
1. **Nothing was run**; behaviour of each project is as documented at the commit read.
2. **Own guidance, not sourced:** sentences marked "own guidance", the existence-leak note, the idempotency
   advice, additive schema changes, the alias-lifetime and prefix suggestions, and the checkpoint paragraph.
3. **Removed:** any limit on tool count or description length from the tool-design skill.

## Related blocks
`agent-mcp-trust-pitfalls`, `agent-sandbox-egress-pitfalls`, `api-design`, `security-hardening`,
`laravel-idempotent-jobs`.
