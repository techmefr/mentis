# § 1 — Tell the three types of documentation apart

> Section 1 of `skills/documentation-adr`. Read it before writing anything down, to decide which of the
> three it is. Point 2 is cited by number from `skills/design-patterns` §5.

1. **ADR** (Architecture Decision Record): a significant decision, hard to walk back: a dedicated
   file, never mixed into the code. The reason it is its own file is that its subject is a *moment* —
   what was true and what was ruled out when the decision was taken — and code moves on while that
   moment does not. Put in a comment, the record gets edited along with the code around it until it
   describes the present, which is the one thing it was not for.
2. **Inline docs** (a comment in the code): only the non-obvious **why** (hidden constraint,
   workaround, surprising behaviour): never what the code already says (existing rule
   `no-comments-in-blade`: no comment if well-named code is enough).
3. **API docs**: the contract consumed by others (see `api-design`), not the same document as an
   ADR. The distinction has teeth: an ADR can say "we chose this shape because of a constraint we
   expect to lift", and putting that sentence in the contract documentation tells every consumer to
   expect a change (`skills/api-design` §2).
4. **The test is who reads it and when.** A future maintainer deciding whether to change something
   reads the ADR; someone reading this function right now reads the comment; someone integrating from
   outside reads the contract. A single document written for all three serves none of them, because
   each reader has to skip most of it to find their part.
5. **Choosing the wrong one is not a filing error, it is a document nobody will read.** A decision
   buried in a comment is invisible to anyone who did not already open that file, which is exactly the
   reader who is about to contradict it. A comment's worth of context put in an ADR is a file that adds
   a hop for a detail that belonged three lines away.
6. **A comment states the constraint, never the intention.** "This has to stay ordered because the
   downstream import reads it positionally" survives; "this will later be extracted into a service"
   becomes false without anything marking it as false, and the next reader treats the stale plan as a
   commitment.
7. **Never restate a rule from a convention block in a comment.** A comment repeating what a
   convention already requires drifts when the convention changes, and it is the copy that will be
   found and believed. Cite the rule, or state the local exception and why it is one.
8. **The commit and the merge request are documentation too, and they are the durable half for
   anything not worth a file.** The reason for a change belongs in the message, where it stays attached
   to the diff it explains — which is what makes an ADR the right form only for a decision *bigger*
   than a change (`skills/ship`).
9. **A repo with a no-unsolicited-docs policy still needs all three kinds.** That policy is about not
   volunteering prose files, not about not recording anything: the constraint goes in the comment, the
   reason goes in the commit, and the decision is *proposed* in the reply or the merge request. Nothing
   goes unrecorded because a file was not the right container (`## When`).
10. **Documentation is a claim about the present that ages differently per type.** A comment is checked
    every time someone reads the code around it; a contract is checked by every consumer; an ADR is
    checked by nobody, which is why it is dated and superseded rather than edited (§3). Knowing which
    of the three you are writing tells you which mechanism keeps it honest.
