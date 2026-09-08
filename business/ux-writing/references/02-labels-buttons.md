# § 2 — Labels and buttons: describe the outcome

> Section 2 of `business/ux-writing`. Read it when a diff adds or changes a button, a link, a field
> label, a menu entry or a confirmation dialog.

1. **A button says what it does**, not where it goes. "Save changes" beats "OK"; "Delete account" beats
   "Confirm". The user who reads only the button — which is most of them — should still be right about
   what happens. It is also the label a screen reader announces on its own, out of the surrounding
   sentence, and the label a voice-control user has to speak, so a button whose meaning depends on the
   text above it is unusable in both.
2. **Confirmation dialogs state the consequence and its reversibility.** "Are you sure?" carries no
   information. "Delete 12 invoices? This can't be undone." lets someone decide. The count is doing
   work: it is the one part a reader can check against what they meant to select, and it is how a
   mis-selection gets caught before the irreversible step rather than after.
3. **The dangerous option is never the default**, and it isn't the one styled to be clicked. A reader
   confirming out of habit lands on the default, which is why the default has to be the survivable
   option (`business/interface-design` §4.8).
4. **Match the words to the destination**: a link labelled "Settings" leading to a page titled
   "Preferences" makes the user wonder whether they arrived. The doubt is not idle — the usual next move
   is to go back and look for the right link, and on a slow connection that is the same page loaded
   three times.
5. **A field label is not a hint, and a hint is not a label.** The label says what the field is; the
   hint says what an acceptable value looks like. Collapsing them into placeholder text loses the label
   the moment the reader types, so anyone interrupted mid-form is left with filled fields and no names
   for them — and assistive technology may never announce it at all (`skills/accessibility`).
6. **Say what a field is for when the name is not enough**, and say it before the field rather than
   after. A rule discovered only on rejection is a rule the reader had to fail to learn (§1.6), and a
   requirement placed after the input is read after the attempt.
7. **Label by what the reader knows, not by what the column is called.** A field named after a database
   column or an internal code asks the reader to learn our schema; where the internal term genuinely is
   the product's term, it belongs in the domain vocabulary and gets used consistently in both
   (`skills/domain-modeling` §1, §5.1 here).
8. **Two controls on one screen never share a label.** "Edit" appearing on every row of a table is
   twelve identical entries in a list of controls, distinguishable only by position — so a keyboard or
   screen-reader user cannot tell which row they are about to change. The fix is a label that names the
   thing, whether visibly or as the control's accessible name.
9. **Never write a label the interface then contradicts.** A button that says "Save" and shows a
   confirmation dialog, or "Download" that opens a preview, teaches the reader to distrust every label
   on the screen — and that distrust is what makes them slow on the screens where the labels are honest.
10. **Say nothing you cannot commit to.** "Instant", "secure", "free", a deadline or a price in
    interface text is a claim the product now owes, and interface text is where such a claim gets made
    accidentally because it reads as encouragement. Anything of that shape goes to whoever owns the
    commitment, not into a diff (`business/product-marketing`).
11. **A label has to survive being longer.** A word that fits in the source language is often half
    again as long once translated, and a button whose text is truncated or wrapped mid-word is a button
    whose outcome is no longer stated. Writing the short form is not the same as designing for the long
    one (`vue-nuxt-vuetify-conventions` §6).
12. **The label is the same word as the action's name everywhere else** — in the menu, in the
    confirmation, in the success message and in the email that follows. A flow that renames its own
    action between steps reads as three different operations, and the reader hesitates at the step where
    the word changed (§4.2).
