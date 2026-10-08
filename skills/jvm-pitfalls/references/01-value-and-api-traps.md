# jvm-pitfalls §1 — Value and API traps

Each rule below names the check Error Prone ships for it, so the build can enforce it. The rule says what
goes wrong silently when it is missing. Everything here applies from Java 8 unless a version is stated.

## 1.1 Equality, numbers and stored values
1. **`BigDecimal.equals` compares the scale as well as the value.** `1.0` and `1.00` are not equal. When the
   number is what you mean, compare with `compareTo(...) == 0`, which ignores scale (a JDK API fact; the
   Error Prone page only states the scale behaviour). Note the same trap in a `HashMap` key or a `Set`:
   they use `equals`. Check: `BigDecimalEquals`.
2. **Never compare boxed primitives with `==`.** The wrapper classes cache instances for some values and not
   others, and the set differs between runtimes and libraries, so `==` can pass for small values in a test and
   fail in production. Use `equals`, or unbox. Check: `BoxedPrimitiveEquality`.
3. **Widen before you multiply.** An arithmetic expression on `int` operands assigned to a `long` is
   computed in `int` and widened at the end, so the intermediate result overflows. The page's own example is
   a nanoseconds-per-day product that wraps to a negative number. Make one operand a `long` literal
   (`24L * 60 * ...`). Check: `IntLongMath`.
4. **Never persist, transmit or index by an enum's ordinal.** The ordinal changes when constants are added,
   removed or reordered, and exists only to support utilities such as `EnumSet`. Key a map by the enum
   itself. When a stable number is needed on the wire or in a column, give the enum an explicit field and
   look values up by it, never `values()[code]`. Check: `EnumOrdinal`.
5. **`String.split` drops trailing empty strings and returns `[""]` for an empty input.** `"".split(":")`
   gives one empty string, `":".split(":")` gives none, and `"a:::".split(":")` gives only `a`. Pass an explicit
   limit of `-1` to keep trailing empties, or use a dedicated splitter that states how empties and
   whitespace are handled, and hold it in a `static final` field. Check: `StringSplitter`.

## 1.2 Time and text
1. **Do not use `java.util.Date`.** The API is full of design flaws; use `java.time`: `Instant` for a physical
   moment and `LocalDate` or `LocalDateTime` for civil time. Check: `JavaUtilDate`.
2. **In a date pattern, `YYYY` is the week-year, not the year.** The week-year starts at the week containing
   the year's first Thursday, so a date in the last days of December can print the next year. Use `yyyy` for
   any calendar date; `YYYY` is for week dates only. Check: `MisusedWeekYear`.
3. **Always name the charset.** APIs that use the JVM's default charset behave differently from machine to
   machine, even for ASCII. Pass a constant from `StandardCharsets`; when in doubt, UTF-8. Check:
   `DefaultCharset`.

## 1.3 Collections, arrays and resources
1. **A `public static final` array is not a constant.** Every non-empty array is mutable, so any caller can
   change its contents. Hold an immutable list instead, or keep the array private and return a copy. Check:
   `MutablePublicArray`.
2. **A method returns the same mutability on every path.** One that returns a fresh `ArrayList` on one branch and
   a `Collections.singletonList` on another gives callers a list that works until the rare input arrives, then
   throws on the first `add`. Return an immutable collection everywhere, or a mutable one everywhere. Check:
   `MixedMutabilityReturnType`.
3. **Do not assign a static field from a constructor.** It is usually an instance field written as a static,
   or an attempt at lazy initialisation that can be read from a static method before the class is even
   initialised; if the laziness is real, use a memoised supplier. Check: `StaticAssignmentInConstructor`.
4. **Replace the obsolete classes.** `LinkedList` almost never beats `ArrayList` or `ArrayDeque`; `Vector`,
   `Stack`, `Hashtable` and `StringBuffer` carry synchronisation that is usually unnecessary (use
   `ArrayList`, `ArrayDeque`, `HashMap`, `StringBuilder`, or a `java.util.concurrent` type when sharing is
   real). Migrating from `LinkedList` to `ArrayDeque` fails on `null` elements, which `ArrayDeque`
   rejects. Check: `JdkObsolete`.
5. **Close the streams that hold a file handle.** The streams returned by `Files.list`, `Files.walk`,
   `Files.find`, `Files.lines` and `Files.newDirectoryStream` wrap an open resource; consuming them without
   `try-with-resources` leaves the handle open. Check: `StreamResourceLeak`. A hand-written
   `finally` that closes is the weaker form (see `java-conventions` §2).
6. **`Class.newInstance` bypasses checked-exception checking.** It propagates whatever the constructor
   throws, checked or not. Use `getConstructor().newInstance()`, which wraps it in
   `InvocationTargetException` and adds three exceptions to handle (`IllegalArgumentException`,
   `NoSuchMethodException`, `InvocationTargetException`). The method is deprecated since Java 9. Check:
   `ClassNewInstance`.

## 1.4 Checks
- Compile with Error Prone and set the checks named above to error; a build that only warns is ignored.
- A test per trap you rely on: `1.0` against `1.00`, an enum with a constant inserted at the front, an input
  of `":"` into the splitter, `2014-12-29` through the formatter (the date the Error Prone page uses).
- Grep for `.ordinal()`, `new SimpleDateFormat`, `YYYY`, `getBytes()` with no argument, `new String(bytes)`.
