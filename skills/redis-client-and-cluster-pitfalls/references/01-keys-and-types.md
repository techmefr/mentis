# redis-client-and-cluster-pitfalls §1 — Keys and data types

Sources: the `redis-core` skill of redis/agent-skills at a84871d (`SKILL.md`, `references/choose-data-structure.md`, `references/key-naming.md`), read 2026-10-15.

## 1.1 Choosing the type
1. **Pick the type from the access pattern, not from the shape of the data.** The source's mapping: a simple value or counter is a String (atomic increment and decrement), a queue or a recent-N list is a List (push and pop at the ends), unique items and membership checks are a Set, rankings and score ranges are a Sorted Set, nested data that needs path-level updates is JSON, an event log with consumer groups is a Stream, similarity search is a Vector Set.
2. **An object whose fields are updated independently is a Hash, not a serialised String.** A String holding the whole object turns every one-field change into fetch, parse, mutate and rewrite of the entire value,. With a Hash a field is read and written on its own and the rest of the object is not rewritten.
3. **A value packed into a delimited string is the same mistake with extra fragility.** The source shows a bicycle stored as four fields joined by semicolons and split on read: the reader depends on the field order and nothing in the key says what each part means.

## 1.2 Key names
1. **Lowercase segments separated by colons, from the general to the specific:** `entity:id:attribute`, for example `user:1001:settings` or `order:2024:items`. No spaces, no mixed casing (the source's bad example is `User_1001_Profile`).
2. **One convention per service, applied to every key.** The source asks for consistency so that keys stay maintainable and debuggable and can be scanned efficiently.
3. **Keys live in memory and travel in every command, so keep them short but readable.** The source's bad example is a dotted reverse-domain path that spells out the application and environment in each key.
4. **Never use a URL or any long string as the key.** Extract a short identifier, or use a digest of the URL; for a large binary value, use a digest of the value as the key rather than the value itself. A full URL as a key wastes memory and slows comparisons.
5. **Prefix multi-tenant keys with the tenant** (`tenant:42:user:7:cart`) so a scan or an ACL rule can target one tenant cleanly.

## 1.3 Checks (own guidance)
1. For every value stored as a serialised String, name the field that is updated on its own; if there is one, it is a Hash.
2. Print ten real keys of the service: they must all follow one pattern, and none may embed a URL, a sentence or the environment name.
3. In a cluster, decide the hash-tag scheme at the same time as the key scheme (§3), because renaming keys later is the expensive part.
