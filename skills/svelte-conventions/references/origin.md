# svelte-conventions — origin and source stamps

> Provenance of `skills/svelte-conventions`. Read it when a rule has to be traced back to its source or checked
> for freshness (`skills/source-freshness`), never to apply a rule.

**Written 2026-10-02, new block, never run on real work (🟡, base to confront with a real project).**

Sources, all primary, read on 2026-10-02 from shallow clones of the `sveltejs/svelte` repository (documentation
under `documentation/docs`, MIT licence; includes the framework's own `best-practices` page) and the
`sveltejs/kit` repository (documentation under `documentation/docs`, MIT licence), at **Svelte 5.57.1** and
**SvelteKit 3.0.0** (the latest releases on the package registry that day):

| Used for | Source |
|---|---|
| §1 | the rune pages (`$state`, `$derived`, `$effect`, `$props`, `$bindable`) and the best-practices page |
| §2 | the template-syntax pages (`each`, `snippet`, `@html`), the context page, the best-practices page |
| §3 | the SvelteKit pages on state management, `load`, form actions, page options, hooks, errors, environment variables, auth, performance, images and icons, the adapter-node page, and the migration guide to version 3 |
| §4 | the testing page |

What is ours: the numbering, the grouping, the mechanical checks, the phrasing. Rule 7 of §3 (every action is a
public endpoint to authenticate and validate) extends the framework's guidance on `locals` and remote-function
validation with the general rule of `skills/security-hardening`; it is not a sentence from those pages.
No text was copied.

**Facts that move, with their pin.**
- Svelte: `createContext` is 5.40+, derived reassignment is 5.25+, `createContext` with programmatic mounting is
  5.50+ (corrected 2026-10-20: this entry said 5.49+ for the context option of `mount`, which the changelog does not
  support), await expressions need an opt-in option and are experimental at 5.57.
- SvelteKit 3 (§3): configuration passed to the Vite plugin, `#lib` replaces `$lib`, `$app/env` replaces
  `$app/environment`, `$app/env/private` and `$app/env/public` replace the `$env/*` modules (deprecated, removal
  in Kit 4), `csrf.trustedOrigins` replaces `csrf.checkOrigin`, minimum Node 22.17, TypeScript 6, Vite 8.
- Remote functions are described in the pages read only where they touch errors, hooks and CSRF; they are not
  covered as a feature, a gap stated.

**Refresh protocol.** Re-read the migration guide of the next major and the best-practices page; give each
pinned fact above an explicit verdict (`skills/source-freshness` §3); stamp the date even if nothing changed.

**Not taken.** Community skill collections for Svelte (some Apache-2.0, one with 16 skills) were listed in the
sourcing notes and not read; none used. The framework's MCP server and its autofixer were not read (an external
tool, outside this block). The legacy-mode documentation was read only to name what is legacy.

## Re-verified 2026-10-20 (🟡, nothing run)

Re-opened on 2026-10-20 from the `sveltejs/svelte` repository (licence file read: MIT, "Svelte Contributors") and the
`sveltejs/kit` repository (licence file read: MIT), `documentation/docs`, main branch, plus the Svelte package
changelog. Latest releases that day: Svelte 5.57.2 and SvelteKit 3.1.0 (the pins above are one patch and one minor
behind; the pages read state nothing that contradicts a rule). Facts only, no text copied.

| Page read | Points confirmed |
|---|---|
| `$state`, `$derived`, `$effect`, `$props`, `$bindable` pages | §1.2 to §1.12 (destructuring, class fields, `$state.raw`, reactive built-ins, export of reassigned state, derived expression free of side effects, `$derived.by`, writable deriveds since 5.25, objects not made deeply reactive, effect only in the browser and in a microtask, untracked reads after `await`, teardown, `untrack`, props changing, ownership warning, bindable fallback rule) |
| best-practices page | §1.1, §1.8, §1.9, §1.11, §1.14, §2.1 to §2.7 |
| each, snippet, `{@html}`, context pages | §2.1 to §2.3, §2.8 (`createContext` from 5.40, reassignment breaks the link, mounted trees get their own context) |
| await-expressions page | §2.11 (experimental, opt-in option, flag removed in Svelte 6) |
| testing page | §4.1 to §4.4 (Vitest, `.svelte` in the file name for runes, `$effect.root`, jsdom shim) |
| Kit pages: load, form actions, page options, state management, environment variables, hooks, errors, adapter-node, performance, snapshots | §3.1 to §3.14 (shared server state, `handleError` kinds `app`, `framework`, `unknown`, prerender limits, `entries`, `'auto'`, `paths.origin` and the `host` header, `src/env.ts` with `defineEnvVars`, `$app/env/private`, snapshots for ephemeral state) |
| migration guide to Kit 3 | §3.8, §3.10, §3.15 (Node 22.17, TypeScript 6, Svelte 5.57.1, Vite 8.0.12, `svelte.config.js` no longer supported, `csrf.trustedOrigins` replaces `csrf.checkOrigin`, cross-origin requests without a content type rejected, `#lib`, `$app/env`, `use:enhance` navigation) |

**Corrected:** the version attached to the `mount` context option (above). **Not re-opened in this pass:** the remote
functions page beyond the CSRF and hook mentions, the auth and images pages behind §3.11 and §3.14, the form-actions
detail behind `use:enhance` and `fail` values, and the attachments reference behind §1.8; they keep their 2026-10-02
stamp.

Independent verification 2026-10-21: 23 checked, 23 matched, 0 corrected, 0 unverified
