# § 3 — Every state, not the happy path

> Section 3 of `business/interface-design`. Read it for any screen or component that loads or displays
> dynamic data, while drawing it or while checking that a mockup is complete.

**Scope first**: this applies only to a screen or component that **loads or displays dynamic data** — a
list, a table, a dashboard, search results, a detail fetched from a server. A purely static screen (an
information page, an empty form with no loading) is out of scope, and demanding states on one is noise
that gets the whole checklist ignored.

Each state has its own **obligation condition** — they are not four boxes to tick:

1. **Loading — mandatory as soon as data is fetched.** No exceptions; the network is not optional. What
   the reader sees without it is the previous screen, or an empty one, for as long as the request takes,
   and the two are indistinguishable from a broken app — so the reliable outcome is a second click and,
   where the action writes, a second write.
2. **Error — mandatory as soon as data is fetched**, covering network, server and permission failures.
   The three are different messages: unreachable is worth retrying, a server failure is worth reporting,
   and a permission failure is not an error the reader can fix by trying again. Collapsing them into one
   message is how a user spends ten minutes retrying something they will never be allowed to see.
3. **Empty — mandatory only where the data *can* be empty** (a list, a search, a filtered table). Not
   required for data that is always present. The distinction matters because an empty state drawn for
   data that cannot be empty is dead surface nobody maintains, and its presence is what makes a reader
   treat the whole list of required states as optional.
4. **Success — mandatory only where there is a user action to confirm** (saving, sending). Not required
   on a read-only screen: silence after a click is indistinguishable from a failure, but there was no
   click.

Two quality rules on top, and they're where these states usually fail:

5. **An empty state offers a way out.** Never stop at "no data": say why it's empty and offer the exit —
   create the first item, clear the filters, change the search. The reason is that the two empty states
   look identical and mean opposite things: nothing exists yet, or everything is filtered out. Without
   the reason, a reader with an active filter concludes their data is gone.
6. **An error message says what to do.** Never stop at "an error occurred": point at an action — retry,
   go back, contact support. A message with no action leaves the reader's only option as reloading the
   whole application, which discards anything unsaved elsewhere on the screen.
7. **A partial failure is a state, and it is the one nobody draws.** A screen assembling several sources
   — a header, a list and a summary panel — can have one of them fail while the others render. Left
   unspecified, the implementation shows a complete-looking screen with one section silently stale or
   empty, which is worse than an error page because nothing tells the reader a number is missing. Say per
   region whether it fails alone or takes the screen with it.
8. **The states have to be reachable while the mockup exists**, not only enumerated in a note. A state
   described in prose next to a drawing of the populated screen is a state whose layout nobody has
   checked: the usual discovery at step 6 is that the empty state has no room for its message, or the
   error row is wider than the column it sits in.
9. **A state that replaces the screen loses what the reader had.** Swapping a table for a full-screen
   error throws away the filters they set and the scroll position they reached; putting the error where
   the rows were keeps them. Which of the two a state does is a decision, and the mockup is where it is
   cheap to make.
10. **A loading state that shifts the layout is a loading state that costs a misclick.** Content
    arriving and pushing the page down under a cursor already in motion is the mechanism, and the visible
    result is the reader activating whatever landed where they were aiming. Reserving the space is the
    fix, and reserving it is only possible if the loading state was drawn at the size of the real one.

**Deliberately not decided here**: the *visual* form of each state — skeleton versus spinner, the exact
anatomy of an empty state, whether success is a toast, inline or a redirect. That's a level of
specification below this one, and pinning it at mockup time over-constrains the implementation. The
code-side blocks own the mechanics (`flutter-conventions` §4, `react-nextjs-conventions` §5.6,
`skills/accessibility` for how the state is announced).

A mockup showing only the populated screen is an incomplete mockup, not a mockup plus details: these
states are where the implementation questions come from, and leaving them out means they get answered by
guesswork at step 6.
