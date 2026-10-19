# gdpr-international-transfers-pitfalls §2 — Mechanisms and their proof

> Part 2 of `skills/gdpr-international-transfers-pitfalls`. Read it when a mechanism is named for a flow or a
> register is audited. Source: Regulation (EU) 2016/679 Articles 45, 46 and 47, as published in the Official
> Journal (OJ L 119, 4.5.2016), https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32016R0679 , read
> 2026-10-19. Original publication, not a consolidated version: read the current text before relying on it.
> Sentences marked "own guidance" are ours.

1. **Route 1 is an adequacy decision.** Article 45(1) says a transfer may take place where the Commission has
   decided that the country, a territory, one or more specified sectors, or the international organisation
   ensures an adequate level of protection, and such a transfer needs no specific authorisation. Article 45(3)
   says the decision is an implementing act that specifies its territorial and sectoral application. Own guidance:
   the register cites the decision relied on, its scope (the whole country, a sector, a list of certified
   recipients) and the date it was checked, because a decision limited to a sector does not cover a recipient
   outside it. The current list was not read: the DPO supplies it.
2. **Decisions change.** Article 45(3) provides for a periodic review of a decision at least every four years;
   Article 45(5) lets the Commission repeal, amend or suspend a decision without retroactive effect when a country
   no longer ensures an adequate level; Article 45(8) says the Commission publishes the list of such decisions in
   the Official Journal and on its website. Own guidance: every row relying on a decision has a review date and
   a named watcher (`business/regulatory-watch`), and the plan for "the decision is withdrawn" is written before
   it happens (which flows, which alternative, who decides).
3. **A withdrawn decision does not forbid everything.** Article 45(7) says a repeal under paragraph 5 is without
   prejudice to transfers under Articles 46 to 49. Own guidance: the fallback in point 2 still has to be a
   mechanism the DPO accepts; the engineer never moves a flow to another route alone.
4. **Route 2 is appropriate safeguards.** Article 46(1) says that without an adequacy decision a controller or
   processor may transfer only if it has provided appropriate safeguards and if enforceable data subject rights
   and effective legal remedies are available. Own guidance: the second condition is a question to the vendor and
   the DPO, not a box the contract title ticks.
5. **Some safeguards need no authority authorisation.** Article 46(2) lists, as available without a specific
   authorisation from a supervisory authority: a legally binding enforceable instrument between public bodies;
   binding corporate rules under Article 47; standard data protection clauses adopted by the Commission;
   standard clauses adopted by an authority and approved by the Commission; an approved code of conduct with
   binding commitments from the recipient; an approved certification mechanism with binding commitments.
   Own guidance: the register names which of the six is claimed, cites the instrument and the signature date, and
   attaches the executed copy with its annexes (`skills/dpa-review-pitfalls` part 1 on missing annexes).
6. **Some safeguards need the authority.** Article 46(3) says that, subject to authorisation from the competent
   supervisory authority, safeguards may also come from contractual clauses between the parties or from
   administrative arrangements between public bodies with enforceable rights; Article 46(4) says the authority
   applies the consistency mechanism in these cases. Own guidance: a row relying on bespoke clauses shows the
   authorisation reference, or is marked "not authorised" and escalated; the engineer does not assume a custom
   clause is enough.
7. **Binding corporate rules are a group instrument.** Article 47 says the competent authority approves binding
   corporate rules through the consistency mechanism if they are legally binding on every group member and their
   employees, expressly give data subjects enforceable rights, and meet the content list of paragraph 2 (the
   transfers covered, the principles applied, the rights, liability, complaint procedures, verification and
   training, among others). Own guidance: a row citing them shows the approval, and the recipient is checked
   against the group members the rules actually cover.
8. **Old instruments carry over only as the text says.** Article 45(9) and Article 46(5) say that decisions and
   authorisations adopted under the previous directive remain in force until amended, replaced or repealed.
   Own guidance: a row relying on an old instrument is flagged for the DPO's review; the engineer does not carry
   old paperwork forward on the strength of its date.
9. **Questions to ask per mechanism.** Own guidance. Adequacy: which decision, which scope, is this recipient and
   this data inside it? Standard clauses: which module or form applies to our role and theirs, are the annexes
   filled, is the executed copy in the file? Group rules: is the recipient a covered member? Code or
   certification: is it approved and does the recipient give the binding commitments? Any: who at the vendor
   signed, and what changes if the vendor's own location or ownership changes?
10. **Proof is a document, not a statement.** Own guidance: for each row the file holds the document that proves
    the mechanism (the decision reference, the executed clauses, the approval), dated and attributed. A vendor's
    web page claiming compliance is a pointer to ask for the document, not the document.
11. **The engineer's job stops at the facts.** Whether a recipient's country laws undermine the chosen mechanism,
    and what extra measures are needed, is not decided here; this block reads nothing on that and routes it to the
    DPO or counsel (part 3, point 7).
