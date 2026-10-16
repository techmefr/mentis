# laravel-blade-view-pitfalls §2 — Output, data and forms

> Part 2 of `skills/laravel-blade-view-pitfalls`. Read it when a value is printed, data reaches a script, or a
> form is added. Sourced from `.ai/laravel/skill/laravel-best-practices/rules/security.blade.php`,
> `style.md`, `eloquent.md`, `blade-views.md` and the index file `SKILL.md` in `laravel/boost` (commit `f1411f9`), read 2026-10-16.
> Sentences marked "own guidance" are ours.

1. **Print user content with the escaping syntax; use the raw syntax only for content sanitised for that
   exact place.** The double-brace syntax HTML-escapes its output. The source says to use the unescaped
   double-brace-and-bang syntax only for content that has been sanitised for the exact HTML context in which
   it is rendered, and adds that escaping rules differ for HTML, URLs, JavaScript and CSS. Its wrong example
   prints a user's bio with the raw syntax; the right one uses the escaping syntax. Own guidance: a search for
   the raw syntax in the templates is a standing review item, and a value printed inside a script, a style or
   an event attribute needs the encoder for that context and not HTML escaping.
2. **Hand server data to JavaScript with the encoder made for it.** The source's example is the `Js::from()`
   helper, which formats a value safely for a script. It says data attributes suit small scalar values, and
   that serialising a large model into an attribute can expose fields that were not meant to be public and
   complicates escaping. Own guidance: build the array that the script needs, with only the fields it reads,
   and pass that.
3. **Put the CSRF token in every state-changing form.** The source says to include the token directive in Blade
   forms that change state and are handled by the `web` middleware group, and that routes deliberately
   excluded from verification, such as validated third-party webhooks, need their own authenticity check. It adds: do not disable the protection only to fix a token
   mismatch. Own guidance: a mismatch is a symptom (a cached page, an expired session, a missing field in an
   ajax call) and the cause is what to fix.
4. **Keep large scripts and styles out of templates.** The source prefers the project's asset pipeline,
   components and existing conventions for substantial JavaScript and CSS; small page-specific scripts or
   styles can be reasonable in layouts or stacks, and large behaviour or style blocks should not be mixed into
   templates.
5. **Cast a date on the model and call it in the template.** The source's contrast: parsing a stored value
   with the Carbon parser inside the template, versus declaring a `datetime` cast so the attribute is already
   a Carbon instance and the template calls `toDateString()` or `format()` on it. It says the conventional
   `created_at` and `updated_at` are cast already. Own guidance: a template that parses is a template that
   decides the stored format; and user-facing formats follow the project's date rule in
   `skills/laravel-date-via-localised-accessors`.
6. **Name a view file in kebab-case.** The source's naming table lists views as kebab-case with an example of
   `show-filtered.blade.php`. Own guidance: follow what the project already does if it differs; the source
   itself says consistency with the codebase comes first.
