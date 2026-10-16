---
name: laravel-blade-view-pitfalls
description: "Use when writing or reviewing Laravel Blade templates and the views a controller returns: components versus includes and the attribute bag (attributes->merge), scripts pushed once per response (pushOnce), props shared with nested components (aware), view composers and what they do not cover, returning a fragment for htmx or Turbo requests, escaping output for its context, passing server data to JavaScript (Js::from versus data attributes), CSRF tokens in forms, and parsing dates in a template instead of casting them on the model."
---

# laravel-blade-view-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for the template layer of a Laravel application. The two sections share
one premise: **a Blade template runs on every render and is read by people who never open the controller, so
each rule is about what the template can no longer do silently**: repeat a script, hide a dependency, print
untrusted text raw, or leave a form without its token. Framework-wide rules (naming, translations, no HTML built
in PHP, no hard-coded user text) are in `skills/laravel-conventions`; the HTTP side of forms is in
`skills/laravel-precognitive-request-scoping`.

## When
- Creating or changing a Blade component, partial, layout or stack.
- A script or style block is added to a template, or server data is handed to JavaScript.
- A route starts answering htmx or Turbo requests with part of a page.
- A template prints a value that comes from a user, or contains a form that changes state.

## Steps

**Read only the section the task meets.** They are independent.

| Part | Covers | Read it when | File |
|---|---|---|---|
| 1 | Components, partials and composition: the attribute bag, includes versus components, stacks, nested props, view composers, fragments | a component, an include or a shared piece of data is written | [`01-components-and-composition.md`](./references/01-components-and-composition.md) |
| 2 | Output, data and forms: escaping, handing data to JavaScript, CSRF in forms, dates, where scripts live | a value is printed, data reaches a script, or a form is added | [`02-output-data-and-forms.md`](./references/02-output-data-and-forms.md) |

## Output / checkpoint
Each rule was exercised, not read off the file: a component was rendered twice on one page and the output
checked for a repeated script (part 1, point 2), a caller-supplied attribute and class reached the root element
(part 1, point 1), a string containing markup and a quote was rendered where the template prints user text and
came out escaped (part 2, point 1), and the form's rendered HTML contains the token field (part 2, point 3).
A template that was only read is not verified.

## Guardrails
- Never print untrusted content with the unescaped syntax (part 2, point 1).
- Never write a state-changing form without the CSRF token, and never switch the protection off to fix a token
  mismatch (part 2, point 3).
- Never push the same script from a component that renders more than once without a once-only stack (part 1,
  point 2).
- Never share data with a wildcard view composer when the matching views need different data (part 1, point 5).
- Never serialise a whole model into an HTML attribute (part 2, point 2).
- This block states the Laravel Boost rule files at the commit in
  [`references/origin.md`](./references/origin.md). No template was rendered while writing it, and the Laravel
  version that supports each directive was not checked.

## Origin
Rewritten from the Laravel Boost best-practice rule files for Blade views, style and security (MIT), read
2026-10-16. 🟡: never run by us; open points are in [`references/origin.md`](./references/origin.md).
