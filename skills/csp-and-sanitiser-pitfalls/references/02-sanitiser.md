# csp-and-sanitiser-pitfalls §2 — Sanitiser

> Section 2 of `skills/csp-and-sanitiser-pitfalls`. Read it when untrusted HTML is rendered unescaped, or when
> the sanitiser's configuration, wrapper or runtime changes. Option names and behaviour are those of the
> DOMPurify README at commit `cde9599`, which describes release 3.4.16, read 2026-10-16. Sentences marked "own
> guidance" are ours. The README's own wiki pages (threat model, attack classes, default allow-list) were not
> read.

1. **Sanitise last and ship the string as it came out.** The README warns that sanitising and then modifying the
   markup can void the effect, and that a library you feed the sanitised markup to must not alter it. It also
   says that not mixing document contexts on the output side stays the caller's job. Own guidance: no
   concatenation, no template that re-parses it, no second sanitiser or markdown pass after it.
2. **`DOMPurify.removed` is for curiosity.** The README says what it lists was thrown out and tells you not to
   make any security-critical decision with it. Do not branch on it, log-and-allow on it or use it to reject
   input.
3. **Server-side, the DOM you choose is part of what you trust.** DOMPurify needs a DOM, usually jsdom, and the
   README strongly recommends the latest jsdom: older versions have known bugs that give XSS even when
   DOMPurify behaves correctly (it names attack vectors in jsdom 19.0.0 fixed in 20.0.0). It says happy-dom is
   not considered safe and combining it with DOMPurify will likely lead to XSS. A third-party edge-runtime
   wrapper is mentioned and explicitly not endorsed. Own guidance: pin the jsdom version in the lockfile and
   update it together with DOMPurify.

   ```js
   import { JSDOM } from "jsdom";
   import DOMPurify from "dompurify";

   const window = new JSDOM("").window;
   const purify = DOMPurify(window);
   const clean = purify.sanitize(dirty);
   ```
4. **Narrow the default, and do not stack settings that override each other.** By default HTML, SVG and MathML
   are all allowed. `USE_PROFILES: { html: true }` limits it to HTML; the README's comment says
   `USE_PROFILES` overrides `ALLOWED_TAGS`, so the two must not be used together. A strict single-purpose
   allow-list is `ALLOWED_TAGS: ['b']`.
5. **Widen the allow-list deliberately.** `ADD_TAGS`, `ADD_ATTR` and `CUSTOM_ELEMENT_HANDLING` extend what
   survives. The README asks you to read its "tags and attributes to think twice about" page first, because a
   few are dangerous in non-obvious ways. Custom elements are all refused by default and the default values
   are described as very restrictive to prevent accidental bypasses. `ADD_TAGS` and `ADD_ATTR` accept
   functions, so an addition can be scoped to one tag instead of applied everywhere.
6. **Treat these toggles as needing a written reason.** The README labels each one risky: `SAFE_FOR_XML: false`
   (only if you handle HTML and nothing else, otherwise XSS), `ALLOW_UNKNOWN_PROTOCOLS: true` (the default
   allows `http`, `https`, `ftp`, `ftps`, `tel`, `mailto`, `callto`, `sms`, `cid`, `xmpp` and `matrix`),
   `ADD_URI_SAFE_ATTR`, `SANITIZE_DOM: false` (minor XSS risk) and `SAFE_FOR_TEMPLATES: true` (not recommended
   for production; allowing template parsing in user-controlled HTML is not advised at all).
7. **A URI regexp runs on attacker values.** The README's note on `ALLOWED_URI_REGEXP` says to keep the pattern
   linear-time. Apply `regex-validation-pitfalls` §2 to it.
8. **Check `isSupported`.** On legacy browsers such as Internet Explorer DOMPurify does nothing and returns
   exactly the string you gave it; the `isSupported` property tells you whether it can work, so you can plan
   your own fallback. Own guidance: when it is false, render the value as text rather than as HTML.
9. **Creating a Trusted Types policy around it.** When Trusted Types is available and `RETURN_TRUSTED_TYPE` is
   `true`, DOMPurify tries to return a `TrustedHTML` value. Inside a policy's `createHTML`, which expects a
   plain string, pass `RETURN_TRUSTED_TYPE: false`. With no policy supplied DOMPurify tries to create its own
   named `dompurify`; if the page already has a strict policy list (for example `trusted-types
   my-organization`) that does not allow that name, the browser blocks it and logs a warning and a CSP
   violation. Calling it from your own policy with `TRUSTED_TYPES_POLICY: null` avoids both.

   ```js
   window.trustedTypes.createPolicy("my-organization", {
     createHTML: (input) =>
       DOMPurify.sanitize(input, { TRUSTED_TYPES_POLICY: null }),
   });
   ```
10. **Never hand your wrapping policy back to DOMPurify.** Passing a policy whose `createHTML` already calls
    `DOMPurify.sanitize` as `TRUSTED_TYPES_POLICY` is circular; DOMPurify throws a `TypeError` to stop the
    recursion. The direction is: your policy calls DOMPurify, never the reverse.
11. **`sanitize()` is not re-entrant.** The README says not to call it from a hook or from a configuration
    callback such as `tagNameCheck` or `attributeNameCheck`: the nested call re-reads its own configuration and
    replaces the one the outer pass is still using, so a strict allow-list can silently widen to the default
    part-way through a document. Either set the configuration once with `setConfig`, or collect the nested
    fragments and sanitise them after the outer call returns.
12. **One persistent configuration at a time.** After `DOMPurify.setConfig` there is a single active
    configuration, and extra parameters passed to `sanitize` are ignored until `clearConfig`. Own guidance: a
    call site that passes options and silently gets none is a bug a test should catch, so assert on the output
    of one hostile sample per call site.
13. **Hooks: `afterSanitize*` hooks are not re-checked.** The README says whatever is written there is not
    validated again, and that attacker-influenced values should go through the `uponSanitize*` hooks. It also
    prefers `keepAttr` and `forceKeepAttr` on the hook event over writing to the allow-list objects, because
    the per-node flags cannot leak between calls.
14. **Node input and in-place mode.** Sanitise an attacker-controlled tree before connecting it to the live
    document: the README says DOMPurify cannot undo engine mutations that fired before the call. For closed
    shadow roots it says to pass untrusted markup as a string, since nodes produced by `setHTMLUnsafe` or
    `parseHTMLUnsafe` can carry a closed root that it can neither see nor sanitise.
15. **Follow its security releases.** The project runs a mailing list for security-critical releases and says a
    release always follows when a bypass is found. Own guidance: treat a DOMPurify or jsdom update as a security
    fix to apply promptly, not a routine bump (`package-manager-supply-chain-pitfalls` covers when a
    dependency-update cooldown should give way).
