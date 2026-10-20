# cms-app-build-pitfalls §2 — Preview, delivery, roles and v2

> Part 2 of `skills/cms-app-build-pitfalls`. Read it when preview, an API, permissions or the first release are
> planned. Mostly craft knowledge; point 1 carries facts from the Payload documentation in `references/origin.md` (source 1), read 2026-10-20. Everything not marked as sourced is our own guidance.

1. **Preview and delivery are different paths.** Symptom: a draft appears on the public API, a preview link
   found in a chat shows unpublished text to anyone, or a preview renders with stale cached content. Fix: the
   public delivery path reads only published snapshots; preview goes through a separate route that requires a
   signed, expiring, entry-scoped token or a signed-in editor, sends no-index and no-store headers, bypasses
   caches, and shows a visible "preview" banner. Check: request a draft without the token on every public
   route, including the API, the feed, the sitemap and the search index. The Payload documentation shows why the check on the API matters: a read with its draft flag returns the newest version whether or not it was published, so public access rules must refuse drafts, and its live preview renders the front end in a frame inside the admin and exchanges messages with it (source 1).
2. **Unpublish and update must reach every copy.** Symptom: an entry pulled for a legal reason is still served
   from a CDN, a feed, a search index or a static build for hours. Fix: a publish event that triggers purge or
   rebuild of each derived copy (cache tags by entry id, search sync, feed, sitemap), an unpublish that does the
   same and is tested end to end, and a list of those copies written in the project. See
   `skills/search-index-sync-pitfalls`, `skills/laravel-cache`.
3. **Roles are abilities per type and per locale.** Typical shape: an author writes and submits, an editor
   reviews and publishes, an admin changes the content model, a translator edits one locale. Symptom: an author
   publishes unreviewed content because the check lives in the button, or an editor of one site edits
   another's. Fix: abilities (create, edit-own, edit-any, submit, publish, unpublish, change-model, manage-media)
   scoped by content type, locale and site, enforced in the write path and the API, not only the UI (see
   `skills/laravel-permissions-not-roles`, `skills/laravel-tenant-context-by-default`).
4. **Approval is a status with a recorded decision.** A review state between draft and published, the reviewer,
   the time, the note, and the revision approved. Symptom: content edited after approval goes live
   unreviewed. Fix: approval binds to a revision; a later edit resets it; publish requires an approval on the
   exact revision where the policy demands.
5. **Rich text is data, stored in a defined format and sanitised.** Store a structured document or a sanitised
   subset, not arbitrary HTML pasted from an editor; sanitise on output as well; keep embeds on an allowlist.
   See `skills/rich-text-editor-pitfalls`.
6. **The delivery API is a contract.** Version it, return only published content and the fields requested,
   paginate with a stable order, expose the locale and the revision or updated time for caching, and keep
   a content type's published shape stable across model changes (§1 point 1). Symptom: a front end breaks when
   an editor renames a field. Fix: delivery names come from a mapping that the model change updates
   deliberately, with a deprecation period.
7. **Search and navigation are derived.** Menus, related links and search results come from the content, with
   a rebuild path and a check for links to unpublished or deleted entries. Symptom: a menu entry leads to a
   404 after unpublish. Fix: references by entry id resolved at delivery, with a defined behaviour for a
   missing target.
8. **Import and migration are staged.** Moving content from another system maps types and fields, keeps source
   ids for idempotent reruns, preserves dates and authors where allowed, rewrites internal links and media
   references, creates redirects, and reports a count per outcome. Test on a sample before the full run.
9. **Accessibility is enforced at the editor, not hoped for.** Required alt text or an explicit decorative
   flag, heading-level checks, link-text hints, table header hints, and a warning before publish. See
   `skills/a11y-hiding-and-tables-pitfalls`.
10. **What to split first.** Content types and entries with drafts and publish; revisions with conflict checks;
    media assets; slugs with redirects; roles and approval; preview; scheduling; locales; then import and
    integrations. Ship the first four before roles are refined.
11. **What is regretted at v2.** Editing the live version; fields changed in place; HTML pasted as the body;
    file paths in text; no redirect table; translations linked by title; preview served by the public path; no
    revision author; permissions checked only in the UI; scheduled posts as a date column. Each is cheap at the
    first migration and expensive once there is content.
12. **Laravel and Nuxt pointers, short.** In Laravel: an immutable revision table with a live pointer, a state
    enumeration with a transition action, an optimistic-lock column checked on update, a scheduled command with
    an action row, signed temporary URLs for preview, cache tags per entry, a media library table with usage
    rows. In Nuxt: fetch delivery content with the locale and a cache key from the revision, render preview
    with the token and no caching, and never expose draft endpoints to the public client.
