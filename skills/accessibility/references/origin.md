# accessibility — origin and source stamps

> Provenance of `skills/accessibility`. Read it when a rule has to be traced back to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

Sourced from WCAG 2.2 (level AA, success criteria taken over), MDN (HTML semantics, ARIA authoring
practices), W3C ARIA APG (modal/accordion/tab patterns). Mechanisms rewritten as an actionable
checklist, no copied text. Market research, no internal production feedback at this stage: same status
as `seo`.

Re-checked on 2026-08-10 against the closed list of success criteria genuinely new in WCAG 2.2 (not
carried over from 2.1): 5 of the 6 at level A/AA were real gaps, now closed — Focus Not Obscured (§1.6),
Dragging Movements (§1.7), Target Size Minimum (§1.8), Redundant Entry (§4.4), Accessible Authentication
Minimum (§4.5). Consistent Help (3.2.6, level A — a help mechanism's position/order staying consistent
across pages) was left out: it's a site-structure concern closer to `seo`'s navigation consistency than
to this block's component-level checklist, and adding it here without a real multi-page help pattern to
anchor it to would be exactly the "we'll need it" this framework's own `design-patterns` guardrail warns
against.

**Sectioned and deepened 2026-09-08.** The four inline sections moved to one file each under
`references/` and the router became a table of triggers. No section was added: the four are the standard's
own shape at component level. Every section and point number was preserved, which matters here because
the 2026-08-10 re-check above cites §1.6, §1.7, §1.8, §4.4 and §4.5 by number as the criteria it closed —
the five new points are still at those exact positions, and the additions were appended after them.

**No threshold was added, and that is deliberate.** The figures in §3.1 and §1.8 are the ones already
sourced from WCAG in an earlier pass and are unchanged; every point added by this pass is a mechanism,
not a number, because a recalled threshold is exactly the failure `skills/source-freshness` exists for
and `business/interface-design` §0.7 states the same rule from the design side.

**What the depth adds.** The original was a checklist of true statements, most of them one line, and its
gap was the same in every section: it said what to do and not what a reader experiences when it is not
done — which is the half a developer needs in order to prioritise, and the half a reviewer needs in order
to argue the point. The additions that were real absences rather than elaborations:

- **§1**: headings as the *navigation* mechanism rather than typography, so a document whose headings
  were chosen for size leaves a screen-reader user reading a dense screen linearly; landmarks and a skip
  link, the highest-value item per line of code on the whole list and the one most often absent because
  it is invisible to a mouse user; the page's declared language, which selects the pronunciation rules
  and whose absence no visual check can see; hover-only affordances, which do not exist for a keyboard
  and misfire on touch; moving or auto-updating content needing a pause; the affordances removed for
  tidiness (text selection, context menu, blocked paste, hijacked scrolling); and a single-page
  navigation that changes the view without moving focus, so the reader concludes the link did nothing
  and activates it again.
- **§2**: that a `role` *replaces* semantics rather than adding to them, which is why absence degrades
  and a wrong value misinforms; that a live region has to exist in the DOM before its content arrives,
  and that `assertive` interrupts whatever is being read; that a state attribute set once at render is
  worse than absent, because it now asserts something wrong half the time; that an accessible name has
  to contain the visible label or a voice-control user cannot activate the control; that `aria-hidden`
  over a focusable subtree produces a tab stop with nothing announced; that a custom widget owes the
  whole keyboard pattern the role promises; that `title` is not a label; and what a tool can and cannot
  check here, which is the mechanism behind the guardrail that a tooled audit does not replace the
  manual pass.
- **§3**: that eyeballing contrast fails in one consistent direction, on the display and in the light it
  was designed in; that a reader's font size is a different mechanism from browser zoom, so a layout
  passing one can fail the other; that non-text controls — a focus ring, an input's boundary, a
  meaningful icon — need contrast too, and a low-contrast one looks like a missing control; that
  colour-only link styling makes a paragraph's interactive words undiscoverable; that text over an image
  has no single ratio and needs a scrim rather than a measurement; reduced motion as a symptom rather
  than a taste; the copied viewport attribute that disables pinch zoom and survives review because
  nobody notices what it removed; and that a dark theme is a second set of colours to measure, not a
  filter over the first.
- **§4**: that the label association is also what makes the label a click target, which is the half a
  mouse user loses without knowing why; that displayed-only errors are every framework's default, so the
  announcement is the part that has to be written deliberately; autocomplete metadata, one attribute
  that decides whether some readers can complete a form at all; the input type as an accessibility
  decision, since it selects the on-screen keyboard and the platform's own validation; focus moving to
  the problem on submission; validation timing, where per-keystroke announces an error while the value
  is still being typed; a disabled control being announced as available and unreachable by keyboard at
  the same time; grouped fields needing a named group, or the options are read with nothing to choose
  between; time limits, which penalise exactly the readers this block exists for; success needing an
  announcement too, or the reader submits again and writes a duplicate; and a multi-step flow saying
  where the reader is, which is the same flow point 4's redundant entry damages.

Router plus sections: 1,027 → 3,896.

**Status.** Unchanged: still no in-house production experience and still not proven doctrine, to be
confronted with the first real audit. What the depth changes is what the block is good for in the
meantime — a reviewer citing a point can now say what it costs the reader, which is what makes an
accessibility remark survive a discussion about priorities. The `link` agent remains the reader for a
whole page or site in production; this block stays scoped to the diff.
