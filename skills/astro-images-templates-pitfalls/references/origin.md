# astro-images-templates-pitfalls: origin and source stamps

> Provenance of `skills/astro-images-templates-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and reading, never run on a real site by us. No Astro project was
built while writing it.

**Merge intent.** A broader Astro conventions block exists only on the unmerged branch of the frontend sourcing
pull request (118). This block was written standalone, with a name that cannot collide, to hold the gaps found
in a comparison against it. It is meant to be merged into the same-named framework block when that pull request
lands, section by section, and then removed.

## Sources (all read 2026-10-08, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| The official Astro documentation: images guide, the assets module reference, the directives reference, the client-side scripts guide, the view transitions guide, the configuration reference, the CLI reference, the version-6 upgrade guide | official docs, read 2026-10-08 | §1 (where files live, dimensions, `inferSize`, the priority prop, defaults), §2 (class:list, script processing, ClientRouter and page-load event, `site`, `astro check`, the `ViewTransitions` removal) |
| One MIT Astro lint tool: its rule explanations and skill files | MIT, read 2026-10-08 | The rule set the review listed (image component, dimensions, deferred scripts, class:list, client-router lifecycle), the eager and high-priority recipe, the `PUBLIC_` and `set:html` warnings |
| One MIT generic Astro skill set | MIT, read 2026-10-08 (not phrased from) | Confirmed topics only |

A third MIT collection of search-engine skills for Astro was read for the review's last item and used for
nothing, see below.

## Rewrite notes
Rules are re-explained principle first. The official documentation was read through a summarising fetch tool,
so wording was not copied. The verification lists are ours.

## Not verified
1. **Script attribute rule.** The documentation read says a script with any attribute other than `src` is not
   processed. That a processed module script does not block parsing is general web behaviour, not an Astro
   statement, and was not checked in the Astro output.
2. **Priority prop availability by version.** It is in the current reference; which release introduced it was
   not checked, so the block names the manual fallback.
3. **Default WebP output** is from the MIT lint tool's skill file, not from the official page read.
4. **`inferSize` build-time reachability** is stated as a precaution; the official page only says it infers
   dimensions when the image is fetched.
5. **Nothing here was run.**
6. **Dropped from the review's list:** the Astro 6 upgrade section (the registry showed the stable tag on a
   7.x release, so a 6.x breakpoint list targets the wrong major; only the `ViewTransitions` to `ClientRouter`
   rename is kept, and both the official guide and the lint tool agree on it), and the Astro SEO gating
   item (IndexNow only on the production host, `lastmod` from git, `llms.txt`): its source is the
   documentation of one vendor's package, with no official Astro statement behind it, and part of the topic is
   policy that belongs to `seo`.
7. **Written by us, not sourced:** the verification lists and the output/checkpoint paragraph of `SKILL.md`.

## Related blocks
`webperf`, `seo`, `accessibility`, `security-hardening`.
