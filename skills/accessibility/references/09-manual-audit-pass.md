# § 9 — Manual audit pass: keyboard, screen reader, zoom

> Section 9 of `skills/accessibility`. Read it when a critical journey must be checked by hand, because §2.12
> and §3.11 say a tooled pass is not enough. Own guidance from general craft knowledge, no source read for this
> section; the criteria themselves are in §1 to §8. Screen reader and browser behaviour differs by pairing, so
> record the pairing used and re-test before relying on a result.
>
> **Where the `§` numbers point.** Every `§N` or `§N.M` below is a section of the `accessibility` block, one
> file per section under `references/`: §1 `01-semantics-keyboard.md`, §2 `02-aria.md`, §3
> `03-contrast-perception.md`, §4 `04-forms.md`, §5 `05-rgaa.md`, §6 `06-document-structure.md`, §7
> `07-media-motion.md`, §8 `08-aria-validity-widgets.md`. Open the one a step cites when you reach it; none of
> them is needed to read this file.
>
> **No browser or screen reader at hand.** The pass then covers only what the code shows (steps 14 to 16, and the
> markup side of steps 3, 5 and 7). Report every step that needed a person as "not tested", never as "no
> finding": the two read alike and mean opposite things. Where a step does not fit the project (no shortcuts, no
> dynamic widget, no media), write "not applicable: <reason>" and move on instead of inventing a finding.

1. **Fix the scope before starting.** Symptom: an audit of "the site" that finds a hundred small things and
   misses the checkout. Fix: list the two to five journeys that matter (sign in, the main task, payment, an
   error path), the pages they cross, and the states each page can be in (empty, loading, error, logged out).
2. **Run the tool first, then put it away.** An automated scan clears the cheap defects so the hour by hand goes
   to what a tool cannot judge. Write down its result and do not count a green scan as a pass of any criterion
   it cannot evaluate (§2.12).
3. **Keyboard pass, mouse unplugged.** Walk each journey with the tab key, shift and tab, enter, space, arrows
   and escape only. Check at every stop: the focus is visible (§1.3), the order follows the reading order, every
   control is reachable and operable, nothing traps focus, a layer takes focus when it opens and gives it back
   when it closes (§1.5), a skip link works, and focus is not hidden under a sticky bar (§1.6). Record the step
   where it fails, not the page.
4. **Screen reader pass, one pairing at a time.** Use one screen reader with one browser, state which, and walk
   the same journeys with the screen off or ignored. Listen for: the page title on arrival, the heading outline
   by jumping from heading to heading, landmarks, each control announced with a name, a role and its state, a
   link whose text makes sense alone, and form errors announced when they appear. Symptom: a button reads as
   "button" with no name. Fix: a name from visible text, not a stray attribute (§2.1).
5. **Test the dynamic parts, not only the first load.** Open, close and operate every widget: menus, dialogs,
   tabs, accordions, autocompletes, toasts. Check that a change of state is announced once, that focus moves
   where the user expects, and that a loading or success message is reachable without sight (§8).
6. **Forms end to end.** Submit empty, submit wrong, submit right. Check that every field has a programmatic
   label, a required or invalid state is exposed, the error names the field and what to do, focus lands on the
   first problem, and nothing already entered is lost (§4).
7. **Zoom and reflow.** Enlarge the page text and zoom the browser up to the levels the standard names for text resize and reflow
   (§3.3 gives the first; read the reflow width from the criterion, never from memory), and use a narrow viewport.
   Check that nothing is cut off, content does not need scrolling in two directions apart from content that
   truly needs it, no control overlaps another, and a fixed header does not eat the screen (§3, §1.8).
   Symptom: a button disappears at high zoom. Fix: fix the layout, never disable zoom.
8. **Check the user's settings.** Turn on a forced-colours or high-contrast mode, a dark scheme, reduced motion,
   and larger system text if the platform offers them. Check that icons and borders survive, that focus is
   still visible, and that motion stops when asked (§7). Own guidance: settings differ by system, note which.
9. **Look at colour and meaning separately.** Check that no information depends on colour alone, status has text
   or a shape, and links are distinguishable in text without relying on hue (§3). Compute contrast rather than judging by eye: from a checkout of this repository run
   `python3 bin/contrast_check.py '#1a1a1a' '#ffffff'` (foreground, background; it prints the ratio only), or, where
   the script is not available, apply the relative-luminance formula of the standard by hand. Read the
   threshold from the standard, never from memory.
10. **Content and media by hand.** Read alternative text against what the image does in context, check captions
    exist and match speech, transcripts exist where needed, and that no flashing content is present (§7).
11. **Write findings so they can be fixed.** Each finding: journey and step, what was expected, what happened,
    the pairing or setting used, the criterion it fails, severity by who is blocked (cannot complete, can
    complete with effort, annoyance), and a suggested fix. Symptom: "poor accessibility" with nothing to act on.
    Fix: one finding per cause, with a way to reproduce it in under a minute.
12. **Say what was not tested.** The report lists screen reader and browser pairings, devices, languages and
    states not covered, and does not claim conformance. A manual pass by one person is a sample, not a
    certificate; where a legal declaration is needed, follow the method of §5.
13. **Retest after the fix, on the same steps.** Symptom: a finding is closed because the code changed, and the
    problem remains. Fix: replay the recorded steps with the same pairing before closing, and keep them as a
    regression checklist for the next release.
14. **Single-character shortcuts can be turned off or remapped.** Symptom: a page binds bare keys (`/` to search,
    `?` for help, `g` then a letter to navigate) and a speech-input user's dictated words, or a keyboard user's
    stray key, fires them. Check: search the scripts for key handlers that react to a printable key with no
    modifier (`keydown` or `keypress` with `event.key` compared to one character) and, for each, whether it is
    inactive inside text fields, can be disabled, can be remapped, or only runs while its own component has
    focus (WCAG 2.1.4; read the exact conditions in the criterion, and `accesskey` is covered in §6.15). Fix: a
    modifier key, a setting that turns the shortcuts off, or scoping the handler to the focused component.
15. **A focus ring removed on the fields people type in.** Symptom: the link and button rules keep a focus style
    while the text areas, inputs and selects set `outline: none` and rely on a 1px border colour change, or on a
    container's `:focus-within`, which the eye does not read as focus. Check: search the stylesheets for
    `outline: none` and `outline: 0`, then for each hit find the replacement rule that applies to that same element
    in the same state and look at its contrast against its neighbours (§1.3, §3.5); the existence of a global
    focus rule is not proof, because it may not select form controls. Fix: one `:focus-visible` rule that covers
    every focusable element, with an outline or ring of its own rather than a recoloured border.
16. **A state change with no announcement.** Symptom: a button whose label flips to "Copied" or "Saved" for a
    second, a counter that updates, a result that appears below the field: sighted users see it and a
    screen-reader user hears nothing. Check: list the places the code changes text or state after an action
    (clipboard writes, save handlers, async results) and for each whether the change lands in a live region that
    already exists in the page, or moves focus to the result (§2.3, §8). Fix: a polite status region that exists
    before the message arrives, and one message per action.
