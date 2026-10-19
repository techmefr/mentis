# c-conventions §2 — Memory, arrays and strings

> Section 2 of `skills/c-conventions`. Read it when an allocation, an array index, a string copy or
> comparison, a pointer into a buffer or a structure with a flexible array member is written. Bracketed
> identifiers trace to the published standard in `references/origin.md`. The other sections and the guardrails
> stay in `SKILL.md`.

1. **Every pointer has a documented owner.** Whoever allocates a block is responsible for freeing it exactly
   once, or hands that responsibility over explicitly. Say in the function's contract (its name, its header
   declaration, the type it returns) whether a pointer is borrowed, owned or transferred. A block that nobody
   frees leaks [MEM31]; a block freed twice, or freed through a different allocator than the one that made it
   [MEM34], corrupts the heap. Free only memory that was allocated dynamically, and pair allocation and
   deallocation functions that belong together [WIN30].
2. **Never touch freed memory.** Reading, writing or freeing a pointer after the block is freed is a classic
   exploitable defect [MEM30]. Do not copy a pointer to a place that outlives the block it points to, and when
   a pointer variable stays in scope after the free, make the code path that can still reach it impossible
   rather than hoping it is not taken.
3. **Allocate enough, and check the size computation.** The size passed to an allocator is computed from
   an element count and an element size: multiply them with an overflow check, or use the zero-initialising
   allocator that takes both factors, since a wrapped multiplication allocates a small block that is then
   filled as a large one [MEM35]. Size the block from the type of the object (`sizeof *p`) rather than a type
   name that can drift. Do not resize a block that was handed out with a strict alignment through a call that
   does not preserve it [MEM36].
4. **Test an allocation result before using it** (§3.1). A request that fails returns null, and the null is then
   written through with an attacker-influenced offset.
5. **No out-of-bounds pointers, and no out-of-bounds subscripts** [ARR30]. A pointer one past the end of an array
   may be formed and compared but not dereferenced; anything beyond that is undefined, even if it is never
   dereferenced. Check the index against the length *before* the access, and keep the length next to the
   pointer (a pair, a struct, or an argument) so the callee can check it. Do not subtract or compare pointers
   that point into different arrays [ARR36], do not do pointer arithmetic on a pointer to a non-array object
   [ARR37], and do not add a scaled integer to a pointer, since the compiler scales it again [ARR39].
6. **A library function that takes a pointer and a length is given a valid pair.** Functions such as `memcpy`
   form pointers from the arguments; if the destination is smaller than the length or the ranges overlap, the
   result is undefined [ARR38]. Use `memmove` when the ranges can overlap.
7. **No variable-length arrays on untrusted sizes.** A size taken from input and used to declare an automatic
   array can be zero, negative or large enough to overflow the stack [ARR32]. Use a heap allocation with a
   checked size, or a bounded fixed array with an explicit limit; compile with the stack-clash and
   variable-size stack checks of §5.5 if any VLA remains.
8. **A flexible array member is declared with the standard syntax and allocated dynamically.** Use the C99
   flexible array form, not a one-element or zero-length array [DCL38], and allocate the structure with room
   for the trailing elements, never as an automatic object or by assignment from another structure [MEM33].
   Compile with the strict trailing-array setting of §5.5 so fortification can use the declared sizes, and
   mark the length member with the counted-by attribute where the toolchain supports it (§5.10).
9. **Strings: the terminator and the size are part of the contract.** A destination buffer has room for the
   characters and the terminator [STR31]; a function that expects a string is never handed a sequence that is
   not terminated [STR32]. Prefer calls that take the destination size and report truncation to calls that
   do not, and treat truncation as an error where the string is a name, a path or a command, not as a feature.
   Never write to a string literal; declare the destination as an array [STR30].
10. **Characters are cast to `unsigned char` before conversion to a wider integer** [STR34, STR37], since a
    negative `char` becomes a negative index into a classification table or a huge value after promotion.
    Do not mix narrow and wide string functions [STR38]. Do not assume that a line-reading function returns a
    non-empty string, and reset the buffer when it fails [FIO37, FIO40].
11. **Numeric parsing reports its errors** (§3.2) and is bounded: after a string-to-number conversion, check
    the end pointer and the error indication, then range-check the result [ERR34, INT31].
