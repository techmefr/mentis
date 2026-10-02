# typescript-patterns §8 — Function and type design

> Section 8 of `skills/typescript-patterns`. Read it when a function signature, a constant, a generic or a public
> module boundary is designed. The other sections and the guardrails stay in `SKILL.md`. Where the repository's own
> conventions or lint configuration say otherwise, they win; the compiler and the linter enforce what they can, and
> this section covers what they leave to judgment.

## Inference and constants
1. **Annotate only to narrow, and let inference do the rest.** An empty `Map`, `Set`, array or state initialiser
   infers a wide type (`any`, `string`): give the type argument. A value that already infers precisely carries no
   annotation, and an annotation that widens (`const role: string = 'admin'`) is a loss. Explicit types are also
   fine where they document intent; the point is never to widen.
2. **Constants that must keep their exact values use `as const`**, and when they must also conform to a broader
   type, `as const satisfies T`: `satisfies` checks the shape without widening, and `as const` keeps literals and
   makes the structure readonly. A readonly array annotated with the broad type loses the literals; an `as const`
   without `satisfies` accepts values that are not members of the intended type.
3. **A list of allowed values is one source for the value and the type**: a constant tuple, and
   `type X = (typeof LIST)[number]`. Loop over the constant, accept the type in signatures.
4. **Prefer a literal union over an enum**, and a constant object or tuple when values must be enumerated at run
   time. An enum emits runtime code and has quirks; a compiler option that forbids syntax needing emission exists
   (`erasableSyntaxOnly`), and a lint selector on enum declarations enforces the rule (§3 has the enum rule).
5. **`readonly` in signatures documents and enforces non-mutation at compile time** (`ReadonlyArray`, `Readonly`);
   it does not freeze at run time. A function that processes data returns a new structure rather than mutating
   its argument.

## `any`, `unknown`, assertions
6. **`any` is not used; `unknown` is narrowed before use.** Anything can be assigned to `unknown`, and nothing can
   be done with it until a check or a validator narrows it (§4, §7).
7. **A type assertion or a non-null assertion is an exception with a stated reason** at the point of use (a
   third-party typing mismatch, say), never a way to silence an error from your own code.
8. **Suppress a compiler error only with `@ts-expect-error` and a description.** It reports when the error is gone;
   `@ts-ignore` stays silently forever. A suppression with no description is a finding.
9. **Choose `type` or `interface` once per project.** Use `interface` where declaration merging is needed
   (augmenting a library's types) and say so.
10. **Types of external services are generated, not hand-written**, from the schema, the contract file or the
    database introspection, so the compile-time contract follows the service. They are compile-time only: they
    do not validate what arrives at run time (§7). Write a type by hand only when no source of truth can be
    read, and record that.
11. **Type-only imports use `import type`** (or the inline `type` keyword): erased at compile time, no run-time
    import, no accidental module side effect, and the difference stays visible (§6 has the compiler options).

## Function design
12. **A function has one responsibility and explicit dependencies.** What it needs comes in as arguments; what it
    computes is returned. A pure function (deterministic, no observable side effect) is the easiest to test and
    reuse. Not everything can be pure (network, storage, logging, rendering), so keep the impure functions small
    and isolate them from the business logic they serve.
13. **Several related parameters become one object parameter**, so call sites name every value and the signature
    can grow without reordering. Keep positional parameters when order and meaning are obvious (a predicate on one
    value, a callback).
14. **Most parameters are required; optional ones are rare.** A function that needs many optional parameters is
    several functions. Parameters that describe mutually exclusive cases are a discriminated union (§4), not
    optional fields with a convention about which pairs go together.
15. **Be explicit on the outside, implicit on the inside.** Exported functions of a library or a module boundary
    carry explicit return types, so a change in the body cannot silently change the public type (the lint rule
    `explicit-module-boundary-types` enforces it). Internal helpers let the compiler infer.
16. **A function that computes returns a value**; one that exists for an effect returns nothing and its name says
    so. A function that does both is split.

## Names
17. **Generic parameters are descriptive and prefixed** (`TRequest`, `TItem`), not `T`, `K`, `U`: more than one
    parameter is easy to confuse, and a bare name can shadow a real type (`<Request extends Request>`).
18. **Acronyms are words** (`UserId`, `HttpClient`), abbreviations are avoided unless universal, and a boolean is
    named as a question (`isActive`, `hasAccess`, `canEdit`).
19. **Use named exports**, so a symbol has one name across the codebase and renames and search are reliable. A
    default export is allowed where a framework requires it (route and page files).
20. **A custom hook or composable returns an object**, not a positional tuple, once it returns more than one
    value, so call sites destructure by name.

## Mechanical checks

```
grep -rnE ":\s*any\b|as any\b|<any>" src
grep -rnE "@ts-ignore|@ts-expect-error *$" src
grep -rnE "\benum +[A-Za-z]" src
grep -rnE "<(T|K|U|V)[,>]" src
grep -rnE "export default" src
grep -rnE "new (Map|Set)\(\)|\[\] *as " src
grep -rnE "^export (async )?function [a-zA-Z]+\([^)]*\) *\{" src
```

- The last pattern lists exported functions without a return type on the same line: review only those at a
  public boundary (rule 15).
- A positional signature of four or more parameters is a candidate for rule 13.
