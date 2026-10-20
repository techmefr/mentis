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
14. **An exit is quicker than its entrance, and the two do not mirror.** Something arriving decelerates into
    place; something leaving accelerates away and takes less time than it took to arrive. A dismissal that
    lingers makes the interface feel slow to obey. The ratio belongs to the design system's tokens (§9.9), not
    to this block.
15. **A spinner that appears for a blink is worse than none.** When the work usually finishes fast, delay the
    indicator so quick results never show it, and once shown keep it long enough to be read. Either rule
    beats a flash that looks like a glitch. Where the wait is long enough to need it, say what is happening
    rather than only that something is (§3.1).
16. **One orchestrated entrance, shown once.** A page or a list may reveal itself in a single staggered
    sequence with a bounded total, triggered by the element reaching the viewport, and it does not replay
    when the person scrolls back or filters. Every section fading in on its own turns the page into a
    perpetual show that never settles. Reveal-on-scroll uses the browser's intersection observation, not a
    scroll listener (`skills/webperf` §2).
17. **A transient layer never moves what is already on the page.** A toast, a banner or a popover stacks or
    floats over the content; pushing the page down and letting it spring back moves the thing the person was
    about to click. Several toasts stack in one corner, and the existing ones keep their place when a new
    one arrives.
18. **A ticking value is announced once, at its final value.** A counter that animates up to a figure, or a
    result count that updates while typing, tells assistive technology the settled value after the movement
    or the pause, not every intermediate step (§9.3). With reduced motion, the final value is shown at once.
19. **Know which criterion a motion falls under, because the preference does not cover all of it.** The
    accessibility standard's criterion on animation from interactions (2.3.3, level AAA) is about motion that
    follows an interaction, such as parallax or things sliding as the person scrolls; essential animation is
    exempt, and movement that merely brings new content into view when scrolling is allowed while extra
    animation added to scrolling must be optional. The criterion on pause, stop, hide (2.2.2, level A) covers
    movement that starts by itself, runs beyond five seconds and sits beside other content, and it counts
    something that starts on hover, focus or on scrolling into view as starting by itself; auto-updating
    content needs a control whatever its length. One animation can fall under both. A standalone loading
    indicator that is not beside other content needs no control. The preference mechanics are in
    `skills/accessibility` §7.8; this block only says to ask the question per animation.
20. **A product has one motion character, written down before the first animation.** One family of easings, a
    short ladder of durations, one way things enter, and one stance on overshoot (none, rare, or playful on
    purpose and stated). Mixed characters read as several products stitched together, and each new animation
    is then a fresh argument. This is what §9.9 asks for as tokens, made a single page the team can point at;
    the values stay the design system's. Where none exists, write the character first and the tokens after it
    (§1.10). A conflict between this page and a one-off request is resolved by changing the page on purpose,
    not by an exception that stays.
21. **Order and direction are decided, not defaulted.** (Optional.) Within a group, the element the eye
    should follow leads, the group shares one direction of entry, and the order on exit is the reverse of the
    entrance rather than a replay. The total and the exit speed stay bounded by §9.16 and §9.14. Skip it for a
    single element.
22. **Anticipation and settle are for interactions that have weight.** (Optional.) A heavy or destructive action
    may wind up before it happens or settle after it lands, because the weight is the message; a toggle, a
    tab or a checkbox never does, because the wind-up is only delay (§9.2, §9.7). Where an interaction is short
    enough that the wind-up would be longer than the action, drop it. The threshold is the design system's
    figure, not this block's.
23. **Review a motion that feels wrong by its symptom, then by its cause.** The symptom names the fix to try
    first, and none of the fixes needs a number from this block:

    | Symptom | Likely cause | First fix to try |
    |---|---|---|
    | Robotic | linear or uniform timing, everything starting and stopping together | an easing family from the tokens, small offsets between items |
    | Slow | duration over budget, a symmetric ease where a decelerating one reads quicker, a long stagger | shorten at the token, decelerate on entrance (§9.14), bound the stagger (§9.16) |
    | Flat | one property moving, no response in the neighbours | let a related element react, only where it explains something (§9.8) |
    | Noisy | many things moving, two competing for the eye | one subject per moment, still the rest (§9.12) |
    | Inconsistent | different easing, direction or duration for the same kind of change | fix at the tokens, not per component (§9.9, §9.20) |
    | Janky | layout properties animating, too many elements at once | the compositor-friendly properties and fewer elements (`skills/webperf` §1, `skills/web-animation-pitfalls` §2) |

    A symptom whose fix removes the effect is the "when in doubt, cut" of §9.12 and is a good outcome.
24. **Dark surfaces and large areas amplify motion.** (Optional.) Bright elements moving on a dark background and
    movement across most of the screen read stronger than the same motion on a small, light surface, and can
    tire the eye sooner. Check the motion on the real surface it ships on, at its real size, and in both themes
    where there are two (§1.13). This block gives no reduction: the source of the idea gave a percentage with no
    basis, so none is carried.
