# telemetry-sensitive-data-pitfalls §3 — Layers, content capture and tests

Redaction is a stack of layers, and each one depends on the previous ones being imperfect. The order matters: the
earlier a layer sits, the less data has travelled.

## 3.1 Auto-instrumented telemetry
1. **Auto-instrumentation has no call site in your code.** A `url.full` with its query string, a `db.query.text`
   with literals or captured request headers are created by the library, so the rules of §2 cannot be applied
   where the value is built (Dash0).
2. **Pick the layer in this order** (Dash0):

| Approach | Use when |
|---|---|
| Instrumentation library configuration | the library can disable or sanitize the field, for example a statement serializer, or an allow or deny list of captured headers; always preferred when it exists |
| Custom span processor or log-record processor | the library has no option, or a blanket policy across every instrumentation library is wanted |
| Collector-side redaction | a safety net in addition to the in-process layer, never instead of it (§3.2) |

3. **A span processor sees every finished span, including those created by auto-instrumentation.** Its end hook can
   overwrite the values of the sensitive attributes (the `authorization`, `cookie` and `set-cookie` header
   attributes in the source's list) with a fixed marker and strip the query string of `url.full` (Dash0). The
   source's samples mutate the span's attributes in that hook; whether the SDK version in use exports the mutated
   values was not tested, so verify with §3.4.
4. **Register the processor before the export processor, on the application's existing SDK or provider.** Do not
   register a second provider after a zero-code auto-instrumentation hook has already initialized one (Dash0).

## 3.2 The Collector as a second layer
1. **Collector-side redaction is defence in depth, not the control.** The Collector sees telemetry after it has
   been serialized and exported, so the data has already left the application process and crossed the network
   (Dash0).
2. **What it can do:** the transform processor can replace authorization headers with a marker, mask card-number
   patterns in log bodies, hash email addresses or usernames to keep correlation, and delete attributes that must
   never be exported (request bodies, unsanitized statements); the filter processor can drop whole records that
   cannot be redacted safely, such as private keys in log bodies (Dash0).
3. **Place redaction after the enrichment processors and before the exporters.** Redaction has to run after every
   attribute has been set, otherwise an attribute added later bypasses it (Dash0). The full processor order and
   `memory_limiter` are in `otel-collector-config-pitfalls` §2; the OTTL expressions for redaction were not read.

## 3.3 Content capture for AI agents and model calls
1. **`captureContent` and `OTEL_LOG_USER_PROMPTS` log raw prompt and completion text.** In a shared or production
   environment that can expose user personal data, secrets embedded in prompts and proprietary code to the
   telemetry backend (o11y-dev).
2. **Keep content capture disabled by default.** If it is needed for debugging, turn it on only in an isolated
   development or staging environment with data governance in place (o11y-dev).

## 3.4 Tests that prove the redaction
1. **Run the assertions after integration tests that exercise instrumented code paths handling user data**
   (Dash0).
2. **Assert that no exported span holds a raw value for a known sensitive header** (`authorization`, `cookie`,
   `set-cookie`): each must be absent or the redaction marker (Dash0).
3. **Assert that `user.id` is not a personal value.** The source's check rejects a value that looks like an email
   address or that contains whitespace, which usually means a display name (Dash0). It catches two shapes; it does
   not prove the value is opaque, so keep the fixture values obviously synthetic and search the full export for
   them (our own guidance).
4. **Test the layer you rely on, not only the last one.** A passing end-to-end check hides a broken in-process
   layer if the Collector layer happens to catch the value (our own guidance).
