# go-conventions §7 — Tests

> Section 7 of `skills/go-conventions`.

1. Table-driven tests give every case a name and run it as a subtest.
2. Tests do not depend on execution order or shared mutable state; independent ones call `t.Parallel()`.
3. Integration tests sit behind a build tag so the default run stays fast and needs no service.
4. A test asserts the observable contract (return values, effects through the public API), not the call
   sequence inside. A test that fails when the code is refactored without a behaviour change is a cost.
5. Prefer a small hand-written fake of an interface over a generated mock of a concrete type; fake the
   consumer-side interface only.
6. Golden and fixture files live in `testdata`; compare structured values with a diffing helper that prints
   the difference instead of two formatted strings.
7. Time-dependent and concurrent code gets a controllable clock or the standard library's synthetic-time
   test facility, never a real sleep.
8. A test file is named after the file it covers, and tests follow the order of the source.
