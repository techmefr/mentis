---
name: cms-app-build-pitfalls
description: "Use when a content management system or editorial back office is designed or built: the minimal model of content type, entry, field, revision, status, media asset, taxonomy and locale, content model changes against existing entries, drafts and publishing with scheduling and unpublish, revisions and who changed what, media storage and derivatives, preview of unpublished content, localisation as linked variants, slugs and redirects, editorial roles and approval, and what gets regretted at v2. Method only; copyright and privacy law is not legal advice."
---

# cms-app-build-pitfalls

A defensive block for building the CMS, not for writing content or for building a site on an existing CMS. A CMS
built in a hurry fails in familiar ways: an editor changes a content type and 2,000 entries lose a field, a
draft is edited while the live page changes under it, a publish overwrites a colleague's work, a preview link
leaks unpublished text, a translated page points at a deleted original, and a renamed slug breaks every
inbound link. The content is mostly craft knowledge; some points are checked against the Payload documentation (see `references/origin.md`).
Rich text editing is in `skills/rich-text-editor-pitfalls`; files and storage in
`skills/document-file-management-pitfalls` and `skills/file-upload-ui-pitfalls`; admin screens in
`skills/admin-back-office-pitfalls`; search sync in `skills/search-index-sync-pitfalls`; translation workflow
in `skills/i18n-catalog-workflow-pitfalls`; the pipeline for a site built on a CMS is in
`skills/astro-images-templates-pitfalls`; roles in `skills/laravel-permissions-not-roles`; AI-generated content
in `business/ai-content-disclosure-and-provenance-pitfalls`.

## When
- A new CMS, headless content service, docs platform or marketing back office is specified or its schema drafted.
- An internal app grows editable pages, articles, a media library, translations or a publishing workflow.
- A feature touches content model changes, drafts, revisions, scheduling, preview or locales.

## Steps

**Read the part you need before the schema or the migration is written.**

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Minimal model and its pitfalls: content model changes, status and publishing, revisions, concurrent edits, media, slugs, locales | a schema or a write path is designed | [`01-model-and-pitfalls.md`](./references/01-model-and-pitfalls.md) |
| 2 | Preview, delivery and caching, roles and approval, search and integrations, what to split first, v2 regrets, framework pointers | preview, an API, permissions or the first release are planned | [`02-roles-integrations-and-v2.md`](./references/02-roles-integrations-and-v2.md) |

## Output / checkpoint
Before building: the content type list with fields, types and constraints; the status list with allowed
transitions and who may perform each; the revision and conflict policy; the media storage and derivative rule;
the slug and redirect rule; the locale model (fallback, linking, per-locale status); and the preview access
rule. Evidence is a test that a migration of a content type keeps existing entries readable, a test that
unpublishing removes the entry from the delivery API and the cache, a test that two editors saving the same
entry get a conflict instead of a silent overwrite, and a test that a draft is unreachable without a valid
preview token. Nothing here was run by us.

## Guardrails
- This block is not legal advice. Copyright of uploaded media, personal data in content and accessibility
  duties depend on the jurisdiction and the use; ask the owner of each.
- Never change a content type destructively in place: add, migrate, then remove in separate steps (§1, point 1).
- Never edit the live version directly: edit a draft and publish it (§1, point 2).
- Never save over a newer revision: compare a version token and report a conflict (§1, point 5).
- Never let a draft be served by the public delivery path (§2, point 1).
- Never change a slug without writing a redirect from the old one (§1, point 8).
- Never link a translation to its source only by a string: use a stable linking id (§1, point 9).
- Never serve uploaded files from a path that executes them (§1, point 7).

## Origin
Written from craft knowledge of building content management systems, then checked on 2026-10-20 against the Payload
documentation (MIT), credited in the origin file; no text was taken. See [`references/origin.md`](./references/origin.md). 🟡:
never run by us.
