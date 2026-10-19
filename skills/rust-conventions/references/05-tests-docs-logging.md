# rust-conventions §5 — Tests, documentation and logging

> Section 5 of `skills/rust-conventions`. Read it when a test is written, when a public item or module is
> documented, or when a diagnostic is emitted. The general test doctrine is `skills/testing-anti-patterns` and
> the observability doctrine is `skills/observability-instrumentation`. The other sections and the guardrails
> stay in `SKILL.md`.

**Tension with the house no-comment rule, stated once.** Rustdoc on the public items of a *published library
crate* is the product itself, not commentary on it: it is what the API's users read. The sections below
describe that documentation. For application code and for crate-internal items the house rule governs, and the
docblock stays to the four things it allows (a type the language cannot express, an exception, a named hazard,
a contract no signature carries).

1. **Tests that only use the public API are integration tests and live under the crate's `tests/` folder.**
   Putting every test in an inline `tests` module makes a source file hold more test than logic, which hurts
   reading and review. When a goal can be reached by either an integration test or a unit test, the
   integration test wins. Reserve in-file tests for private behaviour with no public path.
2. **A test asserts behaviour, not the definition it was built from.** An agent's tests often re-state the
   expected value from the same constant or branch the code under test uses, so they pass by construction and
   only add noise. A constant table is tested through a property it must satisfy (evenly spaced, increasing,
   the direction a related function relies on), not by comparing it to itself. Where such a test exists only to
   satisfy a mutation tool, skip the mutation rather than write the test.
3. **Edge cases that need a failing disk, a late clock or a refused connection are reached through the
   substitution points of §4.5**, not by hoping the real system misbehaves. Test helpers, mock sources and any
   switch that weakens a safety check are behind the single `test-util` feature.
4. **A secret-holding type has a test that proves its `Debug` output hides the secret.** Implement `Debug` by
   hand for such a type, print a placeholder, and assert that the rendered text contains the type name and not
   the value. The test is what keeps a later `derive` from leaking it.
5. **`Send`/`Sync` regressions are tests.** A one-line compile-time assertion per type or per main async entry
   point (§4.8) is enough.
6. **Fuzzing and property tests are named, not assumed.** A parser or decoder that takes outside bytes has a
   fuzz target or a property test, or the review records that it has none. Neither of the two main guides
   consulted here gives a procedure for it (the national guide marks its fuzzing chapter as to be written), so
   this block states the expectation and leaves the tool choice to the project.
7. **Public library items carry a canonical doc.** One summary sentence of about fifteen words on a single
   line; free-form detail; an `Examples` section; an `Errors` section when it returns a `Result`; a `Panics`
   section when it can panic; a `Safety` section when it is `unsafe` or can cause undefined behaviour; an
   `Abort` section when it can end the process. Parameters are explained in prose inside the description, not
   in a table. Examples exercise the item and are compiled by the doc-test run, so they stay true.
8. **Every public module has module-level documentation**: what it contains, when to use it (and when not),
   examples, observable side effects with the guarantees made, and the relevant implementation details. The
   crate root has thorough documentation too, with the metadata fields (`description`, `license`,
   `repository`) filled in `Cargo.toml` and a pointer to release notes that flag breaking changes.
9. **Docs describe the end state, not the design journey.** No "why we chose X over Y" essay and no table of
   which guidelines the change followed in user-facing docs: it is process, it goes stale, and the reader of an
   API wants behaviour. Enduring architecture principles belong in the repository's top-level readme.
10. **Re-exports show up inline.** A `pub use` of the crate's own item is annotated so it appears among its
    siblings in the generated docs; a standard-library or third-party type is not inlined, so the reader sees
    it is external. Links to other items use the doc-link syntax, and implementation details are hidden from
    the rendered docs: show the impls users need and no others.
11. **Production code emits structured events, not prints.** A diagnostic goes through the project's telemetry
    framework; `println!` and `dbg!` are for a command-line program whose interface is its standard output.
    Events have a stable hierarchical name (`component.operation.state`), named properties, and a message
    template whose placeholders are filled at viewing time, not by formatting a string at the call site (which
    allocates on every call). Attribute names follow a published telemetry convention where one exists.
12. **Library telemetry is cheap.** A crate used by others must assume its events are always on. Keep the
    hot inner loop free of events; when unavoidable, emit lightweight events with no formatting allocation, or
    emit one event per batch and let the reader rebuild the detail offline.
