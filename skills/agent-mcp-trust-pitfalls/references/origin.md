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
| MCP specification site, revision 2026-07-28: authorisation, tools and security-best-practices pages (re-read 2026-10-20); RFC 5737 | Specification site content from the repository in the first row (same mixed licence), RFC from the IETF; facts only | Audience validation and resource parameter, tool annotations untrusted, human in the loop, show inputs before calls, validate results, stdio proxy escalation, localhost redirect impersonation, trust policies, consent cookie and state rules re-confirmed, documentation address blocks |
| OpenAI: MCP and connectors guide (risks and safety, approvals) | Product documentation, facts only, read 2026-10-20 | Trusted servers, official over aggregator, approvals by default, logging, URLs in outputs, tool behaviour changing |

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

## Re-checked 2026-10-20
- Against the specification pages: consent registry, consent page, cookie attributes, exact redirect match, state single use and ten-minute example, encoding tricks in IP checks, egress proxy, scheme validation, scope elevation logging, one-click command shown without truncation.
- Newly sourced: stdio proxy escalation (§1.1.7), annotations untrusted (§1.2.5), list-changed notification (§1.2.4), audience rule (§2.2.2), documentation address blocks (§2.4.2), localhost redirect and trust policies (§2.4.4), human approval and result validation (§3.2), URLs in tool output (§3.2.4), vendor approvals and official-server rule (§1.3.5, §3.2.2).

## Rewrite notes
No numeric threshold is quoted. Agent-scan v0.5 issue codes and v0.6 risk names are both used and labelled by
version.

**Decisions where sources disagree:** none found.

## Not verified
1. **Scanner behaviour** was read from documentation, not run.
2. **The protocol revision** read is dated 2026-07-28; other revisions were not checked.
3. **Own guidance, still unsourced:** invisible-character stripping (§1.2.3), diff before auto-update (§1.3.2), scan
   after every update (§1.3.4), the split-sessions suggestion (§3.2.1), saying so in the task (§3.3.4), alerting on
   elevation (§2.3.3), the audience-mismatch test and the separate downstream token (§2.2.2). Searched: the protocol
   specification pages, RFC 8707 context, OpenAI and Anthropic documentation; no source states these.
4. **Removed:** "permission inventory per agent" and all numbering from a third-party security playbook (its
   mixed share-alike content was not used; only its LICENSE and notices were read earlier).

## Related blocks
`agent-sandbox-egress-pitfalls`, `mcp-server-design-pitfalls`, `oauth-oidc-client-pitfalls`,
`security-hardening`, `secret-leak-response-pitfalls`, `credential-lifecycle-pitfalls`.

Independent verification 2026-10-21: 28 checked, 28 matched, 0 corrected, 0 unverified
