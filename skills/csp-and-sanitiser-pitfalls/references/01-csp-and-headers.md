# csp-and-sanitiser-pitfalls §1 — CSP and security headers

> Section 1 of `skills/csp-and-sanitiser-pitfalls`. Read it when a response header policy is written, loosened
> or reviewed. Defaults and option names are those of the Helmet README at package version 8.3.0 (commit
> `876101e`), read 2026-10-16; they change between releases. Sentences marked "own guidance" are ours.

1. **Know the default policy before editing it.** Helmet's default `Content-Security-Policy` is: `default-src
   'self'`, `base-uri 'self'`, `font-src 'self' https: data:`, `form-action 'self'`, `frame-ancestors 'self'`,
   `img-src 'self' data:`, `object-src 'none'`, `script-src 'self'`, `script-src-attr 'none'`, `style-src 'self'
   https: 'unsafe-inline'` and `upgrade-insecure-requests`. The README says the header is powerful but likely
   needs configuration for your app, so the default is a starting point to read, not a finished policy.
2. **Your directives are merged into that default; `null` removes one.** Passing `script-src` replaces the
   default value for that directive and leaves the others; setting a directive to `null` drops it (the README's
   example disables the default `style-src`); `useDefaults: false` starts from an empty policy. Own guidance:
   the configuration object is not the header, so read the value from a real response after every change.
3. **Inline styles are allowed by the default; inline scripts are not.** `style-src` carries `'unsafe-inline'`
   while `script-src` is `'self'` and `script-src-attr` is `'none'`. Own guidance: an inline script block or an
   inline event handler therefore stops working under the default, and the fix is an external file or a nonce
   (§1.4), never `'unsafe-inline'` on `script-src`.
4. **Use a fresh random nonce per response.** The README's pattern: a middleware that runs before Helmet draws
   32 random bytes per request, hex-encodes them into `res.locals`, and a function value in `script-src`
   returns `'nonce-<value>'`; Helmet calls such functions with the request and response. Own guidance: the
   same value must reach the `nonce` attribute of each script tag in the template, and a nonce that is the
   same on every response is just a constant an attacker can read once.

   ```js
   app.use((req, res, next) => {
     res.locals.cspNonce = crypto.randomBytes(32).toString("hex");
     next();
   });
   app.use(
     helmet({
       contentSecurityPolicy: {
         directives: {
           scriptSrc: ["'self'", (req, res) => `'nonce-${res.locals.cspNonce}'`],
         },
       },
     }),
   );
   ```
5. **Roll a new policy out in report-only mode first.** `reportOnly: true` makes Helmet send
   `Content-Security-Policy-Report-Only` instead of the enforcing header. Own guidance: use it to see what a
   policy would break before enforcing; the README shows the option but not a reporting endpoint, so wiring one
   and reading its output is your work.
6. **Helmet checks almost nothing about the policy.** The README says it performs very little validation and
   points to a CSP checker (it names CSP Evaluator). A policy that Helmet emits without complaint can still be
   weak, so run the final header through an evaluator and a browser console.
7. **Removing `default-src` is a deliberate act.** It can be disabled with
   `helmet.contentSecurityPolicy.dangerouslyDisableDefaultSrc`, which the README says is not recommended.
8. **`frame-ancestors` supersedes `X-Frame-Options`.** The README calls the header legacy but still useful on
   old browsers or when no CSP is used; its default is `SAMEORIGIN`, accepted values are `DENY` and
   `SAMEORIGIN`, and the `ALLOW-FROM` directive is not supported by Helmet. Own guidance: express an embedding
   allow-list with `frame-ancestors`, and keep the old header only as the fallback.
9. **`X-XSS-Protection` is sent as `0`.** Helmet disables the browsers' buggy XSS filter by setting the legacy
   header to `0`; the README marks turning that off as not recommended. Do not "enable" the filter.
10. **HSTS: development and preload.** The default is `max-age=31536000; includeSubDomains` (365 days). `preload`
    is off by default and only expresses intent to add the policy to browsers. The README suggests disabling the
    header in local development because it can make the browser force `http://localhost` to
    `https://localhost`, which breaks other apps on the same name. Own guidance: before shipping, confirm every
    subdomain serves HTTPS, because `includeSubDomains` is on by default; preload is a separate decision whose
    consequences the README leaves to the linked MDN page, which was not read here.
11. **`upgrade-insecure-requests` in development.** It is in the default policy, and the README notes that Safari
    upgrades `http://localhost` to `https://localhost`, and suggests disabling the directive in development. In the
    sample below `null` drops the directive in development and `[]` keeps it, with no values, everywhere else.

    ```js
    const isDevelopment = app.get("env") === "development";
    app.use(
      helmet({
        contentSecurityPolicy: {
          directives: {
            "upgrade-insecure-requests": isDevelopment ? null : [],
          },
        },
        strictTransportSecurity: isDevelopment ? false : { maxAge: 31536000 },
      }),
    );
    ```
12. **Not every isolation header is on.** Defaults set `Cross-Origin-Opener-Policy: same-origin`,
    `Cross-Origin-Resource-Policy: same-origin` and `Origin-Agent-Cluster: ?1`; `Cross-Origin-Embedder-Policy` is
    not set unless you opt in (`require-corp` or `credentialless`). The README says the resource policy blocks
    others from loading your resources cross-origin in some cases, so a resource meant to be embedded by
    another site needs that header relaxed on its route (the README shows `same-site`; other values are on the
    MDN page it links, not read here).
13. **`Referrer-Policy` defaults to `no-referrer`.** The policy can be an array, joined with commas, to give a
    fallback. Own guidance: the default suits pages that carry a one-time token in the URL
    (`credential-lifecycle-pitfalls` §2.4), and loosening it site-wide reopens that leak.
14. **Removing `X-Powered-By` is cosmetic.** The README says it offers very limited security benefit and that
    Express has its own switch for it. Do not count it as a control.
