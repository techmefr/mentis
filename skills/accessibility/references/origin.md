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

**Contrast arithmetic added 2026-10-02: `bin/contrast_check.py` (stdlib, formula from the WCAG 2.2
definitions of relative luminance and contrast ratio, knee at 0.04045) written to compute the ratio
instead of eyeballing it; it prints no threshold.

**No threshold was added, and that is deliberate.**** The figures in §3.1 and §1.8 are the ones already
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

**§5 (RGAA) added 2026-09-29.** The block previously deferred all RGAA specifics to "an org design
catalogue" — a skill that isn't actually part of `mentis`, so a plain-repo install of this block had
nothing to read RGAA from at all (`CATALOG.md` §0: a rule can't be left broken on a plain repo). RGAA 4.1
is now written up directly in `references/05-rgaa.md`: what it is and who it legally binds, the 13
thématiques and 106 criteria, the official per-criterion test methodology that is the actual difference
from a WCAG-level judgment call, the mandatory déclaration d'accessibilité (schéma pluriannuel, plan
d'action annuel, per-page mention, required content) and what triggers it, and the sanction regime under
the 2023 decree. `SKILL.md`'s boundary paragraph was rewritten: it no longer names an org catalogue as the
source for RGAA — that catalogue, where one exists, still owns a **mockup-time numeric threshold** (same
carve-out as `business/interface-design` §0), but RGAA itself is now self-sufficient here.

Sources read for §5: the official RGAA 4.1 reference
([accessibilite.numerique.gouv.fr](https://accessibilite.numerique.gouv.fr/), its
[critères et tests](https://accessibilite.numerique.gouv.fr/methode/criteres-et-tests/) and
[champ d'application](https://accessibilite.numerique.gouv.fr/obligations/champ-application/) pages,
and the [RGAA 4.1 PDF](https://accessibilite.numerique.gouv.fr/doc/RGAA-v4.1.pdf)) for the criteria
count, thématiques, test-methodology structure and the RGAA private-sector threshold; secondary
sources (rgaa-checker.com, sk-web.fr, Sorena, Quertum) for the ordonnance 2023-859 sanction amounts
and the EAA's own threshold and transposition date — checked 2026-09-29, both directly against
`accessibilite.numerique.gouv.fr` where that page states the figure.

**Correction made same day, before merge: the private-sector threshold in an earlier draft of §5.2
was wrong.** It stated RGAA's own private-sector threshold as "more than 10 employees and more than
€2M turnover" — that figure is the European Accessibility Act's micro-enterprise exemption (directive
2019/882, French transposition loi n°2023-171 du 9 mars 2023, applicable since 28 June 2025), a
separate regime covering specific EAA-listed services, not RGAA's general private-sector scope. The
official RGAA portal states the RGAA private-sector threshold as **€250M average annual turnover**,
unchanged by the 2023 texts — those texts (ordonnance 2023-859) changed ARCOM's enforcement powers for
the existing population, not the threshold itself. §5.2 now states both thresholds separately, sourced
from the official portal (RGAA's €250M line) and from EAA-specific secondary sources (the microenterprise
exemption), and says explicitly not to read one as settling the other.

**Still flagged unverified inside §5, deliberately, rather than asserted as fact**: the exact sanction
amounts under the ordonnance 2023-859 regime (multiple secondary sources agree on €50k/€25k renewable
~6-monthly, not independently confirmed against the ordonnance's own text); and whether 106 criteria
still holds for whichever RGAA point-release is current when this is read — the count is versioned
and this pass checked 4.1/4.1.2 only, on 2026-09-29, confirmed independently across the official RGAA
4.1 PDF and two independent trackers (Handinova, rgaa-test.fr), which additionally agree on 258 tests
across the 106 criteria (not yet stated in §5.1, could be added). Re-verify the sanction amounts before
they land in a contract or a legal document, same discipline as the contrast thresholds in §3.

§6 to §8 and two additions to §1.2 and §3.8 written on 2026-10-02 after reading the public
`Front-End-Checklist` repository (README and package metadata declare MIT; no licence file is present, so
only the list of topics was used and no sentence was reused) and the layout-and-accessibility sections of
the public `anti-slop` family (MIT). The facts come from the primary documents: the HTML Living Standard
(tabular data, lists, `iframe`, `object`, `autofocus`, `accesskey`, `meta refresh`), WAI-ARIA and ARIA in
HTML (role validity, required owned elements, required names), the W3C ARIA Authoring Practices Guide
(tabs, accordion, tooltip, carousel, breadcrumb patterns), and WCAG 2.2 success criteria 1.2.1 to 1.2.5,
1.3.2, 1.3.4, 1.4.2, 1.4.5, 1.4.13, 2.1.4, 2.2.1, 2.2.2, 2.3.1, 2.3.3, 2.4.3. No numeric threshold is
stated in these sections; flash limits and durations are deferred to the criteria. Not taken:
vendor-specific audit rule counts, tool names as requirements, and the checklist's generic verification
text.
