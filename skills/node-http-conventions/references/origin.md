# node-http-conventions — origin and source stamps

> Provenance of `skills/node-http-conventions`. Read it when a rule has to be traced back to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

Block created 2026-10-02, every rule from a document **read that day** (rule B: mechanisms rewritten in the
house voice, no prose copied). A fact not found in a read source was left out rather than recited.

| Source (public repository, read 2026-10-02) | Licence | Used for |
|---|---|---|
| Express website sources (`expressjs/expressjs.com`, English 5.x guides): error handling, behind proxies | CC BY 4.0 (repository `LICENSE.md`, read: "Attribution 4.0 International") | §1.1 to §1.7. Rewrite with credit. |
| Fastify documentation (`fastify/fastify`, `docs/`, main branch): Recommendations, Validation and Serialization, Hooks, Testing | MIT (repository `LICENSE`, read) | §2. Rewrite with credit. |
| Helmet README (`helmetjs/helmet`) | MIT (repository `LICENSE`, read) | §1.8. |

**Left out:** NestJS, Koa, Hono, serverless adapters, the Helmet FAQ, rate limiting and process-manager choice
(only mentioned by the Express pages, no rule written).

**Version stamp.** Express documentation at major 5 (the 4.x guides sit beside it and differ on async handling).
Fastify documentation as of the main branch on the read date; the version was not recorded in the pages read,
so check the installed major before relying on option names. Helmet at its current README (default header count
may change). Expiry: when the framework major changes (`skills/source-freshness` §2.1) re-read §1.1, §1.7 and
§2.2 first.

**Status.** 🟡, "base to confront with the real thing", like `go-conventions`. Nothing here was run against a
Node service.

## Source pass 2026-10-20

Read this day, as facts rewritten in our words, nothing copied: the Express site pages for security best
practice, performance best practice and the 5.x migration guide (site and repository licence: the repository
`LICENSE.md` read again, title "Creative Commons Attribution 4.0 International Public License", CC BY 4.0, credit
kept); from `fastify/fastify` (MIT, licence read 2026-10-02) the Server, Lifecycle and Encapsulation reference
pages on the default branch; the Helmet README (`helmetjs/helmet`, MIT, licence read 2026-10-02) re-read for the
default header list (13 confirmed, X-XSS-Protection sent as `0`) and the CSP option behaviour.

Result: Express 1.1 to 1.9 unchanged and confirmed by the performance page (async rejections forwarded; production
mode; crash-and-restart). Added Express 10 to 14 and Fastify 14 to 17, each a concrete pitfall from those pages.
Helmet point 8 extended. Nothing deleted, nothing found wrong.

Still unverified: the Fastify version of the Server page (not recorded in the page, main branch), the Express
claim that production mode speeds an app threefold (stated by the page, deliberately not repeated), any
Express-4-only behaviour, and the performance side of Fastify point 12 (rule of thumb, from the documentation,
not measured). No permissive source for rate limiting was read (searched: Express security page only).
