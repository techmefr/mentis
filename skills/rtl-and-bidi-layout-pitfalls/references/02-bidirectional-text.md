# rtl-and-bidi-layout-pitfalls §2 — Bidirectional text in messages

A message that holds a value of the other direction, a Latin brand name in an Arabic sentence or a number in a
Hebrew one, is displayed by an algorithm that reorders runs of text. The facts below come from the bidirectional
section of the Unicode MessageFormat 2 specification, restated in our own words and used as facts only; that
specification is a standard under Unicode's terms and none of its text is reproduced.

## 2.1 Spillover and isolation
1. **A formatted message can mix directions, and the display algorithm can then misplace neighbouring text.**
   The specification calls the result unexpected or undesirable spillover effects; the glossary entry it links to
   for the term was not read.
2. **Isolate each affected formatted value.** The specification says that applying bidirectional isolation to each
   affected formatted value helps avoid the spillover.
3. **The message and each value both need a direction.** Isolation works only when the formatter knows the
   direction of the whole message and of each placeholder. When output is a list of parts and not a string, the
   direction of each formatted placeholder has to be available to whoever assembles the parts.
4. **The default strategy of the specification, for output as one string, wraps values in isolate control
   characters.** It chooses between a left-to-right isolate, a right-to-left isolate and a first-strong isolate
   from the value's direction, each closed by the pop isolate character. A left-to-right value in a left-to-right
   message is left alone unless the value's direction option asks for isolation. Version-bound: the
   specification text at commit e1126e0.
5. **Direction comes from metadata, not from the characters.** The specification says it should not be
   determined by inspecting the characters of the formatted string; a formatter may carry it with the value, or
   derive it from the locale.
6. **A formatter may already put marks inside a value.** The specification's example is an Arabic-locale
   currency amount, where the library inserts invisible marks around the sign and the symbol so that they sit
   next to the number. Own guidance: do not trim, normalise or re-join formatted values in application code, and
   do not build the sentence by concatenation (`vue-nuxt-vuetify-conventions` §6, point 8), because either step
   removes what the formatter added.
7. **Whether a given library does any of this is a question to test.** The specification describes what a
   conforming formatter should do; no library was read for this block. Own guidance: render one sentence per
   message that holds a name, a number and a price in text of the other direction and look at where the
   punctuation lands.

## 2.2 Testing before translations exist
1. **A pseudo locale can emulate right-to-left text.** Lingui's pseudo-locale configuration (version 6.9.1,
   version-bound) has a boolean option, off by default, that emulates right-to-left languages by inserting
   Unicode right-to-left override marks into the messages of the pseudo locale.
2. **Pair it with a real right-to-left locale.** Own guidance: the option acts on the strings; the page
   direction and the layout come from the settings of §1.1, so the pseudo locale shows overflow and untranslated
   strings early and does not replace a check with Arabic or Hebrew content before release.
