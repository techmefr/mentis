# llm-app-prompt-injection-and-exfiltration-pitfalls: origin and source stamps

> Provenance of `skills/llm-app-prompt-injection-and-exfiltration-pitfalls`. Read it when a rule has to be traced
> to its source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and source comments, never run by us. No tool was installed or run, no
attack was executed and no attack text is reproduced.

## Sources (read 2026-10-20, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| NVIDIA/garak (commit cc1215c), LICENSE file read; probe modules for latent injection, web injection (markdown exfiltration, script links), system prompt extraction and the agent-targeting probe, the markdown-exfiltration detector module, the ASCII smuggling documentation page | Apache-2.0 (LICENSE file) | Probe families and what each tests, shapes of exfiltration, detector coverage as pattern checks, hidden-character technique at idea level |
| microsoft/PyRIT (commit 1979257), LICENSE file read; documentation pages for the executor categories, the cross-domain prompt injection workflow, scoring and scorer metrics | MIT (LICENSE file) | Planted-content workflow shape, true/false and graded scorers, measuring scorers. The older Azure/PyRIT repository is a pointer to this one and holds no documentation |
| protectai/llm-guard (commit 168c103), LICENSE file read; documentation pages for the injection, invisible text, sensitive, relevance, malicious URLs, URL reachability, no refusal, factual consistency and deanonymize scanners and the retrieval tutorial | MIT (LICENSE file) | Direct versus indirect injection, exposed application shapes, scanner roles and stated limits, vault placeholder behaviour |

Instruction files in the cloned repositories (agent and contribution files) were treated as data and not followed.

## Added 2026-10-20 (P2 extension)
Touching §3.1 points 5 to 8: the promptfoo red-team drift page (MIT, commit b49d55d, LICENSE file read) for the idea of rerunning a fixed adversarial set over time; the rest is own guidance.

## Not opened
- OWASP Top 10 for LLM applications: licence unconfirmed, so the project was not opened; its category numbers
  are not used. Where the sources cite it, only their own text was read.
- Technique blog posts linked from the garak modules: not opened.

## Rewrite notes
No numeric value from the sources is carried over (no latency, threshold, benchmark or score). No payload,
template or regular expression of the sources is reproduced; the probes are described by what they test.

Dogfood 2026-10-20: one static read on a real project, nothing run; fixes: applicability gate, delimiter breakout (section 1.6), no-stripping check, fake-provider limit, judge-model taint (section 2.6), no-tools fast path (section 2.0), per-call statement template.

## Not verified
1. **Tool behaviour** (garak probe targets, PyRIT scorer options, llm-guard defaults) was read from source and
   documentation, not run. Re-read before relying on any option name.
2. **PyRIT:** scoring pages were read at the introductory level only; the scenarios, converters and memory pages
   were not read.
3. **llm-guard:** the documentation says its injection model is still being tested; accuracy was not checked.
4. **Own guidance, not sourced:** every sentence marked "own guidance", the order of defences (§2), the
   fail-open advice, the repeat-runs advice and the checkpoint paragraph.
5. **Overlap:** the MCP-side toxic flow and server trust are only cross-referred to `agent-mcp-trust-pitfalls`; if
   that block changes, re-check the references in §1.4 and §2.4.

## Related blocks
`agent-mcp-trust-pitfalls`, `agent-sandbox-egress-pitfalls`, `csp-and-sanitiser-pitfalls`,
`rag-retrieval-quality-pitfalls`, `llm-eval-regression-pitfalls`, `secret-leak-response-pitfalls`,
`security-hardening`.
