# mcp-server-design-pitfalls §3 — Exposure and drift

## 3.1 Who sees which tools
1. **The list may vary by the authorisation on a request, not by connection.** The protocol says the set
   returned by `tools/list` must not vary per connection or as a side effect of other requests, but may vary
   by the authorisation presented, for example returning only tools the granted scopes permit.
2. **Decide visibility on the server.** FastMCP can disable tools by name or tag (disabled tools are neither
   listed nor callable) and has an allowlist mode that enables only tools with given tags. The GitHub server
   offers toolsets, individual tools and an exclude list.
3. **Make the restrictive setting win.** The GitHub server documents that read-only mode takes precedence over
   every other configuration and disables write tools even when requested, and that excluded tools win over
   toolsets and individually named tools. Own guidance: design every mode so a narrowing option cannot be
   undone by a widening one.
4. **Content filters are not boundaries.** The same server calls its lockdown mode a best-effort content
   filter, not an authorisation boundary, and says an operator's server-side setting is an upper bound that a
   per-request header cannot relax.

## 3.2 Scope filtering and what happens when it fails
1. **The GitHub server hides tools a token cannot use,** but only for classic personal access tokens, at start-up,
   by reading the token's scopes. For fine-grained and app tokens it shows all tools and lets the API enforce
   permissions; with OAuth on its remote server it issues scope challenges when a call needs more.
2. **It fails open, and says so.** If the scopes cannot be fetched it logs a warning and continues without
   filtering. That is tolerable there because each call is still checked by the API, so filtering is only
   a convenience. Own guidance: do not copy a fail-open filter where the list is the control; decide
   per server what an error returns, and test by breaking the lookup.
3. **Per-call checks decide.** The server's per-tool check receives the call arguments and can ask for more
   scope only when needed (for example workflow files). Keep the enforcement at the call.

## 3.3 Detecting drift
1. **Fingerprint what your clients depend on.** FastMCP documents a recipe, not a fixed contract hash: build a
   payload from a canonical tool key and the protocol-facing tool object, serialise it deterministically and
   hash it. What to include is your policy: always the input schema, the description when documentation drift
   matters, the output schema and annotations when consumers rely on them.
2. **Compare in CI.** The same page stores a manifest of fingerprints per build and reports tools that changed
   or disappeared. Own guidance: fail the build on a change nobody recorded; this is the publisher's side of the
   pinning in `agent-mcp-trust-pitfalls` §1.
3. **Review description changes as interface changes** (own guidance).
4. **A registration clash is a drift too.** FastMCP's default on registering the same tool twice is to warn and
   replace; it can be set to raise an error instead.

## 3.4 Large catalogues
1. **A long list costs context and degrades selection.** FastMCP's tool search replaces the listing with a
   search tool and a call proxy; the original tools stay callable, because search controls discovery, not
   access.
2. **Search respects the authorisation pipeline.** Tools filtered by visibility or auth do not appear in
   results; app-only tools are excluded, and the page says app visibility is not a security boundary.
3. **Descriptions are model input.** For its experimental model-based search, the page warns that a description
   written to argue for its own selection can move the ranking, so treat third-party catalogues accordingly.
4. **Pin the tools that must always be visible** (the page's `always_visible`) and keep that set small.

## 3.5 Renames and removals
1. **Rename with a deprecation alias.** The GitHub server keeps a map from old tool names to new ones and
   resolves old names silently, so a configuration that names an old tool keeps working, on its local and remote
   servers.
2. **State when an alias ends and what replaces the old name** (own guidance).
3. **Tell clients the list changed.** The protocol says a server that declares the capability should send a
   list-changed notification to clients that opened the subscription stream for it; FastMCP sends it
   automatically when tools are added, removed, enabled or disabled within a request context, not during
   initialisation. Do not assume clients refresh by themselves.
