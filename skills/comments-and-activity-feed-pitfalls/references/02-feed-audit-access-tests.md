# comments-and-activity-feed-pitfalls §2 — Feed, audit, access and tests

Source: own craft knowledge, except §2.2.8, §2.5.1, §2.5.8 and §2.5.9 to §2.5.11, which were checked against the W3C ARIA authoring practices feed pattern and the HTML Standard (see origin.md). Unmarked points stay unsourced.

## 2.1 Feed against audit log
1. **They answer different questions.** The feed is for people ("what happened on this invoice"), is filtered by role and can be summarised. The audit log is for accountability ("who changed what, when, from where"), is complete, append-only and read by few.
2. **Symptom: an event missing from the history, or a comment edit that left no trace.** Cause: the feed was built from the editable comment table and application code that remembers to write events. Record audit events at the write path in the same transaction as the change, and build the feed from them for system events.
3. **An audit record holds actor, action, target, before and after of the changed fields (not secrets), time, and request origin.** It never holds the plaintext of values that must not be logged (`telemetry-sensitive-data-pitfalls`).
4. **Append-only is enforced, not hoped for**: no update or delete path in the application, restricted database rights, and a retention job that is the only deleter. If tamper evidence matters, chain records or ship them to storage the application cannot rewrite.
5. **Do not use model listeners that miss bulk writes.** Raw updates, queued jobs and imports skip per-model hooks; record events in the service or command that does the change, not in a callback that may not fire (`laravel-no-observers`).
6. **Events carry stable codes, not rendered sentences.** Render "Ana changed the status from Open to Paid" at read time in the reader's locale, from the code and the old and new values (`i18n-message-format-pitfalls`). Symptom: history in the wrong language, or broken after a wording change.
7. **Store references and display fallbacks** so an event about a deleted user or record still reads ("a removed user").
8. **Group noisy system events**: ten field edits in one save are one event with a list; a status ping every minute is not an event at all.
9. **Keep personal data erasure compatible with audit**: pseudonymise the actor reference instead of deleting rows, and document which fields remain (`dsar-handling-pitfalls`).
10. **The feed reads the audit log, not the reverse.** A user-facing "hide this event" never removes the audit row.

## 2.2 Pagination and ordering
1. **Cursor-page by created time and id**, newest first or oldest first by product need, since new items arrive while reading and offset would repeat or skip rows (`data-table-ui-pitfalls` §1.2).
2. **Add a stable tiebreaker.** Events written in the same second need the id in the sort and in the cursor.
3. **Do not reorder under the pointer**: new items show as "3 new" and join on click; a thread being read keeps its place.
4. **Anchor to an item.** A notification links to a comment id; load the page that contains it and highlight it, then allow paging both ways.
5. **Load more on demand**, with a visible control and a keyboard path; infinite scroll alone hides the footer and the tail of the page from keyboard users and breaks "back to where I was".
6. **Filters on the feed**: all, comments only, events only, mine; the counts follow the same filter (`filters-search-and-saved-views-pitfalls`).
7. **Time display**: relative text ("2 hours ago") needs an absolute time on hover and focus, updates on a timer that does not re-render the list, and uses the reader's zone (`locale-value-formatting-pitfalls`).
8. **The total can be unknown**: show "load older" instead of counting a long history on every request. Confirmed by the feed pattern: an article carries its position and the set size, and the size is -1 when the total is unknown (APG feed).

## 2.3 Live updates
1. **Treat push as a hint**: a pushed comment is fetched or inserted, but the list can always be re-read, so a missed push does not hide a reply (`in-app-notifications-pitfalls` §2.1).
2. **Refetch on focus, reconnect and visibility change**, with the last seen id as the cursor to detect gaps.
3. **Insert only what the viewer may see**; check visibility class on the pushed item before rendering, not only on the initial list.
4. **Your own comment appears at once** (optimistic) with a pending state, replaced by the server item, and removed with an error and retry when it fails. Symptom: a duplicate after the push of your own comment arrives; deduplicate by id and a client token.
5. **Typing indicators are cosmetic** and optional; never block saving on them.
6. **Conflicts between edit and delete** are resolved by the server's version: an edit of a deleted comment fails with a clear message and keeps the user's text.

## 2.4 States
1. **Render separately**: loading, empty (no comments yet, with a prompt to write), empty-filtered, error with retry, offline, and partial (older page failed). Do not show "no comments" for a failed request (`data-table-ui-pitfalls` §2.1).
2. **Pending, sent, failed and edited are states of a comment**, each with a distinct text, not only a colour.
3. **A tombstone and a hidden comment render differently** to readers and to moderators.
4. **Long comments collapse** with "show more", on a node boundary, and keep a link to the full text.
5. **Drafts persist per thread** and survive navigation and reload (`long-and-multistep-form-pitfalls`), and clear on send.

