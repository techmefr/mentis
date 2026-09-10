# vue-nuxt-vuetify-conventions §4 — Naming and style

> Section 4 of `skills/vue-nuxt-vuetify-conventions`. Read it when a symbol, a file or a CSS class has to be named. The other sections and the guardrails stay in `SKILL.md`.

1. Casing fixed per artefact kind (files, components, composables, stores, types, constants) and applied
   without exception.
2. Booleans prefixed `is`/`has`/`can`/`should`. `loading` is ambiguous — a boolean? a promise? a count?
   `isLoading` isn't.
3. A callback parameter is the full singular word of the collection it iterates (`post` in `posts.map`),
   never `p` or `u`. A `reduce` accumulator is named for what it accumulates (`runningTotal`, `byId`),
   never `acc`.
4. Functions declared as arrow functions assigned to a `const`, consistently — the point is one shape
   across the codebase, not a claim that `function` is broken.
5. CSS class names follow a single naming scheme, BEM by default (`.block`, `.block__element`,
   `.block--modifier`) — this is about naming, not about the preprocessor, and applies identically to
   plain CSS. Three shapes are outside the scheme whatever the preprocessor: a **grandchild**
   (`.block__element__sub`) — flatten it, or promote it to its own block, since BEM has no third level; a
   **bare modifier** (`.active`, `.small`) — it says nothing about what it modifies and collides across
   blocks, so it carries its base; and **camel or Pascal case** — the scheme is kebab-case. A
   preprocessor's `&__element`/`&--modifier` nesting under one block root is a shorthand for exactly
   these selectors, not a licence for a different set.
6. Class and style bindings expressed through the framework's binding syntax rather than string
   concatenation built by hand, and split along what actually varies: static class names stay in the
   static attribute, dynamic ones in the bound one. A static name packed into the bound attribute, or a
   template-literal that concatenates the two, hides which half a reader can rely on — the framework
   merges them anyway, so composing one expression by hand buys nothing. Past two dynamic entries, name
   the intent in a `computed` (`cardModifiers`) instead of growing the literal in the template. Use
   classes for finite states (variant, active, size) and a bound style only for continuous values (a
   position, a transform driven by data). Where the framework can read a reactive value from inside the
   style block itself, that beats bridging it through a bound style as a custom property; take the bridge
   when the direct form would genuinely be more complex, and say which case you're in.
7. Don't hand-import what the framework auto-imports (in Nuxt: composables, components, stores, utils,
   and your own project types). A manual import line for an auto-imported symbol is noise that drifts out
   of date; the fix is usually deleting the import, not aliasing it. A folder the framework doesn't scan
   by default is **opted into the scan** (Nuxt: `imports.dirs`) rather than imported by hand file by file
   — one config line against an import in every consumer. Don't list folders already scanned: that reads
   as not knowing what was auto-imported. What genuinely keeps an import is a third-party package and a
   real name collision, and the collision is disambiguated in the one file that has it, not aliased
   globally.
8. Prefer an import alias over a relative path across folders, once the architecture linter resolves it
   (§5.9).
9. **A name says what the thing is, not what type it has or where it came from.** `data`, `info`,
   `result`, `item2` and `payload` describe the plumbing rather than the subject, so the reader has to
   open the definition every time. The bag-names are the same failure at file level — a `Utils`,
   `Manager` or `Helper` module accumulates whatever had nowhere else to go, and nothing in the name says
   what belongs inside it or what does not.
10. **A name has to survive being read somewhere else.** Anything numbered to avoid a collision
    (`useFilter2`, `handleClick3`) is a name that gave up: the second one exists because the first was
    named after its position instead of its subject. And when a symbol is renamed, its file is renamed
    with it — a `useContractSync.ts` exporting `useContractLines` is a search that returns the wrong file
    forever.
11. **Abbreviate only in the domain's own words.** If the business says "SIRET" or "IBAN", use it; if it
    says "customer", `cust` and `usr` are inventions the next reader has to decode, and half the codebase
    will spell them differently. The exception is a loop index in three lines of code, which is not a
    name.
12. **An emitted event says what happened, not what the parent should do.** `saved` and `deleted`
    describe a fact the child owns; `refreshTable` and `closeDialog` describe a decision the parent owns,
    and naming them that way lets the child dictate behaviour it cannot see. The test is whether a second
    parent could reuse the component: it can react differently to `saved`, it cannot react differently to
    `refreshTable`.
