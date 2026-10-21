# dart-pub-workspace-and-publish-pitfalls: origin and source stamps

> Provenance of `skills/dart-pub-workspace-and-publish-pitfalls`. Read it when a rule has to be traced to its
> source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and reading, never run by us. No workspace was created and nothing was
published while writing it. Overlaps with `skills/flutter-conventions` (2026-10-19); cross-referenced, not merged.

## Sources (all read 2026-10-16, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| dart-lang/site-www (commit 85d6c72): `src/content/tools/pub/workspaces.md` | CC BY 4.0 prose, BSD-3-Clause code (LICENSE re-read); credit: the Dart authors | Part 1 rules |
| dart-lang/site-www: `tools/pub/automated-publishing.md` (GitHub Actions sections and the start of the cloud section) | same | Part 2.1 to 2.3 |
| dart-lang/site-www: `tools/pub/publishing.md` (dry-run and retraction passages) | same | Part 2.4 |
| dart-lang/site-www: `tools/pub/security-advisories.md` | same | Part 2.5 |
| Melos (commit fb8b35b): `docs/getting-started.mdx` (first sections) | Apache-2.0 (LICENSE re-read) | Part 1.5 |

### Second pass, re-read 2026-10-20 (pages of the main branch, facts only)

| Source | Licence | What it confirmed |
|---|---|---|
| dart-lang/site-www (main): `workspaces.md`, `automated-publishing.md`, `publishing.md`, `security-advisories.md` | CC BY 4.0 prose, BSD-3-Clause code (the repository licence notice read again); credit: the Dart authors | Workspace support from Dart 3.6.0 and the `^3.6.0` member constraint, glob entries from 3.11, nested workspaces, stray lock and package-configuration files deleted and a stray pubspec failing the get, overrides respected once per workspace, tag-triggered publishing only, tag pattern with the version placeholder, first version published by hand, exported keys as the long-lived fallback, `id-token: write`, reusable workflow strongly encouraged and generated code preferably checked in, required environment, audit log entry, `.pubignore` and `--dry-run`, retraction within seven days and restoration within seven days, advisories read from the GitHub database and `ignored_advisories` affecting the root only |
| Melos documentation (main): `docs/getting-started.mdx` | Apache-2.0 (LICENSE read) | Reading the workspace guide first, Melos as a dev dependency of the root pubspec, no application in the root, `useRootAsPackage`, glob support from Dart 3.11.0 |

No statement of §1 or §2 needed correction. Points not re-opened in this pass: the Google Cloud Build sections after the
service-account step (still not read) and the exact wording of the admin-tab labels.

## Removed in the verification pass (no page supporting them)
- "Apps run from their own folder" and "one analyzer context" as workspace rules from an agent-rules repository
  (MIT): that repository was not opened; the analyzer-context point is kept only as the Dart page's statement.
- Melos script, versioning and release features: the review noted "not read"; still not read, so only the setup
  points on the getting-started page are used.
- The Google Cloud Build publishing sections after the service-account creation step: not read in full.
- Public-API doc-comment requirements for published packages and their conflict with a no-comments house rule:
  stated by the review, no page read here supports it; dropped, listed as not done.

## Not verified
1. **Own guidance:** none flagged.
2. **SDK minimums** (3.6 for workspaces, 3.11 for glob entries) and the seven-day retraction windows are the
   pages' statements for the commit read; they change.
3. **The reusable publish workflow's version tag and the checkout and setup action versions** in the page were not
   used or checked.
4. **The exact admin-tab labels** were not checked on the live site.
5. **Prose is CC BY 4.0, rewritten here**; no sentence is copied.
6. **Other CI hosts** than GitHub Actions and the cloud build service are not covered.

## Related blocks
`flutter-conventions`, `ci-workflow-hardening`, `flutter-release-toolchain-hygiene`.

Independent verification 2026-10-21: 15 checked, 15 matched, 0 corrected, 0 unverified
