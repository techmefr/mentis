---
name: vite-bundler-conventions
description: "Use when configuring or reviewing a Vite project: which environment variables reach the browser, dev-server exposure, pre-bundling and linked packages, production targets, chunking and stale-chunk errors, assets, SSR flags, TypeScript settings, and build and dev performance."
paths: "**/vite.config.*, **/vitest.config.*, **/index.html, **/.env, **/.env.*, **/vite-env.d.ts"
---

# vite-bundler-conventions

Step 6 of the pipeline (`WORKFLOW.md`), cross-stack: the bundler and dev server under Vue, React, Svelte and plain
TypeScript projects alike. **Status: a base to confront with real work**, no in-house project behind it yet (same
status as `go-conventions`). Pinned to **Vite 8** (Rolldown and Oxc based; read 2026-10-02 at 8.3.2). The
supply-chain half of a build (lockfiles, install-time scripts, release cooldown) belongs to
`skills/security-hardening` and `skills/devops-conventions`; this block states the bundler's own exposure and
settings. Webpack, Rspack and esbuild-only setups are not covered.

## When
As soon as `vite.config.*`, an `.env*` file, `index.html`, a `VITE_` variable, an asset import, a dynamic import or
a build script is written or modified, during `code` (6) or `ship` (9).

## Steps

### 1. What reaches the browser
1. **Every variable whose name starts with `VITE_` is written into the client bundle at build time.** It is
   public, not a configuration value. A secret never carries the prefix, and a key that must stay secret is
   used by a backend, a serverless or edge function. The prefix is changeable (`envPrefix`); changing it to an
   empty string or a broad one exposes everything, so it is a finding.
2. **Variables arrive as strings.** `VITE_FLAG=false` is truthy. Parse numbers and booleans once, in a typed
   module, and type the names by augmenting `ImportMetaEnv` in a `vite-env.d.ts` that contains **no `import`**
   (an import turns the file into a module and the augmentation silently stops working).
3. **Env files are not secrets stores.** Files are loaded in a fixed order (`.env`, `.env.local`, then
   `.env.[mode]`, `.env.[mode].local`; an existing process variable beats all of them). Keep `*.local` in
   `.gitignore`. Restart the dev server after editing an env file, as they load at start.
4. **Mode is not `NODE_ENV`.** `vite build` is mode `production` and `NODE_ENV=production`; `--mode staging`
   changes which `.env.staging` is read and not `NODE_ENV`. Branch on `import.meta.env.DEV` / `PROD` /
   `MODE`, never on a copy of the mode in your own variable. `import.meta.env.SSR` is statically replaced, so
   the unused branch is removed from each bundle.
5. **Constants in HTML use `%NAME%`** and are left untouched if undefined, unlike in JavaScript where they
   become `undefined`.

### 2. Dev server exposure
1. **Keep `server.host` at its default unless the device must be reached over the network.** Listening on all
   addresses exposes source and content to the LAN.
2. **`server.allowedHosts: true` and `server.cors: true` are findings.** They let any website reach the dev
   server through DNS rebinding or cross-origin requests and download source code. List the hosts and origins
   explicitly (a leading dot allows the domain and its subdomains).
3. **Leave `server.fs.strict` on** (the default) and widen `server.fs.allow` only for known directories, as
   setting it disables workspace-root detection. The default deny list protects `.env*`, key and certificate
   files; the public directory is **not** filtered, so nothing sensitive goes in `public/`.
4. **A dev server on a shared or remote machine is a service**: treat it like any other exposed port
   (`skills/security-hardening`).

### 3. Dependencies in development
1. **Dev pre-bundles dependencies** into ESM and merges packages made of many files, so one request replaces
   hundreds. It applies to dev only; a bug that appears only in dev can come from here.
2. **Linked workspace packages are treated as source** and are not pre-bundled; if one is not ESM, add it to
   `optimizeDeps.include`, and restart with `--force` after changing it. A dependency imported only through a
   plugin transform is not discovered by the scan: add it to `include` too.
3. **Barrel files hurt dev and bundles.** Importing one export from `./utils` loads and transforms every file the
   barrel re-exports. Import from the file (also a rule in `skills/angular-conventions` §1 for lazy chunks).
4. **Write extensions and use `moduleResolution: "bundler"`** so resolution checks one path instead of walking a
   list; narrowing `resolve.extensions` is allowed if node_modules still resolves.

### 4. Production build
1. **State the browser floor.** The default target is the "baseline widely available" set (Chrome 111, Edge 111,
   Firefox 114, Safari 16.4 at Vite 8). Syntax is transformed, **polyfills are not**: legacy browsers need the
   legacy plugin or a decision to drop them. Do not lower `build.target` without naming the audience.
