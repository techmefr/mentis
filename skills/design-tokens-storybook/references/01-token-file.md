# design-tokens-storybook §1 — The token file

> Section 1 of `skills/design-tokens-storybook`. Read it when a token or group is added, renamed, retyped or
> removed, or an alias is written. The other sections and the guardrails stay in `SKILL.md`.

1. **Pick one notation and keep it for the whole source.** The community format prefixes every reserved
   property with a dollar sign (`$value`, `$type`, `$description`). The build tool's original notation does not
   (`value`, `type`, `comment`). The tool reads either, but the two cannot be combined inside one build, and a token
   named `value` or `type` is only possible in the prefixed notation. New work uses the prefixed notation; an existing source converts in one change with the
   tool's own conversion utility, never by hand in several commits.
2. **A token is an object with a value; a group is an object without one.** An object that has both a value and
   child tokens is invalid and the tool must report it. Groups are for humans and for naming, so nothing should
   infer a token's meaning from the group it sits in.
3. **Names are plain and portable.** A name never starts with `$` and never contains `{`, `}` or `.`, because the
   alias syntax uses them. Names are case-sensitive in the format, but two names that differ only by case collide
   as soon as an output language is case-insensitive or flattens the path, and the second silently replaces the
   first: forbid them in review.
4. **Every token has an explicit, known type.** The type is set on the token, inherited from the closest parent
   group that declares one, or taken from the token it aliases. Nothing else: a tool must not guess a type from
   the shape of the value, so a token with no resolvable type is invalid. Declare the type once on the group for a
   homogeneous run of tokens, and on the token only when it differs.
5. **Use the structured value forms the format defines, not strings.** A colour is an object with a colour space,
   an array of components, an optional alpha between 0 and 1 and an optional six-digit hexadecimal fallback. A
   dimension is a number and a unit, `px` or `rem`, and the unit is required even for zero. Put the fallback on
   every colour that is not in the sRGB space, so a tool that cannot read the space still gets a usable value.
   Check that the pinned build tool reads these object forms before moving a source to them: the pinned version
   reads both the legacy strings and the objects, an older one may read only strings.
6. **Two tiers, and components only read the second.** Primitive tokens carry raw values (a blue at one step of a
   scale). Semantic tokens alias primitives and carry the decision (the colour of a destructive action, the
   padding of a dense row). A component, a story or a stylesheet reads semantic tokens only, so a rebrand edits
   aliases and never a component. Aliases are what the format offers for exactly this: expressing a choice,
   removing repeated values, keeping related values consistent.
7. **An alias is a curly-brace path to a whole token.** `{colors.blue}` resolves to the target's complete value.
   It cannot point at a group or at a piece of a value. A group that needs a base value alongside its variants
   uses the reserved `$root` token name, and the alias is `{color.accent.$root}`, never `{color.accent}`. To reach
   one component of a structured value (the first colour component, say) the format offers a JSON Pointer
   reference; prefer a separate token over it, because the build tool pinned here only resolves references to
   whole tokens.
8. **An alias chain ends on a real token.** The pinned build tool stopped allowing references to anything that is
   not a token (a group, a property inside a value) in its fifth major, and a rename that leaves an alias
   pointing at the old path breaks the chain. Run the build with the tool's warnings visible after every rename.
9. **Describe and retire tokens in the file.** `$description` states the purpose in plain text and is what
   documentation pages and editors show. `$deprecated` is `true` or a string naming the replacement (an alias in
   braces is allowed in the string); `false` re-enables a token inside a deprecated group. Remove a deprecated
   token only after a search shows no consumer, in the same change as the last consumer.
10. **Vendor data goes under `$extensions`, with a reverse-domain key,** and tools must keep extension data they do
    not understand. Nothing a build depends on lives there: it is optional metadata by definition.
11. **The file name says what it is.** The format recommends `.tokens` or `.tokens.json` and the media type
    `application/design-tokens+json`; every such file is also valid JSON.
12. **Keep the source in one place, and generated output out of review.** Token files are authored; the stylesheets
    and constants built from them are generated, carry a generated-file header and are never edited. Commit them
    or build them in CI, but pick one and say which in the build's README.
