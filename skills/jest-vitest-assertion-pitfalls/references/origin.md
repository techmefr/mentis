# jest-vitest-assertion-pitfalls: origin and source stamps

> Provenance of `skills/jest-vitest-assertion-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from lint-rule documentation and reading, never run by us. No test was executed and
nothing was installed while writing it. The Jest and Vitest documentation themselves were not read: every rule is
stated as the plugin pages state it, and version-bound facts carry the plugin version they come from.

## Sources (all re-read in full 2026-10-15, rewritten in our own words, no sample code copied)

| Source | Licence | What it gave |
|---|---|---|
| jest-community/eslint-plugin-jest, `docs/rules`: `valid-expect`, `valid-expect-in-promise`, `valid-expect-with-promise`, `expect-expect`, `no-conditional-expect`, `no-conditional-in-test`, `no-standalone-expect`, `no-focused-tests`, `no-disabled-tests`, `no-done-callback`, `no-identical-title`, `prefer-strict-equal`, `prefer-called-with`, `no-large-snapshots`, `no-interpolation-in-snapshots`, `no-mocks-import`, `no-export`, `no-alias-methods`, `no-deprecated-functions`, `no-unneeded-async-expect-function`, `require-to-throw-message`, `no-error-equal` (commit 0d0c459, 2026-10-12, plugin version 29.17.0 in `package.json`) | MIT (repository LICENSE file, re-checked) | The silent-failure rules, the thrown-error wrapper, snapshot size defaults, the Jest v30 alias note, the `genMockFromModule` removal |
| vitest-dev/eslint-plugin-vitest, `docs/rules`: `hoisted-apis-on-top`, `require-awaited-expect-poll`, `require-local-test-context-for-concurrent-snapshots`, `require-mock-type-parameters`, `prefer-vi-mocked`, `no-import-node-test`, `valid-expect`, `valid-expect-in-promise`, `no-conditional-tests`, `no-focused-tests`, `no-disabled-tests`, `expect-expect`, `no-mocks-import`, `prefer-expect-resolves` (commit 743f81f, 2026-10-11, plugin version 1.6.27 in `package.json`) | MIT (repository LICENSE file, re-checked) | The Vitest-only rules: hoisted calls, `expect.poll`, concurrent snapshots, typed mocks, `node:test` |
| goldbergyoni/javascript-testing-best-practices, `readme.md` sections 1.8 and 1.10 (commit 63a2bb0, 2023-08-08) | MIT (repository LICENSE file, re-checked) | Short inline snapshots and when long external ones are acceptable; expect the error instead of catching it |

The licence of each repository was verified again from its LICENSE file in this session.

## Rewrite notes
Each rule names the plugin whose page states it, because the two plugins differ: Vitest's `valid-expect` does not
check the `await` unless its `alwaysAwait` option is on, while Jest's does. The numbers that appear (50 lines, 3 to 7
lines) are the Jest plugin's default and Goldberg's suggestion, labelled as such.

**Decisions where sources disagree or are only preferences:** `toStrictEqual` everywhere against where a key
matters (§3.1.2); the project decides.

**Own guidance, not from a source:** the reason, owner and date on every `.skip` (§2.2.3), the inference about
`node:test` (§2.4.3), the inference about hoisted calls in a block (§3.4.1), the verification lines, and the
statement that a runner-level forbid-only switch for Jest and Vitest was not checked (§2.1.2).

## Removed from the review item
1. **Dropped by the review, not reintroduced:** the claim about what the Jest runner does with a value returned
   from a test, and the example built on the called-matcher alias. The `no-test-return-statement` page was not
   used, and the alias list is described only by its canonical names.
2. **Dropped as unverifiable from the pages read:**
   - "prefer `toStrictEqual` where undefined keys and class types matter": the page speaks of keys and structure;
     class types are not stated, so only keys are kept (§3.1).
   - "no `.skip` left without a reason": the Jest and Vitest pages do not ask for a reason; the reason, owner and date
     are own guidance (§2.2.3). The reason requirement comes from the Playwright plugin's page.
   - "duplicate test titles": kept for Jest only (`no-identical-title`); the Vitest page was not read.
   - "on CI, the runner's forbid-only mode": Playwright's exists (`forbidOnly`), a Jest or Vitest equivalent was not
     read, so the block says to check (§2.1.2).
   - "do not export from a test file", "never import from `__mocks__`": kept for Jest; the Vitest `no-mocks-import`
     page confirms the second one only.
   - "`vi.fn<Signature>()` and `vi.mocked()`": kept; the page also says the default type is `(...args: any[]) => any`.
   - "`expect.poll` must be awaited": kept from the Vitest page; "snapshot names carry no interpolation" is narrowed
     to what the Jest page says: no interpolation inside the snapshot body.

## Not verified
1. **The Jest and Vitest documentation** (matcher semantics, `resolves`, hoisting behaviour, `expect.poll`,
   concurrent snapshots, run options) was not read.
2. **Jest v30 alias removal and the `createMockFromModule` rename** are as `no-alias-methods` and
   `no-deprecated-functions` state them for plugin 29.17.0; the Jest release notes were not read.
3. **Plugin rules not read:** `max-expects`, `max-nested-describe`, `no-hooks`, `no-test-prefixes`,
   `no-restricted-matchers`, `prefer-expect-assertions`, the Vitest versions of `no-done-callback`,
   `no-identical-title`, `no-interpolation-in-snapshots` and `no-large-snapshots`, and the padding and ordering rules,
   which are taste.
4. **Vitest `expect.element`** is named on the `require-awaited-expect-poll` page; its provider (browser mode) was
   not read.

## Related blocks
`testing-anti-patterns`, `prisma-ops-and-test-hygiene`, `testing-library-query-pitfalls`,
`playwright-e2e-pitfalls`, `flaky-test-triage-pitfalls`, `tdd`.
