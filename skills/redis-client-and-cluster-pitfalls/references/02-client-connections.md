# redis-client-and-cluster-pitfalls §2 — Client, connections and commands

Sources: the `redis-connections` skill of redis/agent-skills at a84871d (`SKILL.md`, `references/pooling.md`, `blocking.md`, `pipelining.md`, `client-cache.md`, `timeouts.md`), read 2026-10-15.

## 2.1 Connections
1. **Never open a connection per request.** The source calls it the single biggest mistake in Redis client code. Either keep a pool of persistent connections that each call leases (redis-py `ConnectionPool`, Jedis `JedisPooled`, go-redis), or share one multiplexed connection across all callers (Lettuce, NRedisStack).
2. **A pool that is too small makes callers wait.** When every connection is leased, the next lease blocks, so a latency spike under load can be the pool and not Redis. Size it to the concurrency of the application.
3. **A multiplexed connection cannot carry blocking commands such as `BLPOP`.** One caller waiting on it would stall every other caller sharing the connection. Blocking consumers get their own connection or a pool-based client.
4. **A client built inside the request handler is the same mistake as an unpooled connection,** even when it is closed with a `with` or `try` block: the source's bad examples create a `Redis` or `UnifiedJedis` object per call.

## 2.2 Batching
1. **Independent commands go in one pipeline: one round trip instead of N.** A loop of single `GET` calls pays the network latency once per key.
2. **Use a non-transactional pipeline by default.** A transactional pipeline (`pipeline(transaction=True)` in redis-py) is for the case where the commands really have to be atomic; it is not a faster pipeline.
3. **The source scopes pipelining to commands that do not depend on each other's results.** Own guidance: a command that needs the previous reply goes in a later batch.

4. **In redis-py a pipeline is transactional unless told otherwise** (client documentation, read 2026-10-20): buffered commands run as one atomic group by default, so the non-transactional form must be asked for explicitly. `execute()` returns one reply per command in order; a pipeline or pub/sub object must not be passed between threads, and the client itself may be shared (connections are leased only while a command runs). The client has no database-switch command: use one client, and possibly one pool, per database.

## 2.3 Commands that walk everything
1. **`KEYS`, `SMEMBERS` on a large set, `HGETALL` on a large hash and `LRANGE 0 -1` on a large list block the server while they run.** Use a `SCAN` cursor loop, `SSCAN`, `HSCAN`, and paginate the list (`LRANGE 0 100`).
2. **A scan is a loop that ends when the cursor returns to 0,** and it takes a `MATCH` pattern and a `COUNT` hint (the source uses `count=100`).
3. **Blocking pops (`BLPOP`, `BRPOP`, `BLMOVE`) are not the same problem:** they wait on purpose and suit queue consumers. Always pass a timeout, never issue them on a multiplexed connection (§2.1.3).

## 2.4 Client-side caching
1. **Enable it only for data read often and written rarely:** configuration, feature flags, a session read on every request. The client keeps a local copy and the server invalidates it on writes.
2. **RESP3 is required.** In redis-py that is `protocol=3` plus a `CacheConfig`; in Jedis the RESP3 protocol on the client config plus a `CacheConfig`. Both examples set a maximum size of 1000 entries; treat it as a sample value.
3. **Skip it for write-heavy or constantly changing data:** the invalidation traffic costs more than the saved round trips. Also skip it where real-time consistency is guaranteed to be needed, and where network latency is not the bottleneck.
4. **It adds memory overhead on the client and makes invalidation of frequently changing data a complication.**

## 2.5 Timeouts
1. **Set connect and read/write timeouts explicitly.** Client defaults vary and can be more generous than the application's failure model allows.
2. **The connect timeout is shorter than the read/write timeout,** so a dead node is detected quickly without cutting healthy slow operations. The source's example is 2 seconds to connect and 5 to read and write, to be tuned, not copied.
3. **Latency-sensitive paths use tight timeouts with retry; batch jobs use longer ones.** Use health checks next to timeouts for robust failure handling.
4. **Own guidance:** a retry after a timeout on a write may repeat a command that did succeed. Retry on timeout freely for reads; for writes make the command idempotent first (see `nestjs-reliability` §4 for the unknown-outcome rule).

5. **The Go client's reference (2026-10-20) states that RESP3 is selected through a protocol option and that client-side caching is experimental, needs RESP3 and database 0, and is disabled with a dynamic credential provider;** its default protocol and its timeout defaults are not stated on the page read, so set both explicitly.

## 2.6 Checks (own guidance)
1. Search the code for the client constructor: it is called once at startup, never inside a handler.
2. Search for `KEYS`, `HGETALL`, `SMEMBERS` and `LRANGE 0 -1` on containers whose size is not bounded.
3. Every blocking pop has a timeout, and none runs on a Lettuce or NRedisStack shared connection.
4. Both timeouts are set in the code, with connect lower than read/write.
