# § 2 — ARIA: only when native HTML isn't enough

> Section 2 of `skills/accessibility`. Read it before adding any `role` or `aria-*` attribute. The
> golden rule in point 1 is what this block's guardrails cite.

1. Golden rule: no ARIA rather than wrong ARIA; an incorrect `role` or `aria-*` is worse than its
   absence (a contract betrayed for assistive technologies). The mechanism is that a role *replaces*
   what the element was: a `role` on a native control overrides the semantics the browser already
   provided correctly, so the attribute added to be helpful is subtractive. Absence degrades; a wrong
   value misinforms, and the reader has no way to detect it.
2. `aria-label`/`aria-labelledby` on every interactive element with no visible text (icon only, close
   button): never a button that's mute to a screen reader. A control announced only by its role is one
   of several identical entries in a list of controls, and the reader's only way to tell them apart is
   to activate one.
3. `aria-live` (`polite`/`assertive`) on dynamic content areas that have to be announced (notification,
   a form error appearing after submission): otherwise the change is invisible to anyone not using their
   eyes. Two details decide whether it works: the region has to exist in the DOM *before* the content
   arrives, because a region inserted together with its message announces nothing; and `assertive`
   interrupts whatever is being read, so it is for something the reader must hear now and nothing else.
4. `aria-expanded`/`aria-selected`/`aria-current` placed on the components that have the visual
   equivalent (accordion, tab, active item): the visual state must have an exposed equivalent. The rule
   is symmetry — every state a sighted reader can see has to be readable the other way — and its failure
   is silent, since the component looks right in every screenshot.
5. **A state attribute has to be kept in sync, which makes it code rather than markup.** `aria-expanded`
   set once at render and never updated is worse than absent: it now asserts a state that is wrong half
   the time, and the reader trusts it. The same applies to `aria-selected`, `aria-checked` and
   `aria-current` — if the value is not derived from the same state the visual is derived from, it will
   drift.
6. **An accessible name has to contain the visible label.** A control labelled "Save" whose
   `aria-label` says something else is a control a voice-control user cannot activate, because they
   speak what they see and the match fails. Where both exist, the visible text is the authority and the
   attribute elaborates on it rather than replacing it.
7. **Never hide something focusable.** `aria-hidden` on a subtree containing a control removes it from
   the accessibility tree while leaving it in the tab order, which produces a stop where the reader is
   told nothing at all. Hiding a decorative icon next to visible text is the correct use
   (`business/interface-design` §5.4); hiding a live region, a layer's content or anything reachable is
   not.
8. **A custom widget owes the whole keyboard pattern, not just the roles.** A role announces what a
   component claims to be, and the reader then expects the interaction that goes with it: arrow keys
   within a tab list or a menu, `Home`/`End`, one tab stop for the group rather than one per item. Roles
   without that behaviour are a promise the component does not keep, and the reader is left tabbing
   through a widget that told them not to.
9. **Prefer the native element even when it is harder to style.** Every custom replacement inherits the
   whole list above — the roles, the states, the keyboard pattern, the focus handling — and each of them
   has to keep working through every later change to the component. The native control is where that
   maintenance is already paid, and reaching for a custom one to satisfy a visual detail is the trade
   worth naming explicitly.
10. **`title` is not a label.** It is unavailable to touch, appears after a delay, is announced
    inconsistently, and cannot be relied on for anything a reader needs — which is why a tooltip and an
    accessible name are two separate requirements on an icon-only control rather than one.
11. **Never add ARIA out of reflex to look tidy.** A pattern copied from another component brings that
    component's roles and states, which now describe a structure this one does not have; the result
    passes a glance and misdescribes the page. If you cannot say what a role changes for the reader, it
    does not go in.
12. **What a tool can check here is a fraction of what matters.** An automated pass catches an invalid
    role or a missing name; it cannot tell you that a name is wrong, that a state is stale, or that a
    widget's keyboard pattern is absent. Those are found by using the component with the keyboard and
    with a screen reader, which is why the guardrail says a tooled audit does not replace the manual
    test on the critical journeys.
