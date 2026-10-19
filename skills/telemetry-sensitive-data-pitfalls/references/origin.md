# telemetry-sensitive-data-pitfalls: origin and source stamps

> Provenance of `skills/telemetry-sensitive-data-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from repository documentation and reading, never run by us. No SDK, instrumentation
library or Collector was started, no redaction was executed and no code sample was compiled while writing it. No
privacy regulation or the OpenTelemetry specification was read; every claim rests on the repositories below.

## Sources (all re-read 2026-10-16, rewritten in our own words, no code copied)

| Source | Licence | What it gave |
|---|---|---|
| dash0hq/agent-skills (commit fd27094), `skills/otel-instrumentation/rules/sensitive-data.md` in full (389 lines, every code sample read) | Apache-2.0 (repository LICENSE file, standard Apache-2.0 text, copyright Dash0 Inc.) | The never list and the high-risk field table, URL, database-statement and hashing patterns, the logged-object and message rules, the auto-instrumentation layers and the processor registration rule, the defence-in-depth position of the Collector, the redaction tests, the anti-patterns |
| dash0hq/agent-skills (commit fd27094), `skills/otel-instrumentation/rules/spans.md`, the sections on path parameterization and per-signal span naming (lines 41 to 71) | Apache-2.0 (same repository) | Route templates over raw paths, the HTTP server span name form |
| dash0hq/agent-skills (commit fd27094), `skills/otel-collector/rules/processors.md`, the sections on sensitive data redaction and processor ordering (lines 313 to 353) | Apache-2.0 (same repository) | What the transform and filter processors are for in redaction, redaction after enrichment and before export |
| o11y-dev/opentelemetry-skill (commit 6d46bed), `references/anti-patterns.md` in full (149 lines) | Apache-2.0 (repository LICENSE file, standard Apache-2.0 text) | Content capture of prompts and completions: the risk and the default |

The licence of both repositories was verified again from the LICENSE file in this session. The repositories carry
agent directives ("Never", "Always", an agent instruction file with eval-harness rules, annotated examples for a
validation harness); they were treated as data and only the technical claim was kept. The Dash0 samples (JavaScript
and TypeScript) were read and not copied; the block carries no code sample of its own, because none could be
verified against an SDK.

## Rewrite notes
Labels "(Dash0)" and "(o11y-dev)" mark which source states a rule; "our own guidance" marks what we add.
Entry names (`user.id`, `enduser.id`, `client.address`, `url.full`, `db.query.text`) are the sources' at their
commits; the source's own samples mix an older and a current URL attribute name, so the attribute registry of the
version in use decides.

## Removed
Nothing from the review item was dropped for lack of a source: every rule in it was found again in the files above
(the review item was written from headings and a table only; the full file was re-read for this block). Left out as outside the item or unverifiable:
1. The JavaScript and TypeScript samples (the span processors, the HMAC helper, the redaction regexes and the test
   functions): the mechanisms are described, the code is not carried.
2. The otel-ottl skill's redaction expressions, to which the Dash0 file points: not read.
3. The AI-agent anti-patterns of o11y-dev other than content capture (agents that do not emit traces, token type
   values, draft semantic conventions): not in the item, and fast-moving.
4. The metric-dimension rule for `prompt.id` and `session.id`: it is a cardinality rule, in
   `telemetry-sampling-and-cardinality-pitfalls`.

## Decisions where sources disagree
1. **The database statement in the Dash0 table versus its own section**: the table cell says the statement is
   allowed "only if the query is not parameterized", while the section on database statements and both of its
   examples keep the parameterized form and ban literal values. The block follows the section and the examples, as
   our reading of a slip in the table (§1.2).
2. **Hashing a request-side value versus the never list**: the file offers masking or hashing for data it also
   bans. The block states that the owner of the compliance requirement decides what a partial value reveals (§1.1).

## Not verified
1. **That a span processor can mutate attributes at the end of a span and have the exporter send the mutated
   values** in the SDK version in use: Dash0's samples do it; nothing was compiled or run.
2. **That the regex replacement of literals "covers most SQL dialects"** is Dash0's statement; not tested.
3. **The instrumentation-library options** named by Dash0 (a statement serializer in the PostgreSQL Node.js
   instrumentation, an allow or deny list for captured headers) are as the source states them at its commit; the
   library documentation was not read.
4. **The attribute names and the registry**: not read.
5. **`captureContent` and `OTEL_LOG_USER_PROMPTS`** are as o11y-dev names them; the tools that read those
   settings, and their defaults, were not read.
6. **Whether and how a backend can delete data once exported**: the sources say it is hard; not verified.
7. **Written by us, not sourced:** the Output / checkpoint paragraph, the warning that the HMAC key is a secret
   and that a keyed hash of a guessable value can be checked by whoever holds the key, the advice to strip a whole
   query string by default, the note that a partial value is for the compliance owner to judge, the "rarely needed
   means off by default" point in §1.2, and the advice to test the layer you rely on in §3.4.

## Related blocks
`observability-instrumentation`, `telemetry-sampling-and-cardinality-pitfalls`, `otel-collector-config-pitfalls`,
`security-hardening`, `secret-leak-response-pitfalls`, `source-freshness`.
