# § 4 — Clients: pooling, pipelining, scanning, timeouts

> Section 4 of `skills/redis-conventions`. Read it when a client is configured, when a loop makes many
> calls, or when code lists keys.

1. **Never open a connection per operation.** Either keep a pool of persistent connections that each call
   leases and returns, or share one multiplexed connection across all callers, depending on what the client
   library offers. A pool is sized to the concurrency of the application, and a call blocks when it is
   exhausted, so an undersized pool shows up as latency, not as an error. A multiplexed connection must not
   carry blocking commands, since one waiting caller would hold up all the others; give those their own
   connection.
2. **Batch independent commands in a pipeline.** Each request-response costs a network round trip, and the
   syscalls to serve it often cost more than the command, so N calls that do not depend on each other's
   results go out together and their replies come back together. Pipeline in bounded batches: the server
   queues every reply in memory until the client reads them. A pipeline is not atomic; ask for a
   transaction (§3.2) only when atomicity is what you need. Where a step needs the previous reply, a script
   (§3.4) is the tool, because a pipeline cannot read in the middle.
3. **Never list the keyspace or a large container in application code.** `KEYS` and a full read of a big set,
   hash or list block the server for the length of the walk; the vendor documents `KEYS` as a debugging and
   maintenance command. Walk incrementally with the cursor-based scan commands (and their per-container
   variants), page through lists in slices, and accept what the scan family states: it gives weak guarantees
   about elements that change during the walk, so it is a sweep, not a snapshot. A need to find keys by a
   property usually means the data wants an index structure of its own (a set of ids) maintained on write.
4. **Blocking commands always carry a timeout.** A consumer that waits forever on an empty list cannot be
   shut down cleanly, and a lost connection is not distinguishable from silence.
5. **Set the timeouts explicitly.** Library defaults vary and can be far looser than the application's
   failure model. Use a short connect timeout so a dead node is detected quickly, a read timeout sized to the
   longest legitimate operation, and decide per call path whether a timeout retries (latency-sensitive path)
   or fails (a path where a duplicated write would be wrong). A retry on a non-idempotent command can apply
   it twice.
6. **A cache outage must degrade the application, not stop it.** Decide for each use what an unreachable
   server means: read through to the source and accept the load (cache), skip the check and log (an
   optimisation), or fail closed (a rate limiter in front of an abuse-prone endpoint, a lock). Wrap the client
   behind one small interface so that decision is made once per use and is testable (`skills/testing-anti-patterns`
   on faking what you do not own).
7. **Client-side caching is for data read often and changed rarely.** With the newer protocol version a
   client can keep a local copy and have the server tell it when a key changes. It pays for configuration,
   flags and similar hot reads; for write-heavy or constantly changing data the invalidation traffic exceeds
   the saving. It needs the protocol version that supports it, so it is a deployment decision, not a flag.
8. **Serialise on purpose.** Choose one encoding for values, keep it stable across deployments (a rolling
   deploy runs two versions that must read each other's values), and treat a value read from the server as
   untrusted input to the deserialiser: do not use a format that can instantiate arbitrary types
   (`skills/security-hardening` on deserialisation).

**Sources:** the vendor's development skills for connection handling (pooling and multiplexing, pipelining,
scanning, client-side caching, timeouts; MIT) and its documentation on pipelining, keys (scan versus keys) and
latency, read 2026-10-02. Points 4, 6 and 8 are reasoning of ours.
