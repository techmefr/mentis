# localisation-vendor-process-pitfalls §1 — Brief and kit

> Part 1 of `business/localisation-vendor-process-pitfalls`. Read it before a job is sent.

A translator works on fragments. What they cannot see, they guess, and the guess is shipped.

## 1.1 The brief
1. **Name the audience and the market, not only the language.** Symptom: Spanish delivered once for every Spanish
   speaker, then the customer in one country finds it odd. Check: does the brief say country, register (formal or
   informal address) and reader (a clinician, a teenager, a buyer)? Fix: one line each, per market.
2. **State the tone and give a style reference.** A short note on voice and two examples of approved text in that
   language do more than "friendly yet professional".
3. **Say what the text is for and where it appears.** A button, a legal notice, a push notification and a
   marketing email want different treatment. Fix: a purpose per file or per group of strings.
4. **Define scope and what is not translated.** Product names, code, placeholders and brand terms are listed up
   front (§2.1). Symptom: a variable name translated and the page broken.

## 1.2 Context for each string
1. **Attach screenshots or a preview.** Symptom: "Order" translated as the verb on a page where it is a noun.
   Fix: a picture or a link to the screen with each batch, or a staging site the linguist can open. Mozilla's
   localization guide says the same for a screen that cannot be tested yet: put links to screenshots or design
   specifications in the string's note, and remove them once the screen is live.
2. **Add a note to every ambiguous string**: who speaks, to whom, what a variable stands for, whether the string is
   a button, a title or a sentence. The note belongs with the string in the file, not in an email. Mozilla's
   guide lists when a note is due: part of the string must stay untranslated, a variable appears (say what it holds
   at run time), the English is ambiguous (bookmark as noun or verb), the string is read aloud by a screen reader,
   or an adjective appears without its noun, since most languages inflect it for number and gender. Its reason:
   linguists often see one string at a time with no code beside it.
3. **Give length limits where the interface has them**, in characters or in pixels, and tell the linguist what
   happens on overflow. Symptom: a button label that breaks the layout in German, and no one knew it was limited.
   Mozilla's guide asks designers to leave room for the translation to be at least 30 percent longer than the
   English and shows a single English term turning into a very long German compound; it advises against forcing
   word breaks in CSS to cope.
4. **Pass whole messages, not sentence fragments.** A sentence assembled from pieces cannot be translated well;
   that is a source fix (`skills/i18n-message-format-pitfalls`), not a translation fix. Mozilla's guide gives
   the reason: three English sentences sharing an opening clause are three different sentence types in Scottish
   Gaelic, so a shared fragment presumes an English grammar; it also says to leave a placeholder so the
   linguist can reorder words, and not to reuse one string for a menu item and a screen title because the
   same word may be a noun in one place and a verb in the other.
5. **Explain plurals, gender and variables in the note**, not through guesses at what a placeholder holds.

## 1.3 The job
1. **Freeze the source before sending, and say so.** Symptom: the vendor translates version one and version three
   arrives while the job is open. Fix: a freeze date, a named person who may change the source, and a rule for
   late edits (§3.4). Mozilla's guide adds a related rule: do not send temporary strings for translation, because
   linguists then translate text that is going to change; keep them out of the localised files until final.
2. **Use a format the tools handle without damage** (the OASIS XLIFF 2.1 standard and the translation tools'
   own import formats are the usual exchange routes; the format is the parties' choice). Send the exported catalogue or the agreed exchange format,
   not copied text from a design file. Check that placeholders and tags survive a round trip on a small sample
   before the full job.
3. **State the deadline for first delivery and for review, and who reviews.** A review window nobody planned is
   spent on the launch date.
4. **Confirm availability for the next round.** Own guidance: ask who will translate the update, so the same
   person or team keeps the terms. Never discover on update day that the linguist left.
5. **Agree who owns the work and the memory.** Whether the translation memory and glossary belong to you, and
   whether you can take them to another vendor, is a contract point; settle it before the first job. Not legal
   advice.
