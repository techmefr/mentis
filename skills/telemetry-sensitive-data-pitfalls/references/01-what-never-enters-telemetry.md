# telemetry-sensitive-data-pitfalls §1 — What never enters telemetry

Attributes, log bodies and span events can capture personal data and secrets by accident, and the capture is
usually a convenience for debugging: a request id is useful, so the whole request gets attached. The decision has
to be made per category, before the code is written.

## 1.1 The never list
1. **These categories never go on a span, a metric or a log, whatever the signal** (Dash0): authentication
   credentials (passwords, API keys, bearer tokens, session cookies, OAuth secrets); financial instruments (card
   numbers, bank account numbers, security codes); government identifiers (social security, passport, tax and
   national identity numbers); health records (diagnoses, prescription data, record numbers); biometric data;
   and the values of the `Authorization`, `Cookie` and `Set-Cookie` headers in full.
2. **The ban covers every field, not only attributes.** The source names span attributes, span status messages, log
   bodies, log attributes, metric attributes and resource attributes (Dash0).
3. **If someone asks to store data from these categories, offer to mask or hash part of it.** That is the source's
   wording for the request; it does not make hashing a card number acceptable by itself, and the compliance owner
   decides what a partial value may reveal (Dash0; the last clause is our own guidance).

## 1.2 Fields that need a condition
These fields help debugging and incident response and carry privacy risk. Evaluate each against the compliance
requirements before it is used (Dash0). The table is the source's, in our words.

| Field | Where | Condition |
|---|---|---|
| `user.id`, `enduser.id` | spans, logs | only an opaque identifier (a UUID, an internal id), never a username or an email; use whichever name the attribute registry of the version in use gives |
| client address (`client.address`, an IP address) | spans, logs | only if needed for abuse detection or geo-attribution; truncate or hash when full precision is not needed |
| email address | never as an attribute | if needed for correlation, use a keyed hash (HMAC) and keep the mapping outside the telemetry pipeline (§2.3) |
| username, display name | never as an attribute | use an opaque `user.id` |
| `url.full` | spans | strip or redact query parameters that carry tokens, session ids or user input (§2.1) |
| request and response bodies | never as an attribute | if body tracking is needed, record a content hash or a size |
| `db.query.text` | spans | only the parameterized form, never literal values (§2.2) |

1. **A table cell is not the last word: read the section it points to.** The source's table says the database
   statement is allowed "only if the query is not parameterized", while its own section on database queries, and
   both of its examples, keep the parameterized form (`... WHERE email = $1`) and ban literal values. The block
   follows the section and the examples; the table cell reads as a slip (Dash0; our reading).
2. **`user.id` is not a free pass.** The identifier has to be opaque to anyone reading the backend: a value derived
   from an email by a keyed hash qualifies (§2.3), the email itself does not. The source's test of that rule is in
   §3.4.
3. **Rarely needed means off by default.** A client address, a header and a body each cost privacy and, for the
   ones with an unbounded value, cardinality (`telemetry-sampling-and-cardinality-pitfalls` §2). If nobody has
   named the question the field answers, do not capture it (`observability-instrumentation` §1; our own guidance).