2. **Set `base` for a nested public path** and use `import.meta.env.BASE_URL` for URLs you assemble yourself;
   it must appear literally because it is replaced statically.
3. **Chunking is configured through the Rolldown output options** (`build.rolldownOptions.output.codeSplitting`)
   or the framework's own setting. Do not hand-split vendors by habit; measure first (a bundle report).
4. **Handle stale chunks after a deploy.** A visitor holding an old page requests chunk files the new deploy
   deleted; the dynamic import fails. Listen for the `vite:preloadError` event and reload the page (or show a
   prompt); keep old assets for a while if the host allows.
5. **Assets: import them, don't point at them.** An imported asset gets a hashed name and is inlined below
   `assetsInlineLimit`; `?url`, `?raw`, `?inline` pick the form. Use `public/` only for a file referenced by
   no source, or one whose name must not change (`robots.txt`), and reference it by absolute root path.
6. **TypeScript for Vite**: set `isolatedModules: true` (the transformer works per file, without types, and
   cannot handle const enums or implicit type-only imports), add `vite/client` to `types` for asset and env
   typings, and remember the type check is a separate step (`tsc --noEmit`); the dev server does not run it.
7. **SSR is a low-level API** for framework authors. In an application, prefer the framework's integration; if
   you do wire it yourself, use middleware mode, build the client and the server entry separately, and branch
   with `import.meta.env.SSR`.
8. **Library mode** externalises the framework and outputs ES plus UMD or CJS; CSS comes out as a separate file
   to export from `package.json`; `process.env.*` is not replaced in library mode, so consumers can set it.

### 5. Speed
1. **Audit plugins first.** A slow `config`, `configResolved` or `buildStart` delays the server start; slow
   `transform` hooks create waterfalls. Profile with `vite --profile` or the debug flags before tuning.
2. **Warm up the few files that gate the page** with `server.warmup`, not the whole tree.
3. **Do less work**: plain CSS rather than a preprocessor where nesting and variables suffice; import SVGs as
   URLs or strings, not as framework components; avoid icon libraries that ship one file per icon.

## Output / checkpoint
A configuration whose exposed surface is stated (which variables are public, which hosts are allowed, which
browsers are targeted), the production build passing, and the type check passing separately. No dedicated
checkpoint: `gate` (7) and `review` (8).

## Guardrails
No comments in the code produced. Never an install: name the plugin, the person runs `pnpm add -D <package>`
(`CONVENTIONS.md`). Never put a secret in a `VITE_` variable, in `public/`, or in a file the dev server can
serve. Never set the allow-everything dev options for convenience. A rule marked with a number (a browser version,
a default) is the pinned major's; read `package.json` before applying it to another.

## Mechanical checks

```
grep -rnE "^VITE_.*(SECRET|PASSWORD|TOKEN|PRIVATE|KEY)" .env*
grep -rnE "envPrefix" vite.config.*
grep -rnE "allowedHosts: *true|cors: *true|host: *(true|'0\.0\.0\.0')" vite.config.*
grep -rnE "import\.meta\.env\.VITE_[A-Z_]+ *(===|==|!==) *(true|false)" src
grep -rnE "^import|^export .* from" src/vite-env.d.ts
grep -rnE "vite:preloadError" src
```

- A secret-looking name in a `VITE_` variable is a finding even when the value is a placeholder: the next person
  pastes the real one.
- Without a `vite:preloadError` listener, a deploy can break open tabs until reload.

## Origin
Rewritten from the official guide and configuration reference of Vite (documentation in the `vitejs/vite`
repository, MIT licence), read on 2026-10-02 from a shallow clone at the 8.3.2 release: environment variables
and modes, features and assets, build, dependency pre-bundling, performance, SSR, the server options, and the
migration guide from 7 to 8. Mechanisms and defaults are the project's, the rules, grouping and wording are ours;
no text was copied. **Facts that move, with their pin (Vite 8):** the default build target values, the move from
esbuild and Rollup to Oxc and Rolldown (an `esbuild` option is converted and deprecated), the Rolldown option
names, and the server defaults. **Not read, a stated gap:** the plugin API, the Environment API, worker options,
the JavaScript API, and the HMR API; Rspack, Webpack and Turbopack were not read. Refresh: re-read the migration
guide of the next major and the server and build option pages, give each pinned fact a verdict
(`skills/source-freshness` §3), stamp the date even when unchanged. Written 2026-10-02, never run on real work.
