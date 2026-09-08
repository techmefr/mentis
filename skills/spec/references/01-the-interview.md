# § 1 — The clarification interview

> Section 1 of `skills/spec`. Read it at the start of step 2, before anything is written down.

1. **One targeted question per ambiguity, asked one at a time, until the scope is sharp.** The exchange
   is the mechanism, not a formality wrapped around a form: an answer usually changes which question
   comes next, so a list of fifteen sent at once comes back with the five easy ones answered and the
   blocking one untouched.
2. **Ask about the case that decides, not about the feature.** "Calendar month or rolling thirty days?"
   is answerable in five seconds and changes the implementation; "can you clarify the context?" moves the
   work back to the person who already thought they had described it.
3. **Interview about the unhappy paths first.** The happy path is what the requester already described,
   and it is the one everybody agrees on. What nobody has decided is the empty state, the invalid input,
   the deleted parent, the refused permission and the concurrent second user — and those decisions are
   what the spec exists to record.
4. **A question you can answer by reading the code is not a question for the interview.** Read the code
   first: existing statuses, existing constraints, what the schema already allows. Asking someone to
   describe behaviour that is already implemented spends their patience on something you could have
   checked, and their answer may well be wrong about their own system.
5. **Write the answers down as you get them, in the words that were used.** Rephrasing an answer into
   your own vocabulary is where a misunderstanding becomes invisible: the requester reads the
   paraphrase, recognises the general shape, and does not notice that "active" now means something
   slightly different.
6. **Distinguish "not decided" from "not said".** A gap the requester has an answer for is closed by
   asking; a gap nobody has ever decided is a decision that needs an owner, and treating the second as
   the first produces an answer improvised on the spot by whoever happened to be in the conversation.
7. **Never fill a gap with a plausible assumption.** The need for an invented rule *is* the finding
   (`business/product-ownership` §7.4). An assumption written into a spec is indistinguishable from a
   requirement three weeks later, and it will be implemented, tested and defended.
8. **A hypothesis stays labelled as one** for as long as it is unconfirmed. "Assuming only active
   contracts count — to confirm" is a usable line in a spec; the same sentence with the caveat dropped in
   the next revision is a requirement nobody decided.
9. **Stop when the remaining questions no longer change what gets built.** Sharpness is not
   completeness: a spec that answers everything imaginable took longer than the feature. The test is
   mechanical — if two possible answers lead to the same code and the same tests, the question can wait.
10. **When the interview cannot close a blocking gap, escalate rather than guess.** Say which question
    blocks the start, who has to answer it, and what you will do meanwhile — usually the part of the
    scope that does not depend on the answer. That is a better outcome than a spec that looks complete
    and rests on an invention.
11. **The interview's output is the input to everything after it.** §2's vocabulary, §3's criteria, §4's
    exclusions and §5's decision records all come out of it, which is why the interview happens before
    any of them are written rather than as a review of a draft.
12. **Where the story's author is also the person building it, the interview still happens** — with the
    epic's owner, with whoever holds the business rule, or in writing with yourself
    (`business/product-ownership` §9). What disappears in that configuration is the person who would have
    asked the awkward question, so it has to be asked deliberately.
