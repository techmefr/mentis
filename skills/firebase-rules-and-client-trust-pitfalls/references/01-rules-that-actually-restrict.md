# firebase-rules-and-client-trust-pitfalls §1 — Rules that actually restrict

Source: own guidance throughout (no source was read; see origin). Rule syntax and limits are the platform's; re-read before relying on a name.

## 1.1 Open rules
1. **A project created in a development or test mode starts with rules that allow everything for a limited time.** After that date access stops, and the usual "fix" is to extend the date or allow everything. Replace the rules before the first real user, not on the day the app breaks.
2. **Search the rules for a blanket allow** (a rule that is true for any path and any operation), and for a match-all path at the top level that grants more than the specific rules beneath it.
3. **Each product has its own rules file:** the document database, the real-time database and file storage are separate. Securing one and forgetting another is common; list all of them.
4. **Default to deny.** Add an allow only for a path you can name and a caller you can describe.

## 1.2 Signed in is not allowed
1. **A rule that only checks that the caller is signed in lets any user read and write any document.** Combine it with an ownership test on the data (the caller's user id equals the owner field, or the path segment holding the user id).
2. **Anonymous sign-in counts as signed in.** If anonymous authentication is enabled, such a rule admits anyone who opens the app. Check the sign-in method as well as the rule.
3. **Ownership on create must test the incoming data,** since the document does not exist yet: the owner field in the new data must be the caller. Otherwise a user can create a document owned by someone else.
4. **Role checks read the role from a trusted place** (§2.3), not from a field in the document the caller writes.
5. **Sharing needs an explicit structure:** a members list or a subcollection that the rule reads, not a wide allow.

## 1.3 Rules are not filters
1. **A query succeeds only if the rules would allow every document it could return.** A client that asks for "all documents" fails even if only some are readable; a rule cannot filter results. Write the query with the same condition as the rule (the owner equals the caller).
2. **When a query fails with a permission error while a single read works,** the query is broader than the rule; fix the query or the data model, not the rule.
3. **A rule that looks up other documents costs a read each time and has limits on how many it may do per request;** design the data so the check needs few lookups, and denormalize the role or the owner into the document when appropriate.
4. **Do not use rules as the only guard for what the query reveals:** counts, existence and error messages can leak that a document exists.

## 1.4 Cascade and operations
1. **In some products an allow at a parent path grants everything below it, and a child rule cannot take it back** (the real-time database works this way); in others rules at different paths are independent. Know which product you are on.
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
1. **Run the rules in the local emulator and test them with a unit-test library.** Put these cases in the suite for every path: the owner can, another signed-in user cannot, an anonymous caller cannot, a missing field is rejected, a forged owner is rejected.
2. **Run the rules tests in CI,** and block deployment of rules that fail them.
3. **Deploy rules and application together through the same pipeline.** Changing rules by hand in the console creates a state no one reviewed.

## 1.7 Checks (own guidance)
1. Print every rules file: no blanket allow, no development-mode expiry.
2. For each path, state in one line who can read, create, update and delete; compare with the intended model.
3. With a second ordinary account and an anonymous session, attempt to read, write, reassign and delete the first account's data; every attempt is refused.
