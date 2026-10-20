# lifecycle-email-program-design-pitfalls §4 — The pre-launch read and the first checks

A flow looks right in the editor and wrong in the inbox more often than anyone expects: a missing name, a link
to a page that was renamed, three messages in an afternoon because two programs collided. The only review that
catches those is reading the sequence the way the recipient will receive it.

## 4.1 The pre-launch read
1. **Send every message of the sequence to a real inbox you control** (the platform's test send, to addresses
   at more than one mailbox provider) and read it as the recipient would, in the order and across the timing
   the flow will actually use. A single message previewed in an editor is not a read of the sequence.
2. **Every merge field has a fallback.** No greeting with a gap where a name should be, no empty product name,
   no "your undefined plan". Test with a contact that lacks each field.
3. **Every link works today**, including the one in the last message, and lands where the message promised. An
   expired offer or a renamed page is the commonest silent defect.
4. **The unsubscribe path is visible** in each message (the platform usually adds it; confirm it in the test
   send), and the preference page, when there is one, sits beside it, not in its place (§3.3).
5. **Subjects differ across the sequence**, and each message has its own job (§2.2).
6. **No message lands in the middle of the night in the recipient's time zone**, and the time zone the platform
   uses is the recipient's, not the sender's. Whether a particular weekday or hour works better is a
   hypothesis for this audience, not a rule (`business/email-campaign-measurement-and-testing-pitfalls`).
7. **Put a test contact through the exits (§1.4).** Move one through the goal after message one, unsubscribe
   one, and let a duplicate entry happen on purpose; confirm the flow stops, suppresses and does not enrol the
   same person twice.
8. **Check the collision (§2.3).** Put the test contact in the other programs that share the audience and see
   what arrives, in what order, in a day.
9. **Read the sender and subject as a stranger would.** The name and address in "From" are one the person
   recognises, consistent for the kind of message, and the subject holds up if it is the only line read.

## 4.2 The first checks after launch
1. **Check early and again later, at intervals the team chooses and writes in the program definition.** Most
   defects (a broken field, a wrong filter, a timing surprise) show in the first days; whether the flow moves
   its goal needs a longer window. The intervals in the sources are conventions, not rules.
2. **Read the audience before the copy.** If the flow's conversion is far below what the same product or shop
   gets organically from comparable visitors, the first suspects are the trigger, the filter, a missing
   never-send rule or the wrong opt-in source, not the wording. Fix those first; copy comes second.
3. **A good-looking number against the organic rate is a statement about the audience.** The people the flow
   selects may already have been likely to act. The honest baseline is a held-out group of eligible people who
   are not mailed (`business/email-campaign-measurement-and-testing-pitfalls`), not last month's figure.
4. **Read the cost side with the goal** (§1.2): unsubscribes and complaints of the program, from the same
   source and window.
5. **Record what you saw and what you changed**, so the next person tuning the flow does not repeat it or
   undo it.
