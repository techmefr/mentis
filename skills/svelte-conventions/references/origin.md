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
- Svelte: `createContext` is 5.40+, derived reassignment is 5.25+, the context option of `mount` is 5.49+,
  await expressions need an opt-in option and are experimental at 5.57.
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
