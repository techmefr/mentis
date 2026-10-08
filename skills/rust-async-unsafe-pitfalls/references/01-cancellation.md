# rust-async-unsafe-pitfalls §1 — Cancellation and select

Sources: the Rust async book (part guide chapters on async/await and on composing futures), the Tokio 1.53.2
`select!` documentation.

## 1.1 Every await can be the last
1. **A dropped future never runs again.** Cancellation is dropping: by owning and dropping the future, by
   `abort` on a task handle, by a cancellation token (cooperative), or implicitly by a macro such as
   `select!`. The cancelled future gets no notification apart from its destructors, and a token does not fire
   when it is cancelled by another route.
2. **Your code may stop at any `await`, including hidden ones in macros, and never resume.** It is cancellation
   safe when it behaves correctly whether it completes or ends at any await point. The async book's example of
   failing this: an async function reads data destructively into an internal buffer and then awaits the next
   item; if it is cancelled, the buffer is dropped and the data is lost.
3. **This is a logic and data-loss problem, not a memory-safety one.** The compiler will not flag it; the async
   book's reference section lists it as an outline only, so the rules here come from the guide chapters and
   from Tokio.

## 1.2 Cancellation safety, as Tokio defines it
1. **Definition:** if a future has not completed, dropping it and recreating it must be a no-op. That is what a
   `select!` in a loop does every iteration, and without it you lose progress when another branch wins.
2. **To judge your own function, look at where its `.await`s are**, because cancellation happens only there:
   if it is correct when restarted while waiting at any of them, it is cancellation safe.
3. **Cancel safe in Tokio 1.53.2** (the documentation says its lists are not exhaustive): `mpsc` and
   `broadcast` `recv`, `watch::Receiver::changed`, listener `accept`, `AsyncReadExt::read` and `read_buf`,
   `AsyncWriteExt::write` and `write_buf`, and `StreamExt::next` on any stream.
4. **Not cancel safe, can lose data:** `AsyncReadExt::read_exact`, `read_to_end`, `read_to_string` and
   `AsyncWriteExt::write_all`.
5. **Not cancel safe because they queue for fairness and cancelling loses your place:** `Mutex::lock`,
   `RwLock::read` and `write`, `Semaphore::acquire`, `Notify::notified`.
6. **Cancelling something that is not cancel safe is not always wrong.** The documentation's example: cancelling
   a task at application shutdown, where partially read data does not matter. Decide per site and name it.

## 1.3 select in a loop
1. **`select!` drops the losers.** Futures created inside the loop body are recreated each iteration and lose
   their state; the async book notes the data-loss and duplicate-processing bugs come from futures holding
   state about some data without holding the data itself.
2. **To keep a future across iterations, create it outside the loop and select on `&mut fut`.** A future that
   is not `Unpin` needs `pin!` for that to type-check.
3. **Do not poll a completed future again.** The `Future` documentation says it should not happen, and a
   `select!` with no state between iterations will do it if a branch finishes and the loop continues. Break
   out of the loop, add an `if` guard on the branch (evaluated only when the macro starts, not on each poll),
   or use a fused future or stream.
4. **Without an `else` branch, a `select!` whose branches are all disabled panics**; the `else` branch runs
   when all branches have stopped without running a block.
5. **Prefer spawning tasks plus a channel or token** when cancellation needs cleanup: a cancelled task can be
   asked to tidy up, which a dropped future cannot. Spawning also gives the scheduler fairer shares, since
   futures joined or selected on one task share that one task's time slice.

## 1.4 join and try_join
1. **`join!` runs futures concurrently on one task, not in parallel**, and keeps going when one future
   finishes with an error. Only `try_join!` cancels the others on the first `Err`, so reach for it when one
   failure should stop the rest.
2. **A panic in a future inside `join!` panics the whole task**, whereas a spawned task's panic is caught by
   the runtime and surfaced through its handle.
3. **A blocking call or a lock held by one joined future stalls the others**, since they share a thread; the
   async book notes a deadlock results if one future waits for a lock another holds (§2.1).
4. **`?` in an async block returns from the block, not the function**, and `break` or `continue` cannot cross
   an async block (use `return` or a `ControlFlow` value). The block's error type is not stated, so a
   turbofish such as `Ok::<_, MyError>(())` is usually needed.
