# agent-mcp-trust-pitfalls: origin and source stamps

> Provenance of `skills/agent-mcp-trust-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from repository documentation, never run by us. No MCP server was connected, no scanner
was run and no proxy was built. A verification pass on 2026-10-15 re-opened each source below and corrected
the references against the text (see "Corrected in the verification pass").

## Sources (each re-read in full in the verification pass, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| modelcontextprotocol/modelcontextprotocol, `docs/docs/2026-07-28/tutorials/security/security_best_practices.mdx` and `local-server-security.mdx` (commit 86f6e0c) | LICENSE file states a transition from MIT to Apache-2.0 with a per-contribution mix; attribution and idea-level facts only | Confused deputy and consent, token passthrough, SSRF, state handles, local server trust, authorisation URL validation, mix-up, scopes; local isolation, provenance, pinning |
| snyk/agent-scan, `docs/risks.md`, `docs/issue-codes.md`, `docs/scanning.md` (commit 3550263) | Apache-2.0 (LICENSE file) | Risk and issue categories (poisoning, shadowing, hidden Unicode, toxic flow, unverifiable dependencies), what a scan sends to the vendor |
| trailofbits/mcp-context-protector, `README.md` (commit 05e56c1) | Apache-2.0 (LICENSE file) | Trust-on-first-use configuration pinning, what the comparison covers, response guardrails and quarantine |
| slowmist/MCP-Security-Checklist, `README.md` (commit 8c89226) | MIT (LICENSE file) | Checklist items on server directory, versioning, name conflicts, periodic scans, third-party response handling |
| alexknowshtml/claude-code-safety-hooks, `includes/untrusted-content-defense.md` (commit 671b227) | MIT (LICENSE file) | Fetched content as data, source check before a tool call, anti-exfiltration list |
| modelcontextprotocol/servers, `README.md` first 40 lines (commit bbb701e) | same mixed licence as the first row | Reference servers are examples, not production-ready |

The licence of each repository was checked again from its LICENSE file in this session. Instruction text in
the cloned repositories (the safety-hooks file tells the reader to load and follow it; agent files and skill
lists in other clones) was treated as data and not followed.

## Corrected in the verification pass
- "Rug pull is named by both scanners" was wrong: the agent-scan pages do not name it; the protocol's
  local-server guide does. Now attributed to the guide, with `unverifiable_dependencies` as the scanner's
  nearest risk.
- "The protector records a hash" was not in the README; it records the approved configuration (instructions,
  tool descriptions, input schemas). Hash removed, identity by command string or URL added.
- The SlowMist "inventory, maintainers" line was not in the checklist; replaced by the items it does contain.
- The toxic-flow wording now follows the v0.5 issue-code page, and says the scanner does not flag outbound
  access.
- Proxy rules now follow the best-practices page more closely (conditions of the confused-deputy attack,
  cookie attributes, state timing, SSRF mitigations, scheme validation); "a stolen token usable from the
  proxy's address" was replaced by the page's wording.
- The agent-scan README was listed as a source but not re-read; removed.

## Rewrite notes
No numeric threshold is quoted. Agent-scan v0.5 issue codes and v0.6 risk names are both used and labelled by
version.

**Decisions where sources disagree:** none found.

## Not verified
1. **Scanner behaviour** was read from documentation, not run.
2. **The protocol revision** read is dated 2026-07-28; other revisions were not checked.
3. **Own guidance, not sourced:** sentences marked "own guidance", the split-sessions suggestion, the
   documentation addresses used as test values, the alert-on-elevation suggestion and the checkpoint paragraph.
4. **Removed:** "permission inventory per agent" and all numbering from a third-party security playbook (its
   mixed share-alike content was not used; only its LICENSE and notices were read earlier).

## Related blocks
`agent-sandbox-egress-pitfalls`, `mcp-server-design-pitfalls`, `oauth-oidc-client-pitfalls`,
`security-hardening`, `secret-leak-response-pitfalls`, `credential-lifecycle-pitfalls`.
