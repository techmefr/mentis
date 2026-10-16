# security-questionnaire-answer-pitfalls §1 — The shape of an answer

The failure this section prevents is the three ways small teams answer their first questionnaire: they say
Yes and hope, they say No and stop, or they write a paragraph that avoids both.

## 1.1 Position, fact, compensating control
1. **Start with a one-word position**: Yes, No, Partial or Info. The reader has many rows to get through and is
   scanning for the position first.
2. **Then the plain fact**, specific and checkable, without adjectives. "Two people have production access"
   beats "access is tightly restricted".
3. **For No or Partial, add what you do instead and why it covers the same risk at your size.** Not an
   apology. The source's contrast: "we don't have X" stalls; "we don't do X, here is the compensating control"
   usually does not.
4. **If the buyer's requirement is firm, say what it would take** to meet it, so a blocker becomes a commercial
   conversation. The reviewer's job is to decide whether the gap is acceptable, not to collect certificates.

## 1.2 The four positions and their traps
1. **Yes**: the control exists today for all of the scope the question covers and you could show evidence
   within a day. The trap: Yes for something true of one system and not another. Say Partial.
2. **No**: the control does not exist. The trap: stopping there.
3. **Partial**: true of some systems or some of the time, or in progress with a real date. The trap: using it
   as a soft Yes. If a reviewer would read it as Yes, rewrite it.
4. **Info**: the question asks what, where or how many. Answer it and stop.

## 1.3 The three failures
1. **A bare No** is truthful and stalls: it reads as a gap with nothing behind it.
2. **An evasive paragraph** is visible from the reviewer's side of the table.
3. **A bluff is the only dangerous one**, because the follow-up is a request for the evidence.
4. **The reviewer is usually not trying to disqualify you**; they need a defensible recommendation. A
   straight No with a control gives them something to write down. A bluff gives them a reason to escalate.

## 1.4 Incident-response answers
1. **Name who decides and who would be called.** The source says naming yourself is a complete answer, and
   naming the outside help you would call is what makes it credible.
2. **List customer reports as a detection channel** if they are one. Omitting them while implying comprehensive
   automated detection is the claim that unravels in a follow-up call.
3. **Separate alerts arriving around the clock from a human acting on them immediately.** If there is no
   on-call rotation, say No and state both halves.
4. **Do not copy a notification deadline out of a template.** Say who is told and how, and that applicable
   contract and legal deadlines take precedence; the number belongs to whoever owns your contracts (§2.3).
5. **Scope support during a customer's own investigation to their data**; unbounded forensic help for any
   incident is an open-ended obligation a cell should not accept.
6. **Claim a post-incident review if you write things down after an outage**, and say where they are kept.
7. **If a breach happened, say so, with what changed.** The source's view is that disclosing with the fix
   attached is survivable and concealment turns a security question into a trust question.
