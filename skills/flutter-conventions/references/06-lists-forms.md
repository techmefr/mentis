# flutter-conventions §6 — Lists and forms

> Section 6 of `skills/flutter-conventions`. Read it when a list, a pagination, a form, the keyboard. The other sections and the guardrails stay in `SKILL.md`.

1. A long list uses the lazy builder, never a fully materialised children list.
2. Paged list: load the next page near the end, show a loading footer, mark the end of the list, and handle
   the error-mid-scroll case. Pull-to-refresh resets to the first page.
3. A form field validates through the form's own validator mechanism, showing **inline per-field errors**,
   not one global message.
4. Choose the validation timing deliberately (on submit, or as-you-type after first interaction); validating
   from the first keystroke flags an empty field the user is still typing into.
5. Disable the submit control while a submission is in flight — a double tap is one order twice.
6. Keyboard: avoid covering the focused field, scroll it into view, set the right keyboard type and action
   (next/done), and let a tap outside dismiss.
