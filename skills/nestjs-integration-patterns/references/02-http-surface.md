# nestjs-integration-patterns §2 — Versioning, the OpenAPI document, deprecation

The API surface is a contract with callers you cannot see. The principle: **a change to the surface is
announced in the document and in the response, and a retired version is retired only after usage proves
nobody is left**. Contract rules (what is a breaking change) are in `api-design`; this section is how Nest
carries them.

## 2.1 Versioning
1. **Enable it explicitly** with `app.enableVersioning`, and choose one scheme: URI (default, a `v` prefix
   that comes after the global prefix), header, media type (`key: 'v='`), or a custom extractor that
   returns a string or an array sorted highest first (Express cannot reliably route multi-version; Fastify
   can).
2. **A route with no version and no default version returns 404**; a version with no matching route returns
   404. Set `defaultVersion` or mark routes version-neutral on purpose.
3. **A route-level `@Version` overrides the controller's**; arrays allow one handler to serve several versions.
   Middleware can target a version with `forRoutes({version})`.
4. **Enable versioning before building the document** or the document misses versioned paths.
5. **Version the smallest unit**: a single route moves to v2 while the rest stays; a whole-API bump is for
   a coordinated break.

## 2.2 Building the OpenAPI document
1. **Create the document through a factory** (deferred), after versioning and global prefix are set.
2. **Serve the UI and the raw document independently**: `ui` and `raw` options (`'json'` and `'yaml'`) let you
   keep the raw document and drop the UI, or the reverse; an empty `raw` disables definitions. Use
   `jsonDocumentUrl` for the path, and `patchDocumentOnRequest` when the document depends on the request
   (host, auth).
3. **Operation ids**: set `operationIdFactory` so generated clients get stable method names instead of
   controller-and-method concatenations that change when you rename a class.
4. **Options worth knowing**: `onlyIncludeDecoratedEndpoints` (document an explicit subset),
   `excludeDynamicDefaults`, `autoTagControllers`.
5. **Exposing the document in production is a choice**, not a Nest default or recommendation: ours is to
   serve the raw document only where its consumers are, behind the same access control as the API, and to
   turn the UI off in production.
6. **Standard-schema libraries** (zod, valibot) can describe a schema through the `schema` option; a
   converter is chosen by the schema's vendor, and a library that natively exposes JSON Schema needs no
   converter. Check the library's own version note before relying on this.

## 2.3 Types the document cannot infer
1. **Generics and interfaces are erased at runtime**, so name the type: `@ApiBody({ type: [Dto] })` for
   arrays, `type: [String]` for primitive arrays, and a lazy `type: () => Node` for circular references.
2. **Name enums** with `enumName`: it produces one reusable schema, so generated clients do not receive a
   duplicate enum per use.
3. **Name schemas** with `@ApiSchema({ name })` when two DTOs share a class name; use `@ApiExtraModels`
   plus `getSchemaPath` to describe `oneOf` responses.

## 2.4 The CLI plugin and its limits
1. **The plugin infers properties from the class**, only for files with the configured suffixes
   (`.dto.ts`, `.entity.ts`); the class-validator shim is on by default, comment introspection off by
   default. A DTO still needs real class-validator decorators for runtime validation; the plugin only
   documents.
2. **Import mapped types** (`PartialType`, `OmitType`) from the Swagger package so they carry the metadata.
3. **It does not run** under a transpile-only tool unless the build checks types or the plugin's metadata
   generator is run; and not under a plain Jest SWC transform. See `node-container-runtime` §3.3.
4. **After changing plugin options, delete the build output** or stale metadata is used.

## 2.5 Deprecation and sunset
1. **Mark it in the document** (`deprecated: true` on the operation).
2. **Obtain consent before shutdown** and monitor usage of the deprecated endpoint until it is nil: headers
   alone are not consent.
3. **Send a `Deprecation` header** on responses (structured-field timestamp, as `@1758095283`, or `true`) and
   a **`Sunset` header** (an HTTP-date) set to the earliest date. Clients should monitor them.
4. **Log every call to a deprecated route** with the caller identity so the usage can be read, and make that
   count a number somebody watches (see `observability-instrumentation`).

## 2.6 Verification
- The generated document was read after the change (paths include version prefixes; enums not duplicated).
- A client generated from it compiles and its method names are the ones you meant.
- A call to a deprecated route shows both headers and a log line.

## 2.7 Nest mapping
All of §2 is Nest-specific except 2.5, which is protocol-level and holds in any framework.
