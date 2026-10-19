# § 9 - Microinteractions

> Section 9 of `business/interface-design`. Read it when a single small interaction is being designed or
> audited: a toggle, an inline edit, a delete, a save, a tooltip, a hover, a transition between two states.
> The large shape of a screen is §7; the states a screen must have are §3.

A microinteraction is one trigger, one response, and the rules between them. Most of the polish people
notice, and most of the damage they notice, lives here: a control that does nothing visible, an animation
that delays the next click, a confirmation for something that could simply have been undone.

1. **Four parts, named, for every interaction you design.** What starts it (the trigger: a click, a key, a
   system event). What the system does (the rules). What the person sees, hears or feels (the feedback).
   What happens the second and the tenth time (the loops and modes). An interaction missing a part is a
   question that reaches implementation unanswered; the usual missing part is the last one.
2. **Feedback is proportional and immediate.** A frequent, low-stakes action gets a small, quick response;
   a rare, consequential one gets a clear, stable one. The failure modes are symmetrical: silence after a
   consequential action makes people repeat it, and ceremony after a trivial one trains them to ignore the
   ceremony.
3. **Silent success is allowed only where the result is visible.** Saving a draft the person can see in
   place does not need a toast; sending a message that leaves the screen does. "Silent" means no extra
   announcement to the eye, never none to assistive technology: a status change that is not a focus
   change is still exposed programmatically (the status-message criterion in the accessibility standard,
   `skills/accessibility`).
4. **Undo before confirm, for anything reversible.** A confirmation dialog interrupts every time to
   protect against a rare error; an undo costs nothing the rest of the time. Use a confirmation only for the
   irreversible, with the consequence stated (`business/ux-writing` §2.2, container choice in §2.6 here).
   An undo has a visible window long enough to be reached and an equivalent that works without a pointer.
5. **An optimistic update shows the result at once, offers undo, and has a visible rollback.** When the
   server rejects the change, the interface returns to the previous state and says so where the person is
   looking. An optimistic update with no failure path is a lie that lasts until the next reload.
6. **Tooltips treat hover and focus differently on purpose.** Hover can wait a moment so that crossing the
   screen does not flicker a dozen labels; keyboard focus shows it immediately, because the person has
   arrived deliberately. Content that appears on hover or focus must be dismissible without moving the
   pointer, must stay while the pointer is over it, and must stay until dismissed (the content-on-hover-or-
   focus criterion in the accessibility standard). A tooltip is never the only place a control's name lives
   (§5).
7. **Refuse these by default.** Animating every property on a state change (it animates things nobody
   meant to animate, including layout); a uniform scale-on-hover applied to every card and button; bounce
   or overshoot easing on utilitarian controls; a focus indicator that fades or travels in (it has to be
   there the moment focus arrives); a celebratory toast for routine success. Each is allowed with a
   written reason (§7.1), and none is a default.
8. **Motion carries meaning or it goes.** Good reasons: it shows where something came from or went, it
   links a cause to its effect, it keeps continuity across a layout change. Test: remove the motion; if no
   one could tell what changed, the motion was explaining something and stays; if nothing is lost, it was
   decoration. Reduced-motion preferences get an equivalent that keeps the meaning, not a bare removal
   (`skills/webperf` for the motion budget, `skills/accessibility` for the preference).
9. **Durations and easings are named tokens of the design system.** A few named steps (quick, standard,
   deliberate) and a small set of easings, chosen once. This block gives no number, for the reason in §0.7:
   a figure here would be a value owned by a system it cannot see. Where none exists, choose the names and
   values once and write them down (§1.10).
10. **Repeated interactions get quieter.** The first time deserves explanation and flourish; the hundredth
    time is a tax. A power-user path (shortcut, remembered choice, no intro animation after the first run)
    is part of the design of a frequent control.
11. **A loop has an exit.** Anything that repeats (polling, a progress indicator, a retry) says when it
    ends and what it does at the end. An indeterminate indicator that runs for ever is a state nobody
    drew (§3.1).
12. **When in doubt, cut.** Remove the effect and look at the result. If the interaction still reads, the
    effect was extra. If it stops reading, the structure was wrong and the effect was covering for it;
    fix the structure.
13. **Audit by forcing the states.** To check an interaction, render each of its states by forced classes
    (§3.11): rest, hover, focus, pressed, disabled, loading, success, failure. An interaction whose
    failure state was never drawn has not been designed (§3.3).
