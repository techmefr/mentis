---
name: htmx-protocol-pitfalls
description: "Use when a server sends HTML fragments to htmx 2.x (response headers HX-Redirect, HX-Location, HX-Trigger, HX-Refresh, HX-Retarget, HX-Reswap, the lost headers on 3xx redirects, polling with every Ns and the 286 status, load polling), when an htmx request needs UX around it (htmx-indicator, hx-disabled-elt against double submit, hx-preserve, attribute inheritance leaking hx-confirm or hx-target to children), or when htmx meets other code (htmx.onLoad and htmx.process for widgets, Vary and ETag for fragment versus full-page responses, history restore, CORS exposed headers, a pinned CDN script with an integrity hash)."
---

# htmx-protocol-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for the htmx behaviours that are decided by the HTTP exchange rather
than by the markup: what the server must send, what the browser eats before htmx sees it, and what htmx does
to the page around the swap. The sections share one premise: **htmx only sees what the browser hands it, and
it only wires up what is in the DOM when it looks**. Each rule says what you see when it is missed.

**Version scope: htmx 2.0.x**, read at the 2.0.11 release. The repository documentation also mentions
material of unclear version scope (an `hx-partial` swap command, form validation on by default in a later
line); none of it is used here, and every rule below applies to 2.0 only. Check the installed version before relying on a point.

Standalone block, written because the broader htmx and Alpine conventions block exists only on an unmerged
branch. It is meant to be merged into the same-named framework block when that lands (see
[`references/origin.md`](./references/origin.md)). Until then it cites only blocks present on the main branch.

## When
- A server endpoint answers an htmx request, redirects after a form post, or has to tell the page to do
  something (navigate, refresh, fire an event, swap elsewhere).
- A page polls, or shows progress for a long task.
- A button double-submits, a spinner is wanted, a video or field must survive a swap, or a child element
  behaves as if it had inherited something nobody wrote on it.
- A third-party widget stops working after a swap, a back button shows a fragment instead of a page, a cached
  response is the wrong variant, or htmx calls fail across origins.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Response side: redirects and lost headers, response headers, polling and 286 | the server answers an htmx request, or an element polls | [`01-responses-and-polling.md`](./references/01-responses-and-polling.md) |
| 2 | Request side: indicators, double submit, preserve, inheritance | a request needs UX, or an attribute applies where it should not | [`02-request-ux-and-inheritance.md`](./references/02-request-ux-and-inheritance.md) |
| 3 | Integration and delivery: widgets after swap, caching, history, CORS, pinned script | htmx meets other JavaScript, a cache, another origin or a CDN | [`03-integration-and-delivery.md`](./references/03-integration-and-delivery.md) |

## Output / checkpoint
Each rule was exercised, not read off the file: the endpoint was called once with and once without the htmx
request header and the two bodies compared (§3), a redirect was followed in a browser with the network panel
open and the header seen to arrive (§1), a poll was stopped by the server and the requests stopped (§1), a
button was clicked twice quickly and one request went out (§2). A rule only read is not verified.

## Guardrails
- Never rely on a response header sent with a 3xx status: the browser follows the redirect internally and
  htmx never sees the header (§1).
- Never send `286` from an endpoint that is not a polling target: it cancels the polling of the element that
  made the request (§1).
- Never hoist `hx-target` or `hx-confirm` onto a container without checking every htmx element beneath it (§2).
- Never return a fragment from a URL a user can open directly without `Vary` or a distinct validator (§3).
- Never push a URL into history that cannot return a full page (§3).
- Security of swapped HTML (escaping, content security policy) belongs to `security-hardening`.

## Origin
Rewritten from the htmx repository documentation and source (BSD Zero-Clause), read 2026-10-08 at the 2.0.11
release, cross-checked against one MIT htmx skill set. 🟡: never run by us; open points are in
[`references/origin.md`](./references/origin.md).
