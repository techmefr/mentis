# long-and-multistep-form-pitfalls §2 — Drafts, dirty state and steps

## 2.1 Draft saving
1. **Decide what a draft is before building it.** Three different things hide behind the word: a browser-local
   copy of typed values (survives refresh, one device), a server-side draft attached to the person (survives a
   device change), and a half-complete real record flagged as incomplete. Symptom: a "draft" feature that is
   lost on another device, or that half-fills a list others can see. Fix: pick one, write down who can see it,
   how long it lives and what discards it. Check each save path against the kind claimed: an autosave that writes only to browser storage while the server draft is written only on step change leaves two kinds in one feature, and a device change loses what was typed since the last step.
2. **Save on a quiet moment, not on every keystroke.** Debounce while typing and save on blur, on step change
   and when the page is hidden. Symptom: a request per character, or nothing saved when the tab is closed. Fix:
   debounce plus a save on the page visibility change (the visibility event fires when the page becomes hidden, including a tab switch, a minimised window and the start of an unload; Page Visibility, W3C, read 2026-10-20, a discontinued spec that points to the HTML Standard); treat unload-time requests as best effort: the Beacon API only queues a small POST, returns false past a size limit the browser sets, gives no result, and does not read a response, so a draft that matters needs the next page load to reconcile it. Also flush on unmount: a route change or a step change that cancels the pending debounce timer instead of running it drops the last edits. Check: grep for the timer clear in the unmount hook and confirm the pending save is run there, not only cancelled.
3. **A draft must not bypass validation rules of the final record, and must not be validated by them.** Store
   it in a shape that accepts missing and invalid values; run the full rules only at submit.
4. **Show the draft state.** "Saved at 14:32", "Saving...", "Could not save, your changes are kept on this
   page". A silent autosave that has been failing for an hour is the worst case. Check that a failed save, a refused payload (size limit) and a false return value reach the person, and are not only logged to the console.
5. **Drafts expire and drift.** Symptom: a draft restored weeks later against changed options (a removed
   category, a new required field). Fix: store a schema version with the draft, re-validate on restore, and
   drop or migrate values that no longer exist, telling the person which.
6a. **Browser storage can refuse or vanish.** The HTML Standard says a write throws a quota error when the quota is exceeded or the user disabled storage, that users can clear persistent data and browsers may expire it, and that persistent data should be treated as potentially sensitive (HTML Standard, web storage, read 2026-10-20). Wrap every read and write, show the failed-save state of 2.1.4, and never make local storage the only copy of a draft that matters.
6. **Sensitive content in local storage stays on the machine.** Symptom: personal or confidential values
   persisted unencrypted on a shared computer. Fix: keep such drafts server-side, or do not persist them; clear
   local drafts at sign-out.
7. **Offer resume and discard explicitly.** On opening a form with a draft, ask once: continue or start over.
   Never overwrite a draft silently with loaded values, nor the reverse.

## 2.2 Dirty state
1. **Dirty is "differs from the baseline", not "an input event fired".** Symptom: the leave-page warning
   appears after focusing a field and typing then deleting a character. Fix: keep the baseline (loaded or last
   saved values) and compare current values by value with a normalising comparison (trimmed strings, null and
   empty treated alike if the server does).
2. **Move the baseline on successful save, not on click.** Symptom: a warning after a successful save, or no
   warning after a failed one. Fix: reset the baseline from the server response.
3. **Server-computed fields change the baseline.** Symptom: the form is dirty right after load because the
   client formatted a number or filled a default. Fix: normalise both sides the same way, or exclude derived
   fields from the comparison.
4. **Warn on leaving only when dirty, in all the ways of leaving.** Browser close and reload (the browser's own
   confirmation, whose text cannot be customised), in-app route changes (use the router's navigation guard),
   and a modal closed by backdrop or Escape. Symptom: the guard covers the link but not the modal. Check:
   leave by each route with a dirty form.
5. **Do not warn after a deliberate discard**, and do not trap people: a warning with "stay" and "leave
   without saving" is enough, with "save and leave" where saving is cheap.

## 2.3 Steps, back, refresh and resume
1. **Put the step in the address** (path or query), so refresh and back return to the same step. Symptom: back
   leaves the whole wizard, or refresh restarts at step 1. Fix: step is part of the route, values come from the
   draft (§2.1).
2. **Never require earlier steps to be re-entered after an error.** Values live outside the step components
   (one store for the whole form), not inside components that unmount on step change.
3. **Deep links and skipping.** Opening step 4 by address without step 2 done must land the person on the first
   incomplete step with a message, not on a broken screen.
4. **Long-running sessions.** A form open for an hour outlives its authentication or anti-forgery token.
   Symptom: submit returns an auth error and the input is lost. Fix: keep the draft, renew the session without
   leaving the page (or show a sign-in in place), and retry the submit afterwards.
5. **Leaving a step is not saving a step** unless you say so. If each step persists to the server, say it in the
   interface and handle partial records (§2.1.1); if only the last step persists, say that leaving loses data.
6. **File uploads inside forms** are separate: upload when picked, keep the returned reference in the form, show
   progress and errors, and handle removal and replacement. A form submit that re-sends large files on every
   retry times out again.
