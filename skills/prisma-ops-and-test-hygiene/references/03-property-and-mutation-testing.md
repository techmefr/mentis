# prisma-ops-and-test-hygiene §3 — Property-based and mutation testing

Example tests check the cases you thought of. Two techniques check the rest: generate cases from a
statement that must always hold, and measure whether the suite notices when the code is broken. Use them
where the cost of a wrong answer is high and the logic is pure enough to test cheaply.

## 3.1 Property-based testing
1. **State a property, not an example**: for any valid input the result satisfies a condition. Typical
   shapes: round trip (decode of encode returns the input), idempotence (applying twice equals once),
   invariants (a total never goes negative, a list stays sorted), and agreement with a slow but obviously
   correct implementation.
2. **A library generates the inputs** (fast-check is the usual JavaScript one): describe the input with
   arbitrary generators (integers, strings, records built from them), and the runner executes the property
   many times (the MIT testing source's comment says 100 by default; not verified).
3. **A failing case is shrunk** to a small one and reported with the seed, so the failure is reproducible;
   keep the printed seed and path in the bug report, and add the minimal case as an ordinary example test.
4. **Constrain generators to valid inputs** with the library's filters and mapping, not by discarding most
   cases (a property run that discards nearly everything proves nothing).
5. **Where it pays**: parsers, serialisers, money and date arithmetic, state machines, pagination, merge or
   diff logic, and permission rules. Where it does not: thin glue and anything that needs a database per
   case.
6. **Keep runs deterministic in CI**: fix the seed in CI or print it on failure and make it replayable.

## 3.2 Mutation testing
1. **Coverage counts lines visited, not lines tested.** A test that runs the code and asserts nothing gives
   full coverage and zero protection.
2. **A mutation tool** (Stryker for JavaScript and TypeScript) makes small changes to the source (flip a
   comparison, remove a call, change an operator) and runs the tests for each. A mutant the tests fail on is
   killed; one they pass on survived, which is a missing or weak assertion.
3. **Read the survivors, not the score.** Each surviving mutant points at a behaviour no test pins; either
   write the test or decide the code is dead.
4. **It is slow**, so run it on changed files in CI, on the modules where defects are costly, and fully on a
   schedule, not on every commit of the whole repository.
5. **Equivalent mutants** (a change that cannot alter behaviour) survive legitimately; ignore them with a
   documented reason, not a blanket exclusion.

## 3.3 Verification
- A property was run against a deliberately broken implementation and found a counterexample, and the
  counterexample was added as an example test.
- Mutation results for one critical module were read and at least one survivor became a new assertion.

## 3.4 Nest mapping
Both run on plain functions and services outside the framework: test the pure core of a module (pricing,
state transitions, validators) directly, and leave the DI wiring to ordinary tests; see
`nestjs-node-conventions` for keeping the core free of framework imports.
