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
| §2.18 (output and input naming) | the angular-eslint rule documentation for the native-output, `on`-prefix and input-rename rules, MIT (holder James Henry), read 2026-10-19 |
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

**Added 2026-10-19 (🟡):** §2.18 from the angular-eslint documentation above. The rule configuration (the input-rename allow-list) was not taken; nothing was run.

## Re-verified 2026-10-20 (🟡, nothing run)

Re-opened on 2026-10-20 from the `angular/angular` repository, `main` branch (licence file read: **MIT**, "Copyright
(c) 2010-2026 Google LLC"), pages under `adev/src/content` plus the root changelog, and from the `angular-eslint`
repository (licence file read: **MIT**, James Henry). Facts only, no text copied.

| Page read | Points confirmed |
|---|---|
| style guide | §1.1 to §1.8, §1.10, §1.11 (consistency first, hyphens, same stem and `.spec`, no `helpers`/`utils`/`common`, `src` and `main.ts`, feature grouping and no `components/` folders, one concept per file, selector prefix and camelCase attribute, `protected` and `readonly`, event handler naming, lifecycle methods and interfaces), §2.6 to §2.7 |
| best-practice file served by the docs site | §2.1 (standalone is the default from v20+, as that file states) |
| inputs page, host elements page | §2.2, §2.3 (transforms pure and static, `booleanAttribute` reads `"false"`, `model()` takes no transform, aliases), §2.8 (the three precedence rules) |
| control-flow page | §2.9 to §2.11 (`track`, `$index`, identity as last resort, no `break` or `continue`, `@empty`, `@default never;`) |
| signals pages (`linkedSignal`, `effect`), resource page, `httpResource` page | §3.2, §3.3 (async and at-least-once, storage and analytics uses), §3.5 to §3.9 (params undefined gives idle, `stream`, `abortSignal`, the six statuses, `chain()` and its statuses, `id` and transfer state with the user-data warning, interceptors apply) |
| forms comparison page | §3.10 (Signal Forms stable from v22) |
| framework changelog, 17.0.0 | §3.4 (`mutate` removed) |
| services page | §4.2 (`@Service`, `autoProvided`) |
| route guards page | §4.11 (never the sole access control) |
| security guide | §5.7 to §5.14 (CSP nonce, `ngCspNonce`, `CSP_NONCE`, CDN caching of nonces, edge generation, `autoCsp`, bypass functions, `allowedHosts`, `trustProxyHeaders`) |
| SSR page | §5.13 (`allowedHosts` in `angular.json`) |
| error-handling page, error-boundaries page | §5.1 to §5.6 (`ErrorHandler`, global listeners provider, `resource` errors, root component creation, `@boundary` in developer preview) |
| zoneless page, skipping-subtrees page | §5.15, §5.16 (zoneless default from v21 and `provideZonelessChangeDetection` for v20, `NgZone` observables to remove, `setInput`, `PendingTasks`, `OnPush` default since v22) |
| defer page, accessibility page | §5.19 (standalone only, `idle` default, barrel files defeat chunks), §5.22, §5.23 (`NavigationEnd`, `ariaCurrentWhenActive`, live region around `@defer`) |
| angular-eslint rule pages `no-output-native`, `no-output-on-prefix`, `no-input-rename` | §2.18 |

Nothing was found wrong in the rules checked. **Not re-opened in this pass:** the unit-testing pages behind §6, the
HTTP testing guide, the data-resolver and loading-strategies pages behind §4.9 and §4.13, the `NG0203` error page
behind §4.1, and the image-directive page behind §2.15; they keep their 2026-10-02 stamp.

Independent verification 2026-10-21: 29 checked, 29 matched, 0 corrected, 0 unverified
