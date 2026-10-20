# outbound-sales-and-crm-hygiene-pitfalls §3 — Sequence state and replies

A sequence is a loop that sends until something stops it. What stops it must be a record every channel reads, not
a habit of the person who happened to see the reply.

## 3.1 One shared state per person
1. **Keep one record of who replied, who opted out and who is paused**, readable by every tool that sends.
   Symptom: a prospect who answered on a social network receives email three the next morning. Check: send a
   test contact through every channel, reply on one, confirm the others stop. Fix: connect the tools to one
   state (the CRM or a table keyed on the person), checked before each touch.
2. **A reply on any channel stops all channels** until a person decides otherwise, including an auto-reply:
   pause, do not continue blindly.
3. **Key the person on several identifiers** (email, profile address, phone), so the same person is one entry
   across channels.

## 3.2 Classifying a reply
1. **Classify every reply**: interested, question, objection, not now, referral, wrong person, auto-reply,
   opt-out, bounce. Unclassified replies are the ones that get ignored.
2. **Mechanical actions can be automatic**: pause on an auto-reply, suppress on an opt-out, remove on a bounce, set
   a reminder on "not now". Everything that answers a human is drafted for a person to send.
3. **Answer an objection once, briefly, and make declining easy.** A second push on a no is how a prospect becomes
   a complaint.

## 3.3 Before a sequence goes live
1. **Read the whole sequence as the recipient**, in order, with real dates. Symptom: a follow-up that assumes a
   reply that never came, or repeats the first message.
2. **Each follow-up adds something**: a new angle, a fact, a question. "Checking in" adds nothing.
3. **Personalisation must connect to the reason for writing.** Test: remove the personalised line; if the
   message still reads the same, the line was decoration.
4. **State the stop rule in the plan**: when the sequence ends, what is logged, and that the last message is the
   last message.
5. **Do not run the sequence from the shared company domain** without checking with whoever owns mail
   reputation; hand over to `business/email-deliverability-and-sender-requirements-pitfalls`.
