# elixir-ecto-oban-pitfalls §3 — Configuration timing

Sources: the Elixir 1.20.4 documentation (`Config`, `Application`, `mix release`, and the Mix and OTP guide chapters
"Configuration and distribution" and "Releases") and the Phoenix SSL guide (tree of 2026-10-07), read 2026-10-08.

## 3.1 Two files, two times
1. **`config/config.exs` is read at build time,** before the application is compiled and before dependencies are
   loaded. It also runs whenever a release is assembled. A call like `System.fetch_env!/1` in it is evaluated on the
   build machine, so the value is the build machine's, and the build fails when the variable is missing there.
2. **`config/runtime.exs` is read when the project or the release starts.** It is the place for environment variables
   and external configuration. In a release it is copied in and run early in boot.
3. **`runtime.exs` has three rules.** It must `import Config` at the top, must not `import_config` other files, and
   must not touch `Mix`, which does not exist inside a release.
4. **Do not call `Mix.env()` from application code.** Use `config_env()` in config files and store the value under a
   key if the code needs it at runtime, as the `Config` documentation shows. `Mix` is only for `mix.exs` and custom
   Mix tasks.

## 3.2 Reading it in code
1. **Read runtime configuration with `Application.fetch_env!/2` inside a function.** The Mix guide prefers `fetch_env!`
   to `get_env` because it raises when the key is missing, so the application does not boot half-configured.
2. **Never read the environment in a module attribute with `fetch_env!` or `get_env`.** At that point the environment
   may not be loaded: Elixir warns, and the call can raise because the application is not loaded or configured.
   The value would also be frozen at compile time, which in a release means baked in at build.
3. **When a compile-time value is really needed, use `Application.compile_env/3` in the module body.** Mix records the
   value and compares it with the runtime value at boot, and fails if they differ. Elixir's own text says compile-time
   environments should be avoided where possible. `compile_env` cannot be called inside a function.
4. **Do not change a `compile_env` key with `Application.put_env`.** The documentation says the compile environment
   must be set before compilation, in the config files.

## 3.3 Phoenix `force_ssl`
1. **`force_ssl` is a compile-time endpoint setting.** The Phoenix guide says it is normally set in `prod.exs` and
   does not work when set from `runtime.exs`. Set it there, and rebuild when it changes.
2. **`force_ssl` redirects everything except localhost.** Behind a proxy set `rewrite_on` for the forwarded headers,
   and exclude any other origin used for health checks (the guide's example excludes `localhost` and `127.0.0.1`).
