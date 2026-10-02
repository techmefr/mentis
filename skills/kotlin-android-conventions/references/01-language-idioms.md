# kotlin-android-conventions §1 — Immutability, null handling, expressions

> Section 1 of `skills/kotlin-android-conventions`. Read it when a variable, a collection, a nullable value or
> a conditional is written. The other sections and the guardrails stay in `SKILL.md`.

1. **Declare read-only by default.** A local variable or property never reassigned is `val`, not `var`.
2. **Declare collections by their read-only interface** (`List`, `Set`, `Map`) when they are not mutated, and
   build them with the factory that returns the read-only type, not one that returns a mutable class.
3. **A nullable value is handled with the tools that keep the type honest:** the safe call, the elvis
   operator for a default or an early exit on an argument, the safe cast. The not-null assertion `!!` turns a
   compile-time guarantee into a runtime exception: reserve it for a case where the code already proves
   non-null and no smarter construct is available, and never in a path fed by outside data.
4. **Late-initialised properties and platform types are the two places a null still escapes the type
   system** (a read before assignment, a value coming from Java). A public function or a property whose
   initialiser is a platform-typed expression declares its Kotlin type explicitly, so nullability is a
   decision and not an inference.
5. **Prefer the expression forms of `if`, `when` and `try`** to a statement that returns in each branch. Use
   `if` for a binary condition, `when` from three branches up. When a `when` guard combines several boolean
   expressions, parenthesise them. A nullable `Boolean` in a condition is compared to `true` or `false`
   explicitly.
6. **Prefer higher-order functions to loops,** except `forEach`, where a plain `for` is preferred unless the
   receiver is nullable or `forEach` ends a longer chain. A complex chain of operations has a cost: weigh it
   against a loop when it is hot. Loop over a half-open range with the open-ended range operator.
7. **Strings:** templates over concatenation, a multiline literal over embedded newline escapes, with the
   margin or indent trimming function to keep the source indentation out of the value.
8. **Default parameter values replace overloads** that only fill a value. Name the arguments when several
   parameters share a primitive type or when a `Boolean` is passed, unless the meaning is obvious.
9. **A type alias names a functional or generic type used several times.** For a name clash, use an import
   alias instead.
10. **Lambdas:** the implicit parameter only in short, non-nested lambdas; declare parameters when nested. Avoid
    several labelled returns in one lambda; restructure, or use an anonymous function.
11. **Naming and layout** follow the language's conventions: a backing property is the private twin of a
    public one, with the same name and a leading underscore; test method names may be descriptive sentences.
    The project's formatter has the last word.
