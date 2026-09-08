# flutter-conventions §9 — Text, motion, monitoring

> Section 9 of `skills/flutter-conventions`. Read it when user-visible text, an animation, crash reporting. The other sections and the guardrails stay in `SKILL.md`.

1. No user-facing string hardcoded in a widget: text, dates, numbers and currency go through the
   localisation layer with typed keys. Currency and date formats are locale rules, not string formatting —
   a decimal comma, a day-before-month order and a currency symbol that follows the amount are all decided
   by the reader's locale, and hand-formatting them produces a figure that is wrong rather than merely
   foreign.
2. **Never assemble a sentence from fragments.** Concatenating a noun, a verb and a count works in the
   language it was written in and nowhere else, because word order is not universal. One parameterised
   message per sentence gives a translator something they can actually reorder — and it gives a reviewer
   something they can read.
3. **Plural is not two cases.** A `count > 1` ternary is already wrong for zero in some languages and for
   the two-to-four band in others, and the mistake is invisible to everyone who speaks the source language.
   Use the localisation layer's plural mechanism, which exists precisely because this cannot be done with an
   `if`.
4. **One key per meaning, never per coincidence.** Reusing a key because two places happen to read the same
   in the source language couples them for ever: the day one has to change, the other changes with it, in a
   language nobody on the team reads. The duplicate string is cheaper than the shared key.
5. **Translated text is longer.** German runs roughly a third longer than English and some languages run
   shorter, so a button sized to its source label truncates or overflows (§3.2's flex overflow, arriving
   from the text layer). Let labels wrap or ellipsise deliberately, and look at the longest locale once.
6. **A right-to-left locale mirrors the layout.** Directional insets and alignment do that for you; `left`
   and `right` do not, so a hardcoded padding leaves the icon on the wrong side of its label and the back
   arrow pointing into the screen. Never render a translation as markup either — a string that reaches a
   rich-text or HTML renderer is a translator with injection rights.
7. Implicit animations by default; an explicit animation controller only where the motion genuinely needs
   driving — and it's disposed (§1.8). The implicit form has no controller to leak and no ticker to leave
   running, which is most of why it is the default rather than a matter of brevity.
8. **Motion is an accessibility setting, not a style choice.** The platform exposes a reduce-motion
   preference because large transitions are a vestibular trigger, so an animation checks it and falls back
   to a cut or a fade. Duration and curve come from the design system rather than from a number typed at
   each call site, or the app's motion stops reading as one app.
9. **An animation off-screen still costs.** A repeating animation whose widget is behind another route keeps
   its ticker on the scheduler, burning frames and battery for something nobody can see — and it is also
   what makes a test's unconditional settle hang for ever (§10.5). Stop it when the screen is not visible.
10. Crash and error reporting initialised once at startup, with the environment and release stamped,
    sampling configured deliberately, and payloads scrubbed of personal data before they leave the device.
    Each of those four is a separate failure if skipped, which is why they are one rule and not four.
11. **Without the release identifier and its symbols, a report is a wall of hex.** A release build is
    obfuscated, so the symbol upload belongs in the same pipeline step that produced the binary — done
    later, or from a developer's machine, it does not match, and the crashes arriving from real users are
    unreadable for the entire life of that version.
12. **Report the non-fatals too.** A caught exception that leaves the user on the error state of §4.5 is
    invisible to monitoring by construction: nothing crashed. That class of failure is the one users
    actually meet, and the only place it shows up is the count of people who stopped using the feature.
13. **An expected failure is not a crash.** Reporting every offline request and every cancelled navigation
    alongside real exceptions raises the volume until the real ones cannot be found — the same harm as
    reporting nothing, arrived at from the other direction. Sample by kind, deliberately.
14. **Scrubbing is about what you attach, not only about what you redact.** Identifiers are enough to
    correlate a report with a user through your own systems; a request body, a form's contents or a screen
    capture puts personal data into a third-party tool, retained under someone else's policy and outside
    the deletion path the app promises.
15. Prefer hand-written code over code generation where the project has taken that position, and don't
    introduce a generation step (and its generated files, its build config, its watch mode) for one model.
    The cost is not local: every contributor and the CI pipeline now needs that step, generated files fill
    every review, and a stale artefact produces a compile error that names a file nobody wrote. It is a
    project-level decision, and one model is not the moment to take it.
