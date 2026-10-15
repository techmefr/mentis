# rails-jobs-migrations-pitfalls §4 — RSpec doubles

Source: the community RSpec style guide (`README.adoc`, commit 7622bb6 of 2023-12-11, CC BY 3.0), read
2026-10-08. The guide is old; check each rule against the RSpec version in use (`source-freshness` §3).

## 4.1 Doubles
1. **Use verifying doubles** (`instance_double`, `class_double`, `object_double`) rather than plain doubles. They fail
   when a method that does not exist is stubbed or one is called with the wrong number of arguments, so a spec
   cannot keep passing against an interface that has changed. Use doubles in isolated, behavioural specs more than in
   integration specs.
2. **Keep `verify_partial_doubles` on.** The guide says there is no justification for turning it off: it is what
   makes stubbing a real object's method check that the method exists.
3. **Avoid `allow_any_instance_of` and `expect_any_instance_of`.** The guide says they point to an object under test
   that is too complex and are ambiguous with receive counts. Inject the collaborator instead.
4. **Do not stub methods of the object under test.** It is a code smell and often a sign of a design problem;
   construct the subject in the state the example needs.

## 4.2 Constants and shared state
1. **Do not declare classes, modules or constants inside an example group.** They are defined in the global
   namespace and leak between examples. Use `stub_const`, or build an anonymous class and stub the constant to it.
2. **Avoid `before` and `after` hooks with `:context` scope.** State created there is shared by every example in the
   group, which the guide calls state leakage. Write `:context`, not the ambiguous `:all`, when you do use it.
3. **Assert a change with `expect { ... }.to change(...)`** rather than comparing an absolute count to a number,
   so the expectation does not depend on records left by other examples.

## 4.3 Not adopted from the same guide
1. **"Always use Timecop":** the repository's Rails guidance freezes time with the framework's own time helpers,
   so a rule that contradicts it is not imported. Waiting for time to pass in a spec is
   `testing-anti-patterns` §3.
2. **"Do not use fixtures":** the guide prefers factories and says tests are best with neither. Which of the two a
   project uses is a decision of that project, not a rule from this block.
