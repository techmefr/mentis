# angular-conventions §2 — Components and templates

> Section 2 of `skills/angular-conventions`. Read it when a component, its inputs and outputs, host bindings or
> a template is written. The other sections and the guardrails stay in `SKILL.md`.

1. **Standalone components only, no `NgModule` for new code.** On Angular 20 and later `standalone: true` is the
   default, so do not write it in the decorator. Import in the component only the directives and pipes the
   template uses (`AsyncPipe`, `DatePipe`), never `CommonModule`.
2. **Inputs, outputs and two-way values are functions, not decorators.** `input()`, `input.required()`,
   `output()`, `model()` replace `@Input`, `@Output` and the `input` + `output` pair. `model()` is for a value
   the component itself writes back, typically a custom form control's primary value; it does not accept an
   input transform and it creates an implicit `<name>Change` output.
3. **An input transform is pure and statically analysable.** It cannot be chosen at runtime or read outside
   state. The built-in `booleanAttribute` and `numberAttribute` cover the two common cases (and
   `booleanAttribute` reads the literal string `"false"` as false). Alias an input only to avoid a native DOM
   property collision or to keep an old name alive.
4. **`input()` is only legal as a property initialiser** of a component or directive. A call anywhere else is a
   compile error, not a style point.
5. **Keep a component focused on presentation.** Validation rules, data transformations and anything that
   makes sense without the screen move to plain functions or services. Keep components small, one
   responsibility each.
6. **Group the Angular members at the top of the class**: injected dependencies, inputs, outputs, queries, then
   methods. The template's API and the dependencies are found in one glance.
7. **`protected` for members only the template reads, `readonly` for everything Angular initialises**
   (`input`, `model`, `output`, queries). Public members are the component's API through injection and
   queries; `readonly` stops a reassignment from silently detaching the signal Angular set up.
8. **Host bindings go in the `host` object of the decorator.** `@HostBinding` and `@HostListener` exist for
   backward compatibility only. Binding precedence when the parent and the component both set the same
   attribute: two static values, the instance binding wins; static against dynamic, the dynamic wins; two
   dynamic, the component's host binding wins. Do not rely on the third case being obvious to the next reader.
9. **Native control flow only**: `@if` / `@else`, `@for`, `@switch`, never `*ngIf`, `*ngFor`, `*ngSwitch`.
10. **Every `@for` has a `track` on a stable unique key** (`id`, `uuid`). `$index` is acceptable for a static
    collection that never reorders. Tracking the item itself (identity) is the last resort and can force the
    whole list to be rebuilt on change. `@for` has no `break` or `continue`; filter the collection first.
    Provide `@empty` rather than a second `@if` for the empty case.
11. **Make `@switch` exhaustive on unions** with `@default never;`. The type check only narrows variables, so
    a signal or function call must be read into a `@let` variable first, otherwise the guard silently does
    nothing.
12. **`class` and `style` bindings, never `ngClass` / `ngStyle`.** `[class.admin]="isAdmin"` and
    `[style.color]="textColor"` are the same idea with a plainer syntax and a lower runtime cost.
13. **Templates stay simple.** A JavaScript-like expression that fits on a line is fine; anything longer moves
    into a `computed()` in the class. There is no numeric threshold, the test is whether the reader has to
    run it in their head. Never rely on globals such as `new Date()` inside a template: they are not available.
14. **Observables in templates go through the `async` pipe**, which subscribes, unsubscribes and notifies
    change detection. A manual subscription whose value is copied into a field is the long way round to the
    same result, with a leak to clean up.
15. **Use `NgOptimizedImage` for static images.** It does not work for inline base64 images.
16. **Component styles and templates in separate files use paths relative to the component file.** Small
    components may keep an inline template.
17. **A native element beats a custom one.** A button variant is an attribute-selector component on a real
    `<button>`, not a `<div role="button">`; a custom text field wraps the native `<input>` through content
    projection so consumers can still set its attributes. See §5 for focus and ARIA.

## Mechanical checks

```
grep -rnE "@(Input|Output|HostBinding|HostListener)\(" src
grep -rnE "\*ng(If|For|Switch)|\[ng(Class|Style)\]|CommonModule" src
grep -rnE "standalone: *true|ChangeDetectionStrategy.OnPush" src --include=*.ts
grep -rnE "@for \(" src --include=*.html | grep -v "track "
grep -rnE "new Date\(\)|Math\.random\(\)" src --include=*.html
```

- Old idioms are findings on a project at the matching major and migration candidates on an older one.
- `standalone: true` and an explicit `OnPush` are redundant from the major where they became the default
  (Angular 20 and 22 respectively); leave them in a project still on an earlier major.
