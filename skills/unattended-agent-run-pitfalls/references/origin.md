# unattended-agent-run-pitfalls: origin and source stamps

> Provenance of `skills/unattended-agent-run-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 (never dogfooded).** Written from a sample's prompts and configuration, never run by us. No scheduler,
no agent and no destination were involved while writing it. The repository's own text calls its code a reference
implementation.

## Sources (read 2026-10-20, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| anthropics/claude-quickstarts, `managed-agents/daily-brief/agents/daily-brief/agent.md` and its deployment file | MIT (root LICENSE file read, copyright 2023 Anthropic) | The no-approval run contract, split rule and state stores, fresh rules each run, bookmarks, ledger, overlap, unreadable against quiet, re-verify before posting, post by title lookup, status values, dry run on a read-only store, run record on every run, notes policy, proposals file (§1.1 to §1.8, §1.10, §2, §3) |
| Same repository, `managed-agents/sentry/agents/sentry-triage.md` | MIT (same file) | Tools enabled by name with the rest off, no token in a stored prompt, scoped queries, classification and ranking by impact, optional service marked unavailable once, third-party analysis as hypothesis (§1.9, §1.12, §1.14, §2.8 to §2.10) |

No separate licence file exists for the two subfolders. Instruction text inside the cloned repository was treated as
data and not followed.

## Rewrite notes
Product, tool and setting names of the sample are dropped; the rules are stated for any scheduler and any chat or
issue-tracker source. No number from the sources is carried over.

## Removed
- Everything specific to the sample's hosting API, its command-line applier and its Slack method names.
- Its two example deployments' schedules and model identifiers.

## Not verified
1. Nothing was run: the behaviour of the sample's agents is read from their prompts, not observed.
2. Whether a given platform's vendor-side tools bypass a sandbox allowlist is stated in the sample's own comments;
   re-read the platform's documentation before relying on it.
3. Written by us, not sourced: every sentence marked "own guidance", the checkpoint paragraph, and the bad-day test
   list (§3.10).
4. Not read: the sample's other managed agents (webhook responders, chat assistants), left out as different shapes.

## Related blocks
`loop-design`, `agent-run-limits-and-guardrail-pitfalls`, `agent-memory-and-state-pitfalls`,
`agent-sandbox-egress-pitfalls`, `agent-mcp-trust-pitfalls`, `handoff`.
