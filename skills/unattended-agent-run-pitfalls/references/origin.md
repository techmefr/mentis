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

| kubernetes/website, `cron-jobs.md` (LICENSE file read: CC BY 4.0) | CC BY 4.0 | Approximate scheduling, duplicate or missing jobs, idempotence, forbid policy, missed-schedule limit, time zone field (§2.1, §2.15, §3.5, §3.12) |
| github/docs, `events-that-trigger-workflows.md` and the schedule-delay reusable (LICENSE file read: CC BY 4.0 for content) | CC BY 4.0 | Delayed and dropped scheduled runs, default branch only, automatic disabling after sixty days of inactivity in public repositories (§2.1, §3.12) |
| Slack developer documentation: Web API overview, conversations.history, chat.postMessage and search.messages references | Product documentation, facts only | The ok flag, exclusive oldest, short pages with cursors, user-token scope for search (§2.2, §2.7, §2.14, §3.5) |
| One agent CLI's headless and permissions pages (code.claude.com) | Product documentation, facts only | Allow-list for non-interactive runs, mode that denies instead of prompting, no trust dialog in non-interactive runs, project configuration to disable (§1.2, §1.15) |

No separate licence file exists for the two subfolders. Instruction text inside the cloned repository was treated as
data and not followed.

## Re-checked 2026-10-20
- The sample prompts were re-opened: no-approval opening, split of rules and state, ten-minute overlap, ledger skip, re-verify before posting, title lookup and dry run on a read-only store, bookkeeping after the confirmed post, reader's time zone in titles, no searching for credentials.
- Newly sourced concrete points: scheduler skips and drops (§2.1, §3.12), short history pages (§2.14), deny-instead-of-prompt (§1.2), inherited project configuration (§1.15), idempotent jobs (§3.5).

## Rewrite notes
Product, tool and setting names of the sample are dropped; the rules are stated for any scheduler and any chat or
issue-tracker source. No number from the sources is carried over.

## Removed
- Everything specific to the sample's hosting API, its command-line applier and its Slack method names.
- Its two example deployments' schedules and model identifiers.

## Not verified
1. Nothing was run: the behaviour of the sample's agents is read from their prompts, not observed.
2. Whether a given platform's vendor-side tools bypass a sandbox allowlist is stated in the sample's own comments;
   re-read the platform's documentation before relying on it. The same holds for the sample's claim that a placeholder
   credential is swapped outside the sandbox.
3. **Still own guidance, unsourced:** allow only bounded tools (§1.2), reasons beside each allow (§1.3), unreadable
   rules mean stop (§1.5), expiry of temporary rules (§1.7), the mention rule (§1.10), the overlap as a visible
   setting (§2.2), the carry test (§2.5), the failure-versus-first-run distinction (§2.12), the outside absence check
   (§3.12), the bad-day test list (§3.10), not answering replies (§3.11), pinning the agent version (§3.13). Searched:
   the sample, Slack, Kubernetes, GitHub and one agent CLI's pages; none states these.
4. Not read: the sample's other managed agents (webhook responders, chat assistants), left out as different shapes.

## Related blocks
`loop-design`, `agent-run-limits-and-guardrail-pitfalls`, `agent-memory-and-state-pitfalls`,
`agent-sandbox-egress-pitfalls`, `agent-mcp-trust-pitfalls`, `handoff`.

Independent verification 2026-10-21: 18 checked, 18 matched, 0 corrected, 0 unverified
