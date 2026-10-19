# node-container-runtime §2 — Runtime configuration

Configuration is the part of a service that changes between environments without a code change. The two
failure modes are opposite: a missing value found at the first request that needs it, and a value silently
defaulted to something wrong. The fix for both is the same: read once, validate at boot, fail loudly.

## 2.1 What NODE_ENV is for
1. **It is a convention, not a feature.** Node itself does almost nothing with it; libraries read it. Express
   and many others switch caching and error output on it, and package managers skip development
   dependencies when it is `production`. Set it to `production` in the image (see `01-container-image.md` §1.4).
2. **It conflates concerns.** One value ends up deciding log format, security checks, behaviour toggles and
   optimisation. A practitioner's argument, which we adopt as a rule of thumb, is to use one explicit
   variable per concern (log level, whether to expose API docs, whether a feature is on) and keep
   `NODE_ENV` for what libraries expect.
3. **Never let `NODE_ENV` alone switch a security or correctness behaviour.** "Skip authentication unless
   production" is one mistyped value from an open service in the wrong environment. Make the dangerous
   behaviour opt-in by a dedicated variable that is absent by default.
4. **`staging` is not a `NODE_ENV`.** Keep the value to `development`, `test` and `production`; describe the
   deployment with a different variable.

## 2.2 Validate at startup
1. **Read the environment in one place**, parse it into a typed object, and pass that object around. Code
   that reads `process.env` anywhere reads it unvalidated and untyped (everything is a string, a missing
   value is `undefined`, `"false"` is truthy).
2. **Validate with a schema** (zod, an env-schema library, or the framework's config validation) and let the
   process exit non-zero on the first failure with the name of the variable, not its value.
3. **Distinguish required, optional with a default, and secret.** Required values have no default; a default
   for a connection string is how a service starts against the wrong database.
4. **Commit an example file** (`.env.example`) with every variable and no real value, and keep the real
   file out of version control and out of the image.
5. **Secrets come from a secret manager or the orchestrator**, not from a committed file; the env file is a
   development convenience.

## 2.3 Env files in Node
1. **`node --env-file=<path>`** loads a file into the environment before the program starts. It was added
   in v20.6.0 and is no longer experimental from v24.10.0 and v22.21.0; multi-line values are supported from
   v21.7.0 and v20.12.0. A variable already in the real environment wins over the file; with several
   `--env-file` flags a later file overrides an earlier one; a missing file is an error.
   `--env-file-if-exists` (v22.9.0) tolerates a missing file.
2. **`process.loadEnvFile(path)`** loads one from code (v21.7.0 and v20.12.0, stable from the same
   versions as above); the default path is `./.env`. Setting `NODE_OPTIONS` inside an env file has no
   effect, so memory flags (see `01-container-image.md` §1.6) must be set in the real environment.
3. **In a container, prefer the orchestrator's environment** over a file baked into the image; use the flag
   for local runs.
4. **If a framework config module already loads the file**, do not add a second loader: two loaders disagree
   on precedence and the bug looks like "the variable is sometimes ignored".

## 2.4 Checks
- Remove one required variable and start: exit non-zero, message names it, no stack of a failed connection.
- Set `NODE_ENV=production` locally and run the test suite's smoke test: no development-only route or
  skipped check is reachable.
- `docker history` and the image filesystem contain no real `.env`.
- Grep the source for direct `process.env` reads outside the config module.

## 2.5 Nest mapping
The Nest config module (`ConfigModule.forRoot`, with a validation schema or function) is the single place to
read and validate; inject the typed values through `ConfigService` or a namespaced config provider rather
than reading `process.env` in a service. Dynamic-module options that depend on config use the async
registration form (see `nestjs-integration-patterns` §3).
