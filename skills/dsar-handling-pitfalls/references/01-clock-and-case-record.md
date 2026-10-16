# dsar-handling-pitfalls §1 — Clock and case record

> Part 1 of `skills/dsar-handling-pitfalls`. Read it when a request arrives, a due date is computed or a case
> tool is built. Time limits: Regulation (EU) 2016/679 Article 12(3) and (4), as published in the Official
> Journal (OJ L 119, 4.5.2016), https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32016R0679 ,
> read 2026-10-16. That is the original publication, not a consolidated or corrected version: read the current
> text before relying on it. Lifecycle shape: the inthhq `dsar` request-lifecycle guide (alpha software).
> Sentences marked "own guidance" are ours.

1. **Treat the request as a case with a lifecycle, not as a query.** The lifecycle guide chains these stages:
   intake, queue and review, identity or authority verification where risk calls for it, fulfilment with a
   manifest, delivery, appeals, and audit with notifications. Own guidance: each stage is an event written on
   the case, with who did it and when, so the case can be replayed.
2. **The response time is from the text.** Article 12(3) says the controller provides information on the
   action taken on a request under Articles 15 to 22 without undue delay and in any event within one month of
   receipt of the request. The period may be extended by two further months where necessary, taking into account
   the complexity and number of the requests. The controller informs the data subject of any such extension
   within one month of receipt, with the reasons for the delay. These statements are about that regulation as
   published; national law and later amendments were not checked.
3. **If no action is taken, the person is told.** Article 12(4) says that where the controller does not take
   action on the request, it informs the data subject without delay and at the latest within one month of
   receipt of the reasons for not taking action, and of the possibility of lodging a complaint with a
   supervisory authority and seeking a judicial remedy. Whether not acting is permitted in a given case is a
   question for the DPO (part 2, point 6).
4. **Store the received date, and compute the due date from it.** Own guidance: the clock in the text runs
   from receipt, so the case records the moment the request reached the organisation (the mail time, the form
   timestamp, the post-room stamp), not the day somebody opened it. Store the computed due date as a separate
   field, and when it moves, store the reason and who moved it. "Why is this late" must be answerable from the
   case alone.
5. **An extension is a recorded event with a notice.** Own guidance: the event holds the reasons, the new due
   date and a copy of what was sent to the person, and the notice goes out inside the first period, since the
   text requires the person to be told within one month of receipt. A case that shows an extended due date and
   no sent notice is a defect to flag.
6. **A refusal is a recorded event with a notice.** Own guidance: the event holds the written reasons and the
   copy sent. The wording of the reasons is drafted with the DPO; the engineer's job is that a refusal cannot
   be closed without the notice attached.
7. **Every channel feeds one queue.** Own guidance: a request can arrive through the support mailbox, a chat,
   a form, a letter, a message to an employee or a processor. Article 12(1) mentions that information may be
   given orally when the person asks and their identity is proven by other means, so do not assume the form is
   the only door. List the channels, route each to the one case queue, and teach the front line to forward
   rather than to answer. A request received by a processor on the controller's behalf is routed under the
   contract; which party's clock applies is a question for the DPO.
8. **Where the person asked electronically, answer electronically.** Article 12(3) says that where the request
   is made by electronic form means, the information is provided by electronic means where possible, unless the
   person asks otherwise. Delivery security is in part 2, point 2.
9. **Clarification and verification are events, and the effect on the clock is not ours to assume.** The
   lifecycle guide has stages for requesting clarification and for verifying identity or authority. Whether
   asking a question or verifying identity pauses, extends or leaves untouched the period is not stated in the
   paragraphs read; do not build a pause into the clock without the DPO's written answer.
10. **Keep the audit trail.** Own guidance: the events above, the notices as sent, the manifest result and the
    delivery log are kept together with the case, so a complaint to the authority can be answered from the
    case file. The retention period of the file is a DPO decision.
