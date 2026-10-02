# swift-conventions — origin and source stamps

> Provenance of `skills/swift-conventions`. Read it when a rule has to be traced back to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Source read on **2026-10-02**; rules are rewritten from the mechanism.

| Source | Pinned at | Licence | What was taken | Use |
|---|---|---|---|---|
| The language project's API design guidelines page (website repository, documentation section) | commit `168af46` of 2026-09-30 | Apache-2.0 for the repository (the Creative Commons exception in the licence file covers only the blog posts) | §1, §2: fundamentals, naming, conventions, parameters, labels, special instructions | rewritten with this credit |

**Added 2026-10-02 (§3 to §6):** the language guide of the book repository (Apache-2.0, commit `1c05984` of
2026-09-15): the concurrency, error-handling, automatic-reference-counting and memory-safety chapters, read in
full for the points used; and the linter project's README (MIT, read from the web that day: configuration,
nested configurations, inline disables, baseline, strict mode). Not covered: typed throws, noncopyable types
and the newer ownership modifiers, strict-concurrency migration modes, the linter's rule catalogue.

**Not read, so nothing attributed:** the vendor's developer documentation, the formatter documentation, and
third-party agent-skill repositories (one carries a source-available licence with use restrictions, idea only,
and was not read).

**Volatile content to re-check:** the guidelines page is older than the language's concurrency features; check
that nothing in §1 or §2 conflicts with the current language version before applying it to new constructs.
