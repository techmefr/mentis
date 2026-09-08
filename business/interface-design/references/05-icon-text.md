# § 5 — Icon and text together

> Section 5 of `business/interface-design`. Read it whenever an icon sits next to a label, or a control
> is icon-only.

1. **The icon's size drives the text's**, not the reverse — text set to match a large icon reads as a
   heading it isn't. The visible consequence is a row that outranks the real heading above it, so the
   reader's eye starts in the wrong place and the page's structure has to be re-derived from position.
2. A **bare** icon and a **framed** icon (one in a padded container) are two different objects with two
   different spacing rules; treating them the same is the recurring mistake. A framed icon's visual
   weight comes from its container, so the pairing rule is not the bare one with padding added. Applying
   the bare rule to a framed icon produces a gap that measures correctly and reads as double, because
   the frame's own padding is already part of the distance.
3. A fixed gap between an icon and its label, from the spacing scale — **and the gap differs depending
   on whether the icon sits before or after the text**, because the optical distance isn't symmetric.
   Two cases, two values, both from the scale. A single value used both ways looks right in one
   direction and loose in the other, which is why the pair of values is worth writing down once rather
   than re-judged per component.
4. An icon next to visible text is decorative: it is hidden from assistive technology rather than read
   twice (`skills/accessibility`). Read twice, the reader hears the concept, then the same concept again
   under whatever name the icon file happens to carry — and that name is usually a shape rather than a
   meaning.
5. An icon-only control needs an accessible name, and it needs a tooltip for sighted users too — a glyph
   nobody recognises is not a label. Both are needed because they serve different readers, and shipping
   only the tooltip leaves the control unnamed to assistive technology while shipping only the name
   leaves a sighted reader guessing.
6. **An icon-only control has to survive being unrecognised.** Only a small, conventional set reads
   reliably on its own; anything else is a puzzle whose answer is discovered by clicking, which is a
   problem in proportion to what the control does. Where the action is destructive or irreversible, an
   icon-only control is the wrong choice regardless of how good the glyph is.
7. **The icon and the label have to mean the same thing.** A mismatch — a download glyph on an export
   action, a pencil on a control that opens a read-only view — is resolved by the reader in favour of
   the glyph, because the glyph is what they scanned. So the mismatch is not a cosmetic inconsistency, it
   is a wrong expectation formed before the label is read.
8. **A tooltip is not a place to put information.** It is unavailable to touch, appears only after a
   delay, and disappears on the first movement, so anything that has to be read to use the control
   belongs in the interface. A tooltip repeating the accessible name is the correct use; a tooltip
   carrying the only explanation of what the control does is a hidden interface.
9. **An icon carrying meaning on its own needs a second cue.** Colour and shape are not available to
   every reader, so a status expressed as a coloured glyph and nothing else is a status some readers
   cannot read at all — and the same is true in a printed or greyscale copy of the screen. The pairing is
   the fix: the glyph plus a word, or the glyph plus a text alternative
   (`skills/accessibility`).
