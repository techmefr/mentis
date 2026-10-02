# § 1 — Role of the data, structure, and key names

> Section 1 of `skills/redis-conventions`. Read it before the first key is named. The structure and the name
> are the two decisions that drive memory, speed and the cost of changing your mind later.

1. **State what happens when the data is gone, before choosing anything else.** Three answers exist and each
   leads somewhere different. *Rebuildable* (a cached copy of a database row, a rendered fragment): the server
   may evict it and lose it, and the code falls back to the source. *Short-lived and tolerable to lose* (a rate
   counter, a one-time token in flight): loss costs a retry, not an incident. *Not rebuildable* (the only
   record of an order, a balance): it does not belong in a store tuned as a cache, and putting it there is a
   design error that the first eviction or restart turns into data loss. Write the answer next to the code
   that sets the key.
2. **Pick the structure from the access pattern, not from the shape of the data.** A plain string for a value
   or an atomic counter; a hash for an object whose fields are read or changed one at a time; a list for a
   queue or the last N items; a set for membership and uniqueness; a sorted set for anything ranked or
   range-queried by score; a stream for an event log with consumer groups; a JSON document when the data is
   nested and updated by path. The default mistake is serialising an object into one string: changing one
   field then costs a read, a parse, a mutation and a rewrite of the whole value, and two writers silently
   overwrite each other's field.
3. **Hash versus JSON is a question about nesting and updates.** A flat object with independently updated
   fields is a hash. Genuinely nested or array-bearing data that is updated by path, or indexed by a search
   module, is a JSON document. Do not reach for the heavier one by habit, and do not flatten nested data into
   delimiter-joined field names to avoid it.
4. **Name keys as a stable hierarchy of colon-separated segments:** entity, identifier, attribute
   (`user:1001:settings`). Lowercase, one separator, one convention per service applied to every key. Keys live
   in memory and travel in every command, so keep them short but readable. Never use a long string or a full
   URL as a key: extract a short identifier, or hash the long input and use the digest.
5. **Prefix by tenant when one server serves several.** A leading tenant segment makes scans, access rules
   and bulk deletion of one tenant's data possible without touching another's, and it is cheap on day one and
   expensive once keys exist without it. It does not replace the access rules of §5.5, which are the
   enforcement.
6. **Build every key in one function.** A key assembled from string pieces in ten files drifts into three
   spellings, and a rename then needs a hunt. One builder per entity makes the layout reviewable, makes a
   namespace change a one-place edit, and gives §2.1 (expiry) and §6.2 (placement tags) a single place to
   live.
7. **Do not rely on the database index number to separate applications.** The numbered logical databases are
   not available on a clustered deployment and they share one process, one memory limit and one set of
   credentials. Separate applications by key prefix with access rules, or by separate instances when their
   loss and eviction behaviour differ (§2.3).
8. **A large value is a latency problem for everyone.** A single command on a multi-megabyte value or a
   container with a huge number of elements blocks the server for its duration, because command execution is
   mostly single-threaded: one slow command delays every other client's request. Split such a value, bound its size at the write site, and measure the size of what is stored
   rather than assuming it.

**Sources:** the vendor's development skills for modelling and key naming (MIT), and its documentation on
choosing a data type and on keys, read 2026-10-02.
