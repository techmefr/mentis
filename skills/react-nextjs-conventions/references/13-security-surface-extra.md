# react-nextjs-conventions §13 — Further security surface

> Section 13 of `skills/react-nextjs-conventions`. Read it when a link opens a new window, a page ships
> inline data to the browser, an object from outside is merged into another, a third-party widget or script is
> added, or the production build configuration is touched. It extends §9 (secrets, `dangerouslySetInnerHTML`,
> URL schemes, redirects, tokens, Server Component payloads), which it does not repeat; the background is
> `skills/security-hardening`. The other sections and the guardrails stay in `SKILL.md`.

1. **A link that opens a new browsing context does not hand over the opener.** Current browsers treat a
   `target="_blank"` link as `noopener` by default, but the attribute is still written explicitly as
   `rel="noopener"`, and `noreferrer` is added when the destination must not learn which page the user came
   from. A link to a user-supplied address additionally passes the scheme check of §9, point 6. The lint rule
   for it stays on, since older embedded browsers do not apply the default.
2. **Data serialised into an inline script is escaped for a script context.** A page that embeds state as
   JSON in a script tag is a sink: a string containing a closing script tag ends the block and starts the
   attacker's. The framework's own mechanism escapes this; a hand-written inline script, a JSON-LD block or a
   preloaded-state blob built with plain JSON serialisation is escaped for `<`, `>`, `&` and the line
   separators, or serialised by a library that does it (`skills/seo` for structured-data blocks).
3. **Merging an outside object into another is guarded against the prototype.** A recursive merge or a
   path-based setter fed with parsed JSON can write to the object prototype through a `__proto__` or
   `constructor` key, changing every object in the process. Use a merge that ignores those keys, build
   targets without a prototype where they are lookup tables, or validate the input into a known shape
   first (§9, validation at boundaries). A spread of an object into props or options copies whatever keys
   it has, so spread only objects your own code constructed.
4. **A content security policy is deployed, and starts strict.** A policy that forbids inline script unless
   it carries a per-response nonce, restricts script, frame and form targets, and reports violations turns
   many injection bugs into console errors. The nonce is generated per request in middleware and passed to
   the framework's script tags; a static value is no protection. Roll it out in report-only mode, fix what it
   reports, then enforce; a permissive wildcard or an unsafe-inline source defeats the point.
5. **A third-party component or script runs with the page's rights.** Pin its version in the lock file, load
   it from one declared place, give a script from another origin an integrity hash, and review what it loads
   in turn; a tag manager hides the list behind a dashboard. A component whose props accept an HTML string is
   `dangerouslySetInnerHTML` under another name and follows §9, point 5. An iframe from another origin gets
   the sandbox attribute with the fewest permissions that work, and its messages are accepted only after
   the origin is checked.
6. **Message listeners check the origin and the shape.** A `message` event handler verifies the sender's
   origin against an allow-list and validates the payload before using it; "any window can post here" is the
   default and is almost never the intent.
7. **Production builds do not publish the source or the toolchain.** Source maps are generated for the
   error tracker and not served publicly unless the project decides to; the header that announces the
   framework is removed; development-only code paths and debugging helpers are removed by the build and
   checked in the built output. The environment variables inlined into the bundle are listed and each read as
   public (§9, point 3).
8. **Form submissions and mutations carry their own anti-forgery.** A server action carries an origin check
   (§9, point 11); a route handler or an API called from the page with the session cookie gets a token or an
   origin check of its own, and cookies that carry a session are `SameSite`. A GET request never changes
   state, since links, prefetching and image tags all issue GETs.
9. **Uploads are checked on the server and stored away from the application.** The client's file type and
   size checks are conveniences; the server verifies the type from the content, limits size, renames the
   file, and stores it outside the served directory or on a separate origin (`skills/security-hardening` §4).
10. **Rendering a user's content in a rich-text editor and back is a round trip through a sanitiser.** The
    editor's output is HTML or a document tree, and both go through the allow-list sanitiser before display
    (§9, point 5), not only on input; stored content may predate the sanitiser.
