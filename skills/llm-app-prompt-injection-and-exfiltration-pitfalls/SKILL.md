---
name: llm-app-prompt-injection-and-exfiltration-pitfalls
description: "Use when an application puts text it does not control in front of a model (retrieved documents, web pages, mail, uploads, tool results) and then renders, stores or acts on the output: where injected instructions come in (direct, indirect, latent in documents, invisible characters), how data leaves through the output (markdown image and link exfiltration, script-bearing links, system prompt extraction, tool calls) and how to close it by design (render policy, least-privilege tools, human gate), and how to test and scan it (attack probes as regression cases, success criteria that look at the outbound path, input and output scanners and their limits)."
---

# llm-app-prompt-injection-and-exfiltration-pitfalls

A defensive block for the person who builds an application around a model, not the person who connects an
agent to someone else's tools. The three sections share one premise: **the model cannot tell data from
instructions, so the application must make the harmful action impossible or gated, and treat any filter as
a way to lower the odds, not as the control**. Connecting an agent to third-party MCP servers, and the
three-part toxic flow, are in `agent-mcp-trust-pitfalls` (this block cross-refers to it and does not repeat
it); isolating what an agent process can touch is in `agent-sandbox-egress-pitfalls`; HTML sanitising and
content security policy are in `csp-and-sanitiser-pitfalls`; retrieved documents as a quality problem are in
`rag-retrieval-quality-pitfalls`; measuring any of this over time is in `llm-eval-regression-pitfalls`.

## When
- Building or reviewing an assistant that reads documents, web pages, tickets, mail or uploads.
- The chat or output renders markdown, links or images, or a model's output is passed to another system.
- A model can call tools that send, write, delete, pay or fetch.
- Adding a prompt-injection filter, or deciding whether a red-team tool result means the app is safe.

**Skip when** no model is called, or no text an outsider can write ever reaches a model and the output is neither rendered, stored nor acted on. Say "not applicable: <reason>" for the block and do not invent a finding. A call with no tools, no rendering of links or images and no secret in context is not exempt: sections 2.1 to 2.4 are closed by construction, and the work moves to integrity (section 2.0).

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Entry paths: direct, indirect and latent injection, hidden characters, tool results, the planted-content test | text from outside reaches the model | [`01-entry-paths.md`](./references/01-entry-paths.md) |
| 2 | Exit paths and design: image and link exfiltration, script-bearing links, prompt and secret leakage, output as input, tools, human gate | the output is rendered, stored, forwarded or acted on | [`02-exit-paths-and-design.md`](./references/02-exit-paths-and-design.md) |
| 3 | Testing and scanners: probe sets, success criteria, scoring, input and output scanners, limits | a test set or a filter is chosen or its result is read | [`03-testing-and-scanners.md`](./references/03-testing-and-scanners.md) |

## Output / checkpoint
For each model call there is a written statement of which inputs an outsider can write to, what the output can
reach (screen, link, store, tool, another model) and which of those reaches is closed by construction (§1, §2).
Write it per call in three lines: "outsider can write: ...", "output reaches: ...", "closed by construction: ... / open: ...". A test document holding planted instructions went through the real pipeline and the result states what was
observed at the outbound path, not what the model said (§1, §3). Any scanner in the path is listed with what
it does not catch (§3.4). A filter with no such list is not a control.

## Guardrails
- Never let output render a remote image or link built from model text without a host allowlist, or the model
  can post conversation data to anyone (§2).
- Never treat a model's refusal in a test as proof that the outbound path is closed; check the path (§3.2).
- Never give a model that reads outside text a tool that sends, writes or pays without a human gate on that
  step (§2).
- Never pass model output to a shell, query, template or another system as if it were trusted input (§2).
- Never count a prompt-injection classifier as the control; it lowers the odds and misses rephrasings (§3).
- Never put secrets, keys or other users' data in a context a model reads next to outside text (§2).
- Never rely on a tag or delimiter around outside text as the boundary; neutralise the closing delimiter inside the text and treat the wrapper as lowering the odds (section 1.6).
- Never let a second model that judges the first one's output be the only barrier, and never read its failure as a pass (section 2.6).
- When only a fake or canned provider exists, say the behavioural test was not run (§1.5, §3.1).
- This block is idea-level guidance from the sources in [`references/origin.md`](./references/origin.md), read on
  the date there. No tool was run and no attack was executed while writing it, and no attack text is reproduced.

## Origin
Rewritten at idea level from the documentation and probe descriptions of garak (Apache-2.0), PyRIT (MIT) and
llm-guard (MIT), read 2026-10-20, plus craft knowledge marked "own guidance" in the references. The OWASP
LLM Top 10 was not opened (licence unconfirmed). 🟡: never run by us; open points are in
[`references/origin.md`](./references/origin.md).
