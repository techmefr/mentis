# modal-drawer-dialog-ui-pitfalls §2 — Stacking, forms and confirmation

Own craft knowledge; only §2.4.2 and §2.3.8 were checked against sources (APG alertdialog, HTML dialog; see origin.md).

## 2.1 Stacking and layers
1. **Symptom: a dropdown, a date picker or a tooltip opens behind the dialog.** Cause: competing z-index values. Fix: one ordered layer scale defined in design tokens (page, sticky header, dropdown, dialog, popover inside dialog, toast); no arbitrary numbers (`design-tokens-storybook`).
2. **Popups opened from inside a dialog render in that dialog's layer or above it**, and are part of its focus order; a popup portalled to the document root can end up outside the inert region and unreachable.
3. **A dialog opened from a dialog** is allowed only when the second is small (a confirm, a picker). Two form dialogs deep means the flow wants a page.
4. **Keep a stack**: Escape, the backdrop and the focus return act on the top entry; closing it returns focus to the dialog below, not the page.
5. **Only the top dialog is interactive**; the ones below are inert, and each keeps its own state until closed.
6. **A toast raised by a dialog action outlives the dialog**; place it outside, and do not return focus to it.

## 2.2 Forms inside a dialog
1. **Symptom: Enter submits twice, or submits a form the user did not mean.** Fix: one real form element with one submit button; the primary action is the submit, not an onClick on a div.
2. **Disable the submit while the request runs, and show progress**; a second press must not send a second request (`long-and-multistep-form-pitfalls`).
3. **Errors are shown next to the field and summarised at the top**, and focus moves to the first invalid field or the summary on a failed submit.
4. **A server error that is not about one field stays in the dialog** with a way to retry; the dialog does not close on failure.
5. **On success, close, return focus (§1.2) and show the result** (a toast, or the updated row highlighted), not only a silent close.
6. **The action order is consistent**: primary on one side everywhere in the product, cancel next to it, destructive visually distinct and never the default focus.
7. **Labels name the action** ("Delete project", "Save changes"), not "OK" and "Yes".

## 2.3 Dirty state and discarding
1. **Symptom: a user types a long message, clicks outside, and everything is gone.** Fix: track "dirty" (a value differs from the initial one) and guard every exit: Escape, backdrop, close button, route change and browser navigation.
2. **Ask once, with a clear choice**: "Discard changes" and "Keep editing", the safe option focused. The confirm is itself a dialog (§2.1) and must return focus to the form.
3. **Dirty means different from the initial value, not touched**; typing and deleting back to the original is clean.
4. **Do not guard a clean form**; a confirm on every close trains users to click through it.
5. **Tab close and reload use the browser's own prompt** only when the form is dirty and the data is not saved elsewhere; keep that listener removed when clean.
6. **A draft that can be saved automatically** is better than a confirm for long text; say when it was saved.
7. **Server changes while open**: if the underlying record changed since opening, say so on submit (conflict message) instead of silently overwriting.
8. **A native dialog close request fires a cancelable event first**: cancel it to show the discard confirm, but a close made by script or by removing the attribute bypasses it, so guard exits you control yourself (HTML dialog).

## 2.4 Destructive confirmations
1. **Name the object and the consequence**: "Delete 'Q3 budget' and its 14 attachments. This cannot be undone." A generic "Are you sure?" gets reflex clicks.
2. **Use the alert-dialog role for a decision that must be made** (the role is for interrupting the workflow to get a response, APG alertdialog), and focus the safe button (the modal dialog pattern gives least destructive focus for irreversible actions, APG dialog; the alertdialog page itself gives no focus rule); the destructive button carries the verb.
3. **Prefer undo to confirm when the action is reversible** (a snackbar with undo for a soft delete); keep the confirm for irreversible actions.
4. **For high-impact deletes, ask for a typed confirmation** of the object's name, and say what is not recoverable.
5. **The confirm does not run the action twice**: disable on press, and let the server be idempotent (`admin-back-office-pitfalls` for audit and dangerous actions).

## 2.5 Drawers and side panels
1. **A drawer that edits a record is a dialog for all the rules above**; one that only shows details is non-modal and must not trap (§1.4).
2. **A drawer opened from a table row keeps the row selected and focus returns to it**, even after the table re-renders (key the row by id, `data-table-ui-pitfalls` §1.4).
3. **Resizable or pinned drawers remember their width per user**, with a sane minimum, and never cover the control that closes them.
4. **Navigating inside the drawer (next record) updates the name and moves focus to the heading**, not to the top of the page.
5. **At small widths a drawer becomes full-screen** (§3.1).

## Checks
```
Type in a form dialog, press Escape, click the backdrop, use the back button: each asks before discarding; a clean form closes at once.
Open a combobox in a dialog and press Escape: only the list closes.
Press submit twice quickly: one request leaves.
```
