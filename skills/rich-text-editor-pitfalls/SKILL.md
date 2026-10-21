---
name: rich-text-editor-pitfalls
description: "Use when a rich text (WYSIWYG) editor is added or reviewed in a business application, whatever the library: choosing the storage format (HTML, structured JSON, Markdown), sanitising stored and pasted HTML, paste from Word and the web, links and images, mentions, character and size limits, collaborative editing limits and who may write, read-only rendering, and editor accessibility (labels, keyboard exit, toolbar, announcements), plus the tests that catch them."
---

# rich-text-editor-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for the field that turns a text box into a document. The premise: **a rich text
field stores markup written by a user, and markup is code**: it is rendered to other users, pasted from documents full
of foreign styles, searched, exported, diffed and edited twice at once. Each defect is a stored script, a paste that
brings a mess, a keyboard that cannot leave the editor or two people overwriting each other. The sanitiser itself and
the content security policy are in `csp-and-sanitiser-pitfalls`; general widget accessibility is in `accessibility`;
mentions in comments and the thread around them are in `comments-and-activity-feed-pitfalls`; file upload for images
is covered by its own block; form behaviour (drafts, leave guards) is in `long-and-multistep-form-pitfalls`.

## When
- A rich text field is added to a form, a comment box, a note, an email template or a knowledge page.
- Stored content is rendered for other users, exported, searched or compared.
- A user reports "my formatting is lost", "paste is a mess", "I cannot tab out", "my edit disappeared".

## Steps

**Read the section the task meets.** Each ends with checks.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Storage format choice, sanitising on write and on render, paste and import, links, images, limits | the field is designed, its stored format changes, or HTML enters the system | [`01-format-sanitising-paste.md`](./references/01-format-sanitising-paste.md) |
| 2 | Mentions, collaborative editing and its trust limits, read-only render, accessibility, search and export, tests, framework pointers | mentions, concurrent editing, accessibility or tests are written | [`02-collab-access-tests.md`](./references/02-collab-access-tests.md) |

## Output / checkpoint
A change is done when: the storage format is chosen on purpose and versioned; HTML is sanitised where it is rendered
and the same code runs on server and client when both write it; paste is normalised through a defined allow-list; the
editor can be left with the keyboard and has a name; and the tests in §2.7 exist. No checkpoint is written: a craft
block, 🟡, nothing here was run in an application.

## Guardrails
- Sanitise with an allow-list at the point of render and treat client sanitising as a convenience (§1.3). Never trust markup because "only our editor writes it".
- Store a format you can migrate and say its version (§1.1). Never store whatever the editor's output happens to be without a schema.
- Run paste through the editor's schema, drop foreign styles and keep a plain-text path (§1.5). Never insert pasted HTML as it came.
- Let only trusted, authenticated users write to a shared document (§2.2). Never filter a collaborative update stream on the server and call it safe.
- Give the editor an accessible name and a keyboard exit (§2.4). Never trap Tab in it without an Escape route.
- Facts about a library are for the commit stamped in `references/origin.md`; re-read before relying.

## Origin
Own craft knowledge, with editor, serialisation, accessibility and collaboration facts re-read in the Lexical documentation
and the Yjs threat model (both MIT, read 2026-10-20). A third pass re-read the DOMPurify documentation (Apache-2.0), HTML link types, WCAG 1.1.1 and UI Events composition (facts only, credited). Details in [`references/origin.md`](./references/origin.md).
