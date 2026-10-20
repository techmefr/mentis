# architecture-fitness-functions-pitfalls §1 — Choosing and writing rules

> Part 1 of `skills/architecture-fitness-functions-pitfalls`. Read it when a rule is designed or written.
> Source, read 2026-10-20: ArchUnit user guide, "What to Check", "Ideas and Concepts", "The Lang API" and "The
> Library API" (Apache-2.0). Sentences marked "own guidance" are ours and rest on no source read.

1. **Start from a decision, not from the tool's menu.** Own guidance: write the sentence first ("the domain code
   does not depend on the web layer", "a module is reached only through its public package"), with the reason
   and the link to the record that holds it. A rule with no sentence behind it has no one to defend it when it
   fails on a deadline.
2. **Rank the decisions by the cost of breaking them.** Own guidance: layer direction, absence of cycles between
   modules and encapsulation of a module's internals are worth a rule because a breach spreads; naming taste
   rarely is. Cap the suite at what the team will actually fix when it goes red.
3. **Know the kinds of check the tool offers.** The guide's "What to Check" groups them: package dependencies
   (nothing in one package may depend on another; or only some may depend on it), class dependencies, where a
   class must live (a naming pattern implies a package), inheritance (implementers of an interface share a
   naming suffix; whoever uses a persistence type lives in the persistence package) and annotations. Own
   guidance: express your decision with the narrowest of these, so a failure points at a cause.
4. **Use the ready-made architectures for the common shapes.** The library layer provides checks for a layered
   and an onion architecture, for slices that must be free of cycles or must not depend on each other, for
   modules with declared allowed dependencies and exposed packages, and a few general coding rules (no console
   writes, no generic exceptions, constructor over field injection). Own guidance: prefer these to hand-written
   copies; they are the shape other maintainers already recognise.
5. **Say what to do in the failure message.** The guide lets a rule carry its own description, and the failure
   report is built from it. Symptom: a build fails with a list of class names and nobody knows what is wrong.
   Fix: a description in the form "X must not depend on Y; move the shared type to Z" (own guidance).
6. **Match by anchored names, not loose substrings.** Own guidance: a package pattern that matches a bare word
   anywhere also matches `foo.bar.service_helper` and test code. Anchor on the module root, and decide
   explicitly whether tests and third-party classes are part of the analysed set; the JUnit support offers
   import options for excluding tests and archives.
7. **Prefer an allow-list for an inner layer.** Own guidance: "the inner layer may depend only on these" cannot
   be undone by a new forbidden module appearing, while "must not depend on A, B, C" misses D. Use the
   deny-form only for a single known bad dependency.
8. **A fitness function can also be a number.** The guide describes architecture metrics (cumulative dependency
   measures, component coupling and abstractness, visibility of members) computed over a chosen partition of
   the code. Own guidance: a metric with a threshold that may only improve is a softer fitness function when a
   hard dependency rule would be too strict; check the tool's definition of each metric before reading a value.
9. **Not every decision is checkable by structure.** Own guidance: runtime properties (latency, availability,
   recovery) need another kind of fitness function: a load test with a threshold (`skills/load-and-capacity-testing-pitfalls`),
   a service-level objective (`skills/slo-design`), a restore drill. Do not force them into a dependency rule.

## Checks (own guidance)
1. Each rule's description names the decision and the fix.
2. The analysed set is stated: which roots, whether tests and libraries are in.
3. Rules for inner layers are allow-lists.
