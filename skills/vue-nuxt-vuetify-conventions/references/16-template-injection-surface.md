# vue-nuxt-vuetify-conventions §16 — The template and bundle injection surface

> Section 16 of `skills/vue-nuxt-vuetify-conventions`. Read it when a template binds a URL, a style, a
> dynamic component or an attribute from data, when HTML is rendered from a string, when a variable is
> exposed to the browser, or when a server route calls out. This section adds to §11's `v-html` and input
> rules and does not repeat them; the background (what XSS, SSRF and secret leakage are) is in
> `skills/security-hardening`. The other sections and the guardrails stay in `SKILL.md`.

1. **Know what the template escapes and what it does not.** Text interpolation and the *value* of an
   attribute binding are escaped. Not escaped, and so each a sink needing its own rule: HTML rendered from
   a string, a URL placed in a link or source attribute, a component chosen at run time, a style string, an
   attribute or event *name* taken from data, and a whole object spread onto an element. A review of a
   template starts from this list, not from "Vue escapes everything".
2. **A URL from data is parsed and checked by scheme, not inspected as text.** A link whose target begins
   with a script scheme runs code when clicked; a prefix test or a pattern over the string is bypassed by
   case, whitespace and encoded characters. Parse it with the platform URL parser against a base, compare
   the resulting protocol with a short allow-list (web, mail, telephone), and fall back to a safe value
   when it fails. This applies to every attribute that takes a URL (link, source, form action) and to
   programmatic navigation and window opening, and an in-app redirect target stays on the same-origin
   allow-list of §11.
3. **A dynamic component comes from a closed map.** `<component :is>` fed a string from data lets the data
   choose what renders; map a known key to an imported component and render nothing for an unknown key.
   Never compile a template from user text: the full build includes the compiler, and a template is
   code.
4. **A style string from a user is a request to the browser.** A raw style value can load an external
   resource, reposition an element over a button or hide a warning. Bind an object whose property names come
   from your code and whose values are validated (a colour, a length) and choose classes from a closed set.
5. **Never take an attribute name or an event name from data, and never spread a user-built object.**
   Binding an object applies each key as an attribute or a DOM property, including the ones that
   interpret their value as HTML. Spread only objects your own code constructed, and pick known keys from
   anything that crossed a boundary.
6. **When HTML must be rendered, sanitise at the sink with a maintained allow-list sanitiser.** Sanitise
   immediately before binding, with a configuration that lists permitted tags and attributes rather than
   removing known-bad ones, and do not alter the string afterwards. Sanitising on the server before
   storing is good defence in depth and never a substitute, since the stored value reaches other clients.
   Rendered markdown is HTML and follows the same rule. A translation message that needs markup is
   rendered with the i18n library's component interpolation, never through `v-html` (§6).
7. **A browser-enforced second line costs little.** A content security policy that forbids inline script and
   restricts script sources turns many injection bugs from a compromise into a console error; where the
   platform supports trusted types, a policy that routes the few HTML sinks through the sanitiser makes a new
   unsanitised sink fail at run time. Neither replaces points 1 to 6.
8. **A variable exposed to the browser is public.** Everything the bundler inlines by prefix (the build
   tool's client prefix, the framework's public runtime configuration, the application configuration file)
   ships to every visitor. A secret placed there is published at the next deploy, and the `.env` file is
   not where to check: open the built output, or list the prefixed names and read each as if it were on the
   front page.
9. **The server-rendered payload is public too.** Whatever the page-data composables, shared state or
   public runtime configuration carry is serialised into the HTML. Return the fields the page renders, not
   the record; never place a token, a secret or another user's data in them; and do not echo runtime
   configuration into state, which copies a private key into the payload.
10. **Session material is not stored in script-readable storage.** A raw token in local or session storage
    is one injected script away from theft; the session cookie is `HttpOnly`, `Secure` and `SameSite`, as
    §11 states for the CSRF cookie, and the protocol is in `skills/auth-session-conventions`.
11. **Validate every server input, all three channels.** Body, query string and route parameters each go
    through the framework's validating readers with a schema; reading them raw and validating "later" leaves
    a path where the handler uses the unvalidated value. A failure answers with an HTTP error and a message
    written for the caller, never the underlying exception text or a stack.
12. **A server-side request to a user-influenced address is an SSRF.** A route that fetches a URL it was
    given runs with the server's network access. Fix the base address in configuration, take only the path
    or an identifier from the caller, refuse absolute URLs, do not follow redirects blindly and refuse
    private and link-local ranges (`skills/security-hardening` §2 carries the full defence).
13. **Forward credentials narrowly in both directions.** Server-side calls to the application's own API
    forward the incoming cookie through the request-bound fetch (§9), never the full header set, and never to
    a third-party origin. A `Set-Cookie` from the backend reaches the browser only because a handler relays
    it on purpose.
14. **A third-party script or component is a code dependency with the privileges of the page.** Load each
    through one declared place in the configuration, pin the version, add a subresource integrity hash for a
    script served from another origin, and treat a component prop that takes an HTML string as the same sink
    as point 6. A tag manager that loads further scripts widens the list without a diff.
15. **Production builds do not publish what the build knows.** Source maps are uploaded to the error
    tracker and not served to the public unless the project decides otherwise, the development tooling is not
    part of the production bundle, and the response does not announce the framework and version.
