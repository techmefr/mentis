# code-baseline §2 — Size and shape

> Section 2 of `skills/code-baseline`. Read it when a file or a class grows, or a name gets vague. The other sections and the guardrails stay in `SKILL.md`.

1. **A new source code file stays under ~200 lines.** Past that, the edit that would cross the line is the
   moment to split.
2. **What the ceiling applies to**: application code (controllers, components, services, jobs, listeners,
   presenters), business logic, and utilities that hold real logic.
3. **What it explicitly does not apply to** — and mis-classifying to dodge the rule is itself the
   anti-pattern: config files and lockfiles (not authored), **tests** (a 600-line test class accumulating
   cases is not a smell), **migrations** (one atomic change per file, splitting defeats the point),
   markdown, generated or vendored files, and **declarative manifests** (route files, config arrays,
   registries — they're lists, and a long list is fine). A 700-line class isn't "config" because someone
   named it a config.
4. **How to split**: find the seam (which section is least tied to the rest), extract a **cohesive unit** (a
   class, a component, a module — not a random bag of functions), name the new file after its
   **responsibility** rather than its origin (`PriceFormatter`, not `OrderControllerHelpers`), then run the
   tests — a split is a refactor.
5. **Splitting to satisfy the count is worse than being over it.** A 195-line file is fine. A 210-line file
   with one coherent purpose and no real seam is fine — flag it rather than vandalise it. `Part1`/`Part2`
   files, and a `Helpers`/`Utils` dumping ground, are both re-entry points for the same problem.
6. **No god class, and no bag-name.** A class named `*Service`, `*Repository`, `*Manager`, `*Helper`,
   `*Util`, `*Handler` invites unrelated methods to accumulate, because nothing in that name can ever be "not
   about that". Name it after **what it does**: an action (`RegisterUser`), a query (`UsersDueForRenewal`), or
   a domain concept with real behaviour.
7. **The smells that flag one**: the bag name itself; more than ~3–5 public methods on the same noun for
   unrelated reasons; verbs from different domains on one class; 6+ injected collaborators; methods that
   never touch instance state (then it's a namespace, not a class); and a test file with five unrelated
   describe-blocks under one name.
8. A single-method `*Service` is the same mistake, smaller: if it does one thing, name it after that thing.
   And a "catalog interface" listing twelve `find…` shapes is the anti-pattern abstracted rather than fixed.
9. **The rule applies to the test tree too**: a helper used by one test file stays a local builder in that
   file; a helper genuinely reused across files gets a named fixture file — never a shared catch-all.
