# international-input-pitfalls §2 — Addresses

An address form is three possible designs, a lookup, several inputs or a textarea, and each one fails a
different group of people. The GOV.UK addresses pattern is written around one country; what follows keeps its
reasoning and drops its national rules.

## 2.1 Lookup
1. **A lookup covers the countries its data covers.** The page says lookups generally work for the UK only. When
   both domestic and foreign addresses are expected, let the user either search or type the address by hand.
2. **Always provide the manual way out.** Say which addresses the lookup supports, and give a manual option for
   people with foreign addresses and for addresses that are missing or badly listed in the lookup.
3. **Accept postcodes however they are typed.** Take upper and lower case, no spaces, extra spaces at the start,
   in the middle or at the end, and punctuation such as hyphens, brackets, dashes and full stops, and ignore the
   unwanted characters instead of rejecting the value. The page says this is easier for users than a message
   claiming the postcode is invalid.
4. **A postcode that is not real gets its own message.** The page shows a distinct error for it. Own guidance:
   apply the format tolerance of the previous point first, so that this error is about the value and never about
   its punctuation.

## 2.2 Several inputs
1. **Use several inputs for the manual path only when both conditions hold.** You know which countries the
   addresses come from, and you can find one format that fits all of them, which the page calls hard once you
   leave one country.
2. **Know what you buy and what you pay.** Several inputs let you extract and validate each part, give help per
   input and let browser autofill work. The cost is that one format rarely fits every address, people do not
   always use the inputs as intended, and an address cannot be pasted in one go.
3. **Make an input mandatory only when the information is really needed, and size it to its content.** A postcode
   input is shorter than a street input. Provide enough inputs for long addresses, for example for a company name
   or a flat number.
4. **The administrative-region input is optional, and removable.** In the page's version the county input is
   optional and is removed when users and the service will not need it; the reason it gives is a rule of one
   country's postal operator, which is not carried. Own guidance: decide per country whether the input exists.
5. **Declare each input.** Each input carries the autocomplete value for its own purpose, chosen from the list the
   page links to in the WCAG 2.2 text (`accessibility` §4.6 gives the reason).

## 2.3 Textarea
1. **A textarea is the manual path for any format.** The page recommends it for foreign addresses and for people
   who cannot find their address in the lookup, because the user types the address as it is written and can paste
   it.
2. **Do not use it when you need the parts.** If the service has to separate the street or the postcode, a single
   textarea cannot give them back accurately, and it is also a poor fit when you must format the address for
   printing.
3. **Declare it.** `autocomplete="street-address"` on the textarea.
4. **Errors say what is wrong.** The page asks for a specific message for each specific error, including its own
   message for a postcode that is not real; error association is in `accessibility` §4.2.
