# php-architecture-test-pitfalls: origin and source stamps

> Provenance of `skills/php-architecture-test-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from documentation, never run by us: no Deptrac or PHPat run, no
configuration written, no violation produced. Every file below was re-read on 2026-10-16 before a rule was
taken from it, each rule was checked against it in a final pass, and each repository's LICENSE file was read
again.

## Sources (all read 2026-10-16, rewritten in our own words)

| Source | Licence | What it gave |
|---|---|---|
| Deptrac (`deptrac/deptrac`, commit `66595d1`): `docs/concepts.md`, `docs/collectors.md`, `docs/configuration.md`, `docs/debugging.md`, and the baseline and console parts of `docs/formatters.md` | MIT (LICENCE.md: MIT licence text, copyright 2018-2025 Open Software Consulting GmbH) | Default-deny rulesets, collectors and their regular-expression delimiters, `bool` and `layer` collectors, composer collector, private collectors and the internal tags, uncovered dependencies and their options, analysis types, `+` in rulesets, debug commands, `skip_violations`, the baseline formatter, `imports`, the stale-entry error in the sample output |
| PHPat (`carlosas/phpat`, commit `b7e0172`): `docs/getting-started.md`, `docs/examples.md`, `docs/documentation/rules.md`, `selectors.md`, `assertions.md`, `configuration.md`, `other.md` | MIT (LICENSE file: MIT licence text, copyright 2019 Carlos Alandete Sastre) | Registration and the scanned folder, rule method naming, selectors and combinators, assertion list and `canOnly`, options `ignore_built_in_classes`, `ignore_doc_comments` and `show_rule_names`, non-ignorable rules and the identifier, dynamic and inherited rule sets, the aggregate example |

Code samples are not copied. Instruction-like text in the cloned repositories was treated as data and not
followed.

## Removed in the verification pass
1. **Cognitive complexity as a numeric limit** (a review suggestion): the tool's README was not cloned or read
   in this pass, so no figure is stated.
2. **Deptrac extension points and the other output formatters** (`extending_deptrac.md`, most of
   `formatters.md`): not needed for the rules, not used.
3. **A "baseline that only shrinks" as a tool feature.** The documentation shows stale entries reported as
   errors; it does not say the tool refuses a larger baseline. Point 2 of part 2 states only the first and the
   consequence is ours.
4. **Pages not read, so nothing is taken from them:** PHPat `project-guidelines.md`, `UPGRADE-0.10.md`,
   `CHANGELOG.md`; Deptrac `upgrade.md`, `bc_policy.md`, `blog`, `examples/`.

## Second pass, read 2026-10-20 (facts only, rewritten)

| Source | Licence | What it confirmed or corrected |
|---|---|---|
| PHPat repository (main): `src/Test/TestParser.php`, `src/Test/RuleValidator.php`, `src/Selector/ClassNamespace.php`, `src/Selector/Classname.php`, `src/Selector/Selector.php`, `extension.neon` | MIT (LICENSE read 2026-10-16, unchanged) | **Corrected part 3, point 2:** the name test is "starts with `test`", not `test_`; non-matching methods are skipped silently, incomplete rules throw. Regex flag behaviour and prefix matching, and the three configuration defaults, now read from code (the former own-guidance sentences) |
| Deptrac repository (main): `docs/concepts.md`, `docs/collectors.md`, `docs/configuration.md`, `docs/formatters.md`, `src/Contract/Config/Ruleset.php` | MIT (LICENCE.md read 2026-10-16, unchanged) | Default-deny ruleset and the uncovered-dependency options, `analyser.types` defaults (`class` and `use`) and the opt-in types, `skip_violations` and the baseline formatter, the composer collector statements. The `+` ruleset prefix of part 1, point 9 was **not found** in the documentation pages of the current main branch or in the `Ruleset` config class, so that point keeps its earlier reading at commit `66595d1` and is marked unconfirmed |

## Not verified
1. **Own guidance, flagged in the text:** loose-pattern pitfalls beyond the page's own sample (part 1, point 3),
   overlapping layers (point 2), the consequence of a class in no layer, of a missing analysis type and of a
   `+` prefix (points 7, 8, 9), one config per view (point 11), the review rule for baseline entries and
   regenerating only to remove (part 2, points 1 and 3), the effect of renaming a rule on its ignores (point
   6), the shared PHPStan baseline (point 7), unregistered and misnamed tests being silent (part 3, points 1
   and 2), the allow-list default for inner layers (point 4), the consequences of the two PHPat options
   (point 5), `final` on a shared rule (point 9).
2. **No tool was run.** Behaviours such as exit codes, failures on stale entries and regular-expression
   matching are the documentation's statements.
3. **Tool versions** were not compared with any project; the documentation at the commit shown may describe
   options that an older release lacks.
4. **PHPat selector documentation** shows `Selector::namespace` inside the combinator examples and
   `Selector::inNamespace` elsewhere; the block uses the latter and does not state which is current.

## Related blocks
`skills/no-catch-all-layer`, `skills/archi`, `skills/domain-modeling`, `skills/php-patterns`.
Overlaps with `skills/laravel-conventions` §9 and §10 (2026-10-19); cross-referenced, not merged.

Added 2026-10-20: the point about a misnamed rule being silent (part 3, point 2) is now sourced from the PHPat code, no
longer own guidance; the unregistered-class half stays own guidance because the registration happens through the PHPStan
container and no code of it was read. Overlapping layers, one config per view, review of baseline entries and the
`final` base rule remain own guidance (design judgement, no page states them).
