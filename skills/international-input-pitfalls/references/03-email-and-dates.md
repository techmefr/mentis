# international-input-pitfalls §3 — Email addresses and dates

Both fields have a strict-looking format and a lenient reality. An email address can be long and unusual, and a
date is written in the order and in the form of whatever the person is copying from.

## 3.1 Email addresses
1. **Say why you ask.** People are more at ease when they know the use, and people with several addresses can
   choose which one to give. A field inside a sign-in box does not need the explanation (GOV.UK email addresses
   pattern).
2. **The field takes up to 254 characters.** The page names that as the longest an email address can be and cites
   an RFC erratum for it, which was not read here.
3. **Help the person get it right, and do not police it.** Check the format, allow paste, show the address back
   so it can be confirmed and changed, and warn on a likely typo of a popular provider while letting the user
   continue, because the address may be genuine. Own guidance: a typo warning is a message, never a validation error.
4. **Make the field wide enough to read its content.** A rule of thumb from the page is at least 30 characters
   visible at once, refined with your own user data.
5. **Declare it.** `type="email"`, `spellcheck="false"` and `autocomplete="email"` (`accessibility` §4.6 and
   §4.7; the phone keyboard side is in `webperf`).
6. **Asking twice is a choice that needs evidence.** The page says to ask the user to repeat the address only
   when research shows it helps.
7. **A confirmation loop is disruptive.** Use one only where email is essential to the service, for example for
   a password reset, to check that the person can read the mailbox they gave.
8. **The format message says what a good value looks like.** The page's wording names the expected shape with an
   example address on a reserved example domain; use the same kind of domain in your own examples.

## 3.2 Dates
1. **Choose the control from the kind of date.** The page separates memorable dates such as a birth date, dates
   copied from a document or card, approximate dates, relative dates, and a pick from a given set.
2. **A memorable date is asked in separate day, month and year inputs inside a fieldset with a legend** that
   carries the question (GOV.UK date input page). Accept month names in full or abbreviated form, and never move
   the focus automatically between the inputs: it is confusing and clashes with normal keyboard control. For a
   birth date, the autocomplete values are `bday-day`, `bday-month` and `bday-year`.
3. **A date copied from a document follows that document.** Make the fields match the order and format of the
   original, so the date can be copied across accurately.
4. **Allow an approximate date where people may not know the exact one.** The page's example is a month and a
   year for "the date you lost your passport".
5. **A relative date is chosen or typed as a relation.** Accept "tomorrow" or "1 day before" for reminders, and
   show the weekday when the weekday matters.
6. **A calendar control has three conditions of use.** Use it only when the person picks a date in the near
   future or recent past, needs the weekday or the week of the month, or needs to see dates in relation to each
   other. It is never the only way in: the date can also be typed into a text input, and the control must not
   depend on JavaScript alone.
7. **An example date shows the order.** Use a day of 13 or more and a month of 9 or less, such as "27 3 2007":
   the day cannot be taken for a month, and the month shows that a leading zero is not needed. The example
   is in day, month, year order, which is the order of the page; the principle is carried: an example whose day
   cannot be read as a month. Own guidance: the order of the inputs and of the example comes from the locale of
   the page, as in `vue-nuxt-vuetify-conventions` §6.
8. **An example inside a hint must be valid for the question.** The date input page asks that an example date in
   hint text is a valid answer to the question being asked.
