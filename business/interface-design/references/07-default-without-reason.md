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
