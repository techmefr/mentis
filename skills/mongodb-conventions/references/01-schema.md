# mongodb-conventions §1 — Schema

Rules hold for the current MongoDB manual (read 2026-10-08). The validation levels `strict` (the default) and
`moderate` and the actions `error` (the default) and `warn` are the ones used here; the manual marks the
`constraint` level as new in version 9.0 and `errorAndLog` as a further action, and neither is covered.

## 1.1 Embed or reference by access pattern
1. **Embed what is read together; reference what is not.** The data modelling best practices page lists
   embedding for data that is queried together, updated together, archived together, or in a "contains"
   relationship; and referencing when the child side has high cardinality, the combined size is too large for
   the application's memory or transfer budget, the embedded data grows without bounds, the data is written at
   different times in a write-heavy workload, or the child can exist without a parent.
2. **Duplicating data is a decision, not a default.** The page says embedding can duplicate data between
   collections, which lets one query return related facts, and that duplication that is too complicated to
   keep consistent is a reason to reference instead.
3. **Plan the schema early and expect to change it.** Large schemas in production are hard to modify, so
   settle the basics first and iterate (the page's own advice).

## 1.2 Bound every array
1. **An array with no bound can reach the 16 MiB BSON document limit.** The manual states the limit as 16
   mebibytes and the unbounded-arrays anti-pattern page adds that large arrays strain resources and reduce
   index performance. Documents above the limit need GridFS, which is a different design.
2. **Bound it by subsetting or referencing.** Keep only the recent or top items embedded and put the rest in
   a separate collection that points back by id, as the anti-pattern page does for book reviews.
3. **State the bound in code,** for example a capped push (`$push` with `$slice`) or a count check, and test
   an insert past it (own guidance; the pages give the problem and the two designs). Monitor real document
   sizes with the size operator `$bsonSize` (MongoDB agent skills, schema design skill, re-read 2026-10-20).

## 1.3 Validate with a rollout path
1. **Write a `$jsonSchema` validator for every collection that other code writes to.** A flexible schema does
   not remove the contract; it moves it to the application unless a validator holds it.
2. **Choose the action and level for the rollout.** `validationAction: "warn"` lets the write through and logs
   the violation, `"error"` (the default) rejects it. `validationLevel: "moderate"` applies the rules to inserts
   and to updates of documents that already match; updates to documents that already violate the rules are not
   required to pass, while `strict` (the default) applies them to every insert and update.
3. **Introduce a validator on a populated collection as `warn` with `moderate`,** read the logged violations,
   fix the data or the rule, then move to `error`. The MongoDB agent skills' validation reference (re-read
   2026-10-20) gives this same four-step rollout: apply with those two settings through `collMod`, find the
   non-conforming documents by querying with `$nor` against the current validator, fix them, then switch to
   strict and error. It recommends `strict` and `error` as the settled state.

## 1.4 Version the schema in the document
1. **Add a `schemaVersion` field and migrate lazily.** The schema versioning pattern keeps documents of
   different shapes in one collection, told apart by that field, which avoids a single large migration; code
   reads every version it may meet and writes the newest. The agent skills' versioning reference (re-read
   2026-10-20) adds: a validator accepting both versions during the migration, a bump only for a rename, a type
   change or a restructure (a new optional field or index needs none), and drift checks (count by version, or
   documents failing the current validator) before old read paths are removed.
2. **Expect more indexes** (unconfirmed 2026-10-20: the agent skills' reference does not discuss indexes across
   versions). If the same field sits at different depths in different versions, one index no
   longer serves every document, so queries on it may need an index per location.
