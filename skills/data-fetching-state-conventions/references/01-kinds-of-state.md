# data-fetching-state-conventions §1 — The four kinds of state and where each lives

> Section 1 of `skills/data-fetching-state-conventions`. Read it when a value needs a home, or a store is about
> to receive a server response. The other sections and the guardrails stay in `SKILL.md`.

1. **Name the kind before choosing the tool.** Every value on a screen is one of four kinds, and each has one
   home:

   | Kind | Owner | Home | Survives reload | Shareable by link |
   |---|---|---|---|---|
   | Server state | a remote system | the query cache | by refetch | no |
   | URL state | the address bar | route params and query string | yes | yes |
   | Form state | the form being edited | the form library or the component | no (unless saved) | no |
   | UI state | the interface itself | the component, else a client store | no | no |

2. **Server state is a cache, not a copy.** It has an owner elsewhere, so it is always potentially stale. A
   server-state library replaces the connectors, action creators, reducers and loading flags that hand-written
   code needs for it, and what remains of global client state after moving server data out is usually small.
   The exception is an application with a large amount of synchronous client-only state (a visual designer, an
   audio editor): that needs a client store, and the query cache is still not a replacement for it.
3. **Never copy a server response into a client store.** The store then holds a snapshot with no expiry and no
   revalidation, and two sources of truth for one fact. Read the cache where the data is used; if a derived
   or merged view is needed, derive it from the cache read.
4. **State that should survive a reload or be shareable lives in the URL**: filters, sort, page, selected tab,
   selected id. Setting it through links and forms also makes it work on a server-rendered page. A store that
   mirrors the URL is a second source of truth.
5. **Do not put form state in a global store.** A half-typed form belongs to the form and is discarded with it;
   the Redux style guide lists form state as something to keep out of the store. Server validation errors
   arrive as a result and are rendered, not stored.
6. **Keep UI state as local as it can be.** A value used by one component stays in it; a value shared by a
   subtree is lifted to the common parent or provided through the framework's scoped mechanism (context,
   provide/inject); only state shared by unrelated parts of the application is a store. The test is whether two
   components would disagree if each kept its own copy.
7. **On a server-rendering framework, module-level state is shared by every request.** A store or variable
   written during a request is read by the next user. Scope state to the request (a per-request client or
   context) and see §2.9. This is a data-leak class, not a performance note.
8. **Derive, don't duplicate.** A value computable from other state is a getter, a derived value or a selector,
   never a second stored field that must be kept in sync. Store the minimal original and derive the rest.
9. **Make the status a state, not a boolean pile.** `idle`, `loading`, `success`, `failure` (or the library's
   equivalent) is one value; `isLoading`, `isError`, `hasData` as independent booleans can contradict each
   other. A disabled query is a fifth situation (no data, not fetching) that the screen must still render.
10. **One mechanism per kind per project.** Two ways to fetch, or two stores for the same kind, is a migration
    in progress or a defect; ask which before adding a third. Reuse before creating (`skills/code`).

## Mechanical checks

```
grep -rnE "(setState|set[A-Z][A-Za-z]+|commit|dispatch)\(.*\b(data|response|result)\b" src
grep -rnE "useEffect\(.*fetch|onMounted\(.*(fetch|axios)" src
grep -rnE "^(export )?(let|const) [a-z][A-Za-z]* *= *(ref|reactive|\\\$state|signal)\(" src/stores src/lib 2>/dev/null
grep -rnE "localStorage|sessionStorage" src
```

- A server response assigned to a store field is the finding of rule 3 unless the store is the query cache.
- A module-level reactive value in a server-rendered application is rule 7 until proven client-only.
