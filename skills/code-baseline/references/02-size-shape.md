# code-baseline §2 — Size and shape

> Section 2 of `skills/code-baseline`. Read it when a file or a class grows, or a name gets vague. The other sections and the guardrails stay in `SKILL.md`.

1. **A new source code file stays under ~200 lines.** Past that, the edit that would cross the line is the
   moment to split.
2. **The count is a proxy; cohesion is the thing.** The question the ceiling is standing in for is how many
   *reasons* the file has to change — a file that only ever changes when one rule changes is fine at any
   length, and one that changes whenever either the API or the presentation moves is already two files at
   any length. The number is there because it is checkable and the real question is not, so use it as a
   prompt to ask the real one.
3. **What the ceiling applies to**: application code (controllers, components, services, jobs, listeners,
   presenters), business logic, and utilities that hold real logic.
4. **What it explicitly does not apply to** — and mis-classifying to dodge the rule is itself the
   anti-pattern: config files and lockfiles (not authored), **tests** (a 600-line test class accumulating
   cases is not a smell), **migrations** (one atomic change per file, splitting defeats the point),
   markdown, generated or vendored files, and **declarative manifests** (route files, config arrays,
   registries — they're lists, and a long list is fine). A 700-line class isn't "config" because someone
   named it a config.
5. **A function's ceiling is much lower than a file's.** Once the body does not fit on a screen, its control
   flow can no longer be read — only reconstructed — and the reconstruction is where a missed early return
   or a mis-scoped `try` (§3.6) survives review. The same applies to nesting: three levels in and the reader
   has stopped tracking which conditions still hold.
6. **How to split**: find the seam (which section is least tied to the rest), extract a **cohesive unit** (a
   class, a component, a module — not a random bag of functions), name the new file after its
   **responsibility** rather than its origin (`PriceFormatter`, not `OrderControllerHelpers`), then run the
   tests — a split is a refactor.
7. **Splitting to satisfy the count is worse than being over it.** A 195-line file is fine. A 210-line file
   with one coherent purpose and no real seam is fine — flag it rather than vandalise it. `Part1`/`Part2`
   files, and a `Helpers`/`Utils` dumping ground, are both re-entry points for the same problem.
8. **The deletion test finds the seam the line count cannot.** If removing a feature means editing files in
   five places, the tree is organised by technical kind rather than by responsibility, and every future
   change to that feature pays the same tax. Conversely, a long file that could be deleted whole is
   cohesive by definition.
9. **No god class, and no bag-name.** A class named `*Service`, `*Repository`, `*Manager`, `*Helper`,
   `*Util`, `*Handler` invites unrelated methods to accumulate, because nothing in that name can ever be "not
   about that". Name it after **what it does**: an action (`RegisterUser`), a query (`UsersDueForRenewal`), or
   a domain concept with real behaviour.
10. **The smells that flag one**: the bag name itself; more than ~3–5 public methods on the same noun for
    unrelated reasons; verbs from different domains on one class; 6+ injected collaborators; methods that
    never touch instance state (then it's a namespace, not a class); and a test file with five unrelated
    describe-blocks under one name.
11. **A file everything imports is a coupling hub.** The shared `utils` module is the usual one: it has no
    concept, so it accumulates (point 7), and because every module depends on it, a change to any part of it
    can affect anything. It also produces the import cycles that are easy to add and hard to see.
12. **Five positional parameters is an unreadable call site.** Nobody reads a call written as
    `create(true, false, 3, null)` correctly, and the day two adjacent parameters share a type, transposing
    them typechecks (§5.4).
    Group them into a named object, or the function is doing more than one thing.
13. **A boolean parameter that switches behaviour is two functions.** `render(isPreview: true)` means the
    body contains both, every future change has to be correct for both, and the call site says nothing about
    which one it wanted. Split them and share whatever is genuinely shared.
14. **A long branch chain over a type is asking for polymorphism or a lookup.** Each new case edits the same
    chain, which means every consumer is re-tested for a variant that does not concern it — the function-level
    form of §5.2. A map from the case to its behaviour, or a type per case, makes the addition additive.
15. **Dead code is deleted.** Version control holds it, and code nobody calls still costs: it is read during
    every investigation, kept compiling through every refactor, and taken as evidence of a supported path
    that nobody has exercised in a year. Keeping it "in case" is the same instinct as commented-out code
    (§1.7) with a compiler behind it.
16. **The third occurrence is the one to extract.** Two similar-looking blocks are often two things that
    happen to agree today, and fusing them is §5.2's mistake at the function level — the abstraction then
    grows a flag per divergence. By the third, the shape is evidence rather than coincidence.
17. A single-method `*Service` is the same mistake, smaller: if it does one thing, name it after that thing.
    And a "catalog interface" listing twelve `find…` shapes is the anti-pattern abstracted rather than fixed.
18. **The rule applies to the test tree too**: a helper used by one test file stays a local builder in that
    file; a helper genuinely reused across files gets a named fixture file — never a shared catch-all.
