# php-architecture-test-pitfalls §2 — Violations and baselines

> Part 2 of `skills/php-architecture-test-pitfalls`. Read it when a violation is waived, a baseline is added
> or changed, or the build fails on a stale entry. Sourced from the Deptrac documentation (commit `66595d1`):
> `docs/concepts.md`, `docs/configuration.md`, `docs/formatters.md`; and the PHPat documentation (commit
> `b7e0172`): `docs/documentation/rules.md`, `docs/documentation/other.md`; read 2026-10-16. Sentences marked
> "own guidance" are ours.

1. **A baseline is a tool for adopting the checker, not for passing a change.** Deptrac's `skip_violations`
   section is a dictionary: the key is the dependent class and the values are the classes it may keep using.
   The concepts page gives the use: put the checker into an existing pipeline without fixing everything first
   and improve gradually while stopping new violations. The formatter page adds that ignoring every error is not
   the best solution, because the current architecture may not allow a change without a new violation. Own
   guidance: a diff that adds a baseline entry is a design decision and is reviewed as one, with the reason in
   the review.
2. **Entries that match nothing fail the run.** In the page's example output a skipped violation that was not
   matched is printed as an error. Own guidance: that is what makes a baseline shrink: when a dependency is
   fixed the entry has to go, so the file only gets shorter, and a stale entry cannot hide a later return of the
   same dependency.
3. **Generate the baseline into its own file and import it.** The baseline formatter (`--formatter=baseline`)
   writes the `skip_violations` section to a file (default `deptrac.baseline.yaml`, set with `--output`), and
   the main config pulls it in with `imports`. The page says this separation is what lets the baseline be
   regenerated without touching the rest of the config. Own guidance: regenerate only to remove entries, and
   check the diff.
4. **Make the waived set visible.** The run option `--report-skipped` prints each skipped violation, and the
   final report counts violations, skipped, uncovered and allowed. Own guidance: put the skipped count in CI
   output so a rising number is noticed.
5. **Decide which rules can never be waived.** PHPat is a PHPStan extension, so by default its errors can be
   silenced like any PHPStan error: by an ignore comment, by `ignoreErrors` or by a baseline. A rule that calls
   `nonIgnorable()` cannot be silenced by any of those, and the page says this applies to all errors of that
   rule only; other rules stay ignorable unless they say so too. Own guidance: use it for the few rules that
   protect a boundary you would never accept a special case on (the domain not using the framework).
6. **A PHPat error is ignored by an identifier derived from the rule's method name.** The page says the
   identifier is currently based on that name. Own guidance: renaming a rule method silently invalidates the
   ignore entries written for it, and a rule that shows up under two names across a rename is hard to track;
   rename a rule in the same change that updates its ignores.
7. **The PHPStan baseline covers architecture tests too.** The PHPat page points out that PHPStan can write a
   baseline of current errors and report only new ones. Own guidance: that baseline mixes architecture errors
   with ordinary static-analysis errors unless architecture tests have their own configuration file, so a
   single "regenerate the baseline" command can accept a new architecture violation along with old type errors.
