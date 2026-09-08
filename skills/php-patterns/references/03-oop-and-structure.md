# § 3 — OOP and structure

> Section 3 of `skills/php-patterns`. Read it when a class, an interface, a trait or a static is
> introduced, or when behaviour has to be placed. Where behaviour belongs in a framework's own layers is
> `laravel-conventions` §1; the language-independent design rules are `code-baseline` §5 and §7.

1. Composition rather than deep inheritance (>2 levels): deep inheritance couples behaviours that
   should stay independent. The cost is paid when reading, not when writing: understanding one method
   means holding four classes in your head, and a change to the base ripples into subclasses nobody
   looked at — which the type system will not warn about, because they still typecheck.
2. An interface defined at the edge (a service's public contract) even with a single implementation:
   makes replacement/mocking easier without breaking the caller. Define it where it is *consumed*, in
   the terms the consumer needs — an interface extracted mechanically from one implementation's public
   methods just restates that class and gives the caller nothing.
3. A mutable static property = hidden global state: to be avoided except in an explicitly accepted
   case (immutable config, not a counter that changes). Its real cost shows up in the tests: state that
   survives between test cases makes the order matter, and the failure appears in whichever test ran
   second, not in the one that set it.
4. `match` (PHP 8+) rather than `switch` for a simple value comparison: no implicit fallthrough,
   returns a value directly. It also compares strictly and throws on an unhandled value instead of
   falling through to nothing — so a new enum case or a new status string produces a loud error rather
   than a silently skipped branch.
5. **A class is `final` until inheritance is a contract you mean to owe.** Once a class can be extended,
   every protected member and every internal call between its own methods is part of its public
   behaviour: changing one breaks a subclass you cannot see. Making a final class extendable later is a
   one-line change; taking the guarantee back is not.
6. **A constructor assigns; it does not do work.** A constructor that opens a connection, reads a file,
   queries the database or reads the clock makes the object impossible to create in a test, in a
   different environment, or twice — and it turns an unused dependency into a real cost, because
   building the object pays for it whether or not the method that needs it is ever called.
7. **A property or method that exists only through `__get`/`__call` is invisible to everything that
   checks.** No analyser, no IDE and no refactor sees it, so a typo becomes a runtime null and a rename
   silently misses the call sites. Where magic is genuinely the design (a proxy, a fluent builder over a
   dynamic schema), it needs annotations so the tooling has something to read.
8. **A trait is compile-time copy-paste, not composition.** Two traits declaring the same method are a
   fatal error the developer resolves by hand; a trait holding state gives every using class its own
   copy of that state; and a trait calling `$this->somethingItDoesNotDeclare` is an undocumented
   interface, satisfied by luck in the classes that happen to have it. Use one to share behaviour that
   genuinely belongs to a concept, and make what it requires explicit — abstract methods or an interface
   — rather than assumed.
9. **`clone` is shallow.** A cloned object shares every nested object with the original, so a
   "copy with one field changed" hands back something that mutates its source. Either hold immutable
   values all the way down (§1.3), or implement `__clone` to clone what has to be independent — and say
   which of the two the class does, because the caller cannot tell.
10. **`==` on two objects compares their properties; `===` compares identity.** Both are usually the
    wrong question for a domain value: two money objects with the same amount and a different currency
    property are unequal, and two that came from different sources are `===`-unequal even when they
    represent the same thing. Give a value object an explicit `equals()` and use it, so the comparison
    the domain means is written down once.
11. **Interface for the contract, abstract class only for behaviour that is genuinely shared.** An
    abstract class with one abstract method and no shared code is an interface that also fixes the
    subclass's parent, and it spends the single inheritance slot for nothing. When shared behaviour does
    exist, keep it small enough that a subclass never has to know the order its parent calls things in.
12. **The namespace is not decoration — the autoloader resolves the file from it.** A class whose
    namespace does not match its directory under the PSR-4 root is not found at all, and the error
    ("class not found") points at the caller rather than at the mismatch. So moving a file means editing
    its namespace and every import of it, in the same change.
13. **`unserialize` on anything a user can influence is remote code execution.** It instantiates
    arbitrary classes and runs their magic methods, so a serialised payload in a cookie, a queue message
    or a database column reached from outside is a way in. Use JSON for data that crosses a boundary,
    and if `serialize` is genuinely needed, restrict the allowed classes explicitly.
14. **A named static factory beats a constructor with flags.** `Report::forMonth($m)` and
    `Report::draft()` say at the call site which object is being built; `new Report($m, true, false)`
    makes the reader open the constructor to find out, and makes the two arguments swappable without any
    error. Keep the constructor as the single place that assigns, and let the factories name the cases.
