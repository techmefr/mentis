# § 4 — Comparison, arrays and the standard library

> Section 4 of `skills/php-patterns`. Read it when a comparison, a condition on a possibly-absent value,
> or an array transformation is written. This is where PHP's defaults differ most from what the code
> looks like it says.

1. **Compare with `===`, and treat `==` as a decision that has to be justified.** Loose comparison
   applies type juggling, and what it juggles changed in PHP 8: `"abc" == 0` was true and is now false,
   while `"1" == "01"` is still true. So a codebase carried across that version boundary contains
   conditions whose meaning changed without the line being edited — and the ones that mattered were
   in guards, where the change flips an authorisation or a filter.
2. **`in_array` and `array_search` compare loosely unless told not to.** Pass the strict flag every
   time: without it, `in_array(0, ['a', 'b'])` was true before PHP 8, and `in_array('1abc', [1])` is a
   match on the number. The lists these run against are usually allow-lists and role checks, which is
   the worst place for a comparison that says yes to the wrong value.
3. **Six different values are falsy, and two of them are real data.** `""`, `"0"`, `0`, `0.0`, `[]` and
   `null` are all false in a condition — so `if ($count)` treats a legitimate zero as missing, and
   `if ($name)` treats the string `"0"` as empty. Write the comparison the code actually means:
   `!== null`, `=== 0`, `!== ''`, `count($x) > 0`.
4. **`isset` answers "set and not null", `array_key_exists` answers "the key is there".** A key that
   exists holding null is `isset`-false, so a config array that deliberately stores null to mean
   "unset this" silently falls through to the default. `??` follows `isset`'s rule, which is usually
   what you want and is worth knowing rather than discovering.
5. **`empty()` is a third question, and it is the falsy list from point 3 plus "not set".** It is the
   right call for exactly one intent — "absent or blank, and I do not care which" — and the wrong one
   everywhere a zero, a `"0"` or an empty string is a value. Reaching for it by reflex is what produces
   a form that refuses to save the quantity `0`.
6. **Array keys are normalised, and `+` is not a merge.** `"1"` as a key becomes the integer `1`, so
   two entries that look distinct are one; `$a + $b` keeps the left-hand value for every key present in
   both, which is a union, not a merge; and `array_merge` renumbers integer keys instead of preserving
   them. Three different behaviours, chosen by punctuation.
7. **`array_filter` preserves keys, so a filtered list stops being a list.** The array is now
   `[0 => …, 2 => …]`, and `json_encode` serialises that as a JSON *object* rather than an array — so
   the API response changes shape depending on which elements the filter removed, and the consumer
   breaks on the request where the first element failed the test. `array_values` after the filter is the
   fix, and it is not optional.
8. **The sort functions sort in place and return a boolean.** `$sorted = sort($rows)` assigns `true` and
   loses the data; `usort` also reindexes the keys, which is fine for a list and destroys a map. Sorting
   has been stable since PHP 8.0, so equal elements keep their relative order — worth relying on, and
   worth knowing was not true before.
9. **A `foreach` by reference leaves the reference behind after the loop.** The loop variable still
   points at the last element, so the next `foreach` that reuses the same variable name overwrites that
   element on every iteration — the array ends up with its last item replaced by a copy of the
   second-to-last. `unset` the variable after the loop, or do not iterate by reference.
10. **Arrays are copy-on-write, so the memory cost lands at the write, not at the call.** Passing a
    large array to a function is cheap until the function modifies it, at which point the whole thing is
    duplicated — which is why a loop that "just adds a flag to each row" can double peak memory on a
    big result set. Iterate and yield, or modify in place deliberately.
11. **A generator is the difference between processing a million rows and running out of memory.** A
    function that builds an array of results holds all of them at once; a function that yields them
    holds one. The tradeoff is that a generator can only be walked once and has no count — so it belongs
    at the boundary that streams, and an array belongs where the caller needs to look twice.
12. **Several array functions throw where they used to warn.** `array_combine` with mismatched lengths
    is a `ValueError` in PHP 8, and passing null where a string is expected is deprecated on the way to
    the same. Validate the inputs before calling rather than relying on the previous version's silence.
13. **A user-supplied string inside a regex needs `preg_quote`.** Without it a search box accepting
    `(` produces a pattern that fails to compile, `preg_match` returns `false`, and the truthiness
    check from §2.9 reads that as "no match" — so the feature silently returns nothing for exactly the
    inputs that break it.
14. **A regex can fail silently on a large subject.** PCRE's backtrack and recursion limits are
    configuration, and hitting one makes `preg_match` return `false` rather than raising anything — so a
    pattern that works on every test fixture returns "no match" on the one real document that is long
    enough. Check for `false` explicitly, and prefer a pattern that cannot backtrack catastrophically
    over one that is merely correct.
15. **`array_first()`/`array_last()` (PHP 8.5) read the first/last element without the mutation risk of
    `reset()`/`end()`.** Both of the older functions move the array's internal pointer as a side effect,
    so calling one mid-`foreach`-by-reference or before a `current()`/`next()` elsewhere in the same
    request reads a different element than the caller expects — a bug that only shows up when two pieces
    of code touch the same array's pointer, which is rare enough to survive review. The new functions
    return `null` on an empty array rather than `false`, so point 3's falsy-collapse still applies to the
    result.
