# typescript-patterns §5 — JavaScript platform habits in the browser

> Section 5 of `skills/typescript-patterns`. Read it when code serialises or parses numbers and dates, issues
> a request from a page, registers a listener, a timer or an observer, builds or parses a URL, writes into
> the DOM, or loads code on demand. What the browser owns as an environment (web storage that can refuse,
> the shape check after parsing, debounced input, console output, cross-window messages, the central error
> handler, the pre-consent inventory) is `skills/browser-runtime` and is not repeated here; this section is the
> language-and-platform layer under it. The other sections and the guardrails stay in `SKILL.md`.

1. **JSON round-trips are lossy, and two cases fail loudly.** Numbers beyond the safe integer range lose
   precision when parsed, so large identifiers travel as strings. Stringifying drops `undefined` and
   functions, throws on circular structures and on `BigInt`, and turns a `Date` into a string. A value that
   must survive a round trip is converted deliberately before and after (§7, point 7), not left to the
   default behaviour.
2. **`fetch` resolves on HTTP errors.** A 404 and a 500 are resolved responses; only a network failure or an
   abort rejects. The response's `ok` flag is checked before the body is used, a non-ok body is parsed
   separately because it often has another shape, and the code distinguishes a rejection (the request did not
   complete) from a refusal (the server answered no). A per-request deadline uses the platform's timeout
   signal, and the abort that follows is an expected outcome: it is not reported as an error.
3. **A superseded request is cancelled, not only ignored.** The abort signal goes to `fetch`; the owner of
   the request aborts it on unmount, on navigation and when a newer request replaces it. A debounce reduces
   how many requests are sent and does not order the responses, so the abort (or a "latest request wins"
   check) is what prevents an old answer from overwriting a new one.
4. **A listener is removed with the thing that owns it.** Remove with the same function reference and
   options it was added with, or register it with the abort-signal option so one abort removes a whole group,
   or with the once option when it fires one time. A listener that never prevents default on scroll or touch
   is registered as passive, so the browser does not wait for it before scrolling. Delegation on a stable
   ancestor replaces many listeners on many children.
5. **Timers and observers are released, and a repeating tick waits for its work.** A recursive timeout is
   preferred to an interval when each iteration must finish before the next begins, since an interval does
   not wait and queues overlap. Observers (intersection, resize, mutation) are disconnected at teardown. Work
   nobody can see is paused: loops check the page visibility state and stop while the tab is hidden, and
   visual updates run in an animation frame, not on a timer.
6. **URLs are built and parsed with the URL classes.** String concatenation produces unescaped separators and
   double slashes. The URL constructor with a base resolves relative references and throws on invalid input,
   so a user-supplied value is parsed inside a guard; query parameters go through the search-params class, and
   a single path segment or value is encoded with the component-level encoder. The same parser is the right
   tool for the scheme check on any user-supplied link (`skills/security-hardening` §1).
7. **Text goes into the DOM as text.** Setting the text content of an element cannot execute markup, where
   setting its inner HTML can. HTML from a string passes through a sanitiser at the point of use, with an
   allow-list; this is the framework-independent form of the template rules in the stack blocks.
8. **Numbers and dates use the platform's internationalisation.** Format dates, numbers, currencies, lists
   and relative times with the Intl classes and the user's locale; a hand-built date string is wrong in most
   locales. Parse numbers with an explicit radix, check finiteness, and keep money in integer minor units or a
   decimal library, because binary floating point makes 0.1 + 0.2 differ from 0.3.
9. **The online flag is a hint, not a fact.** A device can report itself online on a network with no
   internet. Handle the failed request, show the offline state from the failure, and retry only idempotent
   requests, with exponential backoff and jitter, stopping after a bound.
10. **Powerful APIs need a secure context, often a user gesture, and a refusal path.** Clipboard, geolocation,
    notifications, camera and similar APIs exist only on a secure origin, many only from a user action, and
    each can be denied or missing; the code path for denial is part of the feature, and so is the prompt's
    timing, which is tied to the action that needs it (never at page load).
11. **Rarely used code loads when it is used.** A heavy module needed on one screen or one rare action is
    imported dynamically at that point, with a visible loading state and a failure path for the case the
    chunk does not arrive (a deploy replaced it, the network dropped). Importing it eagerly makes every visitor
    pay for the feature a few use.
12. **A module's top level has no side effects.** Importing a module must not start requests, register global
    listeners or read the DOM, so tests, server rendering and tree-shaking behave; work starts from an
    explicit function that the application calls.
