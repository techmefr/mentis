# zig-pitfalls §2 — Allocators and ownership

Rules from the Zig 0.17.0 language reference and release notes unless a rule says otherwise.

## 2.1 The allocator is a parameter
1. **There is no default allocator by convention.** The reference says functions that need to allocate accept an
   `Allocator` parameter, and data structures accept one in their initialisation functions. When linking libc,
   `std.heap.c_allocator` exposes the C allocator; that does not make it a hidden default.
2. **A library takes the allocator from its caller**, as the allocator selection guide says for anything built
   as a library. A reusable function that reaches for a global allocator cannot be used in a context that
   chose another one.
3. **A function that returns memory says who frees it.** The reference's convention is a documented "caller
   owns the returned memory", usually together with an allocator parameter. Name the owner in the docblock
   of every function that returns a pointer or slice it did not borrow.
4. **Zig 0.17.0 lists pass the allocator on each call.** The reference's own example uses
   `var list: std.ArrayList(u21) = .empty;` with `try list.append(gpa, x)`, and the build system page shows
   that `std.ArrayList(i32).init(allocator)` no longer compiles on 0.17.0 (error: no member named `init`).
   Code written against an older release needs migrating, not just recompiling.

## 2.2 Pick the allocator by lifetime
The reference's selection guide, as a decision order:
1. **Bounded by a number known at compile time:** `std.heap.FixedBufferAllocator` over a stack or static
   buffer.
2. **A command-line program that runs start to end:** an `std.heap.ArenaAllocator` over
   `std.heap.page_allocator` with `defer arena.deinit()`, so nothing is freed manually.
3. **A cycle with a natural end, such as a request or a frame:** one arena per cycle, freed at the end of the
   cycle; add a fixed buffer under it when an upper bound is known.
4. **Tests:** `std.testing.allocator`; use `std.testing.FailingAllocator` to prove `error.OutOfMemory` is
   handled.
5. **Otherwise a general-purpose allocator**, set up once in `main` and passed down, or sub-allocators
   derived from it. In fast mode the guide recommends `std.heap.smp_allocator`; when linking libc,
   `std.heap.c_allocator` is likely right for the main allocator.
6. **Zig 0.17.0 note:** the release notes introduce `std.heap.SafeAllocator` as a thread-safe replacement
   that reports leaks on `deinit` and panics or faults on mismatches and double frees, and deprecate
   `std.heap.DebugAllocator`. The language reference of the same release still names `DebugAllocator` in
   the selection guide. Check which one the pinned release ships before choosing.

## 2.3 Leaks fail the test run
1. **Allocate through `std.testing.allocator` in tests.** The default test runner reports leaks found through
   it, prints the allocation stack and fails the run with "tests leaked memory" and a non-zero exit, even
   when every assertion passed. The reference's example is a test missing a single `deinit`.
2. **Do not hand a test an arena to make a leak disappear.** An arena frees everything at once, so it also
   hides a missing free in the code under test. Use it in a test only when the code under test is meant to
   be arena-driven (own guidance).
3. **Test the allocation failure path** with `std.testing.FailingAllocator`; an `errdefer` that was never
   exercised is unverified (see §1.2).

## 2.4 Lifetimes of what you hand out
1. **A pointer to a local is invalid after the function returns**, and dereferencing it is unchecked illegal
   behaviour. A slice is a pointer: returning a slice of a stack array is the same bug.
2. **String literals and compile-time-known constants live in the global constant data section**, which is
   why a literal coerces to `[]const u8` but not to `[]u8`.
3. **Memory from `allocator.alloc` or `allocator.create` lives where the allocator puts it**, so its lifetime
   is the allocator's: a value allocated from an arena must not outlive the arena (own inference from the
   arena example).

## 2.5 Allocation failure is a value
The reference states that by convention Zig code does not treat heap allocation failure as a reason to crash:
`error.OutOfMemory` is returned and the caller decides. It argues against relying on overcommit (not every
operating system has it, real-time and embedded targets do not, and a library that handles failure is usable in
more places). Propagate it with `try`; do not turn it into a panic inside a library.

## 2.6 Related
Release on the error path: §1.2. Static allocation after start-up and bounded sizes as a design rule:
`systems-assertion-discipline` §1.
