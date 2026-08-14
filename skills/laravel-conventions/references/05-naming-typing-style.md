# laravel-conventions §5 — Naming, typing, style

> Section 5 of `skills/laravel-conventions`. Read it when a symbol has to be named, or a docblock written. The other sections and the guardrails stay in `SKILL.md`.

1. House casing applied per artefact kind (classes, jobs, events, listeners, commands, resources, enums,
   views, routes, variables, methods, abilities) without exception.
2. **Names reveal intent**: never `$temp`, `$data`, `$result`, `$array`, `$item`, `$value`, `$x`. The generic
   name pushes the meaning into the reader's head.
3. **No magic strings or numbers with domain meaning.** A domain value (status, type, kind, mode) becomes an
   enum; a queue name, config key or event name becomes a constant or a config entry; a threshold becomes a
   named constant.
4. **Native typed properties and signatures** over docblock-only types: the runtime enforces the former.
5. A docblock is for what the type system can't express (a collection's element type, an array shape, a union
   the signature can't state). **Skip it entirely on a fully type-hinted method** — a docblock repeating the
   signature is a second copy to keep in sync.
6. **Constructor property promotion** for a constructor that only assigns its parameters to properties.
7. String building through interpolation with braced placeholders rather than concatenation splicing quoted
   fragments.
8. Blank lines **between logical steps** inside a method body, so the steps are visible; not between every
   pair of lines.
9. Guard clauses and early returns rather than nested branches; no brace-less single-line statement.
10. **All code in one language — English** — including class and method names, command signatures and
    descriptions, log messages, console output, exception messages, queue and config keys. User-facing text
    is the exception, and it goes through translation.
11. Whether new files declare strict types is a **project-wide decision applied uniformly**, and the
    framework's own scaffolding is the reference point: a codebase half strict and half not gets the downsides
    of both. **The default for a new Laravel file is to omit `declare(strict_types=1)`, matching what
    `artisan make:*` generates** — this overrides `php-patterns`' language-level default (see that block's
    §1.1) precisely at this framework's boundary, where request/route/config values cross as loose scalars
    on purpose. Leave an existing file's declaration exactly as it is either way; this is a default for new
    files, not a retrofit.
