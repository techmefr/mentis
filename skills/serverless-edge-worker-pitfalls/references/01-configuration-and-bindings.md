# serverless-edge-worker-pitfalls §1 — Configuration and bindings

Sources: the `workers-best-practices` skill (`SKILL.md`, `references/configuration.md`, `references/platform-apis.md`) and the Workers rules file of cloudflare/skills at 86505e4, read 2026-10-20.

## 1.1 Compatibility date and flags
1. **The runtime's behaviour is pinned by a compatibility date in the configuration, and an old date keeps old behaviour.** A new function sets today's date; an existing one moves it forward deliberately, after reading the changes in between and running the tests, not as a side effect of another fix.
2. **The Node.js compatibility flag is needed for any library that imports built-in Node modules;** without it the failure is a confusing import error at run time. Check the flag in the configuration, not only that the code runs locally.
3. **The test runner can hide a missing flag:** the vendor's test pool injects the compatibility flag itself, so tests pass while the deployed function breaks. Confirm the flag in the configuration file.

## 1.2 Bindings
1. **Use a binding, not the platform's REST API, for the platform's own storage, queue and database products.** A binding is an in-process reference with no network hop and no token; the REST call adds latency and a credential to leak.
2. **Every environment-object name used in code has a matching declaration in the configuration, spelled identically,** and a durable-object class name in the configuration equals the exported class. An unused binding alone is not a defect; find a concrete consequence first.
3. **Generate the environment type from the configuration with the platform's type command and re-run it whenever a binding changes.** A hand-written type drifts silently when a binding is renamed.
4. **Never type bindings as `any`, `unknown`, `object` or a loose record,** and never force a type with a double cast: it hides exactly the contract errors the generator would catch. Generic bindings (durable-object namespaces, queues, RPC service bindings) carry their parameters.
5. **Where the binding is read depends on the form:** module handlers (`fetch`, `scheduled`, `queue`, `email`) receive it as the `env` argument; classes that extend a platform base class read it from `this.env`. An `env.X` inside such a class, or `this.env.X` in a module handler, is the most common error.
6. **Platform classes are extended, not implemented.** An `implements` loses the inherited context and environment; check the import path and the generic parameter of the base class.

## 1.3 Configuration format
1. **Prefer the JSON-with-comments configuration file over the older TOML one** for new projects: the source says newer features exist only in the JSON form, and comments document decisions. Re-read for your tool version.

## 1.4 Secrets
1. **Secrets never appear in the configuration file or in source.** The plain-variables section holds non-secret settings; secrets are set with the platform's secret command and read from the environment object at run time.
2. **Ignore local environment files in version control** so a local development secret is not committed.

## 1.5 Logs and traces
1. **Turn on logs and traces before production.** Traces have their own switch: the top-level observability switch alone does not enable them, and an environment override can turn either off, so check the deployed environment's effective setting.
2. **Log one JSON object per event and use the error method for errors,** so entries are searchable and carry severity. Set the sampling rate for the workload: full for logs on a small service, low for traces on a busy one.
3. **In review, a function with no logs or traces in its production configuration is a finding.**

## 1.6 Tests in the real runtime
1. **Run behaviour tests inside the platform's runtime with real bindings,** which catches what a plain Node test cannot (binding access, limits, request lifetime).
2. **Cover the nullable return:** a key-value read of a missing key returns null, and code that assumes a string fails only in production.

## 1.7 Checks (own guidance)
1. Diff the generated environment type against the committed one: no difference.
2. Search the configuration and source for key-shaped strings: none.
3. After changing the compatibility date, run the runtime tests and list the behaviour changes read.
