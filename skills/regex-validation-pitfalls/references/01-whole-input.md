# regex-validation-pitfalls §1 — Match the whole input

> Section 1 of `skills/regex-validation-pitfalls`. Read it when a regex is a yes-or-no gate. Restated from the
> OpenSSF Best Practices Working Group guide "Correctly Using Regular Expressions for Secure Input Validation" and
> its rationale page (`wg-best-practices-os-developers`, commit `8259081`, CC-BY-4.0; credit and changes in
> `references/origin.md`), read 2026-10-16. Platform behaviour is version-bound. Sentences marked "own guidance"
> are ours.

1. **Only data that matches completely may pass.** The guide's first rule for validation is that the whole input
   must match the pattern, ideally through a method, function or flag that demands it. Its Python example: in
   Python 3, and not Python 2, use `re.fullmatch` for validation when practical. A regex used as a search finds
   a valid-looking piece inside hostile input and says yes.
2. **If there is no full-match call, anchor the pattern, in normal (not multiline) mode.** Prepend a
   start-of-string marker and append an end-of-string marker, using the right symbols for the platform (§1.3).
   The guide notes that some wrappers only search: its example is a Python validation library whose regexp
   validator has no full-match variant, so you still add the anchors yourself. PCRE can force a full-string match
   with its anchored and end-anchored options, but the guide says that also disables its JIT compilation.
3. **The symbols differ by platform.** The guide's table, for default (non-multiline) mode:

   | Platform | Start | End | Is `$` permissive? |
   |---|---|---|---|
   | POSIX BRE and ERE, ECMAScript (JavaScript) | `^` | `$` | no |
   | Perl, .NET and C# | `^` or `\A` | `\z` (not `$`) | yes |
   | Java | `^` or `\A` | `\z` (`$` works but sources conflict, §1.8) | no, disputed |
   | PHP | `^` or `\A` | `\z`, or `$` with the `D` modifier | yes |
   | PCRE | `^` or `\A` | `\z`, or `$` with `PCRE2_DOLLAR_ENDONLY` | yes |
   | Go, Rust `regex` crate, RE2 | `^` or `\A` | `\z` or `$` | no |
   | Python | `^` or `\A` | `\Z` (not `$`, not `\z`) | yes |
   | Ruby | `\A` (not `^`) | `\z` (not `$`) | yes |

   "Permissive" means that `^cat$` also accepts `cat` followed by a newline.
4. **Do not use `$` until you have verified what it does.** On a permissive platform it matches at the very end
   or just before a final newline, so `abc\n` passes a check meant for `abc`. The guide says to use the explicit
   end marker, and that if you really mean "end, allowing one trailing newline", writing `\n?\z` says so and
   loses nothing. A one-line demonstration in Python:

   ```python
   import re

   re.match(r"^[a-z]{3}$", "abc\n") is not None
   re.fullmatch(r"[a-z]{3}", "abc\n") is None
   ```
5. **Group the alternatives.** The `|` operator has a precedence that makes `^ab|de$` mean "starts with ab, or
   ends with de". Write `^(ab|de)$` (JavaScript) or `\A(ab|de)\Z` (Python). Where the platform has
   non-capturing groups, `(?:ab|de)` is usually more efficient when you do not need the capture.
6. **A regex does not port by copying.** The guide says regex syntax varies between platforms and is not a
   standard, and that someone reusing a regex from the internet must translate it. Its rationale quotes a survey
   in which 94% of developers reuse regexes and 47% wrongly believed the notation is the same everywhere, and
   notes that two web answers and, as of April 2024, the weakness-catalogue entry CWE-625 treat `$` as an
   end-of-string marker where it is not.
7. **Multiline mode and Ruby.** In multiline mode `^` and `$` match at line boundaries, which is the opposite of
   what validation needs. In Ruby they are line anchors even without that mode, so use `\A` and `\z` always; the
   guide cites the Rails security guide and a static analyser that warns on `^` and `$` in Ruby. Prefer
   `\A` and `\z` wherever the platform supports them.
8. **Decision for Java.** The guide's table says `$` is not permissive there and its own tests on several JDK
   versions agree, but one vendor's current documentation describes it as permissive and its survey table marks
   it "yes". The guide itself concludes that `\z` is the safer choice, so use `\z` and leave the question of
   `$` aside.
9. **`\A` and `\z` are not everywhere yet; this is moving.** The guide reports that JavaScript lacks them (a
   proposal sits at stage 2), that Python agreed in 2025 to add `\z` beside `\Z` and implemented it, and that
   the POSIX committee accepted `\A` and `\z` for extended regexes, with the rationale page giving both 2024
   and 2025 as the date. Own guidance: do not depend on them in a toolchain you have not tested; on Python use
   `fullmatch` or `\Z` unless your minimum version is verified to accept `\z`, and in JavaScript or POSIX tools
   use `^` and `$` in normal mode.
10. **Prefer a library validator for a common type.** The guide says that for types common enough to ship with
    validators (an integer, an email address), consider those; regexes are for application-specific shapes. A
    validator does not remove the need to bound the length (§2.4).
11. **Test the near-misses.** The guide's suggestions: tests that take valid values and extend them, for example
    with a trailing newline or a leading one, and more generally inputs that are almost correct, plus fuzzers
    that append newlines. The replay for this block: every gate regex has a test where the valid value plus
    a newline is refused.
