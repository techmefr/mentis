# web-components-forms-a11y-pitfalls §1 — Form participation

Source: the WHATWG HTML standard, custom-elements chapter, read 2026-10-20 (CC BY 4.0), plus own craft knowledge, marked where it is the latter.

## 1.1 Becoming a form control
1. **Symptom: the form submits without the element's value, the element is missing from `form.elements`, and `<label>` clicks do nothing.** Cause: an autonomous custom element is not form-associated by default. Fix: declare a static `formAssociated` property set to true and call `attachInternals()` once, in the constructor; keep the returned object private.
2. **The value goes to the form through the internals, not through the DOM.** Call `setFormValue` with the string to send, a form-data entry set, or null to send nothing. Check: submit a plain form and read the resulting pairs; an element with no `name` attribute sends nothing when the value is a string or a file, as a native control does; a form-data entry set is appended without consulting `name` (the element then names its own entries).
3. **Call `setFormValue` on every change of the value, not only on first render.** Symptom: the form sends the first value forever. The standard's own checkbox example updates it from the attribute-changed callback; any path that changes the value (user input, property set, attribute set) must reach the same setter.
4. **Expose the form-control surface the page expects**: `form`, `name`, `type`, `value`, `validity`, `willValidate`, `validationMessage`, `checkValidity`, `reportValidity`. The standard puts `form`, `validity`, `willValidate`, `validationMessage`, `checkValidity`, `reportValidity` and `labels` on the internals, not on the element, and defines no `name`, `type` or `value` property for you; pages and form libraries read these on the element, so forward them explicitly.
5. **`attachInternals()` is for the element's own code.** Never hand the internals object to other components; whoever holds it can change the role, the value and the validity.

## 1.2 Validity
1. **Symptom: `required` is on the host and nothing blocks submission.** Cause: the platform does not know your element is empty. Fix: call `setValidity` with a flag set, a message and an anchor element (the inner control, so the browser can focus it), and clear it with an empty flag set when the value becomes valid.
2. **Recompute validity when the value or a constraint attribute changes**, not only when the user leaves the field. Symptom: stale "invalid" after the user fixed the value.
3. **Use the form's own validation path.** `checkValidity` and `reportValidity` on the form must include the element; check by submitting with a blank value and seeing the browser's validation UI point at the inner control. Do not render a parallel error system that the form's `novalidate` and `:invalid` styling cannot see.
4. **The message is shown by the browser in the page's language**, and the one you set is yours to translate. Pass it through the same message catalogue as the rest of the page (`skills/i18n-message-format-pitfalls`).

## 1.3 Reset, disabled and restore
1. **Symptom: the form's reset button clears native inputs and leaves the custom element showing its old value.** Cause: the platform calls a reset callback on the element and nobody implemented it. Fix: implement `formResetCallback` to return the value to its default (the attribute's value, not the last typed one) and call `setFormValue` again.
2. **Symptom: the element stays interactive inside a disabled fieldset.** The platform calls `formDisabledCallback` with the new state, and the element receives the `disabled` attribute behaviour of a form control. Fix: implement the callback and stop accepting input, remove the tab stop, and reflect the state to the inner control and to the exposed semantics (§2.1).
3. **Symptom: after back navigation or browser autofill the field is empty.** Implement `formStateRestoreCallback`; it is called with the saved state and a reason ("restore" or "autocomplete"), and restoring means setting the value and calling `setFormValue`. The state is the optional second argument of `setFormValue` (a string, a file or a form-data entry set); pass it when the state is more than the submitted value.
4. **React to a change of form owner through `formAssociatedCallback`** (called with the new form, or null). Symptom: a cloned or moved element keeps listeners on the old form.
5. **Read-only is not disabled.** For a form-associated element the standard gives the `readonly` attribute one effect only: the element is barred from constraint validation. Making the control non-editable, and whether the value is still submitted, is the author's job (the value is submitted unless the form value is null); implement it as such rather than reusing the disabled path.

## 1.4 Attribute against property
1. **Symptom: `el.value = 'x'` works and the attribute `value="x"` in HTML does not (or the reverse), and `getAttribute` shows the old value.** Cause: attribute and property are separate surfaces and the platform does not link them. Fix: decide per member. Configuration (initial state, `name`, `disabled`, `required`) is an attribute, read through `observedAttributes`; live state (the current `value`) is a property; a boolean state is reflected with `toggleAttribute`, not by writing the string "false".
2. **Upgrade order loses a property set before registration.** Symptom: a framework sets `el.value` on the placeholder element before `define` runs; the class's accessor then never sees it, the instance keeps an own data property that shadows it. Fix: in the constructor or first connect, take any own property already on the instance, delete it, and re-set it through the accessor. Own knowledge, commonly called property upgrade.
3. **Do not reflect an object or a long string into an attribute.** Symptom: huge DOM attributes and a re-render loop when the reflecting setter triggers the attribute callback. Guard the callback with an equality check, and keep complex values property-only.
4. **Do not use attribute presence for tri-state values.** "unset", "true" and "false" need an enumerated attribute with a defined default.

## 1.5 Checks
1. A form with the element, a native input, a reset button and a fieldset, submitted and reset by script and by hand.
2. The element created three ways (parsed, `createElement`, defined after markup) and given its value by attribute and by property each time (`web-components-lifecycle-pitfalls` §1 Output).
3. Back navigation and autofill, in a browser, once.
4. Validation with `required`, blank, then fixed.
