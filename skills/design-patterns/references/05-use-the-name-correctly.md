# § 5 — If you use the name, use it correctly

> Section 5 of `skills/design-patterns`. Read it when a pattern name is about to appear in a class name,
> a commit message, an ADR or a review comment.

1. **A misnamed pattern is worse than an unnamed structure.** "Factory" on something that isn't one
   sends every future reader looking for indirection that doesn't exist. The cost is paid repeatedly and
   by other people: the name sets an expectation about how the class behaves — that it builds things,
   that it can be swapped, that there are several implementations — and every reader spends time
   discovering the expectation was wrong.
2. **Name it in the code or in the ADR, once** — not in a comment (`documentation-adr` §1.2, and no
   comments where the naming can carry it). In the code means the type or file name carries it; in the
   ADR means the decision record says which pattern and why. Saying it in both is how the two drift, and
   saying it in a comment puts it in the one place nothing keeps honest.
3. **When a pattern is deliberately not used**, and someone will wonder why, that's a line in the ADR
   (`documentation-adr` §4). It is the cheapest line in the file and the one that stops the same
   discussion from being had every six months — particularly for the Repository-over-an-ORM question,
   which is asked by every newcomer who has worked somewhere it was the house rule.
4. **The domain noun goes first, the pattern name second, or not at all.** `PaymentProvider` and
   `StripePaymentProvider` say what the thing is; `AbstractProviderFactoryStrategy` says only how it is
   built. A reader searching the codebase searches for the domain word — invoice, refund, import — so a
   name assembled from pattern vocabulary is unfindable by everyone who does not already know it exists.
5. **A pattern name in a review comment has to point at the structure.** "This is a Strategy" is a
   claim, and the reviewable version names the branches: which field is switched on, how many cases,
   whether the set is growing. Without that, the remark is a preference and the author is entitled to
   ignore it — and it should not block the diff (§1.5).
6. **Half the catalogue's names mean different things in different communities.** "Repository" in a
   Laravel codebase, in a DDD book and in a .NET shop are three different contracts; "Service" means
   almost nothing at all, which is why `code-baseline` bans it as a class-name suffix. When a name is
   genuinely ambiguous, write the behaviour rather than the label: "one wrapper we own around the vendor's
   client" needs no pattern name and cannot be misread.
7. **The pattern name is not the interface's documentation.** A reader who knows Strategy still does not
   know what the strategies are chosen by, what happens for an unknown value, or which of them is the
   default. Those are the three questions every caller asks, and none of them is answered by the name —
   so they go where the code can carry them: an enum for the choices, an explicit unknown branch, a
   named default.
8. **A pattern that has been removed has to be removed from the ADR too.** An ADR that still says "we
   access data through a Repository" a year after the repository was deleted is worse than no ADR: it is
   a written claim that the next reader will act on, and the code no longer supports it. Deleting a
   structure and leaving its justification standing is the same defect as a stale comment, at a larger
   scale (§6.9).
9. **Don't let the name settle an argument.** A pattern name is a label for an answer, not the answer,
   and a discussion that ends with one has usually skipped both tests that matter: is there a second real
   case (§1.3), and does the framework already do it (§2). If the name arrived before those, the design
   discussion has not happened yet.
10. **The best outcome of this section is often a name with no pattern in it.** Most structures in a
    codebase do not need one: they need a domain name, one obvious place to live, and a test. Reserve the
    catalogue's vocabulary for the cases where it genuinely saves a paragraph of explanation — that is
    what it is for, and it stops working when it is used for everything.
