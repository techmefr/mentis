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
   Fix: a picture or a link to the screen with each batch, or a staging site the linguist can open.
2. **Add a note to every ambiguous string**: who speaks, to whom, what a variable stands for, whether the string is
   a button, a title or a sentence. The note belongs with the string in the file, not in an email.
3. **Give length limits where the interface has them**, in characters or in pixels, and tell the linguist what
   happens on overflow. Symptom: a button label that breaks the layout in German, and no one knew it was limited.
4. **Pass whole messages, not sentence fragments.** A sentence assembled from pieces cannot be translated well;
   that is a source fix (`skills/i18n-message-format-pitfalls`), not a translation fix.
5. **Explain plurals, gender and variables in the note**, not through guesses at what a placeholder holds.

## 1.3 The job
1. **Freeze the source before sending, and say so.** Symptom: the vendor translates version one and version three
   arrives while the job is open. Fix: a freeze date, a named person who may change the source, and a rule for
   late edits (§3.4).
2. **Use a format the tools handle without damage.** Send the exported catalogue or the agreed exchange format,
   not copied text from a design file. Check that placeholders and tags survive a round trip on a small sample
   before the full job.
3. **State the deadline for first delivery and for review, and who reviews.** A review window nobody planned is
   spent on the launch date.
4. **Confirm availability for the next round.** Own guidance: ask who will translate the update, so the same
   person or team keeps the terms. Never discover on update day that the linguist left.
5. **Agree who owns the work and the memory.** Whether the translation memory and glossary belong to you, and
   whether you can take them to another vendor, is a contract point; settle it before the first job. Not legal
   advice.
