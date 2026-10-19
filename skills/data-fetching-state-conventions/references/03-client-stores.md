# data-fetching-state-conventions §3 — Client stores: Redux-style and Pinia-style

> Section 3 of `skills/data-fetching-state-conventions`. Read it when a store, a slice or a reducer is written
> or reviewed. What goes in a store at all is decided by §1; server data does not go in (§1.3). The Vue-specific
> store rules (setup-store syntax, `storeToRefs`) are also in `skills/vue-nuxt-vuetify-conventions` §2.

## Both styles
1. **A store holds only state that needs a global home** (§1.6). The Redux guide says the "single tree" principle
   is over-read: not every value belongs in it, and each piece of state is evaluated for its home.
2. **One store per application in the Redux style; one store per concern in the Pinia style, each in its own
   file.** In the second, separate files let the bundler split code and keep type inference; in the first, app
   logic does not import the store object directly but receives it through the framework provider or middleware.
3. **Keep the state minimal and derive the rest** (selectors, getters): the original list stays, the filtered
   or summed view is computed. Memoise a derived value that is expensive or whose reference identity matters.
4. **Normalise relational data** held in a store: entities by id plus lists of ids, so one update touches one
   place and a lookup is direct. Nested API responses stored as received make every update a tree walk.
5. **Name a slice after the data it holds**, not after its mechanism (`users`, not `usersReducer`).
6. **Model changes as events, not setters.** `orderAdded` with its payload, not `setPizzas` then `setDrinks`:
   fewer calls, a readable log, and the caller needs no knowledge of the state shape. Several unrelated parts of
   the store can react to one event.
7. **Do not trigger a chain of updates for one logical change.** Each update notifies subscribers and can render;
   the intermediate states may be invalid. One event, or one grouped patch.
8. **Put the logic that computes new state next to the state** (in the reducer or the store action), not in the
   click handler that prepares it: it is then testable as a plain function, replayable, and found in one place.
   Computing a generated id before the update is the legitimate exception.
9. **Keep non-serialisable values out of the store**: promises, class instances, functions, `Map`, `Set`,
   symbols. Debugging tools, persistence and server hydration rely on serialisable state.
10. **Type the store** (TypeScript) and use the devtools of the library.

## Redux style (Redux Toolkit)
11. **Never mutate state outside the library's own immutable-update mechanism.** Inside a slice, the
    draft-based update mechanism (Immer) makes "mutating" code safe; outside it, copy. The toolkit's store
    set-up includes a development check for accidental mutation: keep it on.
12. **A reducer is pure**: it depends on its state and action and returns the next state. No request, timer,
    random value or date inside; those belong in a thunk, a listener or the data library (§2).
13. **A slice owns its shape.** Avoid blind `return action.payload` or `{...state, ...action.payload}` reducers
    that trust whatever arrives; type the payload at least. A spread reducer is acceptable for a form-like edit
    where one action per field would add nothing.
14. **Feature folders with one slice file each**, rather than folders by artifact kind (all reducers together).
15. **Select through functions** named `selectThing`, defined with the slice, and read with several narrow
    selectors rather than one that returns a large object. Component-only logic stays out of the selector.
16. **Action type is `domain/eventName`**, created by the toolkit; use the library's data-fetching layer
    for server data (§2) and thunks or listeners for other async logic.

## Pinia style
17. **A store is created when its `use` function is first called inside a component set-up** (or anything that runs
    in an active app). Calling it at module top level, before the plugin is installed, fails; outside a
    component, call it inside the function that runs after installation, or pass the instance explicitly.
18. **A set-up store returns every state property** it wants tracked. A property not returned is not state:
    it is skipped by devtools, hydration and serialisation, and a "private" state property is not possible.
    Do not return what is not store data (a router, an injected value): read those in the component.
19. **Never destructure state off a store**: the store is a reactive object and destructuring loses reactivity.
    Use the library's refs helper for state and getters; actions can be destructured, they are bound.
20. **Group several changes into one patch** (object or function form) for one devtools entry; the state cannot
    be replaced wholesale (assigning the state is turned into a patch).
21. **Cross-store use happens inside an action or getter**, not at the top of the file: call the other store's
    `use` function there. Two stores that import each other at top level create a cycle.
22. **On the server, pass the app's store instance** to `use` (or rely on the framework's integration) so state
    is not shared between requests (§1.7). Hydrate on the client from the serialised state.

## Mechanical checks

```
grep -rnE "mutate|\.push\(|\.splice\(|\+\+" src --include=*Slice.ts --include=*.slice.ts
grep -rnE "(fetch|axios|Date\.now|Math\.random|setTimeout)" src --include=*Slice.ts --include=*.slice.ts
grep -rnE "(const|let) \{[^}]+\} *= *use[A-Z][A-Za-z]*Store\(\)" src
grep -rnE "^const [a-z][A-Za-z]* *= *use[A-Z][A-Za-z]*Store\(\)" src
grep -rnE "return action\.payload|\.\.\.action\.payload" src
```

- A call from a slice file to the network, the clock or a random source is rule 12.
- A destructure of a `use...Store()` result is rule 19 unless it only takes actions.
- A top-level `use...Store()` is rule 17 outside a set-up function.
