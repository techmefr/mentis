# international-input-pitfalls §4 — Storing and showing names, phone numbers and addresses

§1 to §3 are about the form. This section is about what happens to the value afterwards: the column that holds it,
the label printed on a parcel, the greeting in an email, the sort in an admin list. A form that accepts a real
name and then stores it in two boxes of the wrong shape has only moved the refusal one step later. Phone facts come
from the libphonenumber FAQ (Apache-2.0); name and address points are own knowledge, marked "re-read before
relying" where a rule varies by country.

## 4.1 Names
1. **Symptom:** an email greets "Dear Smith", an invoice shows the family name first, a one-word name leaves an
   empty last name that a database or a downstream service rejects. **Cause:** the model assumes a given name and
   a family name in that order. **Fix:** store the name as the person gave it in one field, and add the parts only
   for what the service reads, each optional (re-read before relying: order and parts differ by culture).
2. **Keep the display name apart from the legal name.** Printed documents, payment and identity checks need the
   name as on an official document; greetings, avatars and lists need what the person goes by. Two fields with
   two labels, and a rule for which one each output uses.
3. **Do not derive initials, a greeting or a sort key by splitting on a space.** A name can have one word, several
   family-name words or a family name first. Derive a sort key only through a field the person can see and correct,
   or sort by the whole string with the locale's collator (`collation-and-locale-aware-search-pitfalls` §1).
4. **Do not change case, and do not strip what you do not recognise.** Title-casing breaks names with internal
   capitals, particles and apostrophes; "fixing" accents damages the name. Store exactly what was typed after
   Unicode normalisation to one form, and look at a name in more than one script before declaring a check done.
5. **A name may exist in two scripts.** Allow a second field for a transliteration only where a process needs it
   (a ticket, a customs form), and say which of the two each output prints.
6. **Salutation and honorifics are output text, not data about the person.** If a message needs one, use a neutral
   form and the display name; never infer a gender or marital status from a title or a first name.

## 4.2 Phone numbers
1. **Store the number as a string in an international form, plus the extension apart, never as an integer.**
   A leading zero or plus sign is lost in a numeric column. The library's FAQ also warns that a number longer
   than the safe integer range of JavaScript loses its last digits when parsed into a plain number type.
2. **Keep what the user typed too, when you display it back.** The canonical form is for matching and dialling;
   the typed form is what the person recognises (§1.2.5).
3. **Parse with a default region, and ask for the country when the number has no country code.** A national number
   is ambiguous without one; the library's whole parsing model rests on a region plus the number.
4. **"Possible" and "valid" are two different questions, and neither says "reachable".** The FAQ says a valid
   range is one carriers may assign to subscribers, not a proof that a number is assigned or that a dialled number
   connects (extra digits are ignored in some countries, and old numbers keep working during renumbering). The only
   proof of reachability is a verification step, such as a code sent to the number.
5. **Do not reject a number for being from another country than the address.** The FAQ says region-checked
   validation is rarely the right call because many people hold numbers that belong to another country, mobiles
   most of all. Validate against the number's own country.
6. **Format by the number's country, never by the interface language.** The FAQ states that formatting is
   country-specific and language-independent: a French reader sees a US number in the US way. Some countries
   write numbers in native digits; the library parses them but did not format them at the time of the FAQ
   (re-read before relying).
7. **Short and service numbers are a different data set.** The library's main utility says they are out of scope
   and points to a separate class; do not feed an emergency or carrier short code to the same validator.
8. **Metadata ages.** Number ranges and formats change with national plans, so pin the library version in a
   lockfile and update it on a schedule; a "valid" number in your data can become unassigned or reformatted.

## 4.3 Addresses
1. **Symptom:** a customer abroad cannot place an order, a parcel goes to the wrong line, a required "state"
   field holds a placeholder. **Cause:** one national address shape was used as the schema. **Fix:** which parts
   exist, which are required, the order of the lines and the postcode pattern all depend on the country
   (re-read before relying); drive the form and the checks from per-country metadata, as libaddressinput does for
   its fields and validation (its code is Apache-2.0 and its data CC BY 4.0; only the README was read).
2. **Store the lines as entered, plus a country code.** Free lines and a country code survive every shape; split
   fields (street, number, locality, region, postcode) are a projection of them that a lookup or a person confirms.
3. **Keep the address in the writing the carrier reads.** An address in local script printed on a label is often
   right where a transliteration is not; keep the local form and add a Latin form only where a process asks.
4. **Format on output with the destination country's order, not the sender's.** A label, an invoice and a
   shipping API each need the order of the destination; do not rebuild the order by joining fields with commas.
5. **A postcode is a string.** A leading zero, a space, letters or a hyphen are all valid in some country; never
   cast it, and never validate it with a pattern from another country (the tolerance rules are in §2.1).
6. **Tax, shipping and fraud logic must read the country code, not parse the lines.** Parsing a free-text address to
   decide the country is the national assumption again; the code you stored is the input.
7. **Validation by a service is advice, not a gate.** An address service may not know a new building, a rural
   route or a recent change; let the person confirm what they typed over what the service suggests (§2.1.2).
