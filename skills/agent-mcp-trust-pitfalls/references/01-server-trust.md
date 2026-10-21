# agent-mcp-trust-pitfalls §1 — Server trust

Connecting a server gives its author two things at once: code that runs, and text that the model reads as
instructions. Both have to be vetted, and the second one can change without the first changing.

## 1.1 Local servers are code you run
1. **A local server is an ordinary process with your account's access.** The protocol's local-server guide
   says it inherits your environment variables, can read what your account can read and can open outbound
   connections, and that none of this is governed by the protocol. Its stdio transport is not a sandbox: client
   and server share one trust domain.
2. **A one-click configuration can hide the command.** The security best-practices page requires a client to
   show the exact command, untruncated, and get explicit approval before running it, and suggests highlighting
   patterns such as `sudo`, `rm -rf` or network operations.
3. **Limit who can talk to a local server.** The same page says a server meant to run locally should use stdio,
   or, over HTTP, require an authorisation token or use a restricted local socket.
4. **Run third-party servers isolated.** The local-server guide calls isolation the highest-leverage
   mitigation: a container with no mounts beyond what the server needs, or a dedicated VM or OS sandbox,
   with network denied where none is needed (`agent-sandbox-egress-pitfalls`).
5. **Ask first whether it needs to run locally.** The guide prefers a remote version where one exists, and
   treats a stdio-only server that needs nothing local as a signal worth questioning.
6. **Provenance and pinning of what you install.** The guide asks for an identifiable publisher, the exact
   package name (typosquatting), a pinned version, and notes that pinning a package for a launcher fixes only
   the top-level package while a container image digest freezes the dependency tree. It also says no check
   proves what a server will do, so containment decides what a bad decision costs.
7. **A proxy that spawns local servers turns a web flaw into code execution.** The best-practices page says stdio
   itself is not the weakness, but a local proxy service that starts servers as child processes can be reached with a
   stolen proxy token after a script-injection flaw in the client, and then runs any command the proxy may run. Its
   mitigations: prevent the entry flaws (authorisation URL validation, a content security policy, sanitising input from
   servers), sandbox the spawned processes, restrict their file access, log all stdio use and require extra
   authorisation for sensitive commands. Check: can anything that holds the client-to-proxy token start an arbitrary
   command? Source: MCP security best practices, section on stdio in proxy scenarios.

## 1.2 Descriptions are an attack surface
1. **Tool poisoning:** hidden instructions in a tool description. The agent-scan v0.5 issue codes list it as
   critical (E001), and the v0.6 risk list as `prompt_injection_tool_desc`. The local-server guide adds that
   the poisoned tool need never be called. Read descriptions in full; a client's one-line summary hides them. OpenAI's MCP guide says the same of
   remote servers: malicious ones may carry hidden instructions meant to make the model behave unexpectedly, and its
   built-in safeguards do not replace reviewing inputs and outputs and connecting only to trusted servers.
2. **Shadowing:** a tool from one server references a tool of another server (issue code E002), which can alter
   how the trusted tool is used. Review servers as a set, since all configured servers share one model
   context and a malicious one can steer the others.
3. **Hidden characters:** the v0.5 issue code W021 flags invisible Unicode (format and control characters, and
   tag characters that can encode a whole message), which a human reviewer does not see. Own guidance: strip
   or flag invisible code points when comparing descriptions.
4. **Rug pull:** the local-server guide says definitions can change after approval, so a one-time consent
   dialog and a package pin do not cover them. A related scanner risk for skills is
   `unverifiable_dependencies`: content fetched from a remote URL at runtime lets behaviour change independently
   of what was installed. OpenAI's guide says it plainly for remote servers: a server may change tool behaviour
   unexpectedly, with unintended or malicious results. The protocol's tools page gives the hook: a server that declares
   the list-changed capability sends a notification when its tool list changes, so a client can notice and re-ask.
5. **Annotations are not facts.** The tools page says clients must treat tool annotations (behaviour hints such as
   read-only or destructive) as untrusted unless the server is trusted, so an annotation is not a reason to skip an
   approval.

## 1.3 Pin, then compare
1. **Trust on first use, then pin the configuration.** The context protector records an approved server
   configuration (server instructions, tool descriptions and tool input schemas) and blocks tool calls on any
   deviation until a person approves the change; the comparison ignores tool and parameter order. It checks at
   connection and again on a tools-list-changed notification. The README does not say it uses a hash, so no
   hash is claimed here.
2. **An approval names a version of the descriptions, not a server.** The protector identifies a server by its
   type and its command string or URL, and treats even an inconsequential change in the command as a new
   server. Do not auto-update servers without a diff a person reads (own guidance).
3. **Prefer clients that pin and re-prompt.** The local-server guide says the protocol does not require
   pinning of tool definitions, so it is a property worth choosing a client for.
4. **Scan, with the privacy cost known.** Agent-scan discovers configured agents, servers and skills and checks
   them; it sends data to the vendor's analysis API (tool names and descriptions in v0.5; server configurations,
   signatures and skill files with secrets redacted in v0.6), and its docs suggest pinning a release for stable
   output. Own guidance: scan after every update and treat it as one signal.
5. **Keep the roster small and known.** The local-server guide opens its advice with removing unused servers
   and knowing where each remaining one comes from; the SlowMist checklist adds an authorised directory of
   trustworthy servers, versioned tools to detect change, name-conflict checks before registering a tool,
   and periodic scans of installed servers. OpenAI's guide adds a sourcing rule: prefer the official server hosted by
   the service's own provider over a third party that proxies it, and, if an aggregator is unavoidable, review how it
   uses your data.

## 1.4 What a scanner does not prove
1. **A clean scan is not a trust decision.** The local-server guide states that no check proves what a server
   will do; provenance signals tell you who you are trusting, not that the trust is warranted.
2. **Reference implementations are examples.** The protocol's servers repository says its servers are
   educational examples, not production-ready.
3. **A guardrail on responses is a second layer.** The protector can scan tool responses for prompt injection
   and quarantine them for review, and sanitises ANSI control characters that could mislead a reader.
