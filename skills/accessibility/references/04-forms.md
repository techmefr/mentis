# § 4 — Forms: the most frequently broken point

> Section 4 of `skills/accessibility`. Read it on any diff touching a field, a validation path, a
> multi-step flow or an authentication screen. Points 4 and 5 are the WCAG 2.2 criteria closed on
> 2026-08-10 and are cited by number from `references/origin.md`.

1. Every field has an associated `<label>` (`for`/`id` or wrapping), never a placeholder alone as a
   label: the placeholder disappears as soon as you type. Two consequences follow from the same cause: a
   reader interrupted mid-form is left with filled fields and no names for them, and the association is
   also what makes the label a click target for the field, which is the part a mouse user loses without
   noticing why the form feels imprecise.
2. Error message associated with the field through `aria-describedby`, announced at the moment it
   appears (not only displayed visually). Displayed-only is the default outcome of every framework, so
   this is the point that has to be written deliberately: without the announcement the reader submits,
   hears nothing, and concludes the button is broken.
3. Required fields marked with `required`/`aria-required`, not only by a visual asterisk with no exposed
   equivalent. The asterisk also has to mean something the reader was told — a legend they cannot reach
   is a convention they have to infer from being rejected.
4. **Never re-ask for information the user already gave earlier in the same process** (WCAG 2.2, Redundant
   Entry) — a multi-step form that loses a field's value going back a step, or an address re-typed after
   it was already entered for billing, forces a choice between re-entry and abandoning. Carry the value
   forward, or offer it as a pre-filled/selectable option.
5. **No cognitive test (solve a puzzle, transcribe a code, recall a memorised answer) as the only way to
   authenticate** (WCAG 2.2, Accessible Authentication Minimum) — a password field is fine as long as
   paste and a password manager are allowed (never block paste on an authentication field, see also
   `security-hardening`/the stack conventions), and a CAPTCHA needs a non-puzzle alternative (audio,
   email link) alongside it.
6. **A field declares what it is for, so the platform can fill it.** Autocomplete metadata on name,
   email, address and payment fields is what lets a browser or a password manager complete a form, and
   for some readers that is the difference between a form they can complete and one they cannot. It
   costs one attribute and is omitted by default.
7. **A field's input type is an accessibility decision.** The type selects the on-screen keyboard, the
   built-in validation and the format the platform will accept, so a numeric value in a plain text field
   hands a phone reader the wrong keyboard and loses the platform's own error handling. Use the specific
   type and let it do the work rather than validating the same thing by hand.
8. **On submission, focus goes to the problem.** A summary at the top of the page that the reader cannot
   reach is a summary that does not help; moving focus to the first invalid field, or to a summary whose
   entries link to their fields, is what turns the error list into a route through the form
   (`business/ux-writing` §1.4).
9. **Validation timing is part of the design.** Validating on every keystroke announces an error while
   the reader is still typing the value, so the region fires repeatedly and the message is wrong until
   the last character; validating on blur, or on submit, gives one announcement per field. Where a rule
   can be shown before the attempt, showing it there is better than any timing.
10. **A control's state has to be exposed, not only styled.** A disabled submit button that is only
    greyed out is announced as available, so the reader activates it and nothing happens with no
    explanation — and a disabled control is unreachable by keyboard, which means the reason for the
    refusal has to live somewhere the reader can reach (`business/interface-design` §4.9).
11. **Related fields are grouped, and the group is named.** A set of radio buttons or a pair of date
    fields read one by one without their question is a list of options with nothing to choose between;
    the grouping element and its legend are what carry the question to the reader who hears the options
    out of context.
12. **A time limit needs a way to extend it, and a session ending needs to be recoverable.** A form that
    expires while it is being completed discards work, and completing a form more slowly is exactly what
    several of the readers this block exists for do. Where a limit is genuinely required, it is
    adjustable, extendable, or the work survives it.
13. **Success has to be announced too.** A form that submits and shows a confirmation only visually
    leaves the reader unsure whether anything happened, and the reliable next action is to submit again
    — which on a form that writes is a duplicate record.
14. **A multi-step flow says where the reader is.** Step position, what remains, and what has been kept
    from previous steps: without it, going back to correct one answer is a decision taken blind, and it
    is the same flow where point 4's redundant entry does its damage.
