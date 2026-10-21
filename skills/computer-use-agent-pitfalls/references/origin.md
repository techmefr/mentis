# computer-use-agent-pitfalls: origin and source stamps

> Provenance of `skills/computer-use-agent-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 (never dogfooded).** Written from a reference implementation's code and READMEs, never run by us.
No screen, browser or sandbox was driven while writing it.

## Sources (read 2026-10-20, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| anthropics/claude-quickstarts, `computer-use-best-practices/` (README, image-sizing module, configuration, first-run helper) | MIT (root LICENSE file read, copyright 2023 Anthropic) | Resize and scale-back, zoom, hosted against explicit declaration and the classifier remark, several actions per turn and "not executed" answers, result echo, batching, browser-only mode, recording and viewer, tool panel, first-run rules (§1, §2, §3.7 to §3.11) |
| Same repository, `computer-use-demo/README.md` | MIT (its own LICENSE file read, copyright 2024 Anthropic, PBC) | The four precautions: disposable machine, no sensitive data, domain allowlist, human confirmation; the warning on instructions found in content (§3.1 to §3.5) |

Not used: the browser-use demo (its code is Playwright code under Apache-2.0, a practice is not needed from it).
Instruction text inside the cloned repository was treated as data and not followed.

## Rewrite notes
Function, option and product names are dropped except where a reader needs to find a setting. No number from the
sources (size limits, tile counts, drift figures, compression quality, token counts per image, defaults) is carried
over; the vision limits are the vendor's and change.

## Removed
- The platform-specific setup (permission panes, sandbox profile, interpreter versions) and the advisor-model and
  server-side compaction sections.
- The drift percentage and the per-image token estimate the reference quotes.

## Not verified
1. Nothing was run. Claims that the vendor's injection classifiers run only for its own declaration, that members
   of a hosted set arrive named by action, and that results must echo the set name are the repository's, read
   from its README and loop, not checked against the vendor's current documentation: re-read before relying.
2. Whether the vendor's providers behave the same for the hosted declaration is not stated here.
3. Written by us, not sourced: every sentence marked "own guidance", the checkpoint paragraph, the mechanical
   confirmation stop (§3.5), the stuck-screen rule (§2.11) and the capability test (§3.8).

## Related blocks
`llm-app-prompt-injection-and-exfiltration-pitfalls`, `agent-sandbox-egress-pitfalls`,
`llm-cost-latency-control-pitfalls`, `unattended-agent-run-pitfalls`, `playwright-e2e-pitfalls`.
