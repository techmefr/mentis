# rust-async-unsafe-pitfalls §2 — Locks, blocking and future size

Sources: the Tokio 1.53.2 `Mutex`, `spawn_blocking`, `block_in_place` and crate-level documentation, the Clippy
`await_holding_lock` lint documentation, the Rust async book, and the Microsoft Rust guidelines
(M-YIELD-POINTS, M-ASYNC-STACK-SIZE).

## 2.1 Do not hold a guard across an await
1. **A standard-library or `parking_lot` mutex guard must not be alive at an `.await`.** Tokio's documentation
   says that although the compiler will not stop it when the task is not movable between threads, holding it
   across an await almost never yields correct concurrent code in practice and can easily deadlock. Clippy's
   `await_holding_lock` lint (group `suspicious`, since Clippy 1.45) flags it, and says the two fixes are an
   async-aware mutex or unlocking before the await, by a scope or an explicit `drop`.
2. **Prefer the ordinary mutex when the guard is never held across an await.** Tokio states it is fine and
   often preferred in async code, and that the async mutex costs more; its intended use is shared mutable
   access to an I/O resource such as a database connection. If the value behind the lock is just data, use the
   blocking mutex.
3. **Wrap the lock in a struct with non-async methods** that take the lock inside each method, or give an I/O
   resource to one task and talk to it by message passing (both patterns are Tokio's recommendation).
4. **The lint has a known false positive for an explicitly dropped guard**; the workaround it names is
   wrapping the `.lock()` call in a block instead.
5. **The async mutex is not magic either.** Its `lock` is not cancellation safe (§1.2), it does not poison on
   panic, and a lock held across an await while other futures on the same task wait for it deadlocks (§1.4).
   Limit the scope, keep few locks and take them in a fixed order.

## 2.2 Keep blocking work off the async workers
1. **A blocking call or a long computation on an async worker thread stops every other task scheduled on it.**
   Tasks are swapped only at `.await`, so code that never reaches one starves its neighbours; the async book
   and Tokio both say to use only non-blocking I/O in a task, and the standard library offers only blocking
   I/O.
2. **Run blocking code with `spawn_blocking`**, which uses a thread dedicated to blocking work; Tokio spawns
   more such threads on demand up to a configured limit and queues beyond it.
3. **`block_in_place` is narrower:** it panics on a `current_thread` runtime, it suspends everything else in
   the same task (a `join!` sibling, for example), and what runs inside it cannot be cancelled, so runtime
   shutdown waits for it unless `shutdown_timeout` is used. Prefer `spawn_blocking` when in doubt.
4. **Work that cannot be moved off the task should yield.** The Microsoft guideline says long CPU work with
   no I/O in between should call `yield_now().await` at regular intervals, and suggests 10 to 100
   microseconds of work between yields as a starting point under its stated assumptions (task switches costing
   hundreds of nanoseconds and a thread-per-core model); treat the figure as theirs. When the number of
   operations is unpredictable it suggests the runtime's budget query.

## 2.3 Watch the size of hot futures
1. **Locals that live across an `.await`, and the arguments of the call, become part of the future's state
   machine.** The Microsoft guideline notes a droppable local can cross an await without looking like it (it
   is dropped after the await), and that a large argument grows the future even if unused. Large futures cost
   a copy when boxed or spawned and force a large stack for the deepest chain of them.
2. **For futures on a hot path, track `size_of_val` of the future in a test** with a limit set on the first
   run, and shrink them if it grows: smaller parameters and held values, and returning `impl Future` after
   doing synchronous setup outside the `async` block.
3. **This is a performance rule for hot paths, not a default.** The guideline itself says most async
   functions do not have a problem; measure before restructuring.
