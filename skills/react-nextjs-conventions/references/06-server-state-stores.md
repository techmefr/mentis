# react-nextjs-conventions §6 — Server state and stores

> Section 6 of `skills/react-nextjs-conventions`. Read it when TanStack Query, Zustand or RTK. The other sections and the guardrails stay in `SKILL.md`.

1. Reach for the ecosystem's server-state library (TanStack Query, SWR, RTK Query) rather than
   `useEffect` + `useState` for anything cached, deduped or invalidated. A hand-rolled cache is the part
   that's always subtly wrong — not in the fetch, which is easy, but in the race between two mounts, the
   response that arrives after the component unmounted, and the invalidation nobody remembered.
2. **Server state and client state are different kinds of thing.** Server state has an owner elsewhere and
   is therefore always potentially stale; client state is authoritative because nothing else writes it.
   Copying a query result into a store collapses the distinction and makes you responsible for a freshness
   guarantee you cannot honour — the store now holds a snapshot with no expiry and no way to know it is
   wrong.
3. **Query keys through a central factory**, never literal arrays scattered across files: an invalidation
   only matches if the key is built the same way in both places, and a typo silently invalidates nothing.
   The factory is also where the naming convention of §2.13 can actually be enforced, rather than hoped for.
4. **Every input the query depends on belongs in its key.** A filter, a page number, a sort column or a
   tenant identifier left out of the key means two genuinely different requests share one cache entry, so
   changing the filter shows the previous filter's rows — and the bug is intermittent, because it only
   appears when the earlier result is still fresh.
5. **`staleTime` is a decision about the data, not a tuning knob.** Left at its default, a query refetches
   on every mount and the screen flickers on each navigation; set generously on a figure that has to be
   right — a balance, a stock level, a permission — it shows a stale number confidently. Choose per
   resource, and know which of the two failures you are accepting.
6. **Invalidate; do not hand-write the cache.** Writing the mutation's response into the cache duplicates
   whatever shaping the server does, and the two versions disagree the first time a computed field is added.
   Where an optimistic update is genuinely warranted, it comes with the rollback and the final
   reconciliation — an optimistic write without a rollback path leaves the UI asserting something the server
   refused.
7. **Split the mutation callbacks by concern**: cache invalidation belongs in the hook (it's part of the data
   contract), UI feedback like a toast belongs in the calling component (it's part of that screen). Toasts
   fired from inside the hook appear on screens that never asked for them, including background refetches
   the user did not initiate.
8. Prefer the callback form (`mutate` with `onSuccess`/`onError`) over `await mutateAsync` wrapped in
   `try`/`catch`: a bare `await mutateAsync` without a catch is an unhandled rejection waiting to happen,
   and in a form submit handler it also skips whatever reset or navigation followed it.
9. **A dependent query is gated by `enabled`, never by a conditional hook call.** `if (id) useQuery(...)`
   breaks the rules of hooks (§5.1); `enabled: Boolean(id)` expresses the same intent and keeps the hook
   order fixed. Remember that the gated query is then in a fourth state — not loading, not error, not
   success — and the UI has to say something about it.
10. **A query error is a state, not an exception.** It renders (§5.6) and it decides its own retry policy: a
    default retry on a 401 or a 403 hammers the endpoint on behalf of a user who will never be allowed
    through, and turns one authorisation failure into a rate-limit incident.
11. Read a store through **atomic selectors**, one value per call, never by destructuring the whole store
    object: destructuring subscribes the component to every field and re-renders on all of them. The
    subtler form of the same mistake is a selector that builds a new object — `s => ({ a: s.a })` fails the
    equality check every time it runs, so it re-renders on every store change including the ones it was
    meant to filter out.
12. A store is for state genuinely shared across unrelated components; everything else stays local. The test
    is not "is it used twice" but "would two components disagree if each kept its own copy" — and with
    server data fetched on the server (§7), the answer is often that no client store is needed at all.
13. **The store owns its transitions.** Components dispatching named actions keep every invariant in one
    file; components reaching in and assigning fields spread the rules across the call sites, and then no
    single place can state what a valid state is.
14. **A store is not an event bus.** A boolean flipped in one component, read in another and reset by a
    third is a message passed through shared memory: nothing records who sends it or who must react, and the
    ordering only works by accident. Pass a callback, or lift the state to the common parent.
15. **A persisted store is a schema in someone else's browser.** Writing state to storage means a returning
    user hydrates last month's shape into this month's code, so the persisted slice is versioned with a
    migration — and it never carries a token or personal data, since storage is readable by any script on
    the origin (§9.15).
16. Where the project's server-data layer is Redux Toolkit rather than Query/Zustand: one slice = a typed
    `createSlice` (typed `initialState`, `PayloadAction<T>`, never an `any` action); typed
    `useAppDispatch`/`useAppSelector` wrappers, never the raw hooks in components; `createAsyncThunk` with
    `rejectWithValue` so the slice can tell a business rejection from an exception; a memoised
    `createSelector` for anything derived; RTK Query rather than a homemade thunk for standard cached CRUD.
