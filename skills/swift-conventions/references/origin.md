# swift-conventions — origin and source stamps

> Provenance of `skills/swift-conventions`. Read it when a rule has to be traced back to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Source read on **2026-10-02**; rules are rewritten from the mechanism.

| Source | Pinned at | Licence | What was taken | Use |
|---|---|---|---|---|
| The language project's API design guidelines page (website repository, documentation section) | commit `168af46` of 2026-09-30 | Apache-2.0 for the repository (the Creative Commons exception in the licence file covers only the blog posts) | §1, §2: fundamentals, naming, conventions, parameters, labels, special instructions | rewritten with this credit |

**Not read, so nothing attributed:** the language reference and concurrency documentation, the error-handling
and ownership chapters, the vendor's developer documentation, the formatter and linter documentation, and
third-party agent-skill repositories (one carries a source-available licence with use restrictions, idea only,
and was not read).

**Volatile content to re-check:** the guidelines page is older than the language's concurrency features; check
that nothing in §1 or §2 conflicts with the current language version before applying it to new constructs.
