# rich-text-editor-pitfalls §2 — Mentions, collaboration, access and tests

Sources: Lexical documentation (keyboard accessibility, collaboration FAQ; MIT, commit stamped in origin.md, read 2026-10-20) and the Yjs threat model (MIT, read 2026-10-20) for the facts marked as such; the rest is own craft.

## 2.1 Mentions
1. **A mention is a reference, not text.** Store the user id with the displayed name as a cache, so a rename updates it and a deleted user shows a neutral label. Symptom: "@Ana" stays after Ana became "Ana Martin", and a text match mentions the wrong Ana.
2. **Suggestions come from the server, scoped to who the author may see.** Do not load the whole directory into the page, and never suggest users from another tenant or a restricted group (`laravel-tenant-context-by-default`, `field-and-row-permission-ui-api-pitfalls`).
3. **Debounce the lookup, cancel the stale request and render states**: loading, no match, error. Keep the typed text when the request fails.
4. **The suggestion list is a combobox-style popup.** The editor keeps focus, the popup has a listbox role and an active option the editor points at, and arrow keys, Enter and Escape work. The Lexical documentation lists the same wiring for its typeahead menu: a listbox role on the popup and the editor root pointing at the active option while it is open.
5. **A mention triggers a notification only after the content is saved**, and only for users who may open the target; a draft never notifies (`in-app-notifications-pitfalls` §1, `comments-and-activity-feed-pitfalls` §1).
6. **Mentioning inside an edit notifies only the newly added people**, tracked by diffing the set of ids, otherwise each save repeats the alert.
7. **Escape the display name**; it is user data (§1.4).

## 2.2 Collaborative editing and its limits
1. **Decide whether you need it.** Real-time co-editing buys one thing, simultaneous editing of one document. A comment box, a ticket description or a form field rarely needs it; optimistic locking with a version number and a clear conflict message is far cheaper.
2. **For text edited by one person at a time, use versions.** Send the version you loaded, reject a stale save with the changed copy shown, and keep the user's text so they can merge it by hand.
3. **Shared-type merge models (CRDTs) guarantee that peers converge, not that content is valid.** The Yjs threat model says the protocol is designed for trusted peers and does not protect against a malicious peer who writes destructive operations, which then stay in the history.
4. **Never let an untrusted peer write to the authoritative document.** The same document recommends a separate fork for suggestion-only users, reviewed and merged by a trusted peer. Treat "can comment" and "can edit" as different roles from the start.
5. **Server-side filtering of the update stream is not a boundary.** The Yjs threat model calls it an antipattern: updates are binary operations and selective filtering is exploitable. Authenticate and authorise the peer at connect and on every role change, and close the socket when it is revoked.
6. **Limit update size and rate** at the server so one peer cannot exhaust memory with huge or deeply nested updates, as the same threat model lists.
7. **Decide the source of truth.** The Lexical collaboration FAQ gives two options: treat the shared model as the truth and store snapshots for indexing, or treat the database as the truth and let the server forget room content after a timeout, which means clients that stay offline too long lose their local edits. Pick one, write down the offline limit and tell the user when it is hit.
8. **Store a snapshot in your normal format** (§1.1) on a schedule and on close, so search, export, mail and a rollback do not need the shared model to be running.
9. **History and undo are per user**: one person's undo must not revert another's text. Check what the library does in shared mode and test it.
10. **Presence (cursors, names) is cosmetic**: validate any colour or name a client sends before rendering, since they are user input too.
11. **Plan for loss of connection**: show the state ("offline, changes kept locally"), do not claim saved, and show the conflict result after reconnect.

## 2.3 Read-only render and derived views
1. **Render saved content through the same code as the editor's own preview**, or through a renderer that implements the same node mapping, so the view and the edit agree.
2. **A read-only editor is not a viewer.** It loads the whole editor bundle for people who only read; prefer a light renderer for lists and long pages, and keep the editor for the edit action (`webperf`).
3. **Truncated previews cut at a node boundary** on the plain projection, never in the middle of a tag.
4. **Email and PDF output** use the sanitised HTML with inline-safe markup (`customer-email-review-pitfalls`), and are tested in those targets, not in the browser only.
5. **Printing and dark mode**: stored colours break on a dark background, which is another reason to drop inline colours (§1.3).

