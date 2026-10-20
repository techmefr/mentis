# § 9 — Manual audit pass: keyboard, screen reader, zoom

> Section 9 of `skills/accessibility`. Read it when a critical journey must be checked by hand, because §2.12
> and §3.11 say a tooled pass is not enough. Own guidance from general craft knowledge, no source read for this
> section; the criteria themselves are in §1 to §8. Screen reader and browser behaviour differs by pairing, so
> record the pairing used and re-test before relying on a result.

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
7. **Zoom and reflow.** Enlarge the page text and zoom the browser to a high level, and use a narrow viewport.
   Check that nothing is cut off, content does not need scrolling in two directions apart from content that
   truly needs it, no control overlaps another, and a fixed header does not eat the screen (§3, §1.8).
   Symptom: a button disappears at high zoom. Fix: fix the layout, never disable zoom.
8. **Check the user's settings.** Turn on a forced-colours or high-contrast mode, a dark scheme, reduced motion,
   and larger system text if the platform offers them. Check that icons and borders survive, that focus is
   still visible, and that motion stops when asked (§7). Own guidance: settings differ by system, note which.
9. **Look at colour and meaning separately.** Check that no information depends on colour alone, status has text
   or a shape, and links are distinguishable in text without relying on hue (§3). Compute contrast with the
   script rather than by eye (`bin/contrast_check.py`) and read the threshold from the standard, never from
   memory.
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
