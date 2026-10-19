# flutter-conventions §12 — Dart language habits

> Section 12 of `skills/flutter-conventions`. Read it when an import is added, a future is started and not
> awaited, generated code is touched, a null is forced, a JSON payload is decoded, or the analyser is
> configured. The other sections and the guardrails stay in `SKILL.md`.

1. **One import style per project, enforced by the analyser.** The language's own style guide prefers
   relative imports between files of the same package's library directory; many teams prefer package imports
   everywhere for greppability. Either is defensible and the two lints that enforce them are mutually
   exclusive, so pick one in the analysis options and let the tool decide every case. Outside the library
   directory (tests, tool scripts) a package import is the only option. A file that mixes the styles is the
   half-migrated state, and a debate in review is a sign the lint is missing.
2. **A future that is not awaited says so.** A call that starts asynchronous work and drops the result is
   either a bug or deliberate; the analyser's unawaited-future lint tells them apart. When it is deliberate
   (analytics, a cache warm-up), wrap it in the explicit marker and put the error handling inside the
   operation, because an error raised in a future nobody awaits ends in the zone's uncaught handler and is
   reported as a crash with no caller. Never silence the lint by adding an `async` that awaits nothing.
3. **Generated code is a build output with a policy stated once.** Either the generated files are committed
   and a CI step proves they are current, or they are not committed and the CI generates them; a project
   that does both has merge conflicts in files nobody should read. They are never edited by hand, they are
   excluded from formatting, analysis and coverage, a conflict in one is resolved by regenerating, and the
   generator and its configuration are pinned like any other dependency (§9 prefers hand-written code where
   the project has taken that position).
4. **Every `!` is an assertion with no message.** A null-forcing operator turns a missing value into an
   exception at a distance from its cause. Prefer making the compiler see the check: copy a field to a local
   before testing it (fields are not promoted, locals are), use a pattern with a null check, or return early.
   A bang is acceptable immediately after a check the compiler cannot follow, and never on data from the
   network, a file or user input, where "cannot be null" is a hope.
5. **`late` is a promise about initialisation order, so keep the promise obvious.** A `late` field with an
   initialiser is lazy and fine. A `late` field without one is assigned by a lifecycle method and read after
   it; if the assignment is conditional, asynchronous or can be skipped, the field is nullable with a guard
   instead, because a read before assignment throws at runtime in a place the analyser accepted.
6. **A default value is not a recovery.** Writing `?? ''` or `?? 0` on a value that should exist replaces a
   visible failure with a plausible wrong answer shown to the user (`skills/gate`, step 6). Default only where
   the absent case is a legitimate state with a legitimate display; otherwise fail into the error state of §4.
7. **JSON is decoded at one boundary into a typed object, and a malformed payload is a parse error.** The
   decoded structure is untyped, so each field is read with a check of its runtime type and presence, in one
   function per payload, and a failure raises a typed exception the repository maps to a failure state. Casts
   scattered through the widgets turn a changed server field into a crash on whichever screen reads it first.
8. **Model closed sets as sealed types and match exhaustively.** A state, an event or a result with a fixed
   set of variants is a sealed hierarchy (§7), and the switch over it has no default branch, so adding a
   variant is a compile error at every place that must handle it. A default branch converts that error into
   silent behaviour.
9. **Records are for local multiple returns; a public API returns a named type.** A record in a method
   signature that crosses a layer boundary is an unnamed concept whose fields are positional or ad hoc; give
   it a class, so it can carry documentation by name, validation and equality.
10. **Value types define equality and hash together, over immutable fields.** A class compared by value
    overrides both operators from the same fields (or is generated to), and its fields are final; a mutable
    field in the hash makes an object vanish from a set after a change. State holders emit new instances
    (§7), and collections returned from them are unmodifiable views.
11. **Time has one representation inside the app and another at the screen.** Instants are stored,
    transported and compared in UTC; conversion to local time happens at display, with the user's locale
    (§9). The current time is read from an injected clock (§10, point 8), and arithmetic over days is done on
    calendar fields, since adding twenty-four hours across a daylight-saving change is not adding a day.
12. **Heavy work leaves the UI isolate.** Parsing a large payload, image processing, compression and
    cryptographic work run in a separate isolate through the framework's helper, with sendable arguments and
    results (plain data, not widgets or closures capturing them). A frame budget is gone when decoding a
    megabyte of JSON runs inside a build or a listener.
13. **Catch specific types, and never catch what signals a programming error.** A catch clause names the
    exception it handles. The error class marks bugs (a bad argument, a failed state check) and is not caught
    to be handled; letting it propagate to the reporter is the point. A catch that logs and continues
    (the general rule is `skills/code-baseline` §3) leaves the screen in a state nobody designed.
14. **The analyser configuration is the project's contract, and an ignore directive is a finding.** Enable
    the strict modes for casts, inference and raw types, and a maintained lint set; do not lower a rule to get
    a diff through. A per-line ignore is the one comment the toolchain tolerates, and each one is justified in
    the review by what the rule would have caught; a file-wide ignore is never added. The analyser is clean
    before a change is reported done (`skills/gate`).