## 2.5 Accessibility
1. **The thread is a list of articles.** Each comment has the author, time and class (internal, public) as text a screen reader hears before the body, not as an icon. Replies are nested lists, with the depth stated in text when it matters (`accessibility`). The feed pattern (APG feed) uses a feed container of articles, each named by its title or author line, and allows a feed inside an article for comments on a post; either shape is acceptable, pick one and keep the same one for every thread.
2. **The composer has a name** and a described error; send is a real button, available by keyboard, with the shortcut documented and disabled state explained (`rich-text-editor-pitfalls` §2.4).
3. **Announce your own send and failures** through one polite live region; do not announce every incoming comment loudly, batch them ("2 new comments") (`in-app-notifications-pitfalls` §2.3).
4. **Do not move focus on new comments.** After a send, focus returns to the composer or to the new comment by a stated rule; after a delete, it moves to the next item or the composer, never to the top of the page.
5. **Edit and delete controls are named** with the author and time ("Edit your comment from 10:42"), and a delete confirmation traps and restores focus.
6. **Action menus on each comment are keyboard reachable** and not shown on hover only, because touch and keyboard users have no hover.
7. **Edited and deleted markers are text**, not italic or grey alone.
8. **Relative time elements carry the machine time** so assistive technology and translation can read it. Use the `time` element with a valid `datetime` value; without the attribute its text must itself be a valid date or time and it can hold no child elements (HTML Standard).
9. **Symptom: a screen reader user hears half-loaded items, or never learns that older comments were added.** While several articles are added or removed in one update, mark the feed busy and set it back to not busy afterwards; forgetting the reset hides the changes from some assistive technology (APG feed).
10. **Give each comment its position and the set size** (unknown total: -1) when the list loads in pages, so a reader can tell where they are (APG feed).
11. **A feed has no standard keys**: document the keyboard path (next and previous comment, leave the feed). The pattern suggests Page Down and Page Up between articles and Ctrl+End or Ctrl+Home to exit; they are suggestions, not a convention (APG feed).

## 2.6 Retention and scale
1. **Say how long comments and events live** and prune by schedule; the audit log has its own longer period, set by the business, not by this block (`laravel-pruning-fires-delete-events`).
2. **Index (target, created time, id)** for the feed query and keep the visibility class in the same filter path.
3. **Counts are derived or cached with a rebuild**, as for notification counts (`in-app-notifications-pitfalls` §1.3).
4. **Large imports of historic comments run as jobs**, idempotent per source id, without notifications (`background-jobs-conventions`).
5. **Search over comments uses the plain projection** and applies the visibility filter at query time (`search-index-sync-pitfalls`).

## 2.7 Tests
1. **Thread integrity**: delete a parent with replies; assert a tombstone remains, children stay, counts are right, and a purge removes only childless tombstones.
2. **Edit and delete trace**: edit then delete a comment; assert the edited marker, the preserved history for the auditor, and an audit event with actor and time.
3. **Visibility**: as a customer role, request the thread by API and by feed; assert internal notes, their counts, mentions, previews and notifications are absent.
4. **Permission per action**: a user without delete rights sends a delete with a valid id; assert rejection. A user who lost access to the target gets not found on its comments.
5. **Mentions**: mention a user without access; assert no notification and a warning; edit to add one more mention; assert exactly one new notification.
6. **Feed paging**: create more than two pages of events with equal timestamps; assert page 1 plus page 2 equals the ordered whole with no duplicates, and that an anchored link lands on the right item.
7. **Audit completeness**: change a record through a form, a bulk update and an import; assert an audit event for each, and that none exposes a secret field.
8. **Live update**: drop a push, reconnect; assert the refetch fills the gap; assert your own comment does not appear twice.
9. **Accessibility**: assert author and time text per comment, a named composer, a live-region message after send without a focus move, and a keyboard-only pass through edit and delete.

## 2.8 Framework pointers (reference only)
1. **Laravel** back end: write audit events in the service that performs the change inside the transaction, query comments through a policy-scoped relation, and keep visibility in the query (`laravel-lomkit-rest-api`, `laravel-permissions-not-roles`, `laravel-no-observers`).
2. **React or Nuxt query layers**: key the thread by target and filter, merge pushed items by id, keep previous data while loading the next cursor (`data-fetching-state-conventions` §2).
3. **Rich text**: use the stored format and projection from `rich-text-editor-pitfalls`; a comment box is a small instance of the same editor, not a separate textarea with ad-hoc markup.
4. **Vuetify or similar kits** have timeline and list components; check their semantics (list roles, time elements, focus handling) against §2.5 instead of assuming them (`vue-nuxt-vuetify-conventions`).
