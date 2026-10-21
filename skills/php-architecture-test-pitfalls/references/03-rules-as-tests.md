# php-architecture-test-pitfalls §3 — Rules as tests

> Part 3 of `skills/php-architecture-test-pitfalls`. Read it when an architecture test is written, or one
> never seems to fail. Sourced from the PHPat documentation (commit `b7e0172`): `docs/getting-started.md`,
> `docs/examples.md`, `docs/documentation/rules.md`, `selectors.md`, `assertions.md` and `configuration.md`,
> read 2026-10-16. Names are PHPat's. Sentences marked "own guidance" are ours.

1. **Register the test class, and scan the folder it lives in.** PHPat tests are classes you list in the PHPStan
   configuration with the `phpat.test` tag, and the page warns that the architecture tests folder has to be
   among the paths PHPStan analyses. Constructor arguments can be passed when registering. Own guidance: a test
   class that is not registered contributes nothing and the run stays green, so a rule is only verified once it
   has been seen failing.
2. **A rule is a public method whose name starts with `test` (what follows is free, `testFoo` and `test_foo` both
   qualify) or that carries `#[TestRule]`, returning a rule builder or an iterable of them.** The test parser in
   PHPat's source walks the public methods of each registered class and keeps those two kinds; any other method is
   ignored, with no message, so a misnamed rule is silent. A rule that is built but incomplete (no subjects, no
   assertion, no constraint, or a relation assertion with no targets) is not silent: the validator throws an
   exception that names the rule. The rule's reported name is the class, the method and, for an iterable, the key.
3. **Say what to select with the selector that states it.** The documented selectors include
   `inNamespace`, `classname`, `withFilepath`, `extends`, `implements`, `appliesAttribute`, `isFinal`,
   `isReadonly`, `isEnum`, `isInterface`, `isTrait`, `isAbstract`, and combinators `Not`, `AllOf`, `AnyOf`,
   `NoneOf`, `OneOf`, `AtLeastCountOf` and `AtMostCountOf`. Name, namespace and path selectors accept a
   regular expression only when the `regex` argument is true; the page shows the argument set explicitly. The
   source shows what each mode does: with the flag the string is handed unchanged to `preg_match`, so it needs its
   own delimiters; without it a namespace selector is a prefix match on whole segments (`App\Domain` matches
   `App\Domain\Sub`, not `App\DomainX`) and a class name selector is an exact match. Pass the flag and a
   delimited pattern together, and do not rely on a bare string being read as a pattern.
4. **Prefer "can only depend on" to "must not depend on" for inner layers.** `shouldNot->dependOn()` is a deny
   list: anything not listed is allowed, including a vendor package nobody thought of. `canOnly->dependOn()`
   asserts that the selected classes depend on nothing outside the target set, and the page uses it for the
   rule that a domain namespace depends only on itself. Own guidance: use the deny form for a short list of
   things that must never be used anywhere, and the allow form for the layer boundaries.
5. **Know what counts as a dependency.** Two options change it: `ignore_built_in_classes` (relations with PHP
   and extension classes, default false) and `ignore_doc_comments` (relations that appear only in doc comments,
   default false; the extension's default configuration file sets both, and `show_rule_names`, to false). Own guidance: with the defaults, an allow-list rule on a domain layer also has to list
   `DateTimeImmutable` and the like, and a class named only in a doc comment counts as used; decide both on
   purpose and write the decision into the rule's `because()` text.
6. **Pick the assertion that says the intention.** The assertion set covers: extend, implement, include (a
   trait), apply an attribute, be final, abstract, readonly, an interface, an enum, invokable, have only one
   public method (optionally with a given name), construct (use another class's constructor), be named, and
   `shouldNot->exist()` to forbid a class altogether. The examples page uses them for: inner layers not
   depending on outer ones, model and view not depending on controllers, handlers extending an abstract
   handler (selected by name pattern), and entities implementing an interface.
7. **Give the aggregate root its own selector, not a loose name.** The aggregates example selects the root
   by an interface and excludes it from the "no direct access" rule, so members are reachable only through
   the root. Own guidance: select by the interface, not by a folder, so a moved root keeps being the exception.
8. **Always add `because()`.** The page's example passes a message that says what to do instead. Own guidance:
   a failing architecture test with no reason makes the next developer ask for an exception; the message is
   where "implement it another way" and the pointer to a how-to go. `show_rule_names` adds the rule name to the
   assertion message.
9. **Reuse a rule per module with a base class, and register the concrete one.** An abstract test with an
   abstract method returning the module name can build the rule with `sprintf`, and each module extends it;
   only the concrete subclasses are registered. A rule method can also return an iterable of rules, one per
   module, so a new module is one new entry. Own guidance: the base rule's method should be `final` so a
   subclass cannot weaken it, as the page's example already does.
