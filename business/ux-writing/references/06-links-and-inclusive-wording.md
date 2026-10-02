# § 6 - Links, instructions, plain language and inclusive wording

> Section 6 of `business/ux-writing`. Read it when a diff adds a link, writes an instruction that points at
> something on the screen ("click the green button"), or sets the register and vocabulary of text a wide
> audience reads. The facts here are cited from the accessibility and internationalisation standards;
> where a figure or a list would be needed, the point says to read it at the source.

## Links

1. **A link says where it goes.** Its purpose can be worked out from the link text together with its
   surrounding sentence or list item at minimum (the link-purpose-in-context criterion, WCAG 2.2 SC
   2.4.4, level A) and, where the layout allows, from the link text alone (SC 2.4.9, level AAA). "Click
   here", "read more", "learn more", "more", "link" fail the second and rely entirely on the first.
   Why it matters beyond the standard: screen readers and voice-control tools list a page's links out of
   context, and a list of eight "Read more" entries is eight identical choices.
2. **Test by listing.** Extract the page's links and read the list alone, as a person using a links list
   would. Every entry should still say what it opens. A mechanical pass catches the worst: search the
   source for link text that is only a stock phrase, and group links by text.
3. **Same text, same destination; different destination, different text.** Two links with the same visible
   text that go to different places force a guess, and the same destination under two different texts
   suggests two things. Group the rendered links by text and compare their targets; a mismatch is a
   finding. Components with the same function are identified the same way everywhere (SC 3.2.4,
   level AA). When the visible text is repeated by design (a "Delete" per row), make the accessible
   name distinct and keep the visible words inside it, so voice control that speaks the visible label
   still works (SC 2.5.3, Label in Name).
4. **Say what the link does when it is not a navigation.** A link that opens a new window or tab, downloads
   a file, starts a call or an email, or leaves the site says so in its text or in an adjacent label. For a
   file, the type is part of the name; the size helps the person on a metered connection.
5. **The link text matches the destination's own title** (see `02-labels-buttons.md` point 4). A link
   named "Pricing" that leads to a page titled "Plans" starts a moment of doubt that a matching heading
   avoids (SC 2.4.6, Headings and Labels).
6. **A link is a link, a button is a button.** Something that goes to an address is a link and carries a
   real address; something that acts on the current page is a button. Wording follows: a link names a
   place, a button names an action (`02-labels-buttons.md` point 1).

## Instructions that point at the screen

7. **Never rely on sensory characteristics alone.** "Click the green button", "use the menu on the right",
   "press the round icon", "when you hear the beep" assume the person sees colour, position, shape or
   hears sound (SC 1.3.3, level A). Name the control by its label: "Select Save changes". Position and
   colour may be added as a second cue, never the only one. The same instruction also fails when the
   layout changes on a narrow screen and "right" is now "below".
8. **Instructions survive translation and reflow.** "See the table above" breaks when the table moves.
   Link to it, or name it.
9. **Say the key, not the glyph.** "Press Enter" rather than a symbol that a keyboard layout or a
   translation will change; and give the platform's own name for a modifier key where the product runs on
   more than one platform.

## Plain language

10. **Write for the reader who is not on the team.** Short sentences, one idea each, familiar words, the
    verb in the active form, the actor named. Where the text needs more than lower-secondary reading
    ability, the standard asks for a supplement or a simpler version (SC 3.1.5, level AAA); treat it as the
    goal for any text that is not specialist by nature.
11. **Define on first use.** Expand an abbreviation the first time it appears and keep a glossary link for
    the unusual words and idioms (SC 3.1.4 and SC 3.1.3, level AAA). An internal term used with the public
    is the commonest violation (`05-mechanics.md` point 1).
12. **Do not score readability with a formula you were handed.** Readability formulas are calibrated for one
    language and break on others; applying an English formula to French or German produces a number with
    no meaning. Test with a person from the audience, or read it aloud, and use a language-specific
    method only where one exists for that language.
13. **Idioms and metaphors travel badly.** "Hit the ground running", "ballpark", "low-hanging fruit" mean
    nothing translated and little to many native readers. Say the thing.
14. **Never say "just", "simply" or "easy".** They tell the reader that failing is their fault. Give the
    steps and let the reader decide how hard they were.

## Inclusive wording

15. **Do not assume ability.** "See", "look at", "walk through", "stand-alone" are fine in their ordinary
    sense; "as you can see", "obviously" and "even a beginner can" assume what they claim. Prefer verbs
    that fit any way of using the product ("find", "select", "go to").
16. **Do not assume a person.** No default gender for "the user", "he" or "guys" for a mixed group; use
    "they", the role, or the plural. Do not ask for a title, a gender or a marital status unless the
    process needs it (`business/data-protection` principles apply to the question itself).
17. **Replace terms that carry a harm they do not need.** Master and slave, whitelist and blacklist,
    sanity check, dummy value, grandfathered, and similar metaphors have common neutral replacements
    (primary and replica, allowlist and blocklist, confidence check, placeholder value, legacy).
    **Do not carry a list in your head or in this block.** Such lists change; read the organisation's
    style guide or a maintained public inclusive-language guideline at the time of writing, and follow
    it. Where code identifiers are public API, renaming is a migration (`skills/deprecation-migration`),
    not a wording edit.
18. **Describe people the way they describe themselves.** Person-first and identity-first phrasing are
    both in use and communities differ; follow the people concerned or the guideline the organisation has
    adopted. Describe a condition only when it is relevant.
19. **No violence, no shock, no stereotype as a figure of speech.** "Kill the process" is a command name
    and stays in a command reference; "kill it with fire" in a user-facing message does not.

## Images, symbols and culture

20. **A picture or symbol with a local meaning needs a locale decision.** Hand gestures, body language,
    animals, colours, holidays, mailbox and money icons, a checkmark that means "wrong" in some
    conventions: pick images with no strong local meaning, or serve a variant per locale (`skills/seo` for
    the URL side, the i18n conventions of the stack for the content side).
21. **A flag is a country, not a language.** A language picker is labelled with each language's own name in
    its own language. One language is spoken in many countries and many countries use several languages.
22. **Text in an image is a translation and an accessibility problem.** Avoid images of text except where
    the wording is the image (a logo) (SC 1.4.5, level AA). A screenshot with a caption that needs
    translating is a re-shoot per locale.
23. **Direction and letters are content.** Icons that point or progress (back, next, a progress bar) must
    mirror in right-to-left locales, and icons that use a letter or a word (a bold "B", a "?") belong to
    one alphabet. Check them as part of a locale pass, not at launch.
