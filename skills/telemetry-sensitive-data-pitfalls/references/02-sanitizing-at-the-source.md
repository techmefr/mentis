# telemetry-sensitive-data-pitfalls §2 — Sanitizing at the source

The first line of defence is in the process that creates the telemetry, because it is the only place the raw value
has not yet been serialized and sent over a network. The rules below are the ones to apply at the call site.

## 2.1 URLs and paths
1. **A URL's query string carries tokens, session ids and user-supplied input.** Strip it entirely, or redact the
   specific parameters (replace their values with a fixed marker) before the URL becomes a span attribute
   (Dash0). Stripping everything is the safer default, because redaction by key list only covers the keys you
   thought of (our own guidance).
2. **A path with an embedded identifier is both a cardinality and a leak problem.** `/api/users/12345` as a span
   attribute multiplies values and may expose an internal id. Use the route template the framework exposes (the
   source's example: Express's `req.route.path` gives `/api/users/:id`), and fall back to replacing segments that
   look like UUIDs or numbers with placeholders only when the framework gives no template (Dash0).
3. **A span name follows the template too.** The source's naming table for an HTTP server span is the method plus
   `http.route`, for example `GET /api/users/:id`, never the raw path (Dash0).

## 2.2 Database statements
1. **Auto-instrumentation may capture the statement text with its literal values.** Check that the library
   records the parameterized form (`... WHERE email = $1`) and not an inlined literal (Dash0).
2. **When the library captures literals, fix it in this order** (Dash0):
   1. A library-level option, the simplest and cheapest fix; the source names a statement serializer option of the
      PostgreSQL instrumentation for Node.js as an example.
   2. A custom span processor that replaces quoted strings and numeric literals in the statement with a
      placeholder before export. The source says such a replacement covers most SQL dialects; that was not tested.
   3. Redaction in the Collector's transform processor. It is the weaker option because the raw statement has
      already left the application process over the network; it only keeps it from long-term storage.
   4. Last resort: stop recording the statement, and accept the loss of statement-level visibility.

## 2.3 Hashing for correlation
1. **When a sensitive value must be correlated across services, use a keyed hash (HMAC), not the value.** The
   result is a stable identifier that joins across services without exposing the original (Dash0).
2. **Keep the mapping from hash to value in a separate, access-controlled system, never in the observability
   backend** (Dash0).
3. **The key is a secret.** A keyed hash of a guessable value (an email address) can be checked against guesses by anyone
   who holds the key, so the key lives in the service's secret store and is not logged or exported (our own guidance; the source's
   sample reads the key from an environment variable).

## 2.4 Logged objects and messages
1. **Select fields explicitly; never spread an object.** Passing a request body, form data or a headers object
   directly to a logger or a span attribute call carries whatever the user sent, including passwords and tokens.
   Name the safe fields one by one (Dash0).
2. **The message string can leak too.** Interpolated user input (`"Payment processed for <email>"`) bypasses the
   structured fields. Pattern-based redaction of the message is a safety net only; the source's patterns cover card
   numbers, social security numbers, email addresses, JWTs and common API-key prefixes, and the source says plainly
   that this is not exhaustive (Dash0).
3. **Do not echo user input into an error message or a span status message.** Describe the class of error
   (`ValidationError: invalid email format`), not the value that failed (Dash0).
4. **Redaction by field name** (credentials, authorization headers) is the stronger structure for logs; it is in
   `observability-instrumentation` §2 and not repeated here.
