---
name: agent-sandbox-egress-pitfalls
description: "Use when an agent or the code it generates is run inside a sandbox, or a sandbox for agents is configured: why filesystem and network isolation must come as a pair, how to write the read, write and network rules (deny then allow, allow only), what an allowlisted domain still leaks (exfiltration, fronting, resolved addresses), the escalation paths left open (docker socket, PATH and shell rc files, weaker nested modes, proxy variables) and the limits of local code sandboxes."
---

# agent-sandbox-egress-pitfalls

A defensive block for the layer under the agent. The four sections share one premise: **a sandbox is a list of
what is allowed, and every entry on the list is a path out for a hostile instruction; the list has to be
written and tested as a list of exits**. Deciding whether tools can be trusted is in `agent-mcp-trust-pitfalls`;
guards that run inside the agent's loop are in `agent-hook-guard-pitfalls`; container and CI hardening is in
`ci-workflow-hardening` and `security-hardening`.

## When
- Configuring a sandbox, a container or a restricted shell for an agent that runs commands.
- Letting a model write code that is executed, by a tool or by a code-agent framework.
- Choosing which domains and paths an agent may reach.
- A review asks "what can the agent do if it is told to leak this repository".

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | The isolation model: both filesystem and network, the rule shapes, what to deny by default | a sandbox is designed or its config changes | [`01-isolation-model.md`](./references/01-isolation-model.md) |
| 2 | Egress: allowlisted domains, fronting, resolved addresses, proxy variables, tools the vendor runs outside the sandbox | the agent needs network access | [`02-egress.md`](./references/02-egress.md) |
| 3 | Escalation paths: sockets, PATH and rc files, mandatory deny paths, nested and weaker modes | a path or a mode is added to the allow list | [`03-escalation-paths.md`](./references/03-escalation-paths.md) |
| 4 | Generated code: local sandboxes versus remote execution, import and attribute filters | a model's code is executed | [`04-generated-code.md`](./references/04-generated-code.md) |

## Output / checkpoint
Each exit was tried, not read off the config: from inside the sandbox a read of a denied secret failed, a
write outside the allowed paths failed, a request to a host that is not on the list failed, and a request to
an allowed host carrying a file was either impossible or visible in a log (§1, §2). The escalation list in §3
was walked line by line and each item is either absent or recorded as a decision. A config that was only
parsed is not verified.

## Guardrails
- Never configure filesystem isolation without network isolation, or the reverse (§1).
- Never allow a write path that a shell, a git hook or another program reads and runs later (§3).
- Never treat an allowed domain as safe for data; it is a place data can be sent (§2).
- Never leave a vendor-run web search or fetch tool on in a job that reads untrusted text; the allowlist does not
  cover it. Switch it off, or scope it and test the scope (§2.4).
- Never mount a container runtime socket into the sandbox (§3).
- Never run a weaker nested mode without writing down what it gives up (§3).
- Never describe a local interpreter filter as a sandbox for hostile code (§4).
- This block restates the sandbox runtime's documentation and a code-agent framework's guide as of the
  commits in [`references/origin.md`](./references/origin.md). Nothing was run, and no sandbox was started,
  while writing it.

## Origin
Rewritten from the Anthropic sandbox-runtime README (Apache-2.0) and the Hugging Face smolagents secure code
execution and agent-building guides (Apache-2.0), read 2026-10-15. 🟡: never run by us; open points are in
[`references/origin.md`](./references/origin.md).

Section 2.4 (vendor-run web tools bypass the allowlist) was added 2026-10-20 from the agent definitions of claude-quickstarts (MIT); see [`references/origin.md`](./references/origin.md).
