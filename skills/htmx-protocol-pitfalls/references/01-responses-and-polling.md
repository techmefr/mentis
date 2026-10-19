# htmx-protocol-pitfalls §1 — Responses and polling

Applies to htmx 2.0.x. The server drives much of the page by what it returns; most failures here are silent:
the header never arrived, or the poll never stopped.

## 1.1 Redirects and the lost header
1. **Response headers are not processed on a 3xx status.** The browser follows the redirect inside the request
   and htmx receives the final response; headers on the redirect itself are gone. Where htmx headers matter,
   answer with a non-redirect status such as 200.
2. **After a successful form post, return the HTML directly.** htmx does not need Post/Redirect/Get; the
   fragment can be the response. If the whole page must change, send `HX-Redirect` or `HX-Location` on a 200.
3. **`HX-Redirect` does a full page reload** through the browser. Use it for destinations that are not htmx
   endpoints or that carry different head content or scripts.
4. **`HX-Location` navigates without a reload.** It acts like following a boosted link: new history entry, an
   AJAX request to the path, the response swapped into the body or into a target you name. The value is a path,
   or JSON with a required `path` and optional `target`, `swap`, `values` and the other context fields of the
   ajax API.

## 1.2 Other response headers
1. **`HX-Trigger`, `HX-Trigger-After-Swap`, `HX-Trigger-After-Settle`** fire client events: immediately,
   after the swap step, or after the settle step. A bare event name fires it; JSON carries details (a value or a
   nested object, read from `event.detail`). The event fires on the triggering element and bubbles to the body,
   so a listener elsewhere on the page needs `from:body` in its `hx-trigger`.
2. **`HX-Refresh: true`** reloads the whole page. Only the exact value `true` counts.
3. **`HX-Retarget`** takes a CSS selector and changes where the content is swapped. **`HX-Reswap`** takes any
   `hx-swap` value and changes how. **`HX-Reselect`** takes a CSS selector for which part of the response is
   used and overrides an `hx-select` on the triggering element.
4. **`HX-Push-Url` and `HX-Replace-Url`** change the address bar: push adds a history entry, replace does not.

## 1.3 Polling
1. **`hx-trigger="every 2s"` polls.** Each tick issues the request and swaps the response.
2. **The server stops it with status `286`.** The element cancels its polling. Use it when the task is done.
   `286` is a deliberate signal, so no other endpoint should return it.
3. **Load polling is the alternative.** An element with `hx-trigger="load delay:1s"` and `hx-swap="outerHTML"`
   replaces itself with the response; as long as the endpoint keeps returning the same element, it keeps
   polling, and the poll ends when the response no longer contains it. This fits endpoints that have a natural
   end, such as a progress bar.
4. **Pick one of the two per element,** and make the end condition explicit on the server.

## 1.4 Trigger modifiers that protect the server
1. **`delay:<time>`** waits and restarts the countdown on each new event; **`throttle:<time>`** discards events
   that arrive inside the window. Active search is `keyup changed delay:500ms`.
2. **`changed`** issues a request only if the element's value has changed.
3. **`from:<selector>`** listens on another element and is not re-evaluated if the page changes.

## Verification
- Answer a form post with a 302 and with a 200 plus `HX-Redirect`, and check in the network panel which one
  navigated (§1).
- Return `286` once and confirm the poll requests stop (§1).
- Fire an event with `HX-Trigger` and confirm a `from:body` listener reacts (§1).
