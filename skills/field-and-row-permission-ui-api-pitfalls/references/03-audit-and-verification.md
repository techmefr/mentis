# field-and-row-permission-ui-api-pitfalls §3 — Audit and verification

## 3.1 Audit
1. **Log permission-relevant changes as events:** role or permission granted or removed, who did it, to
   whom, when, from where, and the before and after. Symptom: "who gave this person access?" has no answer.
2. **Log reads of sensitive fields and bulk reads** (exports, impersonation sessions, view-as), not every
   read: who, what resource or field class, how many records, when. Choose the sensitive set deliberately; a
   log of everything is not read.
3. **Log refusals in aggregate.** A burst of refused requests from one person across many identifiers is the
   signature of probing. Alert on the pattern, not on each refusal.
4. **The audit log is append-only and readable only by a narrow role**, stored apart from the data it
   describes. If application administrators can edit it, it proves little. Retention follows the legal and
   business need (`business/data-protection`; not legal advice).
5. **Do not put the restricted values themselves in the audit log.** Record that a field was read or changed
   and, where needed, a reference or a hash; the log's readers may be a wider group.
6. **Record the actor and the on-behalf-of.** Jobs, impersonation and integrations act for someone; keep both.
7. **Audit entries are written in the same transaction as the change** (or from the same outbox), so a change
   without an entry or an entry without a change cannot happen.

## 3.2 Verification
1. **A permission matrix test:** for each resource, each role (and the unauthenticated case), each record
   relationship (own, same team, other team, other tenant) and each state, the expected result of read, list,
   search, export, create, update, transition and delete. Generate it from the rule definition (§1.1.5) so a
   new role or field adds rows to the matrix.
2. **Test the API directly as the restricted user**, not through the interface. Hidden-button tests prove
   nothing about enforcement.
3. **Test fields, not just resources.** For each restricted field: absent from the detail, list, search
   result and export; rejected as sort and filter key; ignored on write.
4. **Test the leak channels:** counts and facets, error messages, timing on sensitive lookups, cached
   responses across two users, notification and email bodies, background job output.
5. **Test the scope after a permission change** without a new session: removed access takes effect on the next
   request, including cached flags, index content and open exports.
6. **Negative tests for new endpoints are a merge condition.** A route that can be called and has no
   authorisation test is the usual origin of the next incident. Add a check in review that lists routes with no
   declared rule.
7. **Review the rule definition, not just the code.** Ask the business owner to read the matrix: "may a team
   lead see a colleague's salary?" is a question for them, not for the developer.

## 3.3 Checklist for a review
1. For each resource, where is the row scope defined, and do all queries pass through it?
2. For each response shape, are fields allow-listed, including nested records?
3. For each update endpoint, which fields does each role write, and what happens to the others?
4. Do lists, counts, search, sorting, filtering, export, notifications and jobs apply the same scope?
5. What does a refused request return, and does it differ for existing and absent records?
6. Does the interface render from server-sent flags, and does a stale flag degrade gracefully?
7. Which events are audited, where are they stored and who can read them?
8. Which tests would fail if someone removed the scope from one endpoint?
