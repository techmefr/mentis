---
name: combobox-autocomplete-ui-pitfalls
description: "Use when an autocomplete, combobox, typeahead, async select or tag picker is written or reviewed in a web application, whatever the framework: options fetched as the user types (debounce, cancelled and out-of-order responses, minimum length), keyboard behaviour and the combobox ARIA pattern (focus stays in the input, active option, announcements), the empty, loading, error and no-match states, multi-select with chips and removal, creating a new option, selected values that are not in the loaded options, and the tests that catch them."
---

# combobox-autocomplete-ui-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for the field that looks like a text input and behaves like a small search
application. The premise: **a combobox works when the developer types a word that has results and uses a mouse.** It
breaks on a slow network (an old answer replaces a new one), on a keyboard (focus leaves the input, Enter submits the
form), on a screen reader (nothing says the list opened), on an edit form (the saved value is not in the first page of
options) and on "no match" (a blank panel). Generic widget ARIA rules are in `accessibility` §8; where the request
state lives is in `data-fetching-state-conventions`; a search box with facets and saved views is
`filters-search-and-saved-views-pitfalls`.

## When
- A field offers suggestions, a searchable select, a tag or recipient picker, or an address or entity lookup.
- A user reports "I see the results of the previous word", "Enter sent the form", "my saved value shows blank", "I can't pick it with the keyboard".
- A select grows beyond what is comfortable as a plain list (roughly: more than a screen of options, or options that come from a server).
- A custom select built from a button and a list, with no text input, is reviewed: use §2.6 and the checks of §2.1.3, §2.1.4 and §2.2.3.

**Skip when** the project has no field where the user types to find an option and no options loaded from a server: then §1, §2.2.5 and §3.3 to §3.5 are "not applicable: no typing and no async options", and only §2.6 (select-only) plus the shared parts of §2.1 to §2.4 apply to a custom select. Say "not applicable: reason" rather than invent a finding. A plain search box that filters a page's list is not a combobox.

## Steps

**Read the section the task meets.** Each ends with checks.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Async options, debounce, cancellation and races, minimum length, selected value outside the loaded page | options come from a server | [`01-async-options-and-races.md`](./references/01-async-options-and-races.md) |
| 2 | Keyboard model, the combobox ARIA pattern, screen reader announcements, touch, the select-only variant | the field is built or reviewed for access | [`02-keyboard-and-aria.md`](./references/02-keyboard-and-aria.md) |
| 3 | Empty, loading and error states, multi-select, creating options, tests, framework pointers | states, chips, "add new" or tests are written | [`03-states-multiselect-tests.md`](./references/03-states-multiselect-tests.md) |

## Output / checkpoint
A change is done when: a response is applied only if it answers the current query (§1.2); a stored value renders
its label without being in the loaded page (§1); focus never leaves the input while the list is open (§2.1); the
role, state and relation attributes of §2.3 are present and tested; every state in §3.1 renders distinctly; and the
tests in §3.7 exist. No checkpoint is written: a craft block, 🟡, nothing here was run in an application.

## Guardrails
- Keep only the answer to the latest query (§1.2). Never let a slow earlier request overwrite a newer list.
- Store the option id and render its label from the record, not from the list (§1). Never depend on the stored option being among the loaded ones.
- Keep real focus in the input and point at the active option by reference (§2.1). Never move focus into the list items.
- Make Enter choose the highlighted option only when the list is open (§2.2). Never let it submit a form around an open list.
- Render loading, no match and failure differently (§3.1). Never show "no results" for a failed request.
- Facts about a standard or a library are for the date in `references/origin.md`; re-read before relying.

## Origin
Own craft knowledge, with the pattern facts recalled from the public WAI-ARIA authoring practices without reading
their pages. No permissive source was read for this block. Details in [`references/origin.md`](./references/origin.md).
