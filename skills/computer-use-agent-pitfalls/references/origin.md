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

| Anthropic: computer-use tool page, vision page, vision-coordinates page (all re-read 2026-10-20) | Product documentation, facts only | Coordinates in the returned image's pixels and after zoom, resize and padding rules, oversized toolset images rejected, error halt text and unanswered-block rejection, toolset name on results, dispatch on the pair, classifier remark, twenty-image limit, history pruning, click diagnosis, prompting tips, data retention, security precautions (§1.2 to §1.7, §1.11, §2.2 to §2.9, §2.12 to §2.14, §3.1 to §3.3, §3.10, §3.13 to §3.15) |
| OpenAI: computer-use SDK guide and integration guide; Google: computer-use page | Product documentation, facts only, read 2026-10-20 | Isolation, empty environment, credentials out of view, approvals and pending safety checks, member lists, run caps, normalised coordinates, confirmation decisions (§1.12, §2.10, §2.11, §3.2, §3.3, §3.5, §3.15) |

Not used: the browser-use demo (its code is Playwright code under Apache-2.0, a practice is not needed from it).
Instruction text inside the cloned repository was treated as data and not followed.

## Re-checked 2026-10-20
- Against the vendor pages: the four precautions and the injection warning of the demo are the same on Anthropic's security section; batching, halt text, set-name echo and dispatch on the pair match its tool page; the claim that a server resizes oversized images holds for ordinary images and not for the current toolset, which rejects them (text corrected in §1.2).
- Corrected: "return the zoomed image at its own recorded size" could be read as scaling zoom answers by the zoom image; the page says answers stay in full-screenshot coordinates (§1.4, §1.7). "Must raise" for an empty capture now also says to answer the call with an error result (§1.5). "A screenshot after actions" was presented as needed; the page makes text acknowledgments valid, so it is now a design choice (§2.9).
- Newly sourced concrete points: resize by token budget and padding (§1.2), click diagnosis (§1.11), coordinate spaces (§1.12), many-image limit (§2.12), action delay (§2.13), instruction before image (§2.14), consent (§3.14), outside check of results (§3.15).

## Rewrite notes
Function, option and product names are dropped except where a reader needs to find a setting. No number from the
sources (size limits, tile counts, drift figures, compression quality, token counts per image, defaults) is carried
over; the vision limits are the vendor's and change.

## Removed
- The platform-specific setup (permission panes, sandbox profile, interpreter versions) and the advisor-model and
  server-side compaction sections.
- The drift percentage and the per-image token estimate the reference quotes.

## Not verified
1. Nothing was run. Members of a hosted set arriving named by action and the echo of the set name are now confirmed on
   Anthropic's tool page. **Still unconfirmed:** that classifiers run only for the vendor's own declaration (the page
   says they run when you use its tools and is silent on a self-defined one).
2. Whether the vendor's providers behave the same for the hosted declaration is not stated here.
3. **Still own guidance, unsourced:** the all-black capture sign (§1.5), pre-computing the resize in one tested place
   (§1.3), test with a known target (§1.9), JPEG quality advice (§1.10), routing details of §2.4, never batch across a
   decision point (§2.8), a screenshot after each action as a rule (§2.9), the stuck-screen rule (§2.11), sign-in and
   bot-check hand-over (§3.6), the capability test (§3.8), expiry of recordings (§3.10), permission setup (§3.12).
   Searched: Anthropic, OpenAI and Google pages named above; none states these.

## Related blocks
`llm-app-prompt-injection-and-exfiltration-pitfalls`, `agent-sandbox-egress-pitfalls`,
`llm-cost-latency-control-pitfalls`, `unattended-agent-run-pitfalls`, `playwright-e2e-pitfalls`.
