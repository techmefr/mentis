# prose-lint-gate-pitfalls §2 — Keeping the rules trustworthy

> Part 2 of `skills/prose-lint-gate-pitfalls`. Read it when the checks must stay trustworthy over time.
> Sources: the Elastic Vale rules repository and the Grafana writers' toolkit (Apache-2.0), the Vale packages
> index (MIT); each rewritten in our own words. Points marked own guidance are ours.

## 2.1 Pin what can change under you
1. **Naming a package installs its latest release**, so the rules can change when the package does. The
   packages index says to give the release address instead of the name when a new rule appearing on its own
   would be disruptive: shared repositories, and CI that fails on new alerts.
2. **A listing is not a promise about the future.** The same index says a package's address points at its latest
   release, so review shows what it checked when listed, not what it will check later.
3. **Pin the tool too** (own guidance, from two comments in Elastic's own files): its tests strip trailing
   whitespace because a recent release of the linter began including it in the reported match, and its
   configuration notes that a later release started linting fenced code blocks when code is listed among the
   skipped scopes. A tool upgrade changes what a rule matches without any rule changing.
4. **Sync the local copy when the rules change.** Grafana's setup says that after pulling the toolkit, each
   author must run the package sync again; otherwise their editor and CI apply different rules.
5. **Release the rules as versions.** Elastic publishes its rules as a tagged package, so a consumer can update
   by a sync and know which version it holds.

## 2.2 Local and global must not mix
1. **Run the rule tests against the local rules only.** Elastic's development notes say to pass a flag that
   ignores the global configuration, because otherwise the linter may load the globally installed copy of the
   rules instead of the one being edited.
2. **A rule that passes locally and fails in CI** (or the reverse) usually means two rule sets were in play
   (own guidance, a consequence).

## 2.3 A rule that stopped firing is detected by a planted violation
1. **Every rule has a fixture with a planted violation at an expected line**, and a test compares the reported
   matches with the expected line and text. Elastic's runner holds one entry per rule for a shared fixture file.
2. **The test fails when a rule has no assertion and when an assertion is left for a rule that no longer
   exists.** Both directions matter: the first leaves a rule untested, the second leaves a test proving
   nothing.
3. **Test the boundaries as well as the hit**: Elastic checks that fenced code and metadata stay unlinted, that
   inline code is masked and not dropped, and the edges of the first-person rule.
4. **Test after any tool or package upgrade** (own guidance), since a silent change in matching is exactly what
   the planted violation catches.

## 2.4 Cut false positives at the source
1. **Keep vocabulary files** for product names, third-party names and technical jargon, so the spelling rule
   does not flag them. Elastic keeps three such files and one for geographic names; Grafana generates part of
   its rules from a dictionary whose entries carry metadata (product, abbreviation, established abbreviation).
2. **Filter what is not prose**: code, flags, identifiers, file extensions, camel-case names and
   underscore-prefixed field names. Elastic does it with skipped and ignored scopes for code and with token
   patterns, and ships its experimental spelling rule switched off by default.
3. **Make adding a word cheap.** Grafana documents the steps to add a word, a product or an abbreviation to the
   dictionary, and offers an issue for anyone who cannot edit the template.
4. **Count false positives and fix the filter, not the author** (own guidance): a rule whose findings are
   mostly noise is the rule that gets disabled for everyone.