## 2.4 Accessibility
1. **The editing surface is a textbox, so it needs a name.** Associate a visible label with it, set the multi-line role where the library does not, and keep the description and error text linked (`accessibility`, `long-and-multistep-form-pitfalls`).
2. **Tab must leave the editor.** If Tab indents lists, document the key and give an Escape route that blurs the editor so the next Tab moves on. The Lexical documentation states the same contract: Tab follows normal focus order by default, and the indent behaviour is an opt-in that still needs Escape to release focus.
3. **The toolbar is one tab stop.** Arrow keys move between its buttons and Tab leaves it as a whole, with a documented shortcut to jump from editor to toolbar. The library documentation lists the same pattern for its toolbar.
4. **Toolbar buttons have names and pressed state** (`aria-pressed` for bold, a label for icon-only buttons). A colour swatch needs a text name, not a hex only.
5. **State changes are announced politely**: "link added", "bold on", character limit reached. Use one live region and avoid announcing on every keystroke (`in-app-notifications-pitfalls` §2.3).
6. **Formatting must survive without sight.** Headings are real headings, lists are real lists, links have descriptive text and images have alternative text; the editor should warn on an empty alternative.
7. **Modal pieces trap and restore focus**: the link dialog, the image dialog and the emoji picker return focus to the editor on close.
8. **Contrast and zoom**: toolbar and editor text meet the contrast rules and reflow at zoom without clipping the toolbar.
9. **Drag handles and block menus need a keyboard path**, since pointer-only block reordering excludes users.
10. **Spellcheck and language**: keep spellcheck on, set the document language, and mark passages in another language.

## 2.5 Behaviour users notice
1. **Autosave drafts** locally and tell the user, but do not overwrite a newer server version on restore (`long-and-multistep-form-pitfalls`).
2. **Warn before leaving with unsaved changes**, and clear the warning on save.
3. **Undo works after paste, formatting and mention insertion**; test the sequence.
4. **Do not lose the content on a failed save**; keep the editor state, show the error and retry.
5. **Mobile keyboards change selection and composition**: test with input method editors and dictation, since composition events are where editors break.
6. **Right-to-left text and mixed direction** need direction per block (`rtl-and-bidi-layout-pitfalls`).

## 2.6 Search and export
1. **Index the plain projection**, with mentions as the display name and ids kept as structured fields (`search-index-sync-pitfalls`).
2. **Export through the same sanitiser**, and for spreadsheet export prefix cells that start with formula characters (`csv-xlsx-import-export-pitfalls`).
3. **Personal data inside documents** is in scope of access, erasure and retention requests (`dsar-handling-pitfalls`).

## 2.7 Tests
1. **Hostile markup**: post each sample through the API, not the editor, and assert the rendered output has no script, handler or script URL.
2. **Round trip**: save, reload and save again; assert the stored tree is unchanged, and that a document of the previous format version migrates.
3. **Paste fixtures**: a word processor sample, a web page sample and plain text; assert allowed structure kept and foreign styles dropped.
4. **Limits**: assert the character count on the projection, and the server rejection of an oversized or deeply nested document.
5. **Mentions**: rename a user and assert the rendered name; mention a user outside the author's scope and assert it is not suggested or notified.
6. **Concurrency**: two stale saves of one version; assert the second gets the conflict response with the changed copy. For shared editing, a peer without the edit role cannot change the authoritative document.
7. **Keyboard and names**: Tab in and out of the editor, Escape from a dialog back to the editor, a toolbar with one tab stop, an accessible name on the field; run an automated check plus one manual pass.
8. **Server and client agree**: the same input yields the same sanitised output on both sides.

## 2.8 Framework pointers (reference only)
1. **Headless editors** (a document model plus your own markup) fit design systems and own the schema, paste rules and serialisation; start from one rather than a ready-made toolbar editor you cannot restyle. Declare the node list and the format version in one place.
2. **Laravel** back end: sanitise in a single service used by the write path and the render path, never in a model accessor scattered across views (`laravel-no-fat-models`, `csp-and-sanitiser-pitfalls`).
3. **Vue or React**: load the editor lazily, and keep the content in the form state as the stored format, not as markup strings concatenated by the component (`vue-nuxt-vuetify-conventions`, `react-nextjs-conventions`).
4. **Framework-level HTML directives** that render raw markup (`v-html`, `dangerouslySetInnerHTML`, `{!! !!}`) are allowed only on sanitiser output (`laravel-blade-view-pitfalls`).