13. **Name the positive.** `isNotReady` and `disableSubmit` produce a double negative at every call site
    (`v-if="!isNotReady"`), which is where the reading mistake happens. Pick the affirmative form and let
    the caller negate once.
14. **A translation key is not an identifier.** Keys are full source sentences (§6.2), so they never leak
    into variable or prop names — a prop called `errRequiredField` is the key wearing a variable's
    clothes, and it drifts the moment the sentence is edited.
15. **In a codebase that already chose, consistency beats correctness.** If the project spells booleans
    or classes one way, follow it in a feature branch and change the convention in a dedicated pass with
    the whole tree. A branch that half-migrates a convention leaves a reviewer unable to tell an
    intentional change from an oversight, and leaves the next reader with two rules and no arbiter.
16. **If a name needs a comment, the name is wrong.** This block produces no comments in code, which is
    not an austerity measure: a comment explaining what a symbol holds is a rename waiting to happen, and
    the rename survives the next edit while the comment does not.
17. **A component name is always multi-word**, root `App` and the framework's own built-ins
    (`<Transition>`, `<KeepAlive>`) excepted. HTML elements are single-word, so `Item.vue` or `Card.vue`
    collides in spirit with a future native tag and reads, in a template, as if it might be one; `TodoItem`
    or `ProductCard` cannot. [Vue.js style guide,
    vuejs.org/style-guide/rules-strongly-recommended.html.]
18. **A prop is declared `camelCase` and bound `kebab-case` in the template — not a project choice.** The
    declaration lives in JavaScript, where `camelCase` is native; the binding lives in an HTML-parsed
    template, which is case-insensitive, so `greetingText` becomes `greeting-text` at the call site. Writing
    `greetingText="…"` in the template still works while it's a static string and silently stops matching
    once it needs to bind a JS expression — a divergence between the two casings anywhere in the same
    project is the tell that one file copied the wrong half. [Vue.js style guide,
    vuejs.org/style-guide/rules-strongly-recommended.html.]
19. **An acronym in a name follows the artefact's own casing, not the acronym's own capitalisation.**
    `PascalCase`/`camelCase` lower every letter of the acronym but the first (`XmlParser`, `userId`,
    `loadHtml`), because `XMLParser`/`userID` breaks the word-boundary a reader's eye uses to split a
    compound name, and the two spellings coexisting in one codebase (`Id` here, `ID` there) is a second,
    silent naming scheme nobody agreed to.
20. **A collection is named plural, its singular is what a callback parameter over it is named (point 3),
    and a `Map`/lookup keyed by id says so in its own name** (`postsById`, not `posts` reused for two
    different shapes). A plural holding a single record, or a singular holding an array, is a type the name
    lied about before the reader reaches the type annotation.
21. **A generic type parameter is a name, not a bare `T`, once the function has more than one of them or the
    parameter means something specific** (`TItem`, `TPayload` over an undifferentiated `T`, `U`). A single,
    genuinely generic parameter on a short utility can stay `T` — the rule is that `T` communicates nothing
    once a second parameter or a domain meaning enters, the same failure point 9 names for a bare `data`.
22. **A barrel file (`index.ts` re-exporting a folder) is named for what it re-exports being obvious from the
    folder path, never for what's inside it** — the file itself carries no naming decision beyond re-export
    order, because a symbol renamed inside the folder and not in the barrel is the collision point 10
    already covers, just one layer removed.
23. **A single-file component's own filename is `PascalCase` or `kebab-case`, picked once for the whole
    project and never mixed** — `PascalCase` matches how the component is referenced in a template or an
    import (`import UserCard from './UserCard.vue'`) and is what editor autocompletion expects, which is why
    it is the more common default; a project already on `kebab-case` files stays there rather than drifting
    file-by-file. [Vue.js style guide, vuejs.org/style-guide/rules-strongly-recommended.html.]
24. **A test file's name states what it verifies, not the tier it runs in.** `UserCard.spec.ts` next to
    `UserCard.vue` is discoverable by the file it covers; a name built around "unit" or "e2e" alone forces
    the reader to open the file to learn what it actually checks, and duplicates information the test
    runner's own folder convention already carries.
