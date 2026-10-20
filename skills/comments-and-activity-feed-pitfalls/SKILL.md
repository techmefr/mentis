---
name: comments-and-activity-feed-pitfalls
description: "Use when comments, replies or an activity feed (history, timeline, audit trail) are added to a record in a business application, whatever the framework: threading depth, edits and deletes that keep the thread coherent, mentions and notifications, who may read, write, edit and delete, system events against human comments, audit integrity, pagination and live updates, and accessibility of the thread, plus the tests that catch them."
---

# comments-and-activity-feed-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for the conversation and the history attached to a record. The premise: **a
comment thread is shared memory, and the activity feed is the account of what happened**; defects are a reply under a
deleted parent, an edit nobody can see was made, a private note shown to the customer, a feed that cannot be paged or
that disagrees with the audit log, a mention that leaks a title. The editor inside the comment box is in
`rich-text-editor-pitfalls`; the notifications a comment triggers are in `in-app-notifications-pitfalls`; row and field
visibility rules are in `field-and-row-permission-ui-api-pitfalls`; list mechanics (paging, states) follow
`data-table-ui-pitfalls`.

## When
- A comment box, a reply thread, a notes panel or a record timeline is built or reviewed.
- A user reports "my reply vanished", "I cannot tell what was edited", "the customer saw an internal note", "the history is missing events".
- Moderation, retention, mentions or system events are added to an existing feed.

## Steps

**Read the section the task meets.** Each ends with checks.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Data model, threading, edit and delete semantics, mentions, visibility classes, permissions, moderation | the comment table, thread shape or permission rules are written | [`01-model-threads-permissions.md`](./references/01-model-threads-permissions.md) |
| 2 | Activity feed and audit separation, pagination, live updates, states, accessibility, retention, tests, framework pointers | the timeline, its paging or its tests are written | [`02-feed-audit-access-tests.md`](./references/02-feed-audit-access-tests.md) |

## Output / checkpoint
A change is done when: threads have a defined depth and a rule for deleted parents; edits and deletes are visible as
such and recorded; visibility (internal against public) is a stored class enforced by the query, not the interface;
the feed is cursor-paged and distinguishes human comments from system events; and the tests in §2.7 exist. No
checkpoint is written: a craft block, 🟡, nothing here was run in an application.

## Guardrails
- Pick a thread depth and say what happens to children of a deleted parent (§1.2). Never delete a parent row and leave its replies orphaned.
- Store the visibility class on each comment and filter in the query (§1.6). Never hide internal notes with a CSS class or a client filter.
- Show that a comment was edited or deleted and keep the history for those who must audit (§1.3). Never rewrite a comment silently.
- Keep the audit log apart from the feed that people read (§2.1). Never use the editable comment table as the audit record.
- Page the feed by cursor and do not reorder what the reader is looking at (§2.2). Never load the whole history.
- Facts about a library are for the date stamped in `references/origin.md`; re-read before relying. Points without a credit in the reference files remain own guidance.

## Origin
Mostly own craft knowledge: no permissive source on comment systems was found. Only the feed and thread accessibility points (§2.2.8, §2.5) and the time element (§2.5.8) were checked, against the W3C ARIA authoring practices feed pattern (facts only, credited) and the HTML Standard (CC BY 4.0), read 2026-10-20. Details in
[`references/origin.md`](./references/origin.md).
