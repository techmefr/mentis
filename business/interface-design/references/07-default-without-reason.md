# § 7 - A default without a reason

> Section 7 of `business/interface-design`. Read it when a visual treatment is being chosen for how it
> looks (glass, glow, gradients, shadows, a decorative colour, a status dot), and in every audit.

A default is a choice nobody made. The model's habits and the web's fashions fill a mockup with
treatments that have no function, and the sum looks like every other product. The remedy is not a list of
banned styles (styles change; a list is stale on arrival) but a requirement that a treatment can say why it
is there.

1. **Three levels.**
   - **Forbidden outright:** things with no defensible reason in any product (a hand-drawn fake browser
     bar, §3.13; invented metrics, §3.12; a status dot with no state behind it).
   - **Allowed with a written reason:** a treatment is fine when a one-line reason sits next to it in the
     brief or the task notes ("glass behind the player controls so the cover art stays visible"). No
     reason, no treatment.
   - **Consistency locks:** once a decision exists (corner radius family, one shadow recipe, one accent
     role), every screen follows it; deviating is a finding even if the deviation looks nicer.
2. **Caps on dose.** Effects such as translucent glass, glows and drop shadows live on one or two elements
   per screen at most. Colour is two or three base hues plus one accent; the accent marks the thing to act
   on, and a second accent competes with it. A status indicator (dot, pill, badge) exists only when a real
   state drives it.
3. **The logo test.** Remove the logo and ask whether the design is still recognisably this product's. If
   it could belong to anyone, the screen is made of defaults; find the decision that makes it specific
   (type, density, a signature layout, a consistent illustration rule) and apply it.
4. **Audit severity follows the level.** A forbidden item is critical. A treatment with no written reason is
   major. A broken consistency lock is major when visible on the same screen as the lock, minor otherwise.
   An exceeded dose is minor until it hides content.
5. **No catalogue of looks.** This block does not name graphic modes to choose from. A mode list invites
   picking a style first and finding the content afterwards; the direction (§0.9) comes first and the
   treatments follow from it.
6. **No stylesheet stamps.** Do not leave a comment in the CSS announcing the design system or the tool
   that produced it. The tokens are the record.
7. **Counted caps per page.** Rules a grep or a count can check, stated as a ceiling whose number comes from
   the project's design system (or is chosen once and written down), never a figure carried over from
   elsewhere:
   - small uppercase, widely tracked labels above headlines: capped relative to the number of sections;
   - one layout family (a given grid or card arrangement) used once per page;
   - alternating image and text splits: capped in a row;
   - text elements in the hero: capped, with no tagline, trust strip or pricing teaser stacked in it;
   - the navigation fits on one line at desktop width;
   - a bento or feature grid has exactly as many cells as there is content;
   - a divider under every row of a list is replaced by grouping;
   - no badge or pill laid over an image (a caption below, outside it);
   - no scroll cue, and no generic "Step 1 / Step 2 / Step 3" labels: name the step by what it does.
   A count that exceeds its cap is a finding under §7.4's severity rules.
8. **An application screen is built around the decision it serves.** The default dashboard shell (a
   sidebar, a row of statistic cards, a big chart, a recent-activity feed) is a layout looking for
   content. Start from the decision instead: who opens this screen, what do they decide, what do they
   need to see to decide it. Then:
   - a chart answers one named question; its title is that question or its answer, and an unlabelled
     chart is a decoration;
   - a statistic card has a source, a period and a comparison (§3.12); a card with a number and an up
     arrow and nothing else is removed;
   - an activity feed exists when someone acts on the events in it, otherwise it is filler;
   - table columns are the ones a reader uses (§10.6), not the columns the database has;
   - filler data in a mockup is replaced by realistic structure or an honest placeholder (§3.12).
   Severity follows §7.4: a card with an invented figure is critical (forbidden), a chart without a
   question is major.
9. **Tells of a build that was never looked at.** Treatments that show a screen was produced and shipped
   without a human reading it, each forbidden unless a reason is written: a version number, a release
   date or an "all systems operational" strip in a hero; "Step 1 / Step 2 / Step 3" with no content
   behind the numbers; a scroll cue; a decorative status dot with no state; lorem text or a person named
   after a placeholder; a sample paragraph describing what the page will say. These are examples of a
   class, not a catalogue (§7.5): the class is "a surface that says nothing true about this product".
10. **One focal point per screen, and white space that is structure.** The screen has one place the eye is
    meant to land and one primary action (§4); everything else is arranged to support it. Space between
    groups is how grouping is shown (§1.5); it is not what is left over after the content is placed, and
    it is not filled because it looks empty. A screen with three focal points has none.
