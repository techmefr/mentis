# svelte-conventions §3 — SvelteKit: data, forms, errors, security, rendering

> Section 3 of `skills/svelte-conventions`. Read it when a route, a `load`, an action, a hook, an environment
> variable or a rendering option is touched. Pinned to **SvelteKit 3.0** (Node 22.17+, Svelte 5.57+,
> TypeScript 6, Vite 8, per its migration guide); `Kit 3` marks what changed against 2.x.

1. **A server has no per-user memory.** Servers are long-lived and shared: a module-level variable written by a
   request is read by the next user. Authenticate through cookies and persist to a database. Keep `load`
   functions pure: return data, do not write to a store or global.
2. **Pick the `load` kind by what it needs.** `+page.server` / `+layout.server` runs only on the server, so it
   may read a database, the filesystem, private variables and cookies, and must return data the framework can
   serialise. `+page` / `+layout` (universal) runs on the server during the first render and in the browser
   afterwards, suits calling an external API without private credentials, and can return non-serialisable
   values. When both exist, the server result is the `data` the universal one receives.
3. **Use the supplied `fetch` in `load`.** It forwards the page's cookies and authorization header on the
   server, allows relative URLs, calls internal routes without an HTTP hop, and replays the server response in
   hydration instead of refetching. Cookies reach only the same host or its subdomains; for anything else use
   the `handleFetch` hook, deliberately.
4. **Avoid waterfalls.** Independent requests start together (all `load` functions run concurrently); call
   `await parent()` only when the result is needed, and after the unrelated requests have started. A universal
   `load` that chains API calls from the browser pays a round trip per step; move the chain to a server `load`.
   Stream slow, non-essential data as unawaited promises in a server `load`, and give each streamed promise a
   rejection path, since a promise that rejects before rendering starts can crash the server. Headers, status
   and redirects cannot change inside a streamed promise.
5. **`redirect()` and `error()` throw; never call them inside a `try` whose `catch` swallows them.** Use them
   from helpers to stop execution. Since 2.x you do not `throw` them yourself.
6. **Mutations are form actions (or remote functions), which are `POST`.** An action reads
   `request.formData()`, returns data or `fail(status, { …values })` with the previously entered values (never
   the password), or redirects. A page cannot mix a `default` action with named ones. Progressively enhance with
   `use:enhance`, which only works on `method="POST"` forms pointing at actions. The form must work without
   JavaScript. After an action, `load` reruns but `handle` does not: update `locals` yourself when the action
   changes the session cookie.
7. **Treat every action and `+server` handler as a public endpoint**: authenticate and authorise inside it
   (`locals` is filled by `handle`), validate the input with a schema, return only safe fields. Remote-function
   `route`, `params` and `url` in `handle` describe the calling page, never the endpoint, so do not authorise
   from them.
8. **CSRF protection is always on in Kit 3** for form submissions and remote functions: cross-origin mutating
   requests are rejected, including those with no `Content-Type`. Allow a specific external origin with
   `csrf.trustedOrigins` (replaces `csrf.checkOrigin`, removed in Kit 3), and set `paths.origin` to the
   public origin when the server cannot derive it behind a proxy (adapter-node derives it from the `host`
   header otherwise).
9. **Errors have four kinds and one hook.** `handleError` runs for every error with `kind` `app` (from
   `error()`, safe to show), `framework` (a 404, 405, 413; terse and safe), `validation` (a remote-function
   argument; issues are not exposed unless you return them) and `unknown` (anything else, never shown to the
   user). Use it to log and to return a safe object, and never let it throw. Do not log routine 404s. A
   `+error.svelte` catches errors in `load` and rendering for its subtree; an error in the root layout falls
   back to `error.html`. Use `<svelte:boundary>` for a finer scope.
10. **Environment variables are declared, typed and split private or public.** Kit 3 declares them in
    `src/env.ts` with `defineEnvVars` and imports from `$app/env/private` (server only; the build refuses to
    bundle it for the browser) and `$app/env/public`; the old `$env/*` modules are deprecated and go in Kit 4.
    A validator (a Standard Schema library or a function) makes an invalid value fail at start or build.
    `static: true` inlines the value and lets the bundler drop dead branches. In 2.x, use the `$env/*`
    modules and the same private/public split.
11. **Auth: choose sessions or tokens knowingly.** A session id in a database can be revoked at once but costs
    a lookup per request; a signed token (JWT) is checked without a datastore and cannot be revoked at once.
    Check cookies in `handle` and put the user in `locals`; prefer an established library over writing one.
12. **Page options say how a route renders.** Prerender only a page that every visitor sees identically; a page
    with actions cannot be prerendered; `url.searchParams` cannot be read while prerendering; a route marked
    `prerender = true` that the crawler cannot reach fails the build, so list its `entries` or use `'auto'`.
    SPA mode causes request waterfalls (an empty page, then the script, then the data).
13. **Keep state that must survive a reload in the URL** (filters, sort) and disposable UI state in a
    `snapshot`. Page and layout components are reused across navigations: values derived from `data` must be
    `$derived`, and code that has to rerun on navigation uses the navigation hooks, not `onMount`.
14. **Performance basics from the framework's own page**: preload fonts deliberately (they are not preloaded
    by default), use the image plugin for sized, modern-format images, lazy-load rarely used code with dynamic
    `import()`, keep third-party scripts few, host the frontend next to the backend, and measure the
    production build in preview mode, not in dev. Avoid icon libraries that ship one file per icon.
15. **Kit 3 changes to check on upgrade**: configuration lives in the Vite plugin, not `svelte.config.js`;
    the `$lib` alias becomes a `#lib` subpath import declared in `package.json`; `$app/environment` is
    `$app/env`; `use:enhance` forms posting to another page navigate to it. Run the official migration command
    once the project is on the last 2.x.

## Mechanical checks

```
grep -rnE "^(export )?(let|const|var) [a-zA-Z_]+ *=" src/routes src/lib --include=+*.server.ts --include=hooks.server.ts
grep -rnE "\\\$env/(static|dynamic)|\\\$app/env/(private|public)" src
grep -rnE "csrf|trustedOrigins|checkOrigin|paths:.*origin" vite.config.* svelte.config.js 2>/dev/null
grep -rnE "redirect\(|error\(" src/routes | grep -B0 "try"
grep -rnE "export const (prerender|ssr|csr)" src/routes
```

- A mutable module-level variable in a server file is rule 1 until proven constant.
- `checkOrigin: false` or a wildcard trusted origin is a finding.
