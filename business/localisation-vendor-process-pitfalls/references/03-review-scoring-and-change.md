# localisation-vendor-process-pitfalls §3 — Review, scoring and change

> Part 3 of `business/localisation-vendor-process-pitfalls`. Read it when a result comes back or the source moves.

## 3.1 Who reviews
1. **Use a second linguist, native in the market, who did not translate it.** A review by the translator is a
   second read of the same blind spots; a review by an internal speaker with no training is often taste.
2. **Give the reviewer the brief, the glossary and the context** that the translator had. Symptom: a reviewer
   "fixes" what was right under the brief, and the vendor learns nothing.
3. **Separate review in context from review of the file.** Strings read in a spreadsheet pass checks that fail on
   screen: overflow, wrong gender around a variable, a button with no verb. Fix: a pass in the staging build, with
   the real interface.
4. **Check functional breakage separately.** Placeholders, tags, number and date formats, links and the order of
   variables: mechanical checks catch these before a person reads for meaning (`skills/i18n-catalog-workflow-pitfalls`).

## 3.2 Score on errors, not on feeling
1. **Agree the error categories and their weights with the vendor before the first job.** Typical headings are
   accuracy (meaning lost, added or wrong), fluency, terminology, style, locale conventions and omission. The MQM
   typology lists seven top-level categories: terminology, accuracy, linguistic conventions, style, locale conventions,
   audience appropriateness, and design and markup, with omission and mistranslation as subtypes of accuracy; it is
   a catalogue from which a project selects the types and depth it needs, and weights are optional, for example a
   higher weight on accuracy for legal text (MQM Council pages). Take the list and weights from the version you both
   adopt and re-read it then; this block names no threshold.
2. **Count errors by category and severity**, with a segment reference and a correction each. MQM names four severity
   levels (neutral, minor, major, critical), judges severity by the impact if the error were found after publication, and
   lets a single critical error fail a text whatever the score; three or two levels are also used. Symptom: "the
   quality is not good enough" and no way to fix it. Fix: a list the vendor can apply and argue with.
3. **Define the pass mark in advance and per content type.** A legal notice and a social post do not tolerate the
   same things; MQM likewise has each project set its own threshold, expressed as acceptable penalty points per a
   reference word count, and notes that different content types may need different ones. The score is normalised by the
   source word count of the evaluated sample, so say how many words were sampled. A threshold chosen after seeing the result is a verdict, not a test.
4. **Sample on purpose.** Draw segments across content types, lengths and files, including the hard ones. Say how
   many and how chosen. Symptom: a pass score from the first fifty short strings. Check: does the sample include
   the long, the ambiguous and the legally sensitive ones?
5. **Calibrate reviewers.** Two reviewers score the same sample and compare; a large gap means the categories are
   read differently. The MQM pages use the word calibration for something else, rescaling the raw score so the pass band is
   readable, and note that calibrated scores may not compare across organisations; this point stays own guidance: do this once at the start of an engagement and again when the reviewer changes.
6. **Do not score a style preference as an error.** Record preferences as a style note for next time and keep the
   score for departures from the brief, the glossary and the language itself. MQM has a neutral severity that flags a
   preference or a point to review without adding any penalty, which is the place for it.

## 3.3 Close the loop
1. **Return findings with category, correction and reason**, and let the vendor answer. A disputed item is
   decided by the content owner against the brief, not by volume.
2. **Update the glossary and the memory from the review**, then tell the linguists. The feedback that stays in a
   mail changes nothing.
3. **Track the score over time per vendor and per language.** One bad batch is information about a batch; a
   trend is information about the vendor, and feeds `business/vendor-management`.
4. **Keep praise and fixes in the same note.** Linguists who only hear about errors stop asking questions.

## 3.4 When the source changes
1. **Treat a late change as a new job.** Symptom: a sentence changed in the source after the freeze and a
   vendor's version describes the old one. Fix: send the diff, list the strings affected and re-check the ones
   that sit next to them, since context shifts.
2. **Send only the changes, with their old translations**, so the linguist sees what moved and the memory is
   updated, not rebuilt.
3. **Version the source and the delivery together**, so any shipped string can be traced to a source version.
4. **Plan the release for the slowest language**, or decide in advance to ship with a fallback language for a
   pending one and say so.
5. **A new language is a new project**, not a copy of the last: a market brief, a reviewer, a glossary, a layout
   check (right-to-left and expansion: `skills/rtl-and-bidi-layout-pitfalls`) before the strings are bought.
