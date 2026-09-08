# interface-design — origin and source stamps

> Provenance of `business/interface-design`. Read it when a rule has to be traced back to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**An org design-system skill catalogue (10 skills: foundations and grid, spacing scale and rhythm, buttons,
chips, containers decision tree, icon-text coupling, screen states, mockup accessibility, mockup UX writing,
inspiration search from a story)** — rules extracted, de-identified and rewritten generically, with **every
house value deliberately left out** (grid step, pixel sizes, spacing steps, type scale, component heights)
because those are owned per design system and a copied number is a wrong number in the next project
(rule C). The two overlapping subjects were **not** duplicated: mockup accessibility stays with
`skills/accessibility` (which cites its standard) and mockup copy stays with `business/ux-writing`; this
block cross-references both instead of restating them. Mechanisms rewritten, no copied text.

**Deepened 2026-08-06.** The first pass wrote this block from the catalogue skills' descriptions. This pass
read the **bodies**, which is where the reasons, the exclusion lists, the carve-outs and the anti-pattern
catalogues live — a description states the rule, a body states when it doesn't apply. What that added here:
the **production-versus-audit mode** discipline (§0) that every one of those skills opens with and no
description mentions, the caution principle on numeric thresholds, the scope limit on screen states (dynamic
data only) with a per-state obligation condition rather than four boxes, the two quality rules on empty and
error, the deliberate refusal to fix the visual form of a state at mockup time, "a modal is an autonomous
context so it carries its own primary", and choosing modal versus bottom sheet by role rather than by
appearance. Stamped 2026-08-06.

**Sectioned and deepened 2026-09-08.** The six inline sections plus §0 moved to one file each under
`references/` and the router became a table of triggers, with §0 marked read-every-time because the mode
changes how every other section reads. No section was added: the seven already covered the subject. Section
and point numbers were preserved throughout — nothing outside this block cites them, but §4 cites §2.6, §6
cites §1.9 and §0.2, and the guardrails now cite the points they enforce.

**What the depth adds.** The original stated its rules and, in most sections, not what the reader sees when
one is broken — which is the half a designer needs in order to argue for the rule against someone who
disagrees, and the half an auditor needs in order to write a finding that lands. The additions that were
real absences rather than elaborations:

- **§0**: that the two modes fail in *opposite* directions, so naming the mode is what stops a production
  pass from becoming a list of hedges and an audit from becoming an uninvited redesign; that a
  disagreement about intent is never a finding; that a finding names the element and not the screen; and
  that most of what an audit of a mockup turns up is *absence*, which is invisible in a screenshot and
  therefore the part that reaches step 6 unresolved.
- **§1**: that two values both taken from the scale can still be wrong together, when the gap inside a
  group exceeds the gap between groups — the one check the scale cannot do for you; that a token is a
  *name*, so copying the number it resolves to defeats it while looking identical in the mockup; and that
  where no scale exists, choosing one is the deliverable rather than a side effect, because a scale living
  only in the mockup's geometry has to be reverse-engineered by measuring rectangles.
- **§2**: the scroll contract each container carries, which is why "it grew" is the usual reason a modal
  became the wrong choice with nobody having changed the decision; that a layer over a layer leaves no
  unambiguous meaning for dismiss; that a container decides where focus lives and where it returns, which
  the drawing cannot show; and the asymmetry that makes this decision belong here at all — reversible on
  paper, expensive in code, and for the implementer the cheapest option is always whichever container the
  surrounding code already uses.
- **§3**: the partial failure, the state nobody draws, where one region of an assembled screen fails and
  the reader sees a complete-looking screen with a silently missing number; that the three error causes
  (unreachable, server, permission) are three different messages and collapsing them makes a reader retry
  something they will never be allowed to see; that a state replacing the screen discards the filters and
  scroll position the reader had; and that a loading state which shifts the layout costs a misclick.
- **§4**: that a destructive action is never a screen's primary, since primary styling is where the hand
  goes by default; that a disabled control with no reason is indistinguishable from a broken one; the
  in-flight state of anything that writes, which is the state drawn least and the one whose absence
  produces duplicate writes; that the focus state is not the hover state; and that a control's label is
  its accessible name, so four identical "Confirm" labels are four indistinguishable entries in a list of
  controls.
- **§5**: that an icon-only control has to survive being unrecognised, which rules it out for
  irreversible actions however good the glyph; that a mismatch between glyph and label is resolved by the
  reader in favour of the glyph, because the glyph is what they scanned; that a tooltip is not a place to
  put information, being unavailable to touch and gone on the first movement; and that an icon carrying
  meaning alone needs a second cue, in a greyscale copy as much as for a reader who cannot use colour.
- **§6**: that the constraints a reference imports are the ones it does not show — data volumes, the
  permission model, the device mix; that a reference is prior art and not evidence, so the reason is the
  mechanism stated in a sentence rather than "a big product does it this way"; that the rejection is the
  part that gets re-litigated and therefore the part worth writing down; and that prior art gathered
  after the screen is drawn is a justification, since it gets filtered for whatever agrees with the
  drawing.

Router plus sections: 2,041 → 5,938.

**Status.** The catalogue behind this block is unchanged and still stands, and the depth is ours: written
from what goes wrong between a mockup and step 6, not from a source that can be re-checked. The block has
no design system of its own behind it, and never will have — by construction, since the numbers are exactly
what rule C keeps out, and that is why every rule here is a discipline or a decision tree instead.
