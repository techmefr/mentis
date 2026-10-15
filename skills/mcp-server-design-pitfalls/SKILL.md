---
name: mcp-server-design-pitfalls
description: "Use when an MCP server is designed, extended or reviewed from the publisher's side: tool names, descriptions and annotations (annotations are untrusted hints), structured output next to text, protocol errors versus tool errors, deterministic ordering, timeouts that do not undo side effects, which tools are visible to which caller (read-only mode, scope filtering that must not fail open), fingerprints to catch drift in CI, tool search for large catalogues and renaming with deprecation aliases."
---

# mcp-server-design-pitfalls

A block for the person who publishes tools to agents. The three sections share one premise: **the tool list is
an interface that a model reads and a client caches; changing it silently, hiding it incorrectly or reporting
failure in the wrong channel breaks callers that nobody can see**. Deciding which servers to trust is in
`agent-mcp-trust-pitfalls`; isolating what a server may touch is in `agent-sandbox-egress-pitfalls`; the HTTP
contract of the API behind it is in `api-design`.

## When
- Adding or renaming a tool, changing its schema or its description.
- A client shows a tool as read-only and you must decide whether to believe it.
- Returning errors, partial results or large outputs.
- Serving different tools to different callers, or serving hundreds of tools.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | The tool contract: names, descriptions, annotations, input and output schemas | a tool is added or its schema changes | [`01-tool-contract.md`](./references/01-tool-contract.md) |
| 2 | Results and errors: structured plus text, protocol versus tool errors, ordering, timeouts | a tool returns data or fails | [`02-results-and-errors.md`](./references/02-results-and-errors.md) |
| 3 | Exposure and drift: visibility, read-only precedence, scope filtering, fingerprints, tool search, renames | tools differ per caller, or the catalogue changes | [`03-exposure-and-drift.md`](./references/03-exposure-and-drift.md) |

## Output / checkpoint
The server was called by a real client with each class of caller (full, read-only, restricted scope) and the
tool list each saw was compared with the intent (§3). A failing tool was provoked and the error arrived in
the channel the model reads (§2). A fingerprint of the tool list is stored and a CI step fails when it
changes without a recorded approval (§3). A server that was only unit-tested is not verified.

## Guardrails
- Never rely on a tool annotation as a security control; clients must treat it as untrusted (§1).
- Never reuse a tool name across servers a client may load together (§1).
- Never report a failure only as text inside a success result (§2).
- Never assume a timeout cancels what the call already did (§2).
- Never let a failed scope or visibility lookup grant the full tool list (§3).
- Never rename or remove a tool without an alias or a recorded break (§3).
- This block restates the protocol's tools page and three server projects' documentation; the protocol text was
  used for facts only. Nothing was run while writing it; see [`references/origin.md`](./references/origin.md).

## Origin
Rewritten at idea level from the Model Context Protocol tools specification (attribution only, mixed
licences), the FastMCP tool, fingerprinting and tool search documentation (Apache-2.0), the GitHub MCP server
scope, renaming and configuration documentation (MIT) and a tool-design skill (MIT, no numeric threshold kept),
read 2026-10-15. 🟡: never run by us; open points are in [`references/origin.md`](./references/origin.md).
