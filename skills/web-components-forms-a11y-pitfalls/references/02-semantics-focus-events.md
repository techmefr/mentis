# web-components-forms-a11y-pitfalls §2 — Semantics, focus and events

Source: the WHATWG HTML and DOM standards, read 2026-10-20 (CC BY 4.0), plus own craft knowledge, marked where it is the latter.

## 2.1 Default semantics
1. **Symptom: a custom `<fancy-button>` is read as plain text, cannot be tabbed to, and Enter or Space do nothing.** The platform gives an autonomous element no role from its name. The standard's own example of a button needs a tab stop, a role, state attributes and a label added by hand, and a tab stop removed again when the element becomes disabled. Fix: use a native element inside the shadow root when you can (a real `<button>`), and only reach for a role when there is no native equivalent (`skills/nuxt-semantic-element-first`, `skills/accessibility`).
2. **Set default role and aria state on the internals, not on the host attributes.** The internals carry defaults that a page author can override with their own attributes, and the host stays free of attributes you wrote on their behalf. Symptom of the alternative: the element writes `role` on itself, and a user of the element cannot change it.
3. **Keep the semantics in step with the state.** Symptom: a checkbox shows checked and is announced unchecked, because the visual state changed and the aria state did not. One setter updates the value, the form value (§1.1), the visual and the aria state.
4. **Give the element an accessible name, and say where it comes from.** A slotted label, an `aria-label` the page sets, or a label element pointing at it through form association (§1.1). The `for` attribute of a label must name a labelable element in the same tree as the label (the standard says so), so a label inside the root cannot name a control outside it and the reverse; check with a screen reader, not with the attribute alone.
5. **Id references do not cross shadow boundaries.** `for` is specified as same-tree (the standard's label element); `aria-labelledby` and `aria-describedby` behave the same in practice, but the ARIA specification was not read, so check them in the target browsers. Fix: keep label and control in the same tree, slot the label into the root, or set the name through the internals.

## 2.2 Focus
1. **Symptom: clicking the element focuses nothing, or tabbing goes to the host and then to the inner input, so two stops for one control.** Cause: the host and the inner control are both focusable, or neither is. Fix: attach the shadow root with focus delegation, so focusing the host moves focus to the first focusable inner element and the host is not a separate stop; the declarative form has an attribute for it (§3.3).
2. **Symptom: `label.click()` or `form.reportValidity()` cannot move focus into the element.** Anchor `setValidity` to the inner control (§1.2.1), and expose a `focus()` that forwards.
3. **Do not set a positive tabindex** and do not remove the focus outline without a replacement; see `skills/a11y-lint-wiring-pitfalls`.
4. **Disabled means unfocusable.** Remove the tab stop and, for a form control, rely on the disabled state callback (§1.3.2). Symptom: keyboard users reach a control that ignores them.

## 2.3 Custom states
1. **Symptom: styling depends on the host having classes like `is-open` that the element writes on itself.** Cause: using the host's attributes for internal state leaks it into the public API and into the page's selectors. Fix: expose internal states through the internals' state set and let page CSS match them with the custom-state pseudo-class.
2. **Pair a custom state with the semantics it implies**; a visual "open" state with no `aria-expanded` is a visual-only state.
3. Own knowledge, re-read before relying: support for the pseudo-class is recent in some engines. Keep a fallback (an attribute, or a part) where older browsers matter.

## 2.4 Events across the shadow edge
1. **Symptom: a listener on the page never fires for an event dispatched from inside the element.** Cause: a dispatched event does not leave the shadow root unless it is composed; the platform's own UI events are composed, a `CustomEvent` created with default options is not, and it also does not bubble. Fix: dispatch from the host, with `bubbles` and `composed` set on purpose, and document each event in the element's surface.
2. **Symptom: `event.target` in a page listener is the host, not the inner button.** That is retargeting: the target is rewritten, for any listener in a tree that does not contain the original target, to the host of the shadow tree. Fix: do not read the inner node from an outer listener; carry what the outer code needs in `detail`, or read it from the event's path inside the element.
3. **A closed root hides its nodes from the event path.** The composed path is cut at a closed shadow root, so tooling that inspects `composedPath` from outside sees only the host. This is a reason not to close roots (`web-components-lifecycle-pitfalls` §2).
4. **Re-dispatch, do not forward, when the event should look like yours.** Symptom: a `change` from an inner input reaches the page with the inner input's semantics; native `change` is not composed. Fix: listen inside, then dispatch your own event on the host with the value you want, and stop the inner one if the page should not see two.
5. **Do not rely on the same event name meaning two things.** A custom event named like a native one (`click`, `input`, `change`) confuses form libraries. Prefix or namespace yours, and state when it is cancelable.
6. **A stopped propagation hides the event from outer listeners and analytics**; stop it only with a stated reason and a test.
7. **Check with an outer listener.** Add a listener on `document` and one on the host in a test, trigger the interaction, and assert on target, count and `detail` (`skills/testing-library-query-pitfalls` for the query side).
