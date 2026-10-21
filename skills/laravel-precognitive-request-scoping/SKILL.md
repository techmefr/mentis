---
name: laravel-precognitive-request-scoping
description: "Use when a FormRequest sits behind HandlePrecognitiveRequests (as-you-type validation) and one of its rules is costly, calls an outside service, or checks a file: condition it on isPrecognitive(), because the real FormRequest runs before the controller is skipped."
---

# laravel-precognitive-request-scoping

Narrow trigger extracted from `skills/laravel-conventions` §6.17, so a FormRequest validation rule
that misbehaves under live validation routes here directly instead of only through the whole Laravel block.

## When
Writing or reviewing a FormRequest used on a route with `HandlePrecognitiveRequests` (live, as-you-type
validation): a rule that is expensive, that reaches an outside service, or that depends on an uploaded file;
or any middleware on that route with a side effect.

## Steps
1. **A precognitive request runs the route's middleware and resolves the controller's dependencies,
   including the FormRequest, and then skips the controller method.** The validation rules are the real
   ones; only the action is not executed (documentation, Precognition, Introduction).
2. **Live validation fires often.** The client helpers send a debounced request on each change or blur of a
   field, so a rule that is slow, rate-limited or paid is called far more than at submission. When the client
   names the fields it validates, the framework narrows the rules to those fields rather than running them
   all (`FormRequest::createDefaultValidator` filters the rules for a precognitive request).
3. **Use `$this->isPrecognitive()` inside `rules()` to choose a lighter rule for live validation.** The
   documentation's example keeps the cheap password length rule live and adds the "uncompromised" check (an
   outside lookup) only on the real submission.
4. **Files are not uploaded or validated in a precognitive request by default.** A rule that requires a file
   must be made conditional on `isPrecognitive()` or the field reports as missing; a client can opt in to
   sending files on every validation request, at the cost of repeated uploads.
5. **Check the other middleware on the route.** Anything with a side effect (a counter, an audit line, a
   notification) runs on a precognitive request too, and has to test `$request->isPrecognitive()` to skip it.
6. **Test both modes.** Make a precognitive request with the test helper and assert the success helper, and
   assert that nothing the controller would have written exists.

## Output / checkpoint
Every rule that is costly, external or file-dependent behaves deliberately when `isPrecognitive()` is true,
and no middleware on a precognitive route repeats a side effect for it.

## Guardrails
- A rule that is cheap and pure fires on every change and needs no scoping.
- Do not invent a uniqueness false positive: the controller does not run, so no row is created by the
  precognitive request itself; a uniqueness rule reads the database as it is.
- The full FormRequest section lives in `skills/laravel-conventions` §6 — read it for the neighbouring
  validation rules this one sits beside.

## Origin
Extracted from `skills/laravel-conventions` §6.17, then corrected on 2026-10-20 against the framework's
Precognition documentation, 12.x (read for facts only, our words: Introduction, Customizing Validation Rules,
Handling File Uploads, Managing Side-Effects, Testing) and the framework source (MIT, LICENSE read), files
`HandlePrecognitiveRequests.php` (marks the request and swaps in the precognition dispatchers) and
`FormRequest.php` (rule filtering in `createDefaultValidator`). The earlier text claimed a uniqueness rule gives a
false positive on a row about to be created and that the full validation re-runs on every keystroke; neither is
supported by those sources and both were removed. Not verified: the exact moment the dispatcher stops the
controller (that code sits in classes not opened). Mechanisms only, rewritten in our words.

Independent verification 2026-10-21: 8 checked, 8 matched, 0 corrected, 0 unverified.
