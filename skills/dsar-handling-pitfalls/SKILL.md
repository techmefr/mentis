---
name: dsar-handling-pitfalls
description: "Use when a data-subject request (access, erasure, correction, portability, objection) is received, built into a product or support process, or audited: the request as a case with a received date and a computed due date, the extension and refusal notices, intake from every channel, the manifest of systems searched, secure delivery of the package, and what stays a question for the DPO."
---

# dsar-handling-pitfalls

A defensive block for the operating side of a data-subject request: the process around the request, not the
rule behind it. The failures are mechanical: the clock starts when somebody noticed instead of when the
request arrived, an extension is granted but never told to the person, the search skips the index or the
backups, the export goes to the wrong address. The only legal text read for this block is the response-time
rule of Regulation (EU) 2016/679 (the GDPR) Article 12, paragraphs 3 and 4, as published in the Official
Journal, and it applies to that regulation only. Whether a person is entitled to a given right in a given case,
and any exemption, is decided by the DPO or counsel. What the code of a product must provide (export, deletion,
correction) is in `business/data-protection`; how a legal statement is dated and sourced is in
`business/regulatory-watch`; the documents a company publishes are in `business/legal-documents`. This block
is a working method for qualified people, not legal advice.

## When
- A request from a person about their personal data arrives, by any channel.
- A product or a support team is about to build or change the intake, the queue, the export or the deletion.
- A request is late, was extended, was refused, or went wrong (wrong recipient, missing system).
- The process is audited, or tested for the first time.

## Steps

**Read only the part the task meets.** Part 1 first when a request is in flight or a queue is designed.

| Part | Covers | Read it when | File |
|---|---|---|---|
| 1 | Clock and case record: received date, due date, extension and refusal notices, intake from every channel, lifecycle events | a request arrives, a due date is computed, or a case tool is built | [`01-clock-and-case-record.md`](./references/01-clock-and-case-record.md) |
| 2 | Package, delivery and the DPO line: manifest of systems searched, secure delivery, what is not an engineer's call, an end-to-end test | the answer is assembled or sent, or the process is tested | [`02-package-delivery-and-dpo-line.md`](./references/02-package-delivery-and-dpo-line.md) |

## Output / checkpoint
No pipeline checkpoint (business layer). For each request or process under review: the date received and the
computed due date with the reason for any move, the channel it came through, the list of systems searched with
a result each, the notices sent (extension, refusal, completion) with their dates, the delivery channel, and the
questions routed to the DPO with a named owner. Evidence for a process is a dummy-person case that went from
intake to closure with every event recorded.

## Guardrails
- This block does not replace advice from a qualified lawyer or the DPO; it never states that a request must
  be fulfilled, may be refused or is exempt.
- Never compute a due date from memory: it comes from the text read and from the received date stored on the
  case (part 1).
- Never leave an extension or a refusal unsent: both are notices to the person with reasons (part 1).
- Never mark a request complete before every system on the manifest has a result (part 2).
- Never send personal data over a channel that does not authenticate the recipient (part 2).
- Never paste a real person's data into a prompt, a ticket or a fixture; use a dummy person.
- Time limits other than those of the regulation read, national rules and later amendments were not checked:
  say so in the answer and ask the DPO.

## Origin
Lifecycle shape from the inthhq `dsar` documentation (Apache-2.0); time-limit statements from Regulation (EU)
2016/679 Article 12(3) and (4), read on EUR-Lex 2026-10-16. The full provenance, what was removed and what is
our own guidance are in [`references/origin.md`](./references/origin.md). 🟡: never run by us.
