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

## Re-verified 2026-10-20 (🟡, nothing run)

Licences read on 2026-10-20: `swiftlang/swift-org-website` (Apache-2.0; head `39f5245`, the page content under
`documentation/api-design-guidelines`), `swiftlang/swift-book` (Apache-2.0; head `1c05984`, the same commit as the pin
above, so the chapters are unchanged) and `realm/SwiftLint` (MIT, "The SwiftLint Contributors"). Facts rewritten, no
text copied.

| Source | Points confirmed |
|---|---|
| API design guidelines page | §1.1 to §1.14 (clarity, omission, roles, weak types, fluent phrases, `make`, side effects, mutating pairs, Booleans and protocols, terminology, case and acronyms, shared base names and return-type overloads, free functions, computed property cost), §2.1 to §2.7 (parameter names, defaults and position, label rules, tuples and closures, documentation summary rules and markup keywords, unconstrained polymorphism, `#fileID`) |
| Concurrency chapter | §3.1 to §3.9 (suspension marked, thread not guaranteed, `async let`, task groups, cancellation, `addTaskUnlessCancelled`, handler race note, unstructured and detached tasks, three isolation forms, main actor and `await`, sendable forms, top-down adoption, stdlib omits the blocking bridge) |
| Error-handling chapter | §4.1 to §4.7 and new §4.8, §4.9 (throws and `try`, `try?`, `try!`, top-level runtime error, `defer`, no unwinding, typed throws) |
| Reference-counting and memory-safety chapters | §5.1 to §5.5 (cycles, weak and unowned, capture lists, `unowned(unsafe)`, in-out overlap checked at compile or run time even on one thread) |
| SwiftLint README | §6.1 to §6.4 (configuration, nested rules, baseline keys, strict, `swiftlint:disable` forms and `all`) |

**Corrected:** the documentation scope (the guidelines say every declaration), detached versus plain `Task`
inheritance, the nested-configuration merge rule, the Boolean nonmutating condition. **Added:** §4.8, §4.9, a note on
`--config`. **Marked as the block's own:** the unchecked-escape ban (§3.8), the catch-all argument (§4.4), the
weak-reference-is-no-cache remark (§5.2), "a diff never adds to a baseline" (§6.2). **Still unverified:** the
complexity-markup behaviour in every tool, strict-concurrency migration modes, noncopyable types and newer ownership
modifiers, the linter rule catalogue, and the formatter. The guidelines page remains older than the concurrency
features.

Independent verification 2026-10-21: 16 checked, 16 matched, 0 corrected, 0 unverified
