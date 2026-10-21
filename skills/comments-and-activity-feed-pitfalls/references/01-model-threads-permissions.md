# comments-and-activity-feed-pitfalls §1 — Model, threads and permissions

Source: own craft knowledge, with one vocabulary fact from the W3C Activity Streams 2.0 Vocabulary (tombstone, read 2026-10-20, see origin.md).

## 1.1 The model
1. **One comment table per kind of commentable, or one with a polymorphic target.** Polymorphic (target type, target id) is flexible but has no foreign key and no cascade; if you choose it, index the pair and check the target exists and the author may see it on every write (`laravel-no-cascade-delete`, `laravel-tenant-context-by-default`).
2. **Columns that earn their place**: id, target reference, parent id (nullable), author id, body in the stored format, visibility class, created time, edited time, deleted time, and a version for concurrent edits.
3. **Keep the tenant on the row** so a query by target alone cannot cross tenants.
4. **The author is a reference with a cached display name** only if the history must keep showing the old name; otherwise show the current one and a neutral label for a removed user.
5. **The body is in the editor's stored format** (`rich-text-editor-pitfalls` §1.1) with a plain projection for search, previews and notifications.
6. **Order by created time and id**, never by edited time, so an edit does not move a comment in the conversation.

## 1.2 Threading
1. **Choose a depth on purpose**: flat (one stream), one level of replies, or deep trees. Business records are usually well served by flat or one level; deep nesting makes narrow columns and lost context.
2. **Flat threads still need "in reply to"**, shown as a quoted snippet that links to the parent, so a reply is understandable out of order.
3. **Reply to the root, not the reply, when depth is one**: the interface rewrites the parent to the root and keeps the quoted snippet.
4. **Symptom: a reply remains under a deleted parent and shows "undefined" or disappears.** Decide: a deleted comment becomes a tombstone ("This comment was deleted") that keeps its place and children, and is purged only when it has no children and retention allows. Activity Streams 2.0 has the same object for the same job: a Tombstone stands for a content object that was deleted, can sit in a collection to show that something used to be at that position, and records the former type and the deletion time.
5. **Count what is visible**: the "12 comments" label and the thread count follow the same visibility filter as the list (§1.6); tombstones are not counted, or are counted in both places.
6. **Load children lazily with their own cursor** when a root has many replies, and show "view 8 more replies" with a count.
7. **Resolving threads** (anchored review comments) is a state on the root: resolved by whom and when, reopened by a new reply or an explicit action, and filtered with a control.

## 1.3 Edits and deletes
1. **Say that an edit happened.** Show "edited" with the time, and keep the previous versions where trust or compliance needs them (support conversations, approvals). Symptom: a dispute about what was written and nobody can tell.
2. **Limit who and how long.** The author edits within a stated window or while nobody has replied; later changes become a new comment. An administrator edit is marked as such.
3. **Edits carry a version**: send the loaded version and reject a stale save (`rich-text-editor-pitfalls` §2.2).
4. **Notifications on edit are narrow**: only newly added mentions notify; a typo fix notifies nobody (`in-app-notifications-pitfalls` §1.4).
5. **Delete is soft by default.** Mark deleted time and actor, clear or hide the body from readers, keep the row for the thread and the audit. A soft-deleted row needs a purge path (`laravel-pruning-fires-delete-events`).
6. **Hard delete is for erasure requests and abuse**, performed through a defined action that also removes derived copies: search index, notifications, mail digests, exports (`dsar-handling-pitfalls`, `search-index-sync-pitfalls`).
7. **Undo for a delete** (a short window with a visible control) is cheap and avoids support tickets.
8. **A deleted target takes its comments with it by an explicit rule**: archive, keep for audit or erase, never an accidental cascade.

## 1.4 Mentions and notifications
1. **Mentions are references to users** (`rich-text-editor-pitfalls` §2.1); the comment save extracts the set of ids from the stored tree, not from a text pattern.
2. **Notify only users who may open the target.** A mention of someone without access either grants nothing and warns the author, or offers to share, but never silently reveals the record.
3. **Notify participants by subscription**: author of the root, previous commenters, watchers. Let a user mute a thread; a mention overrides a thread mute unless the user muted mentions.
4. **One notification per user per comment**, even when they are mentioned and subscribed; collapse in the sender (`in-app-notifications-pitfalls` §1.4).
5. **Do not notify during import or backfill** of historic comments.
6. **Reply by mail is an input channel**: authenticate the sender, strip quoted history and signatures, and apply the same sanitiser and size limits (`customer-email-review-pitfalls` for the mail side).

## 1.5 Permissions
1. **Four separate rights**: read, write, edit own, delete own, plus moderator rights to hide or delete others'. Do not fold them into "can edit the record" (`laravel-permissions-not-roles`).
2. **Rights follow the target's access**: losing access to the record removes access to its comments, including the cached title in notifications and the feed.
3. **Check on the server, per comment, for every action.** Hiding a button is not a control; an id in a request must be re-authorised (`field-and-row-permission-ui-api-pitfalls`).
4. **Rate-limit and size-limit writes** and cap body length on the projection, so a loop or a paste cannot flood a thread.
5. **Attachments in comments follow the file upload rules** and inherit the comment's visibility class.

## 1.6 Visibility classes
1. **Internal notes and public replies on one record are a common need** (support, approvals, case work). Store the class on each comment: internal, shared with the customer, public.
2. **Filter in the query, not in the interface.** Symptom: an internal note visible in the customer portal API response because only the template hid it.
3. **Default to the safer class**, show the class as a visible label and a different background plus text (not colour alone), and confirm when a comment is about to cross from internal to external.
4. **Mentions, notifications and previews inherit the class**: an internal comment never produces a customer-facing mail, push or search snippet.
5. **Changing the class later is an audited action**, and promoting an internal note to public re-runs the sanitiser, mention and notification rules.
6. **Counts, exports and feed items obey the class** too; a count that includes internal notes tells a customer something.
7. **Check the cross-tenant case**: a user from another organisation on the same record sees only the classes intended for their role.

## 1.7 Moderation and abuse
1. **Report, hide and restore** are separate actions with actor and reason; a hidden comment keeps its place as a tombstone with the reason shown to moderators.
2. **Blocked users and spam** are handled at the write path (rate limit, link limit, duplicate detection), not by deleting afterwards.
3. **Keep moderator actions in the audit log** (§2.1) and show them in the feed to those entitled.
4. **Edit rights do not imply the right to see edit history**; decide and enforce both.
