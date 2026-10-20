---
name: modal-drawer-dialog-ui-pitfalls
description: "Use when a modal, dialog, drawer, side panel, bottom sheet or confirmation prompt is written or reviewed in a web application, whatever the framework: focus moved in on open, trapped, and returned to the trigger on close, Escape and backdrop dismissal, scroll lock and layout shift, stacked dialogs and layered popups, the native dialog element against a hand-built one, dirty-state confirmation before losing a form, mobile and small-screen behaviour, dialogs that are addressable by URL and survive reload and the back button, plus the tests that catch them."
---

# modal-drawer-dialog-ui-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for the layer that sits on top of the page. The premise: **a dialog looks
right when it opens by a mouse click on a desktop and is wrong everywhere else.** Keyboard focus stays on the page
behind it, Escape closes the wrong layer, the page scrolls under it, a second dialog breaks the first, a half-filled
form disappears on a stray click, the back button leaves the site instead of closing it, and on a phone the footer
buttons sit under the keyboard. Generic focus and ARIA rules are in `accessibility` §1 and §8; form behaviour is in
`long-and-multistep-form-pitfalls`; a field that opens a dialog to create an option is in
`combobox-autocomplete-ui-pitfalls` §3.5.

## When
- A modal, drawer, side panel, sheet, lightbox or confirm prompt is built or reviewed.
- A user reports "I could tab behind the popup", "Escape closed everything", "my text is gone", "back left the page", "the page jumps when it opens".
- A dialog is opened from another dialog, from a menu, or by a link that should be shareable.

**Skip when** the project has no layer over the page (no modal, drawer, sheet or confirm prompt). Then say "not applicable: no overlay layer" rather than invent a finding; the same goes for a section whose situation is absent (no URL-addressable dialog, no native shell).

## Steps

**Read the section the task meets.** Each ends with checks.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Choosing dialog or page, native element, focus in and back, trap, Escape, backdrop, scroll lock, naming | any layer over the page is built | [`01-focus-dismissal-scroll.md`](./references/01-focus-dismissal-scroll.md) |
| 2 | Stacking, popups inside dialogs, dirty-state confirmation, destructive confirms, async submit | a dialog holds a form, an action or another layer | [`02-stacking-forms-confirmation.md`](./references/02-stacking-forms-confirmation.md) |
| 3 | Mobile and sheets, URL-addressable dialogs and history, tests, framework pointers | a dialog ships, is shareable, or is tested | [`03-mobile-url-tests.md`](./references/03-mobile-url-tests.md) |

## Output / checkpoint
A change is done when: the dialog has a name and focus moves into it on open and back to the trigger on close
(§1.2); the page behind is inert, not only covered (§1.4); Escape and the backdrop close only the top layer and
never lose a dirty form (§1.3, §2.3); scroll is locked without layout shift (§1.5); a shareable dialog survives
reload and back (§3.4); and the tests in §3.6 exist. No checkpoint is written: a craft block, 🟡, nothing here was
run in an application.

## Guardrails
- Make the page behind unreachable for keyboard and screen reader (§1.4). Never rely on a dark overlay alone.
- Return focus to the control that opened the dialog, or to a stated fallback (§1.2). Never drop it on the document.
- Ask before discarding typed data (§2.3). Never close a dirty form on a backdrop click without a confirm.
- Close only the topmost layer on Escape (§1.3, §2.1). Never let one key press tear down a stack.
- Use a page, not a dialog, for long or multi-step work or content that needs its own URL (§1.1). Never nest a workflow in a modal because it was quick to build.
- Check how many places build the same dialog markup (§1.6). Never fix a dismissal or focus defect in one copy and leave the others.
- Facts about a browser feature or library are for the date in `references/origin.md`; re-read before relying. A point without a credit to the HTML Standard or the authoring practices is still own guidance.

## Origin
Own craft knowledge. The platform facts of §1.2 to §1.4 and §2.4 were checked on 2026-10-20 against the HTML Standard (CC BY 4.0, licence file read) and the W3C ARIA authoring practices modal dialog and alert dialog patterns (facts only, credited, no text copied). No other permissive source was read. Details in [`references/origin.md`](./references/origin.md).
