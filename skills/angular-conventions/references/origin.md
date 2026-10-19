# angular-conventions — origin and source stamps

> Provenance of `skills/angular-conventions`. Read it when a rule has to be traced back to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Written 2026-10-02, new block, never run on real work (🟡, base to confront with a real project).**

Sources, all primary, read in full or in the relevant sections on 2026-10-02 from a shallow clone of the
`angular/angular` repository (documentation under `adev/src/content`, MIT licence; repository `AGENTS.md`
read the same day) and from the published site (angular.dev), at **Angular 22.2.1** (the latest release on
the package registry that day):

| Used for | Source |
|---|---|
| §1, §2.5-2.8, §2.12, §1.10-1.11 | the official style guide (`best-practices/style-guide`) |
| §2 (standalone, inputs, control flow, images), §3.4, §3.10 | the framework's machine-readable best-practice file served from angular.dev, plus the component, input, host-element and control-flow guides |
| §3 | the signals, `linkedSignal`, `effect` and `resource` guides; the forms comparison page |
| §4 | the DI, injection-context, services, interceptors, route-guards, loading-strategies and data-resolver guides |
| §5 | the error-handling best practice, the `@boundary` guide, the security guide, the runtime-performance pages (subtrees, zone pollution, slow computations), the zoneless guide, the `@defer` guide, the accessibility page |
| §6 | the unit-testing overview, the HTTP testing guide, the routing testing guide, the zoneless testing section, the component-harness overview, the repository's own `AGENTS.md` testing rules (act, wait, assert) |

What is ours: the numbering, the grouping into six sections, the mechanical-check commands, and the phrasing of
every rule. The facts (defaults, names of APIs, which version changed what) are the framework's. No text was
copied.

**Facts that move, with their pin.** These are the rules most likely to be wrong against another major; the
dated pin is the version in which the documentation read states them.

- `OnPush` is the default strategy: **v22** (§2, §5.15).
- Zoneless is the default: **v21**; `provideZonelessChangeDetection` is for v20 (§5.16).
- `standalone: true` is the default: **v20+** (§2.1).
- Signal Forms are stable: **v22** (§3.10). `@boundary` and `@error` are in developer preview at the pinned
  version (§5.5). The `@Service` decorator is documented at the pinned version (§4.2); a project that cannot
  use it keeps `@Injectable({providedIn: 'root'})`.
- The default test runner for a new CLI project is Vitest (§6.2); Karma is documented only as a migration source.

**Refresh protocol.** Fetch the documentation for the project's major (or read the copy shipped with the
package if the version provides one), then give each fact above and each rule an explicit verdict
(`skills/source-freshness` §3). Stamp the date even when nothing changed, and record whether the stamp is a
verification or an edit.

**Not taken.** The repository's own contributor rules (Bazel, commit format) concern the framework's
development, not applications. Community Angular rule collections without a licence were not read (idea only,
none used). Angular Material, the CDK and SSR hydration details beyond the points above were not read and are
not covered: a gap, stated.
