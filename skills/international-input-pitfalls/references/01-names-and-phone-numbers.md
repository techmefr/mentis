# international-input-pitfalls §1 — Names and phone numbers

A name and a phone number look like the simplest fields in a form, and they are where a check written for one
country refuses the most people. The GOV.UK pages put the cause plainly: the field was shaped for the common
case, and the exceptions were never asked about.

## 1.1 Names
1. **Ask for a name only when the service needs it.** The GOV.UK names pattern opens with that condition. Own
   guidance: a field the service never reads is a refusal waiting for someone with an unusual name.
2. **Decide between one field and several on purpose.** Not every name splits into first and last, and every
   extra name field is one more place where a real name does not fit or is entered in the wrong box. A single
   field takes the widest range of names but cannot reliably give back the parts. Own guidance: if nothing in the
   service reads a part of the name, use one field.
3. **Label by what the field holds.** One field is labelled with the full name. For several fields the page uses
   first name and last name, and, for users from outside the country the service was written for, given names
   and family name (the page states this for the UK; the principle is carried, no country list). Say whether the
   common name or the name as written on an official document is wanted.
4. **Size fields from real data and accept every character.** Use population data or the names of existing
   users to choose the length, and accept digits and symbols.
5. **Declare the field to the platform, and turn spellchecking off.** `autocomplete="name"` for one field,
   `given-name` and `family-name` for two, with the reason in `accessibility` §4.6; `spellcheck="false"` so a
   browser does not underline a correct name. The page ties the autocomplete values to WCAG 2.2 success
   criterion 1.3.5, which was not read here.
6. **A middle name is optional and unmarked.** Ask only if the service needs it, label it with the plain words
   for middle names, and leave the word "(optional)" out of the label: people who have a middle name fill it in
   and the others skip it.
7. **Do not ask for a title, and never offer it as a select.** It is extra work, it asks the person to reveal
   their gender or marital status, and the range of titles cannot be predicted. If one is unavoidable, use an
   optional text input, and use people's names correctly in what you send back.
8. **Let users change their name.** If the service stores personal details, name changes belong in the profile:
   people change names for many reasons, and a hard process distresses them and may make them leave.

## 1.2 Phone numbers
1. **Ask for a number only when needed, and give another way to be reached.** Not everyone has or can use a
   phone (GOV.UK phone numbers pattern).
2. **Accept the formats people use.** Allow extra spaces, hyphens, dashes and brackets, and country and area
   codes.
3. **Validate with a library built for the job.** The page names Google's libphonenumber library as validating
   numbers from most countries, so that the user can be told about a real error. Own guidance: a hand-written
   expression for the digits is the same national assumption as in the previous point, written in one line.
4. **Say which kind of number is needed.** Put it in the label or hint: a local one, an international one or a
   mobile one.
5. **Do not mask the input or show a placeholder answer, and do not reformat what was typed.** Masking makes it
   harder to type a number the way the person knows it and to compare it with the source they are copying from.
   The GOV.UK Notify team saw people confused by a returned version of their number, for example with a country
   code added.
6. **Declare the field.** `autocomplete="tel"` (`accessibility` §4.6).
7. **A `tel:` link is not free.** It styles the number as a link, which misleads on devices that cannot call;
   some mobile browsers already detect numbers; and unless the user has set a default app, some browsers and
   operating systems start a setup process when the link is followed. If you need the link, make sure it does not
   look like one on devices that cannot call.
8. **Example numbers come from ranges reserved for fiction.** The page shows the idea with one country's
   regulator list; no range is carried here, because a range is valid only in its country. Own guidance: look the
   range up for each country you show, and never use a real subscriber's number.
9. **Extensions and short codes are an open question.** The page itself says it needs more research on
   international numbers, extensions and SMS short codes, so a project that needs them decides and records the
   decision rather than citing a pattern.
