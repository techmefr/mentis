# dotnet-async-exception-pitfalls §3 — Runtime hygiene

Small traps in the base class library. `System.Threading.Lock` needs .NET 9 and C# 13; the
`RegexOptions.NonBacktracking` option needs .NET 7; the other rules apply to supported .NET versions.

## 3.1 Lock targets
1. **Never lock on `this` or on a publicly accessible instance such as a `Type` object.** Any other code can
   take the same lock.
2. **Lock on a private readonly field used only for locking.** On .NET 9 and later with C# 13, declare it as
   `System.Threading.Lock` instead of `object` when it is only used inside `lock`.
3. **Prefer `LazyInitializer.EnsureInitialized` to a hand-written `Interlocked.CompareExchange` for lazy
   fields,** unless the return value of the exchange is needed to know which caller initialised the value.

## 3.2 Events
**An anonymous delegate cannot be unsubscribed:** `MyEvent -= (s, e) => { }` creates a new delegate and
removes nothing. Keep a method or a stored delegate when the subscriber's lifetime is shorter than the
publisher's. Unsubscribing in `Dispose` is our own guidance for static or singleton publishers.

## 3.3 Keys and collections
1. **A struct used as a key in a `Dictionary`, `HashSet` or `ConcurrentDictionary` should define its own
   equality.** With default `ValueType` equality, lookup and insertion can become significantly slower.
2. **Do not call `Enumerable.Contains` on a set.** It uses the set's lookup only when the source implements
   `ICollection<T>` for the searched type; otherwise it scans every item. With a comparer it never uses the
   set's lookup. Call the set's own `Contains`.
3. **Use `StringComparer.Ordinal.GetHashCode(s)` (or the comparer you mean) instead of
   `s.GetHashCode()`** so the comparison is explicit.

## 3.4 Numbers and dates
1. **`Math.Round` with no mode rounds a midpoint to the nearest even number** (banker's rounding, member
   `MidpointRounding.ToEven`). State the mode when the domain expects away-from-zero, and test a `.5` value.
2. **Do not convert `DateTime` to `DateTimeOffset` implicitly.** For `Local` and `Unspecified` kinds the
   offset is the local system's, so the result depends on where the code runs; for `Utc` the offset is zero.
   Convert explicitly with the offset you mean.

## 3.5 Input and processes
1. **Give every `Regex` that runs on untrusted input a match timeout,** or use
   `RegexOptions.NonBacktracking` (.NET 7 and later), which guarantees linear-time matching. Neither
   protects against an untrusted pattern; do not build patterns from user input.
2. **Set `UseShellExecute` explicitly on `ProcessStartInfo`.** The default is `false` on .NET and `true` on
   .NET Framework. It must be `false` to redirect input, output and error streams, and to set a user name.
3. **Do not write your own certificate validation callback.** Such callbacks are often used to bypass
   validation altogether.

## Verification
- A search for `lock (this)` and `lock (typeof` finds nothing.
- A rounding test pins `2.5` and `3.5` to the intended results.
- A regex run on a pathological input returns within its timeout.
