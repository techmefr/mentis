# agent-sandbox-egress-pitfalls: origin and source stamps

> Provenance of `skills/agent-sandbox-egress-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from repository documentation, never run by us. No sandbox was started, no config was
tested and no denied operation was observed. A verification pass on 2026-10-15 re-read both sources below in
full and corrected the references against them.

## Sources (re-read in full in the verification pass, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| anthropics/sandbox-runtime, `README.md`, all 1077 lines (commit 9a277e5) | Apache-2.0 (LICENSE file) | Dual isolation, read and write rule shapes and precedence, config traps, network allowlist, resolved-address check, proxy routing per platform, escalation risks, mandatory deny paths, weaker modes |
| huggingface/smolagents, `docs/source/en/tutorials/secure_code_execution.md`, all lines (commit 96f33fa) | Apache-2.0 (LICENSE file) | Model-written code risks, local executor limits, two sandbox approaches and their trade-offs, best practices |

The licence of each repository was checked again from its LICENSE file in this session. `building_good_agents.md`
from the same repository was read earlier but no rule here rests on it, so it is not listed as a source.

## Corrected in the verification pass
- "Filesystem isolation alone lets the agent change its own limits" was not in the README; replaced by its
  actual statement (exfiltration without file isolation, unrestricted network without network isolation).
- Proxy-variable section: the README says tools that ignore the variables fail to connect, not that they
  bypass the sandbox; per-platform mechanisms and external-proxy behaviour added; "raw sockets may not go through
  the proxy" corrected (SOCKS5 handles other TCP).
- "Allow narrow methods where the proxy supports it" was unsupported and was removed.
- Escalation: "launcher script" and "flag that disables the sandbox per command" were not in the README and were
  removed; the README's actual relaxations (weaker nested sandbox, weaker network isolation, Apple Events) and
  the project-local-config warning were added.
- Generated code: the "wildcard defeats the filter" claim was reversed against the guide (wildcards are
  supported); the step-limit claim now reflects the operation cap and the guide's timeout advice; the
  keys-in-reach reasoning now follows the guide's two-approach trade-off.

## Rewrite notes
Numeric defaults (search depth, proxy port range, caps) are not quoted; the block points to the README.

**Decisions where sources disagree:** none found.

## Not verified
1. **Nothing was executed**; every behaviour is as documented at the commits above.
2. **Windows (alpha) details and the TLS-termination section** were read but not turned into rules.
3. **Own guidance, not sourced:** sentences marked "own guidance", the mirror suggestion, the scoped-credential
   suggestion, the untrusted-output advice and the checkpoint paragraph.
4. **Removed as unverifiable:** rules about any sandbox product not read in full.

## Related blocks
`agent-mcp-trust-pitfalls`, `agent-hook-guard-pitfalls`, `ci-workflow-hardening`, `security-hardening`,
`credential-lifecycle-pitfalls`.

## Section 2.4, added 2026-10-20
One source, licence file read the same day: `anthropics/claude-quickstarts`, `managed-agents/daily-brief` and
`managed-agents/sentry` agent definitions (MIT, root LICENSE, copyright 2023 Anthropic). It gave the statement that
vendor-run web tools sit outside the sandbox allowlist and the practice of disabling them for jobs that read
untrusted text. Not verified: that claim is the sample's own comment, not checked against the platform's current
documentation, and nothing was run.
