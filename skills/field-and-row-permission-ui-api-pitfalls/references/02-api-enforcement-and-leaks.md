# field-and-row-permission-ui-api-pitfalls §2 — API enforcement and leaks

## 2.1 Reads
1. **Authorise by the record, not only the endpoint.** Symptom: changing the identifier in the address returns
   another person's record (an object-level authorisation failure; no source was read for how common it is). Check: as person A, request B's record by identifier, on every resource endpoint. Fix: load
   through the scoped query (§1.1.3), so a record outside the scope is simply not found.
2. **Filter columns in the serializer, by allow-list.** Symptom: a new column on the table shows up in every
   response. Fix: each response shape names its fields; serialising a whole model is the defect. Include
   relations and nested objects: a restricted field often leaks through an embedded related record.
3. **Hidden is hidden everywhere the field can surface:** detail, list, search results, sorting and filtering
   by that field (sorting by a restricted salary reveals ordering), autocomplete, tooltips, exports, emails,
   webhooks, logs. Symptom: filter "salary above 5000" returns a count that discloses the value. Fix: reject
   filter and sort parameters on fields the person cannot read.
4. **Counts, facets and aggregates are reads.** A total that includes rows the person cannot see, or a facet
   showing "Region X: 3" for a hidden region, leaks. Compute them from the scoped query.
5. **Search and indexes.** A search index holding all rows must filter by the person's scope at query time (a
   filter on a stored scope attribute), or each tenant or group gets its own index. Re-check when the
   permission changes: the index copy is stale until reindexed. Reindex behaviour is in
   `skills/search-index-sync-pitfalls`.
6. **Generated and batch endpoints** (GraphQL, query-by-filter REST layers, "include" parameters) let a caller
   ask for relations you never meant to expose. Apply the rule on each resolver or included relation, and cap
   depth and breadth.
7. **Caches.** A response cached under a key that omits the person, role or tenant serves one person's view to
   another. Key by scope, or do not cache personalised data in shared caches. Browser-cache headers on
   authenticated responses deserve the same thought. In HTTP caching (RFC 9111) a shared cache may not reuse a response to a request that carried an Authorization header unless the response explicitly allows it (public, s-maxage or must-revalidate), and the unqualified private directive tells shared caches not to store a response at all; the usual leak is therefore adding public or s-maxage to a personalised answer, or varying on the wrong request header (a response is reused only when the request headers named by Vary match). Check: look at the cache directives and Vary of an authenticated endpoint.
8. **Background jobs, notifications, emails and webhooks run without a request.** The job reads as the system.
   Give it the initiating person's scope, or re-check at send time; a notification that quotes a restricted
   field leaks it into an inbox you cannot revoke.

## 2.2 Writes
1. **Allow-list writable fields per role.** Symptom: sending `{"role":"admin"}` or `{"owner_id":...}` in an
   update body changes it (mass assignment). Check: send every column name to the update endpoint as a
   restricted user. Fix: a fixed list of fields the endpoint accepts for that role, anything else ignored with a
   logged warning or rejected; never bind a request body to a model wholesale.
2. **Re-check the row on write.** The row the person may read is not always one they may change, and the
   change itself may move the row out of their scope (reassigning to another team). Check both before and
   after: may they edit this record, and may they produce this result.
3. **Server-controlled fields are never taken from the request:** owner, tenant, status transitions,
   timestamps, computed totals, approval flags. Derive them on the server.
4. **State transitions are actions with their own rules**, not field edits. "Set status to approved" as a patch
   bypasses the approval rule; expose transitions as named operations and refuse the status field on update.
5. **Bulk actions apply the row rule per row**, not once for the batch. Report which rows were refused. A
   "select all" over a filter must re-run the filter under the person's scope on the server (do not trust a list
   of identifiers or a count from the client).
6. **Relations written through a parent** (attach, sync, nested create) need the check on the target record too:
   linking to a record the person cannot see can disclose or corrupt it.
7. **Import and file upload are writes** with the same field and row rules (`skills/csv-xlsx-import-export-pitfalls`
   §1.1). A bulk import is how restricted fields get set by people who lack the screen.
8. **Optimistic concurrency** is an integrity control, not an access control, but pair them: a refused write
   should not reveal the current value to a person who cannot read it.
9. **A merge-patch body can erase through null.** In JSON Merge Patch (RFC 7396) a null member means remove that member, and absent members are left alone. Run the field allow-list over every member present, nulls included: a restricted user sending {"approved_by": null} is a write attempt, not a no-op.

## 2.3 What a refusal says
1. **401 versus 403 versus 404** (RFC 9110 section 15.5.2, section 15.5.4, section 15.5.5). 401 means valid credentials are missing and the server must send an authentication challenge; 403 means the request is understood and refused, and a client should not automatically resend the same credentials (a SHOULD NOT; the refusal can also be unrelated to the credentials); 404 may be used by a server that does not want to disclose that a resource exists, and section 15.5.4 says so for forbidden resources. Hence: unauthenticated is 401; authenticated but not allowed is 403; for a record
   whose existence is itself restricted, answer 404 so identifiers cannot be probed. Decide per resource and
   keep it consistent. Symptom: "403 for existing, 404 for absent" lets anyone enumerate identifiers.
2. **Error text must not echo restricted values or names.** The problem-details RFC (9457) warns that error bodies, stack dumps and implementation details can leak data about the system and its users, and says the details given must be vetted; it also notes that a generic refusal such as 403 to a write needs no extra problem type. "Customer Dupont already has an open order" tells
   the reader that Dupont is a customer. Say what the person can act on.
3. **Equalise timing where it matters.** A much faster answer for non-existent identifiers is an oracle on
   sensitive lookups (login, account existence). Reason about it for the few places where existence is
   secret; do not chase it everywhere.
4. **Do not rely on obscurity of identifiers.** Random identifiers reduce guessing, not authorisation; the
   check stays (point 2.1.1).

## 2.4 Layers and bypasses
1. **Enforce in a layer every path goes through** (a query scope or policy applied by the data layer or the
   service layer), not in each controller. Symptom: the admin console, a console command, a report job and a
   webhook handler each re-implement the filter and one drifts.
2. **Internal and admin interfaces are not exempt.** They have their own roles and need the same scoping and
   audit; "internal" tools are where bulk leaks happen.
3. **Raw queries and reporting connections bypass the application layer.** If analysts or dashboards read the
   database directly, give them views that carry the restrictions, or a separate scoped copy, and review who has
   the credentials.
4. **Database-level row security** is a backstop for the application's scoping, not a replacement for
   field-level rules in the serializer; the generated-API case is in
   `skills/postgres-operations-and-exposed-api-pitfalls`.
5. **Tenant isolation is the strongest row rule.** Treat a missing tenant condition as a defect by default; see
   `skills/laravel-tenant-context-by-default` for the principle.
6. **Third-party integrations get their own narrow credentials and scopes**, not a person's session or an
   all-access key, and their reads go through the same filters.
