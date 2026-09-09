# php-patterns — origin and source stamps

> Provenance of `skills/php-patterns`. Read it when a rule has to be traced back to its source or checked
> for freshness (`skills/source-freshness`), never to apply a rule.

Sourced from PHP-FIG (PSR-12 style, the base PSRs), the official PHP documentation (types, enums,
`readonly`, `match`, comparison and array semantics, `DateTimeImmutable`, the multi-byte and cryptographic
functions) and established modern PHP market practice. Mechanisms rewritten, no copied text. Market
research, no deep internal production feedback at this stage: same uncertainty status as `gimli`.

**Re-checked directly against the PSR-12 text on 2026-08-10**: almost every rule in it is pure formatting
(brace placement, line length, keyword casing) already enforced mechanically by Pint/PHP-CS-Fixer, which
is why this block never restated it. One rule genuinely changes behaviour rather than layout —
`declare(strict_types=1)` — and that one was a real gap, closed at §1.1. Everything else PSR-12 states
(instantiation parentheses, `elseif` over `else if`, `// no break` comments) stays a formatter's job, not
a hand-applied rule. `go-conventions` was filtered the same way on the same day.

**§1.1 corrected 2026-08-11**, cross-checked against the actual installed org catalogue's Laravel
plugin (`no-strict-types`) rather than a market source: the PSR-12 rule closed as a gap on
2026-08-10 is exactly right at the language level, but the real, currently-installed house catalogue
carries a **deliberate, dogfooded reversal** of it for Laravel specifically — Laravel's framework boundary
relies on scalar coercion (route/request/config values arrive as loose strings), so `strict_types=1` turns
that coercion into a runtime `TypeError` instead of catching anything static analysis (Larastan) doesn't
already catch. This is the mechanism working as designed (`laravel-conventions` sits above this block
precisely to override it where the two disagree), but until this pass the override existed only in
principle — nothing here or in `laravel-conventions` named this specific, easy-to-miss conflict, so reading
either block alone (without independently knowing the catalogue's rule) produced confidently wrong advice
on the one stack this framework actually supports.

**Sectioned and deepened 2026-09-08.** The block was a single `SKILL.md` of 960 rules words — the smallest
of the three blocks in `CATALOG.md`'s `laravel` row, and the last of the language-level blocks to have had
no depth pass. Its three inline sections moved to one file each under `references/` with a router table in
`SKILL.md`, and two were added. §1 kept its number and §1.1 its position, because `laravel-conventions`
§5.12 cites it by number as the rule it overrides.

The two new sections are where the block was silent rather than terse, and both are language-level by
construction — nothing in them belongs to a framework:

- **§4 comparison, arrays and the standard library.** PHP's defaults differ from what the code looks like
  it says more here than anywhere else: `==` changed meaning for string-to-number comparison in PHP 8,
  `in_array` is loose unless told otherwise, six values are falsy and two of them are real data, `isset`
  and `array_key_exists` answer different questions, `+` on arrays is a union and `array_merge` renumbers,
  and `array_filter` preserving keys turns a JSON array into a JSON object depending on which element was
  removed. The by-reference `foreach` leaving a live reference behind is included because it is the one
  that produces corrupted data rather than an error.
- **§5 time, numbers and text.** `DateTime` mutating in place while also returning itself; a date with no
  timezone taking the server's default; a day not being 86,400 seconds and a month having no fixed length;
  floats not holding decimals; integer overflow becoming a float silently; byte-based string functions
  cutting a UTF-8 character in half, which then makes `json_encode` return `false` and the response empty;
  `hash_equals` and `password_hash` over `===` and a hash function; `random_int` over `mt_rand`/`uniqid`
  for anything that must not be guessable.

The three original sections were deepened the same way as the other blocks — mechanism plus what the
reader or the next maintainer actually sees, one point per real failure mode, every original point kept
verbatim. The additions worth citing: `catch (\Exception)` not catching `\Error`, so the block written to
catch everything lets exactly the programmer errors through (§2.4); an exception wrapped without
`$previous` deleting its own cause (§2.5); a `return` inside `finally` discarding a pending exception in
silence (§2.6); `assert()` being compiled out in production, so a check written as an assertion holds only
in development (§2.14); a typed property with no default being uninitialised rather than null (§1.7);
variance errors being fatal at class-load time, i.e. on the first request that reaches the class rather
than at deploy (§1.12); `clone` being shallow (§3.9); and `unserialize` on user-influenced input being
remote code execution (§3.13). Router plus sections: 960 → 5,386, which takes the `laravel` row of the
depth table from x4.27 to x3.45.

**Status unchanged.** Still 🟡, and for the same reason as before the pass: sourced from the specification,
the documentation and market practice, with no deep in-house PHP production experience behind it. Depth is
not dogfooding — `gimli` keeps reading this block in a question register.

**Dogfooded once, 2026-09-09.** A small framework-free PHP CLI was written against this block as its only
reference — it reports how old the dated source stamps behind each block in this repo are, PHPUnit as the
only dev dependency, 52 tests green, run against the real clone. It lives outside this repo, with its
findings beside it. Four gaps came back, all closed here, and none of them was findable by re-reading:
`createFromFormat` normalising an impossible day into the next month and reporting it as a *warning* with
`error_count: 0`, so both plausible guards pass it (§5.15); a `DateInterval`'s `days` being unsigned, with
the direction only in `invert`, so a "days remaining" becomes "days overdue" with the same figure on the
screen (§5.16); `final` making a class undoubleable by the test framework, where the fix is §3.2's
interface and the tempting one is deleting the keyword (§3.15); and the deep-copy fix in §3.9 being a
fatal error on a `readonly` property up to PHP 8.2 and legal only from 8.3, measured both ways (§3.16).
The checkpoint also gained a clause: it routed to `gate` and `gimli`, both of which assume the framework
layer above, and said nothing about how framework-free PHP gets verified.

**The status still does not change.** One small CLI written by the same agent that wrote the block is not
in-house production experience, and the operator is still new to PHP. What the exercise bought is four
mechanical defects and a checkpoint that no longer assumes Laravel. Two things the pass also showed and
did not change: the router discriminates almost nothing here, because a language-level block has no
section a real PHP project can avoid — only the money and randomness points of §5 never applied — and
that is a property of the subject rather than a defect in the table.

**Widened against PHP 8.4's current type-system surface, 2026-09-09.** Same method as the other widenings
this week: checked against the language's own release notes, since §1 predates PHP 8.4's property hooks
and asymmetric visibility. Two points added: asymmetric visibility (`public private(set)`) as point 3's
`readonly` generalised for the property a method legitimately mutates later, where `readonly` would refuse
the mutation outright; and a property hook as a fix for point 7's uninitialised-property class of bug only
where the hook computes rather than causes a side effect — a `set` hook that dispatches an event or writes
to a log turns an assignment that looks free into one that is not. Nothing here answers the catalogue
comparison a second time.
