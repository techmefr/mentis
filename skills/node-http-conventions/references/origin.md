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

**Read but not used for rules:** the Express security and performance best-practice pages are not in the
repository clone that was read (the tree has the guides only), so no rule on cookies, sessions, rate limiting or
process managers is claimed for Express. The Fastify lifecycle, server and plugin-encapsulation reference pages,
the Helmet FAQ and the Node.js documentation were not read. Left out: NestJS, Koa, Hono, serverless adapters.

**Version stamp.** Express documentation at major 5 (the 4.x guides sit beside it and differ on async handling).
Fastify documentation as of the main branch on the read date; the version was not recorded in the pages read,
so check the installed major before relying on option names. Helmet at its current README (default header count
may change). Expiry: when the framework major changes (`skills/source-freshness` §2.1) re-read §1.1, §1.7 and
§2.2 first.

**Status.** 🟡, "base to confront with the real thing", like `go-conventions`. Nothing here was run against a
Node service.
