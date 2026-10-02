# angular-conventions §1 — Structure, naming and files

> Section 1 of `skills/angular-conventions`. Read it when a file is created, named or placed. The other
> sections and the guardrails stay in `SKILL.md`.

1. **When a rule here contradicts the style of the file you are editing, keep the file consistent.** Mixing two
   conventions inside one file is worse than diverging from the guide; migrate a whole file or leave it.
2. **File names use hyphens and match the main identifier.** `UserProfile` lives in `user-profile.ts`, its
   template in `user-profile.html`, its styles in `user-profile.css`: same stem, three extensions. A second
   style file adds a word that says what it styles (`user-profile-settings.css`). The test of a unit is the
   same stem plus `.spec.ts`.
3. **A file with several primary identifiers takes a name for their common theme**, and a file with no common
   theme is split. `helpers.ts`, `utils.ts` and `common.ts` are findings: a name that could hold anything will.
4. **All UI code lives under `src`, the bootstrap in `src/main.ts`.** Configuration and scripts stay outside
   `src`, so the root of every project reads the same.
5. **Group by feature, never by kind.** `show-times/film-calendar/` is a place; `components/`, `directives/`
   and `services/` as top-level folders are a filing system that scatters one feature across the tree. Split a
   directory when its listing stops being scannable.
6. **A component's files and its unit test sit in the same directory.** A separate `tests/` mirror of the tree
   means a rename leaves the test behind.
7. **One concept per file.** For Angular classes that is one component, directive or service. Two small classes
   that form one concept may share a file; when unsure, take the smaller file.
8. **Directive selectors carry the application prefix**, and an attribute selector is camelCase
   (`[mrTooltip]`). The prefix is what keeps a third-party element from being matched by accident.
9. **No barrel file in front of a lazily loaded component.** The bundler sees a barrel as one module and keeps
   everything it re-exports in the main chunk, so a `@defer` or `loadComponent` behind it produces no separate
   chunk. Import the component from its own file (see §5).
10. **Name an event handler for what it does, not for the event** (`saveUserData()`, not `handleClick()`).
    The fallback `handleKeydown(event)` is allowed when one handler dispatches on the event details to several
    named methods, and only then.
11. **Lifecycle hooks stay short and call named methods.** `ngOnInit() { this.startLogging(); }` tells the
    reader what happens; the hook name only says when. Implement the lifecycle interface (`OnInit`) so a
    misspelt hook fails to compile instead of never running.

## Mechanical checks

```
grep -rnE "(helpers|utils|common)\.ts$" src
grep -rnE "^export \* from" src --include=index.ts
find src -maxdepth 3 -type d \( -name components -o -name directives -o -name services -o -name pipes \)
grep -rnE "\(click\)=\"handle[A-Z]" src --include=*.html
```

- A barrel hit matters only when something behind it is lazily loaded; read the importer before flagging.
- The folder-by-kind hit is a finding at the top of `src` and a fine name inside one feature.
