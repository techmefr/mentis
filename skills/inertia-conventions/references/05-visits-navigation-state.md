# § 5 — Visits, navigation and the deployed app

> Section 5 of `skills/inertia-conventions`. Read it when navigation is written, when a page has to keep
> something across a visit, or when the app's behaviour after a deploy is in question.

1. **Navigation between pages goes through `<Link>` or `router.visit()`, not a plain `<a href>`.** An
   anchor does a full browser navigation: the whole bundle boots again, every shared prop is recomputed,
   and any in-memory state in the app is gone. Nothing errors, so this is a defect that only shows up as
   slowness — and it shows up worst on the slow connection you are not testing on.
2. **A `<Link>` is a `GET` by default, so a destructive action needs the method stated** (§3.12). Give it
   the verb and render it as a button rather than an anchor: a link that deletes is reachable by anything
   that follows links, and it is also the wrong element for a keyboard reader, who is told it navigates.
3. **Two visits fired in a row do not both land — Inertia cancels the one in flight.** That is what makes
   a search-as-you-type box correct without any work: only the last request's response renders. A
   hand-rolled `axios` call in the same place has no such rule, so a slower earlier response can arrive
   last and the reader sees results for a prefix of what they typed. This is the concrete reason §1.2's
   shadow endpoint is not merely redundant.
4. **A visit resets the scroll position to the top unless it is told to preserve it.** Changing a filter
   on a long table therefore throws the reader back to the top of the page, away from the control they
   just used. Preserve scroll on any visit that re-renders the page the reader is already reading, and
   leave the default on a visit that genuinely moves somewhere else — landing halfway down a new page is
   just as disorienting in the other direction.
5. **A visit re-renders the page component with fresh props, and local component state is reset unless
   it is preserved.** An open accordion, a partially typed field, a selected row: all gone after a
   filter change, because from the framework's point of view the component was recreated. Preserving
   state is the fix for a page that visits itself; for state that must survive a real navigation or a
   refresh, the URL (§1.9) or the server is the place, not the component.
6. **Inertia compares an asset version on every visit, and a mismatch turns the visit into a full page
   load.** That is the mechanism that gets the reader onto the new frontend after a deploy: without it,
   a browser that has been open across the deploy keeps running the old bundle against the new server
   and fails in ways nobody can reproduce — a prop the old code doesn't know about, a route that moved.
   So the version has to be wired to something that actually changes when the assets change (the build
   manifest's hash), and a version that is a hardcoded string is the same as having none.
7. **The visit's URL is the reader's state, and the back button is a feature you either support or
   break.** Anything the reader would expect to find again — the filter, the tab, the page number — has
   to be in the URL; anything transient — an open dropdown, a hover — must not be, or the back button
   becomes a way to close a menu. A visit that replaces the history entry instead of pushing one is the
   right choice for a refinement of the current page, and the wrong one for a navigation.
8. **The page's data is kept in the browser's history entry, so it outlives the session.** After a
   logout, the back button can restore a rendered page — with its props — from history without asking the
   server anything, which on a shared machine means the next person can read it. Where a page carries
   anything the logout is supposed to end access to, the history has to be encrypted or cleared on
   logout; treating logout as purely a server-side event is what leaves it readable.
9. **Server-side rendering is optional and separate, so by default a page is an empty shell to anything
   that does not run JavaScript.** A crawler, a link preview, a scraper or a reader with scripting
   blocked gets the app's skeleton and no content. That is fine for an authenticated internal app and
   not fine for a public page that is supposed to be indexed or shared — and the decision is a deploy
   decision (a second process to run and monitor), not a flag to flip in a diff.
10. **Prefetching a link issues the real request.** It is a genuine speedup for a page the reader is
    likely to open next, and a bug for a `GET` route with a side effect — a hover then records a view,
    consumes a token, or marks something read without a click. It also multiplies load: a table of two
    hundred prefetching rows is two hundred requests the server did not see before.
11. **A section that has to stay live is a partial reload on an interval, not a `fetch`.** Reloading the
    one prop keeps the page's single data path (§1.2), goes through the same authorization, and stops
    when the page does. A hand-rolled poller usually outlives the component that started it, and the
    request that arrives after the reader navigated away renders into nothing — or worse, keeps a
    session alive that would otherwise have expired.
12. **A visit has no visible progress unless the progress indicator is mounted.** Inertia ships one and
    it is the reason a click feels like it did something; a page that removed it, or a visit configured
    to skip it, leaves the reader with a dead-looking interface for the length of the request. If a
    specific visit is fast enough not to warrant the bar, say so per visit rather than removing it
    globally.
13. **A visit that fails at the network layer is not a validation failure and has no error bag.** The
    dropped connection, the 500, the expired session (§3.13) all end the visit with the reader still on
    the old page and nothing changed on screen. Decide what that looks like once, at the app level,
    rather than in each form: silence is the default and it is indistinguishable from success.
14. **`router.reload({ interval })` is point 11's interval reload as a first-class option, not a
    hand-rolled `setInterval`.** It still needs the same decision point 11 already asks for — what a
    section polls, and whether it's worth the request — but it stops automatically when the component
    unmounts, which is exactly the leaked-poller failure a hand-rolled one risks. It composes with `only`
    (§2.3): poll the one section, not the whole page, every interval.
15. **`<Link prefetch>` is point 10's hover-prefetch made declarative, and it adds two triggers point 10
    didn't have: mount and a stated cache duration.** `prefetch="mount"` issues the request as soon as the
    link renders, which is right for a link the reader is virtually certain to follow next (a wizard's
    "continue") and wrong for one of many in a list — the mount trigger does not wait for a hover signal
    at all, so it multiplies point 10's request-count warning by every link on the page rather than only
    the ones actually hovered.
