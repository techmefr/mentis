# go-performance §2 — Allocation

Apply these where a profile (§1) or a benchmark with allocation counts points at allocation, not by default.

## 2.1 Preallocate when the size is known
1. **Slices:** `make([]T, length, capacity)` reserves the backing array up front. The slices article says
   growing a slice means allocating a larger one and copying, which is what repeated `append` does when
   the capacity runs out.
2. **Maps:** `make(map[K]V, n)` takes a capacity hint. The language specification says the initial capacity
   does **not** bound the size: the map still grows. A wrong hint costs memory, not correctness.
3. **Do not preallocate a guess.** Own guidance: a hint far above the real count wastes memory for every
   instance, so use it where the count is known or cheap to bound.

## 2.2 Build strings with `strings.Builder`
Repeated `+` on strings in a loop copies the growing string each time; `strings.Builder` exists to build a
string with write methods while minimising memory copying. Its zero value is ready to use, `Grow(n)`
guarantees room for `n` more bytes in one step, `Reset` empties it for reuse, and **a non-zero Builder must
not be copied**. The first clause is an inference from the Builder's stated purpose.

## 2.3 A small slice can keep a large array alive
Re-slicing does not copy: the whole backing array stays in memory while any slice refers to it (slices
article). When a function keeps only a small part of a large buffer, copy that part into a new slice so the
buffer can be freed.

## 2.4 `sync.Pool` last, and only for temporary objects
1. **A pool caches allocated but unused items to relieve pressure on the collector,** and the
   documentation's example of good use is the temporary output buffers `fmt` keeps.
2. **Items can disappear at any time without notice,** `Get` may ignore the pool and return nothing, and a
   pool must not be copied after first use. A pool is a cache, never storage for state you need.
3. **A free list inside a short-lived object is not a good fit,** because the overhead does not amortise.
4. **Reset what you take out before reusing it** (the documentation's example resets the buffer after `Get`).
5. **Add one only where a profile showed the allocation** and measure again afterwards (§1.4). The
   "profile first" half is own guidance.

## 2.5 Left out on purpose
Interface boxing, reflection in hot loops and struct field order for cache lines are not given as rules
here: the only sources read for them in the earlier research were idea-only, and no documentation page
covering them was read in this pass.
