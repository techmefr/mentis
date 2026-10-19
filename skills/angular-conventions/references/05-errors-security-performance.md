# angular-conventions §5 — Errors, security, performance and accessibility

> Section 5 of `skills/angular-conventions`. Read it when an error path, a binding to a URL or to HTML, a lazy
> boundary or an interactive control is written. The other sections and the guardrails stay in `SKILL.md`.

## Errors

1. **Handle an error where the operation was started.** The code that called the API has the context to pick a
   message, a retry or a state; use `try` / `catch` or `catchError` there. Angular reports to the global
   `ErrorHandler` only what it ran itself (a constructor, a lifecycle hook, an async-pipe subscription); it
   does not catch an error thrown by a service method that your component called.
2. **The global `ErrorHandler` is for reporting, not recovery.** Provide a custom one in the application
   config to forward unexpected errors to logging or error tracking, with the route and message. An error that
   reached it may mean corrupted state.
3. **Keep the global listeners on.** `provideBrowserGlobalErrorListeners()` forwards `error` and
   `unhandledrejection` to the handler; the CLI adds it to new applications. Remove it only when you install
   your own listeners.
4. **A `resource` shows its error in `status` and `error`**, and the async pipe forwards to the handler: those
   are the contracts under which Angular catches async errors for you. Any other promise or observable is yours
   to catch.
5. **`@boundary` / `@error` wraps a section of template in a fallback** (developer preview; check the preview
   status before relying on it). `$reset` retries, `when` clauses go from most to least specific, and a final
   clause without `when` is the catch-all. It does not catch errors in content projected into a wrapper, because
   that content belongs to the declaring view: wrap the wrapper and its projected content together.
6. **Errors thrown while the root component is still being created cannot reach the handler.** Custom elements
   defined while their tag is already in the page are the usual case; defer the throwing code until bootstrap
   finishes.

## Security

7. **Treat every bound value as untrusted, every template as code.** Interpolation escapes. Binding to
   `innerHTML` is sanitised by the framework, which removes dangerous content and can alter the rest;
   sanitisation depends on the context (HTML, style, URL, resource URL), and resource URLs cannot be sanitised
   at all.
8. **Never build a template from a string that contains user input**, on the client or on the server. Compile
   templates ahead of time (the default in the CLI) and never ship the JIT compiler to production. Build dynamic
   forms from a data description, and generate server HTML with an escaping template language, never with
   Angular template syntax.
9. **`bypassSecurityTrustHtml`, `...Script`, `...Style`, `...Url` and `...ResourceUrl` are audit points.** Each
   needs a stated reason, the narrowest context, and a value built in a component method from a validated piece
   (a video id checked against a pattern, then composed into a URL), never from a raw user string. Where Trusted Types are
   enforced, any use also requires the `angular#unsafe-bypass` policy to be allowed.
10. **Avoid direct DOM access** (`document`, an `ElementRef` native element, third-party DOM libraries) with
    untrusted data; where unavoidable, run the value through `DomSanitizer.sanitize` with the right
    `SecurityContext`.
11. **Add a Content Security Policy and Trusted Types enforcement** as defence in depth: the minimal policy for a
    new application is `default-src 'self'` plus nonce-based `style-src` and `script-src`. The nonce is unique,
    unpredictable and per response: pass it through the `ngCspNonce` attribute or the `CSP_NONCE` token. Do not
    generate a nonce at an origin whose response a CDN caches, since every visitor then gets the same value;
    generate it at the edge, or use hashes (`security.autoCsp`, not usable with server rendering, covers scripts
    only, and `frame-ancestors`, `report-uri` and `sandbox` are ignored in a meta tag).
12. **Cross-site request forgery protection is a two-sided contract.** The built-in interceptor copies an
    `XSRF-TOKEN` cookie into an `X-XSRF-TOKEN` header on mutating same-origin requests, but only protects
    anything if the server sets the cookie and verifies the header. Give each application sharing a domain its
    own cookie name; rename with `withXsrfConfiguration`; disabling it with `withNoXsrfProtection` needs a
    replacement named in the same change.
13. **Server rendering validates the `Host` and forwarded headers against an allow-list.** Configure
    `allowedHosts` explicitly, never `*` unless another layer validates the headers, and enable
    `trustProxyHeaders` only behind a proxy that overwrites them.
14. **Keep Angular current and unmodified.** Security fixes ship in releases; a private fork falls behind them.

## Performance

15. **Prefer `OnPush`-compatible components and signals.** `OnPush` is the default from v22; before that, set it
    explicitly. A subtree is re-checked only when it gets a new input by template binding, handles an event, or
    is marked dirty; mutating an object while keeping its reference does not count as a new input.
16. **New applications are zoneless** (the default from v21). Do not add `provideZoneChangeDetection`
    over it. Change detection is notified by `markForCheck` (the async pipe calls it), `ComponentRef.setInput`,
    a signal read in a template, or a bound listener. Replace `NgZone.onStable`, `onMicrotaskEmpty` and
    `isStable` (they never fire or are always true) with `afterNextRender`, `afterEveryRender` or a
    `MutationObserver`. `NgZone.run` and `runOutsideAngular` may stay: removing them can regress libraries used
    by zone-based applications.
17. **Register asynchronous work that should block server serialisation with `PendingTasks`** in a zoneless
    application, via `run` or `add` and the cleanup in `finally`.
18. **Keep slow computations out of templates and hooks.** Fix the algorithm first, then a pure pipe (re-run
    only when inputs change) or memoisation (several results, more memory). Do not force layout reads in
    hooks that run every cycle.
19. **Defer what is not needed for first paint with `@defer`.** Only standalone dependencies not referenced
    outside the block are deferred; give nested blocks different triggers to avoid a request cascade; never
    defer content visible in the first viewport, which shifts layout; `idle` is the default trigger; the
    server renders the `@placeholder` unless incremental hydration is configured. A barrel import defeats it
    (§1.9).

## Accessibility

20. **Pass the accessibility engine and WCAG AA** as the framework's own best-practice file requires: focus
    management, contrast and ARIA. The engine finds a fraction, the manual pass is `skills/accessibility`.
21. **Bind ARIA through attribute binding**, and use property binding for the ones that take element
    references. Prefer the native element (§2.17); for custom widgets use the CDK or the headless ARIA
    directives rather than rebuilding keyboard behaviour.
22. **After a navigation, move focus** to the main content heading from the `NavigationEnd` event so focus does
    not fall back to the body; mark the active link with `aria-current` through
    `ariaCurrentWhenActive`, since the active class is only a visual cue.
23. **Wrap a `@defer` block in a live region** so a screen reader hears the placeholder, loading and final
    states change.

## Mechanical checks

```
grep -rnE "bypassSecurityTrust|innerHTML|outerHTML|ElementRef.*nativeElement|document\." src
grep -rnE "provideZoneChangeDetection|NgZone\.(onStable|onMicrotaskEmpty|isStable)" src
grep -rnE "allowedHosts|trustProxyHeaders" angular.json src server.ts 2>/dev/null
grep -rnE "withNoXsrfProtection|HTTP_INTERCEPTORS" src
grep -rnE "Content-Security-Policy|CSP_NONCE|ngCspNonce" src server.ts angular.json 2>/dev/null
```

- Every `bypassSecurityTrust` hit is read against rule 9; an unexplained one is a finding.
- A `*` in `allowedHosts` is a finding unless the review names the layer that validates the headers.
