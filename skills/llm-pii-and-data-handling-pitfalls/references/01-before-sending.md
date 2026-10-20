# llm-pii-and-data-handling-pitfalls §1 — Before sending

Source: documentation of the anonymise and deanonymise input and output scanners of llm-guard (MIT), read 2026-10-20. Points marked "own guidance" are not from a source. Not legal advice.

## 1.1 Send less
1. **Start from the task, not from the record** (own guidance). Symptom: a whole customer row, ticket thread or
   document goes in to answer one question. Check: for each field in the prompt, name the part of the answer that
   needs it. Fix: select fields, truncate threads, and pass an internal id where the model only needs identity
   continuity.
2. **Tool results are prompts too** (own guidance). A tool that returns a full profile puts it in the context.
   Fix: shape the tool's output to what the model may see, rather than trusting the model to ignore the rest.
3. **Decide the class of each field once** (own guidance): never sent, sent as placeholder, sent as is. Keep the
   table next to the prompt code so a reviewer can compare it with what is sent.

## 1.2 Placeholders and the round trip
1. **The source's pattern is a vault.** Detected values are swapped for numbered placeholders before the call, the
   originals sit in a vault, and a second step on the model output puts the originals back where a placeholder
   appears. The first scanner can also substitute plausible fake values and take lists of names to allow or to
   always hide.
2. **The vault is itself sensitive data** (own guidance). Symptom: a long-lived shared vault holding every
   customer's originals. Fix: scope it to one request or session, never log it, delete it with the session.
3. **The round trip breaks when the model rewrites the placeholder** (own guidance). Symptom: "[REDACTED_PERSON_1]"
   becomes "Person 1" or a possessive and is not restored, or is restored in the wrong spot after a
   summary. Check: run real prompts through the round trip and diff. Fix: instruct the model to copy
   placeholders verbatim, and treat an unrestored placeholder as a visible failure, not as acceptable text.
4. **Fake substitutes can collide with real people** (own guidance). A generated name may match a real one. Prefer
   neutral placeholders when the output is shown to humans.
5. **Placeholders keep structure but remove meaning.** If the task depends on the value (a date range, a city),
   redaction changes the answer; transform the value instead (offset, generalise) and say so.

## 1.3 What a detector misses
1. **Detection is statistical.** The source builds on a named-entity recogniser plus patterns for formats such
   as card numbers, emails, addresses of the network, identifiers and bank numbers, and states a threshold
   parameter (re-read the current default before relying on it). Anything outside the trained entities or
   patterns passes through. Record the entity list as the list of what you claim to cover.
2. **Language matters.** The source says entity detection is English-specific, with a separate recogniser for
   Chinese. A French or German prompt can pass with names and addresses intact. Check: run a labelled sample in
   each language you serve and count misses.
3. **Context identifiers are missed by design** (own guidance): a rare job title plus an employer, a unique
   incident description, a free-text complaint. These identify without matching any pattern. Fix: minimise first
   (§1.1); do not lean on detection for them.
4. **Obfuscated forms** (spelled-out digits, spaced characters, "john dot doe at") partly pass. The source does
   list some bracketed email forms; test your own variants.
5. **Latency is a cost of the control** (own guidance). The source publishes timings measured on its own
   hardware; measure on yours before putting a detector in a synchronous path.

## 1.4 Checks
1. The field table (never, placeholder, as is) matches the prompt code in review.
2. A labelled sample per served language reports detector misses, and the misses are written down.
3. The round trip is tested on summaries, lists and possessives, and an unrestored placeholder fails the request.
4. The vault is scoped to a request or session and absent from logs.
