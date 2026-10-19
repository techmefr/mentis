# swift-conventions §2 — Parameters, labels, documentation

> Section 2 of `skills/swift-conventions`. Read it when a signature is written, a label chosen or a public
> declaration documented. The other section and the guardrails stay in `SKILL.md`.

1. **Choose parameter names for the documentation that mentions them.** The name does not appear at the call
   site but reads inside the doc sentence (`predicate`, `newElements`, not `includedInResult` or `with`).
2. **Use default values when one value is the common case,** and put defaulted parameters last. One method
   with defaults is simpler to learn and document than a family of overloads that differ by omitted
   arguments, and families hide surprises such as an explicit `nil` not meaning the same as omission.
3. **Labels.**
   - Omit all labels when the arguments cannot be usefully told apart (`min(a, b)`).
   - In an initializer that converts a value without losing information, omit the first label; in a narrowing
     conversion, label the first argument with the narrowing it performs (`truncating`, `saturating`).
   - If the first argument is part of a prepositional phrase, label it, starting at the preposition; if the
     first two arguments are parts of one abstraction, move the preposition into the base name
     (`moveTo(x:y:)`).
   - If the first argument is part of a grammatical phrase with the base name, omit its label; a label is
     needed where the phrase would otherwise mislead (`dismiss(animated:)`, not `dismiss(false)`).
   - Label every other argument. A defaulted argument can be omitted, so it never takes part in a phrase and
     is always labelled.
4. **Name tuple members and closure parameters** where they appear in an API, chosen like parameter names.
5. **Document every declaration of a published API.** The documentation comment begins with a one-fragment
   summary ending in a period, saying what a function does and returns (omitting null effects), what a
   subscript accesses, what an initializer creates, or what any other entity is. Further paragraphs use full
   sentences; use the recognised markup keywords for parameters, returns, throws, complexity and notes. If the
   API cannot be described simply, it may be the wrong API. Internal code follows the no-comment rule of
   the house; this rule is for the declarations other people compile against.
6. **Take care with unconstrained polymorphism** (`Any`, an unconstrained generic) in overload sets: when the
   element type can itself be a sequence, two overloads can collide. Give the second overload a distinguishing
   label (`append(contentsOf:)`).
7. **In production code that ships to users, prefer the file-identifier literal over the full-path literal**
   for assertion and logging defaults: it takes less space and does not leak the developer's path. Use the
   full-path literal for test helpers and scripts that never run for end users.
