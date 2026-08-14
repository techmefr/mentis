# react-nextjs-conventions §6 — Server state and stores

> Section 6 of `skills/react-nextjs-conventions`. Read it when TanStack Query, Zustand or RTK. The other sections and the guardrails stay in `SKILL.md`.

1. Reach for the ecosystem's server-state library (TanStack Query, SWR, RTK Query) rather than
   `useEffect` + `useState` for anything cached, deduped or invalidated. A hand-rolled cache is the part
   that's always subtly wrong.
2. **Query keys through a central factory**, never literal arrays scattered across files: an invalidation
   only matches if the key is built the same way in both places, and a typo silently invalidates nothing.
3. **Split the mutation callbacks by concern**: cache invalidation belongs in the hook (it's part of the data
   contract), UI feedback like a toast belongs in the calling component (it's part of that screen). Toasts
   fired from inside the hook appear on screens that never asked for them.
4. Prefer the callback form (`mutate` with `onSuccess`/`onError`) over `await mutateAsync` wrapped in
   `try`/`catch`: a bare `await mutateAsync` without a catch is an unhandled rejection waiting to happen.
5. Read a store through **atomic selectors**, one value per call, never by destructuring the whole store
   object: destructuring subscribes the component to every field and re-renders on all of them.
6. A store is for state genuinely shared across unrelated components; everything else stays local.
7. Where the project's server-data layer is Redux Toolkit rather than Query/Zustand: one slice = a typed
   `createSlice` (typed `initialState`, `PayloadAction<T>`, never an `any` action); typed
   `useAppDispatch`/`useAppSelector` wrappers, never the raw hooks in components; `createAsyncThunk` with
   `rejectWithValue` so the slice can tell a business rejection from an exception; a memoised
   `createSelector` for anything derived; RTK Query rather than a homemade thunk for standard cached CRUD.
