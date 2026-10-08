# htmx-protocol-pitfalls §2 — Request UX and inheritance

Applies to htmx 2.0.x. These are the attributes around a request: what the user sees while it runs, what
prevents it running twice, what survives the swap, and which attributes reach elements that never declared
them.

## 2.1 Indicators and double submit
1. **The `htmx-request` class marks a request in flight.** It is put on the requesting element, or on the
   element named by `hx-indicator` (a CSS selector). A child with the `htmx-indicator` class is invisible by
   default (opacity 0) and becomes visible while its ancestor or itself carries `htmx-request`.
2. **Write the indicator CSS for both cases** when you change the mechanism: the indicator as a child of the
   element with `htmx-request`, and the indicator carrying both classes.
3. **`hx-disabled-elt` adds the `disabled` attribute during the request.** The value is a selector, `this`,
   `closest <selector>`, `find <selector>`, `next`, `previous`, or a comma-separated list of them (not `this`
   in a list). On a submit button it stops a second click from sending a second request. An indicator alone
   does not prevent a double submit.
4. **`hx-disabled-elt` on a whole form** is done by naming the fieldset or the form's controls with a
   selector, so inputs and the button are locked together.

## 2.2 Preserving elements across a swap
1. **`hx-preserve` keeps an element unchanged when an ancestor is swapped.** It matches by `id`: set a stable
   `id`, and the response needs an element with the same `id`; its type and other attributes are ignored.
2. **It is not inherited.**
3. **Some elements cannot be preserved properly.** A text input loses focus and caret position, and iframes and
   some videos misbehave; the documentation points to a morphing swap extension for those.
4. **Do not combine it with `hx-swap="none"`** for requests whose response could contain a preserved element:
   the element can be lost.
5. **It can relocate an element.** A preserved element that appears in a new place in a partial or out-of-band
   response is moved there, not copied.

## 2.3 Inheritance
1. **Most htmx attributes are inherited.** An attribute on a parent applies to the element and every htmx
   element beneath it. That is why hoisting works, and why hoisting `hx-confirm` or `hx-target` onto a wrapper
   silently attaches a confirm dialog or a swap target to every child, including a cancel link.
2. **Undo it on a child with the value `unset`** (for example `hx-confirm="unset"`).
3. **Stop it from a parent with `hx-disinherit`.** `hx-disinherit="*"` disables inheritance of everything
   below, and a list of attribute names disables only those.
4. **Turn it off globally with `htmx.config.disableInheritance`.** Attributes are then inherited only where
   `hx-inherit` says so. Choose this for a large app where hoisting has become a source of surprises.
5. **Check children when moving an attribute up.** The failure is not on the element you edited.

## Verification
- Click a submit button twice within a few milliseconds and confirm one request in the network panel (§2).
- Move an attribute to a wrapper and click every htmx element inside it; none may behave differently (§2).
- Swap an ancestor of a preserved element and confirm it kept its state (§2).
