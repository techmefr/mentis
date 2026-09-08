# § 4 — Buttons and chips

> Section 4 of `business/interface-design`. Read it when action hierarchy is being decided, or when a
> filter bar, a toolbar or a set of status indicators is being drawn or audited.

1. **One primary action per autonomous context** — per page, per modal, per panel. Two primaries means
   the hierarchy is undecided, and the user has to make that decision instead. What that costs is a
   pause on every visit to the screen, and on a destructive pair it is worse than a pause: the two
   equally weighted buttons are chosen by position, and position is the thing that changes between
   platforms.
2. **A modal, a drawer or a bottom sheet is an autonomous context**: it carries its own primary button,
   independently of the page underneath. That's what "per autonomous context" means, and it's the part
   people get wrong when they count primaries per screen. Counting per screen produces the opposite
   error — a modal with no primary at all, so the action it exists for is styled as secondary and reads
   as optional.
3. Below it, a fixed ladder (secondary, outlined/inline, link with icon, link only) used for its
   meaning, not for variety. The ladder is information: a reader who has learned that a link-only
   control is a minor, reversible action reads the next screen faster. Rungs picked for variety spend
   that learning and return nothing.
4. **Size is driven by the container, not by importance**: a button in a compact toolbar is small
   because the toolbar is compact, not because the action matters less. Encoding importance in size
   collides with the container rule the moment the component is reused, and the visible result is the
   same action at two sizes on two screens, which reads as two different actions.
5. Full-width is for a constrained container (a drawer, a bottom sheet, a narrow form), not a way to add
   emphasis on a wide page. A full-width button on a wide page puts its label at one end and the reader's
   attention at the other, and gives a pointer a target it has to cross the screen to reach.
6. **A chip is not a button.** Chips come in distinct kinds — filter, selection/choice, input, and
   informational/status — and mixing them is what makes a filter bar unreadable. A status chip that looks
   clickable will be clicked. What happens then is the part worth stating: nothing happens, so the reader
   concludes the screen is broken, and the ones that do respond teach them to click the ones that don't.
7. Each chip kind keeps its own fixed height, font size and padding; a chip resized by hand stops
   matching every other chip on the screen. The mechanism is that chips are read as a row, not
   individually, so a single off-scale chip is visible as an error even to someone who cannot say why.
8. **A destructive action is never the primary of a screen it shares with ordinary work.** Primary
   styling is where a reader's hand goes by default, and default is the wrong place for an irreversible
   effect. Its confirmation, when there is one, is a container decision (§2.6) and the confirming button
   is the primary *of the confirmation*, which is the only context where destructive and primary belong
   together.
9. **A disabled control has to say why, somewhere the reader can find.** Disabled with no reason is
   indistinguishable from broken, and the reader's next move is to try the same thing again from a
   different route. Where the reason cannot be shown, the honest shape is an enabled control that
   explains the refusal when used — and either way the mockup has to state which, because the
   implementer's default is neither.
10. **Every action's own states are part of drawing it**: hover, focus, pressed, disabled, and the
    in-flight state of anything that writes. The in-flight one is the one that matters most and is drawn
    least: a submit button that stays live during its request is a duplicate write, and the reader's
    evidence for pressing twice is that nothing appeared to happen.
11. **The focus state is not the hover state**, and a control whose focus ring was removed for looking
    untidy is a control a keyboard user cannot locate. This is the single most common way a mockup makes
    a screen unusable without looking wrong (`skills/accessibility`).
12. **A control's label is its accessible name, so the label is not decoration.** "Confirm" appearing
    four times on one screen is four identical entries in a list of controls, with nothing to choose
    between them; the words themselves belong to `business/ux-writing`, but the requirement that they be
    distinguishable is a hierarchy decision made here.
