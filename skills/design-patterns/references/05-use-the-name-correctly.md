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
11. **A file or class suffix is a promise about behaviour, and the suffix has to be true on day one.**
    `*Factory` promises the class builds and returns instances of something else, not that it also
    validates, persists or notifies as a side effect; `*Strategy` promises the class is one of several
    interchangeable implementations behind a shared interface, not the only one that will ever exist. A
    suffix chosen for how official it sounds rather than for what it commits to is the seed of the next
    misnamed-pattern complaint (§1).
12. **Naming drift is the failure mode of a correctly-named pattern left alone.** A `PaymentGateway`
    interface named for the Adapter it started as slowly grows methods that only one implementation needs,
    until the interface is Adapter in name and god-interface in shape — nothing renamed it, the behaviour
    just moved. Catching this is a review question, not a one-time check: does every method on the
    interface still make sense for every implementation, today, not at the point the name was chosen.
13. **A test file's name should say what breaks, not which pattern it covers.** `StrategyTest` tells a
    reader nothing about which branch failed; `RefundStrategySelectionTest` or a test named for the
    behaviour under test — "falls back to the default channel when the requested one is unknown" — tells
    them exactly what regressed. The pattern name belongs on the production class; the test name belongs to
    the behaviour, because that is what a failing test report actually needs to communicate at 2am.
14. **Two names for the same shape in the same codebase is worse than either name alone.** If one module
    calls its provider abstraction a "Strategy" and a neighbouring module calls the identical shape a
    "Handler" or a "Driver", a reader has to learn the codebase's synonyms before they can even search it.
    Pick one term per shape and keep a one-line note of the choice where naming conventions already live,
    rather than let each author's preferred vocabulary win locally.
15. **A pattern name in a variable or parameter, as opposed to a type name, is almost always noise.**
    `strategyInstance`, `factoryResult`, `theObserver` tell the reader nothing the type annotation or the
    IDE's inline type hint doesn't already say, and they add a word to every call site that has to be read
    past. Reserve the vocabulary for the type; name the variable for the domain value it holds —
    `provider`, `refund`, `handler` for the one actually resolved this call.
16. **A pattern name inside an error message or a log line is a debugging tell, not documentation.**
    `throw new Error("Strategy has no handler")` tells whoever reads the incident channel at 2am that a
    dispatch failed, not what business operation was being attempted or which input caused it. The
    message a caller sees should name the domain failure — "no refund channel configured for this
    provider" — and leave the pattern vocabulary in the code that only developers read.
17. **Pattern vocabulary belongs in identifiers, never in user-facing strings.** A validation message,
    a toast, an admin screen's label should never say "Factory" or "the default Strategy" — the reader
    on the other end has no reason to know the word and every reason to be confused by it. If a string
    meant for a user has drifted into naming its own implementation, that string was written from the
    code outward instead of from what the user needs to know.
18. **A rename that only touches the identifier, not the shape, silently invalidates the ADR that named
    it.** Renaming `InvoiceStrategy` to `InvoiceHandler` through an IDE's rename-symbol tool is safe for
    the compiler and unsafe for the reader: the ADR (§5.2) and any review comment that said "this is a
    Strategy" now refer to a name the code no longer has. A pattern-carrying rename is a documentation
    change, not just a refactor, and needs the same grep-and-fix pass as deleting the pattern outright
    (§6.9).
19. **One class filling two pattern roles under one name means the name has stopped being specific.** A
    class that is simultaneously "the Strategy" callers pick between and "the Factory" that constructs
    the other Strategies is neither cleanly — a reader asking "which one is this" gets two contradictory
    answers from the same identifier. Split the two responsibilities into two named things, or drop the
    pattern name entirely and describe what the class actually does (§5.10).
20. **A file that keeps its pattern-derived name across an unrelated rewrite hides the rewrite in blame
    history.** Renaming `OrderState` to `OrderStrategy` because the implementation changed shape, without
    a commit that says so, means the next person who blames the file for a bug finds a naming change where
    they expected a behavioural one. Keep the name stable across cosmetic changes and change it, with a
    reason in the commit message, only when the shape genuinely stopped matching the label (§5.12).
21. **A pattern name borrowed from a different catalogue than the one this repo uses is worse than an
    unnamed structure, because it looks precise while being wrong.** Calling a plain callback registry a
    "Publisher" (a term from a messaging-system vocabulary, not GoF's Observer) or calling a validation
    pipeline a "Middleware Chain" when the codebase's own convention calls that shape Chain of
    Responsibility (§3.11) forces a reader to first work out which glossary is in play before they can even
    check whether the name fits. One glossary, consistently applied, is worth more than a technically
    defensible synonym borrowed from elsewhere.
