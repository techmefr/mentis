# testing-anti-patterns — origin and source stamps

> Provenance of `skills/testing-anti-patterns`. Read it when a rule has to be traced back to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

Rewrite of `testing/testing-anti-patterns` and `testing/condition-based-waiting` from a market skills
repository (the companion repo of the upstream this framework responds to), merged into one block
because they're one responsibility: tests that report safety they don't have. The five anti-patterns
and the wait-on-a-condition rule are theirs. The incomplete-mock item is reinforced by our own
experience of a mocked search engine missing a method, which presented as a database bug; the
"never increase the sleep" and "a flaky test is a bug report" formulations are ours.

**Dogfooded, 2026-09-10.** Applied as a review lens (no new code written) over six real test suites
from earlier this session — xUnit (`/tmp/dogfood-csharp`), pytest (`/tmp/dogfood-python`), Flutter
widget/unit tests (`/tmp/dogfood-flutter`), `go test` (`/tmp/dogfood-go`), vitest/RTL
(`/tmp/dogfood-react`), and vitest for NestJS (`/tmp/dogfood-nestjs`). Five of the six suites were
clean against every pattern in this block: no mock-existence assertions, mocks built from real shapes
(the C# `FakeOptionsMonitor`, the Python `InMemorySource`), no test-only production methods, and the
Python/Go suites in particular already do condition-based waiting with an explicit timeout
(`asyncio.wait_for`/`TaskGroup` timeouts, `context.WithTimeout`) rather than sleeping.

One real instance of §3 was found and fixed: `item_list_controller_test.dart` in the Flutter project
waited on the 300ms debounce in `ItemListController.onQueryChanged` with hardcoded
`Future<void>.delayed(Duration(milliseconds: 400))` margins — a real wall-clock duration guess, not a
virtual-clock advance, so it was exactly the pattern this block warns about (margin above a timer,
liable to flake under CI load). Rewrote it to poll the controller's own `notifyListeners` stream for
the expected state via a small `waitUntil` helper with a timeout, per §3.2-3.3. The one legitimate
`Future.delayed` left in that file (racing two `onQueryChanged` calls to prove the later one wins) was
already commented as deliberate, satisfying §3.4.

Gap found in the block itself, now fixed as §3.6: nothing distinguished a real wall-clock
`sleep`/`Future.delayed` from a fake-timer/virtual-clock advance (`tester.pump(Duration(...))` in
Flutter, `vi.advanceTimersByTime` in JS). The Flutter widget tests in `item_list_screen_test.dart` and
`countdown_badge_test.dart` use `tester.pump(const Duration(...))` repeatedly and, read against the
original wording ("never wait for a duration; wait for the condition"), look like the same
anti-pattern — they are not: `tester.pump` runs inside Flutter's deterministic fake-async test zone
and cannot flake on machine speed. Applying the rule literally there would have produced a false
positive against idiomatic, correct code. §3.6 names the exemption explicitly so the lens doesn't
misfire on this widely-used idiom.

**Sections 6 to 8 and the reserved-values fixture rule, 2026-10-02.** Sections 1 to 5 are the block as it
was, moved unchanged into `references/` when it became a router, plus one new point, §5.4 (fixtures built
from the values the standards reserve for examples, so that a non-measurement shows in the output), taken
from a public prose-and-quality-gates repository (MIT licence, read 2026-10-02) whose gate used reserved
fixture values for that reason; the RFC numbers and the explanation are ours. §6 is new: idea taken from the
public ECC repository's regression-testing skill for AI-assisted development (MIT licence, read 2026-10-02),
whose observation is that a model reviewing its own change shares the blind spot that produced it; the
catalogue of recurring regressions was rewritten, widened with the patterns this repository's own reviews
keep finding (renames that miss strings, the edited expectation, one instance fixed and the class left, the
non-existent API, the near-duplicate), and the upstream's stack-specific code samples and its sandbox-mode
test harness were not taken. §7 is new: the polluter-bisection idea comes from a helper script in the
public Superpowers repository (MIT licence, read 2026-10-02) that runs test files one at a time to find the
one that creates a stray artefact; the mechanism was rewritten as a method (the list of leaking state, the
halving, the random order with a printed seed) with no script copied, and the project may write its own. §8
is new: the practice of making every test name the break it catches, from the same repository's guidance
on good tests; the revert-proof step and the deletion rule are ours. Differences on purpose: no percentage
target (the upstream testing rules prefer 80%), no mandated assertion style. The facts about reserved
names and address ranges (RFC 2606, 6761, 5737, 3849) were written from the RFC texts as known, **not
re-fetched on the day**.
