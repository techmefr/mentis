# firebase-rules-and-client-trust-pitfalls §1 — Rules that actually restrict

Source: official platform documentation (page footers state CC BY 4.0 for text, Apache-2.0 for code samples) read 2026-10-20, rewritten (query rules, rules conditions, real-time database security, rules basics, rules unit tests, anonymous sign-in); the rest is own guidance. Rule syntax and limits are the platform's; re-read before relying on a name.

## 1.1 Open rules
1. **A project created in a development or test mode starts with rules that let anyone in.** The expiry that people report for that mode (after which access stops, and the usual "fix" is to extend the date or allow everything) was not stated on any page read, so treat it as unverified. Replace the rules before the first real user, not on the day the app breaks. Checked: the rules basics page says locked mode (deny all) is the default for new instances of the three products, test mode lets anyone in, and the rules must be updated before production because a deployed app is publicly reachable even before launch; the document-database page's sample allow-all rules carry a never-in-production warning.
2. **Search the rules for a blanket allow** (a rule that is true for any path and any operation), and for a match-all path at the top level that grants more than the specific rules beneath it.
3. **Each product has its own rules file:** the document database, the real-time database and file storage are separate. Securing one and forgetting another is common; list all of them.
4. **Default to deny.** Add an allow only for a path you can name and a caller you can describe.

## 1.2 Signed in is not allowed
1. **A rule that only checks that the caller is signed in lets any user read and write any document** (the rules basics page calls this a development option, not a production setting). Combine it with an ownership test on the data (the caller's user id equals the owner field, or the path segment holding the user id).
2. **Anonymous sign-in counts as signed in (our reading).** The anonymous sign-in page says such accounts exist so that people can work with data your rules protect, but it does not state how a bare signed-in check treats them. If anonymous authentication is enabled, assume such a rule admits anyone who opens the app, and test it. Check the sign-in method as well as the rule.
3. **Ownership on create must test the incoming data,** since the document does not exist yet: the owner field in the new data must be the caller. Otherwise a user can create a document owned by someone else.
4. **Role checks read the role from a trusted place** (§2.3), not from a field in the document the caller writes.
5. **Sharing needs an explicit structure:** a members list or a subcollection that the rule reads, not a wide allow.

## 1.3 Rules are not filters
1. **A query succeeds only if the rules would allow every document it could return.** A client that asks for "all documents" fails even if only some are readable; a rule cannot filter results. Write the query with the same condition as the rule (the owner equals the caller). Confirmed: queries are all or nothing, rules are checked against what the query could return, and rules can also constrain query properties such as the limit and the order (document-database query-rules page, read 2026-10-20).
2. **When a query fails with a permission error while a single read works,** the query is broader than the rule; fix the query or the data model, not the rule. A fetch by identifier is the exception the query-rules page notes: rules are evaluated against the actual document there, not a potential result set.
3. **A query with an `or`, `in` or `array-contains-any` condition needs each value to satisfy the rule on its own** (query-rules page): a rule requiring a field above five rejects a query whose list holds one smaller value. A collection-group query needs rules version 2 and a recursive wildcard rule for that collection name, or it is denied however the single-collection rules read.
4. **A rule that looks up other documents costs a read each time and has limits on how many it may do per request** (Firestore rules conditions page, re-read 2026-10-20: 10 lookup calls for a single-document or query request and 20 for multi-document reads, transactions and batched writes; going over returns a permission-denied error, cached lookups do not count, and the calls are billed even when the rules reject the request); design the data so the check needs few lookups, and denormalize the role or the owner into the document when appropriate.
5. **Do not use rules as the only guard for what the query reveals (own guidance):** counts, existence and error messages can leak that a document exists.

## 1.4 Cascade and operations
1. **In some products an allow at a parent path grants everything below it, and a child rule cannot take it back** (the real-time database works this way; confirmed again: a shallower read or write rule overrides a deeper one, so a child rule cannot revoke it, real-time database security page, re-read 2026-10-20); in others rules at different paths are independent (not re-checked). Know which product you are on. The same page says validation rules do not cascade and run only for non-null values, so a validation rule never blocks a delete and every relevant one must pass for a write.
2. **A single "write" permission covers create, update and delete.** Split by operation: creation has a different test (§1.2.3) from update (the owner is unchanged) and delete (an owner or administrator).
3. **On update, compare the old and the new data:** the owner field, the role, the creation time and counters are not changeable by the client.
4. **Deletes need their own rule;** a collection that users must not empty gives the rule to administrators only.

## 1.5 Validate what is written
1. **The client is not trusted to send well-formed data.** Check in the rule or in a function: required fields exist, types are right, strings and lists have a length limit, and unknown fields are rejected.
2. **Numbers that grant value (balances, scores, counters) are not client-writable.** Update them from a server function and make the rule forbid the field.
3. **Server timestamps beat client time:** require the field to be set by the server's timestamp value, or the client chooses its own history.
4. **Files:** the storage rules check the caller, the path, the content type and the size. A user-supplied file name must not choose another user's folder, and uploaded files that others will see (images, documents) are untrusted content (§2).
5. **Replacing a file** may need update permission as well as create; test it, as a missing rule shows only when a user re-uploads.

## 1.6 Test the rules
1. **Run the rules in the local emulator and test them with a unit-test library** (the rules unit-tests page: seed data with a helper that bypasses rules, then use a signed-in context with optional claims, a signed-out context, and assert-succeeds and assert-fails wrappers; emulator data persists between tests, so clear it between them). Put these cases in the suite for every path: the owner can, another signed-in user cannot, an anonymous caller cannot, a missing field is rejected, a forged owner is rejected.
2. **Run the rules tests in CI,** and block deployment of rules that fail them.
3. **Deploy rules and application together through the same pipeline.** Changing rules by hand in the console creates a state no one reviewed.

## 1.7 Checks (own guidance)
1. Print every rules file: no blanket allow, no development-mode expiry (the platform's own example flags a bare signed-in check as acceptable only during development).
2. For each path, state in one line who can read, create, update and delete; compare with the intended model.
3. With a second ordinary account and an anonymous session, attempt to read, write, reassign and delete the first account's data; every attempt is refused.
