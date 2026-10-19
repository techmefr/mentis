# php-architecture-test-pitfalls §1 — Layers and rulesets

> Part 1 of `skills/php-architecture-test-pitfalls`. Read it when layers are defined or a rule misses a
> dependency. Sourced from the Deptrac documentation (commit `66595d1`): `docs/concepts.md`,
> `docs/collectors.md`, `docs/configuration.md` and `docs/debugging.md`, read 2026-10-16. Option names are
> Deptrac's. Sentences marked "own guidance" are ours.

1. **Everything between layers is forbidden until a ruleset allows it.** The concepts page says all
   dependencies between layers are forbidden by default and that a ruleset lists, for each layer, the layers it
   may use. A layer mapped to nothing (`~`) may use no other layer. Write the allowed edges and nothing
   else; an edge added to make a build pass is the same decision as a waived violation (part 2).
2. **A layer is a name plus collectors, and a class can sit in several layers.** Each layer lists one or more
   collectors; a class matched by two layers belongs to both. Own guidance: when a class lands in two layers,
   both layers' rules apply to it, so overlapping collectors make rules harder to read; prefer disjoint ones
   and use the layer collector with `must_not` (point 4) to carve out a sub-area.
3. **The name-pattern collectors are loose regular expressions.** For `class`, `classLike`, `interface`,
   `trait` and `directory` the page says the delimiters and the case-insensitive modifier are predefined
   (`/.../i`, and `#...#i` for directories). `classNameRegex` takes a regular expression you write. The page's
   own example pattern for controllers matches any class whose full name contains the word `Controller`
   anywhere. Own guidance: such a pattern also picks up a `Controllers` namespace segment, a test double or a
   class that merely mentions the word. Anchor patterns to a namespace prefix or a directory, and prefer a
   collector on something the code states (an interface it implements, a class it extends, an attribute it
   carries) over one on how it is spelled.
4. **Combine collectors instead of widening a pattern.** The `bool` collector takes `must` and `must_not`
   lists: everything that matches all of the first and none of the second. The `layer` collector re-selects what
   another layer collected, and the page uses it to take a sub-domain out of a broader domain layer.
5. **Vendor coupling is a layer too.** The `composer` collector builds a layer from the packages named in
   `composer.json` and `composer.lock` (PSR-0 and PSR-4 packages only, per the page). The page lists what it
   enforces: development-only packages stay out of production code, code does not use transitive
   dependencies that only arrived because a required package needs them, and some packages are used only by
   particular layers.
6. **Make a layer's public surface explicit.** A collector marked `private: true` can be referenced only from
   inside its own layer, even where the ruleset would allow it; the page names two uses: a library one layer may
   use and nobody else, and a layer with a public API over a private implementation. A class tagged `@internal`
   or `@deptrac-internal` cannot be referenced from outside its layer, and this overrides the ruleset.
   `analyser.internal_tag` adds a custom tag name.
7. **A class in no layer is invisible, not forbidden.** The page calls these uncovered dependencies: they can be
   reported (`--report-uncovered`) or made to fail the run (`--fail-on-uncovered`). PHP's built-in classes are
   left out by default (`ignore_uncovered_internal_classes`). Own guidance: a new directory that no collector
   matches escapes every rule while the run stays green, so run with the failing option, or at least list
   unassigned classes in CI.
8. **Check the analysis types, not only the layers.** The `analyser.types` option takes `class` and `use` by
   default; `file`, `function`, `function_call` and the two superglobal types are opt-in, as are custom emitters.
   Own guidance: a dependency that exists only as a call to a user-defined function, or a read of a
   superglobal, is not seen until the matching type is enabled.
9. **A `+` in front of a layer in the ruleset allows that layer and every layer it allows.** Own guidance:
   that is transitive permission, so reserve it for stable low layers and do not use it on a layer that itself
   allows many.
10. **Look at what a layer contains before trusting it.** The debug commands, one result per line so they combine
    with other tools: `debug:layer <layer>` lists the tokens a layer matched, `debug:token` says which layers a
    token belongs to, `debug:unassigned` lists tokens in no layer and exits with code 2 when it ran fine but
    found some (usable in CI), `debug:dependencies` lists a layer's dependencies on one other, and
    `debug:unused` lists ruleset entries that allow nothing (or fewer uses than `--limit`), which are candidates
    for removing an edge.
11. **Several views are several config files.** The page says one project can have multiple configuration files
    for different architectural views (layering, bundles, vendor coupling). Own guidance: a project with one
    big file mixes concerns, and a violation then names no view.
