# design-tokens-storybook §2 — The token build

> Section 2 of `skills/design-tokens-storybook`. Read it when the token build is configured, a platform output is
> added, or a theme or brand is introduced. The other sections and the guardrails stay in `SKILL.md`.

1. **Know the order the pinned tool runs in, because a bug is always in one stage.** It reads the configuration,
   finds the token files, parses them, deep-merges them into one dictionary, runs the global preprocessors, then
   per platform: preprocessors, transforms, reference resolution (looped with transitive transforms), then per
   output file: filter, format, file header, and last the actions. Debug by asking which stage produced the wrong
   value: a wrong merge is a source problem, a wrong unit is a transform, a missing token is a filter.
2. **Deep merge makes file layout free and collisions loud.** Files in `include` load first, then `source`, later
   wins. Two `source` files defining the same path produce a collision warning; a `source` file overriding an
   `include` file does not, because that is the intended way to theme. Treat a collision warning as an error: it
   means two files disagree about one token.
3. **One configuration, one platform per output family.** A platform is a build target (web stylesheet, native
   resources, constants for scripts) with its own transforms. Transforms are isolated per platform, so the same
   token becomes `1rem` in one output and `16` in another without either knowing. Do not post-process a generated
   file with a script to fix a unit: add or choose the transform.
4. **Transform order matters, and a name transform is applied once.** Transforms run in the listed order; two name
   transforms override each other. Start from the tool's predefined group for the platform (the stylesheet group
   already covers colour, size, font family, shorthand borders, shadows, typography and transitions) and add
   only what it lacks. A custom transform declares what it applies to through a filter, so it never touches a
   token of another type.
5. **Value transforms skip aliased tokens unless they are transitive.** Because transforms run before references
   resolve, a token that aliases another is not transformed itself; the target is, and the reference then points
   at the transformed value. A transform that must act on an aliased token (darken the colour another token
   points at) is declared transitive, and returns undefined to defer when its own input is still an unresolved
   reference. The predefined transforms are not transitive.
6. **Keep references in the stylesheet output when themes switch at runtime.** With reference output on, a
   semantic custom property is emitted as `var(--color-primary)` pointing at the primitive, not as a copied
   value, so overriding the primitive under a theme selector re-points everything that aliases it. With it off,
   every alias is flattened and a theme must redefine each semantic token. It is supported only by the formats
   that list it (the stylesheet, Sass, Less, and some native formats), not by JSON.
7. **Filtering and reference output interact.** If a filter removes a token that another still references, the tool
   warns; use the tool's reference-output filter helper so the dependent token falls back to the resolved value,
   and use the matching helper when a transitive transform already changed the value, since putting the
   reference back would undo that work.
8. **Themes and brands are layered builds, not copied files.** The base set is `include`; each theme or brand is a
   small `source` set that overrides only the tokens that differ, built into its own output (a selector scoped
   to the theme attribute or class, or a separate file). A theme file that restates the whole set drifts from the
   base on the next edit. The community resolver module exists to describe contexts (light, dark, high
   contrast, sizes, reduced motion) without a combinatorial explosion of files, but it is a draft, and the pinned
   tool's documentation does not mention it: do not write a resolver file and expect the build to use it.
9. **Composite values are not CSS.** A shadow, border or typography token is an object; a stylesheet needs a
   shorthand string. Use the predefined shorthand transforms (they are in the stylesheet group), or expand composites
   into one token per property when a consumer needs the parts. A format that prints `[object Object]` is a
   missing transform.
10. **A custom format is code under test.** Register hooks in the configuration file (a script, not JSON), keep
    each hook a small pure function, and test it with a fixture dictionary. Formats are handed a flag saying
    which notation the source uses; branch on it rather than hard-coding the property name, or test both.
11. **Pin and upgrade deliberately.** The fifth major requires a recent Node (22 or newer), fixed reference
    syntax characters (curly braces and a dot), and strict references. Read the migration page before the bump
    and rebuild with the output committed in a branch to diff it: a token file that did not change should
    produce an output that did not change.
12. **The build runs in CI and fails on warnings.** Set the tool's warning level to `error`, which turns five
    cases into failures: a value collision in the source, a name collision on export, an action with no undo,
    an output file with no tokens left after filtering, and a reference to a filtered-out token. Set the
    broken-reference level to `throw` as well, since by default a broken reference only logs. A token pipeline
    whose warnings are read by nobody is how a wrong brand colour ships.
