# mcp-server-design-pitfalls §1 — The tool contract

## 1.1 Names and descriptions
1. **Names are unique within a server and limited in form.** The protocol's tools page says a name should be
   1 to 128 characters, case-sensitive, drawn from letters, digits, underscore, hyphen and dot, and unique
   within the server.
2. **Collisions happen across servers.** The page says a client or proxy that aggregates servers may see two
   servers each exposing `search`, and should disambiguate, for example by prefixing a server identifier; the
   server's own `name` is not guaranteed unique and should not be used for that. The tool-design skill gives
   the same advice for namespacing (`db_*`, `web_*`) and a verb-noun pattern with the same parameter name
   throughout the catalogue. Own guidance: prefix your own tool names so aggregation is not the client's problem.
3. **The description is the model's documentation.** The tool-design skill says to answer what the tool does,
   when to use it, what inputs it takes (types, constraints, defaults, format examples) and what it returns,
   including error conditions. Treat descriptions as code: version and review them, since they rot as the API
   behind them changes.
4. **Do not write instructions about other tools into a description.** The agent-scan issue code E002 flags a
   tool that references a tool of another server, as a shadowing pattern (`agent-mcp-trust-pitfalls` §1);
   your own server is scanned the same way.
5. **Consolidate overlapping tools, but not into a tool with too many modes.** The skill's consolidation
   principle says each tool should have one unambiguous purpose and overlap causes selection errors; it also
   warns that a tool with too many parameters or serving different use cases becomes hard to call correctly.
   Split such a tool, which also lets you permit its parts separately (that last point is own guidance).
6. **A tool with no parameters** should declare an input schema that accepts only an empty object, which the
   page marks as the recommended form.

## 1.2 Annotations are hints
1. **Annotations describe the tool; they do not enforce anything.** The protocol says clients must treat
   them as untrusted unless they come from a trusted server, and FastMCP's documentation calls them advisory
   hints that do not enforce security boundaries.
2. **A client may use them to skip confirmation.** The FastMCP page says clients use `readOnlyHint` to decide
   when to skip confirmation prompts, so an annotation that is wrong removes a safeguard. The defaults it lists
   assume the worst (not read-only, destructive, open world); set the real values.
3. **Do not take security decisions from values the client supplies.** FastMCP can inject values such as a user
   ID on the server so they are not part of the schema the model sees; the protocol's security section
   requires servers to validate inputs and apply access controls (§3).
4. **One more rule from the same section:** servers must rate limit tool invocations and sanitise tool
   outputs.

## 1.3 Schemas
1. **Define the input as a schema and validate it on the server.** The protocol requires servers to validate
   all tool inputs. FastMCP coerces compatible inputs by default (a string `"10"` for an integer) and has a
   strict mode that rejects them; choose on purpose.
2. **If you declare an output schema, conform to it.** The protocol says servers must provide structured
   results that conform, and clients should validate them (§2).
3. **Keep a schema change additive where you can** (own guidance); §3 covers retiring a field or a tool.
