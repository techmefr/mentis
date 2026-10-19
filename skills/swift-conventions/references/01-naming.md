# swift-conventions §1 — Naming and fluent usage

> Section 1 of `skills/swift-conventions`. Read it when a type, method, property or protocol is named. The
> other section and the guardrails stay in `SKILL.md`.

1. **Clarity at the point of use is the first goal.** A declaration is written once and used many times: judge
   a design by reading a use, not the declaration. Clarity beats brevity; brevity is a by-product of the type
   system, never an aim.
2. **Include every word that removes an ambiguity for the reader, and omit the rest.** `remove(at:)` says the
   argument is a position; a bare `remove(x)` could mean the element. Drop words that only repeat the type.
3. **Name variables, parameters and associated types by role, not by type.** Not `string`, but `greeting`;
   not `widgetFactory`, but `supplier`. If a protocol name is the role, add a suffix to the protocol to avoid a
   clash with the associated type.
4. **Compensate for weak types.** When a parameter is an untyped object, `Any`, or a bare `Int` or `String`,
   put a noun for its role in front of it so the call reads clearly (`addObserver`, `forKeyPath`).
5. **Make call sites read as grammatical phrases.** Fluency may degrade after the first argument or two when
   they are not central to the meaning.
6. **Factory methods begin with `make`.** The first argument of an initializer or factory call does not form
   a phrase with the base name (`Color(red:...)`, not a contorted phrase).
7. **Side effects drive the name.** No side effect: a noun phrase (`x.distance(to:)`). A side effect: an
   imperative verb phrase (`x.sort()`, `x.append(y)`).
8. **Mutating and non-mutating pairs are named consistently.** Verb operation: imperative for the mutating
   form, past participle (or present participle when the verb has a direct object) for the non-mutating one
   (`sort`/`sorted`, `stripNewlines`/`strippingNewlines`). Noun operation: the noun for the non-mutating
   form, the `form` prefix for the mutating one (`union`/`formUnion`).
9. **Boolean members read as assertions** about the receiver (`isEmpty`, `intersects(_:)`). Protocols that say
   what something is read as nouns; capability protocols end in `able`, `ible` or `ing`. Other types,
   properties, variables and constants are nouns.
10. **Terminology.** Avoid obscure terms where a common word works; if a term of art is used, use it in its
    established meaning (do not surprise an expert, do not confuse a beginner). Avoid abbreviations unless
    a web search finds the meaning at once. Prefer precedent to the beginner-friendly invention (`Array`, not
    `List`, for a contiguous structure); in a domain with a widely precedented short form (`sin`), precedent
    wins over the no-abbreviation rule.
11. **Case:** types and protocols in upper camel case, everything else in lower camel case. Acronyms that are
    normally all capitals in American English are uniformly cased by position (`utf8Bytes`, `UTF8`,
    `userSMTPServer`); other acronyms are treated as ordinary words.
12. **Methods share a base name only when they share a meaning or live in distinct domains;** never overload
    on return type alone, which breaks type inference.
13. **Prefer methods and properties to free functions,** except when there is no obvious `self`, when the
    function is an unconstrained generic, or when function syntax is the established domain notation.
14. **Document the complexity of a computed property that is not constant time,** since readers assume a
    property access is cheap.
