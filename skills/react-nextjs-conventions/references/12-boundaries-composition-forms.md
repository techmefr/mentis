# react-nextjs-conventions §12 — Boundaries, composition, context, forms and refs

> Section 12 of `skills/react-nextjs-conventions`. Read it when a failure or a loading state has to be
> contained, a component takes children or slots, a context is introduced, a form is built, a portal or a
> ref is used, or an external store is subscribed to. Hooks and effects are §5, server state is §6, the
> server/client split is §7. The other sections and the guardrails stay in `SKILL.md`.

1. **Decide where state lives by asking who needs it.** Used by one component: local state. Needed by a
   parent and its children: lift it to the nearest common parent. Needed deep in a subtree and rarely
   changing: context. Server data: the query library (§6). Shared by unrelated screens and changing often:
   a store. Derivable from any of these: not state at all (§5, point 2). Moving state up "in case" is how a
   whole page re-renders on a keystroke.
2. **A failure is contained by an error boundary placed where the user can recover.** An uncaught render
   error unmounts the whole tree down to the nearest boundary, so without one a failure in a chart blanks the
   page. Put a boundary around each region that can fail independently (a widget, a route segment, a list
   item that renders foreign content), give it a fallback that says what happened and offers a retry that
   resets the boundary, and report the error with its component stack to the monitoring tool. Boundaries do
   not catch errors in event handlers, asynchronous code or the server render; those need their own handling.
3. **Suspense and the error boundary come as a pair.** A boundary that suspends needs a fallback that has the
   shape of the content (a skeleton of the real layout, so nothing jumps), placed around the part that
   suspends and not the whole page, and a sibling error boundary for the case the promise rejects. A
   suspending component with no boundary above it reaches the root and replaces the whole screen with the
   fallback.
4. **An external store is subscribed to with the dedicated hook.** A value that lives outside React
   (a browser API, a global store, a media query) is read with the external-store subscription hook, which
   keeps every component on one consistent snapshot during concurrent rendering and supplies a server
   snapshot for hydration. A hand-written effect that copies the value into state tears under concurrent
   rendering and flashes the wrong value on first paint (§5, point 19).
5. **Children and slots over configuration props.** A component that takes `children` (or named slots as
   props that are elements) is composed by its user; a component that takes a growing list of flags to
   switch parts on and off is a configuration language nobody can read. When the variants differ in
   structure, make them separate components that share a smaller one.
6. **A compound component shares its internal state through a context that only its parts read.** A tabs,
   menu or accordion family is a parent that owns the state and parts that consume it, so the user composes
   the markup and the parts stay consistent. The context's hook throws a clear error when used outside the
   parent, as the state is otherwise `undefined` three levels down. The parts are exported together under the
   parent's name or from one module.
7. **A context carries one concern and changes rarely.** A value that changes on every interaction put in a
   context re-renders every consumer, so a context holds configuration, the current user, the theme, or a
   stable object of actions; frequently changing state goes to a store with selectors (§6). Split a context
   whose consumers need different halves, and keep the provider's value stable (§5, point 18).
8. **Prefer composition to inheritance and to cloning children.** Reuse comes from functions, hooks and
   components that take other components; never from a class hierarchy of components. Reaching into the
   children to clone them with injected props couples the parent to the child's props and breaks on a
   wrapper; pass a render prop, a context or a slot instead.
9. **A form field is controlled or uncontrolled, and the choice is made per form.** Uncontrolled fields,
   read from the submitted form data, are the default for a form that validates on submit: no state per
   keystroke, no re-render. Controlled fields are for what must react on every change (a live preview,
   dependent fields, input masking). A form library owns the state of a complex form (§5, point 5) and the
   components do not duplicate it. Switching a field between the two modes during its life is a bug the
   framework warns about.
10. **Validation runs on the client for the user and on the server for the system.** The client's schema
    shows messages early; the server revalidates the same shape and is the only one that counts. Errors are
    shown next to the field with the accessible association (`skills/accessibility`) and the focus moves to the
    first invalid field on a failed submit; the submit button stays enabled and the pending state is shown
    on it (§5, point 21).
11. **A ref is for what React does not own.** Focus, scroll position, measurement, a media element's
    methods and a third-party widget's instance live in refs. Reading or writing a ref during render makes the
    render impure; do it in an event handler or an effect. Passing a ref to a child uses the framework's
    current ref-as-prop form on recent versions and the forwarding wrapper on older ones; check which the
    project's React major supports before writing either.
12. **A portal renders elsewhere in the DOM and stays in the React tree.** Modals, popovers and tooltips are
    portalled to escape overflow and stacking contexts. Events still bubble through the React tree, not the
    DOM tree, so a click inside a portalled dialog reaches the handlers of its React ancestors. Focus
    trapping, escape-to-close, scroll lock and restoring focus on close are the component's job and are
    tested (`skills/accessibility`), which is the argument for using the component library's dialog (§8).
13. **An identity-changing key resets state on purpose.** Changing the `key` of a component remounts it with
    fresh state; use that to reset a form when the record changes instead of an effect that copies the new
    props into old state (§5, point 2). An unstable key (a generated value on each render) resets the
    component on every render and loses focus.
14. **A custom hook has one job and a name that says it.** It composes other hooks, returns what the caller
    needs and nothing more, and does not hide a side effect behind a name that sounds like a read. A hook used
    by one component stays in that component's file until a second user appears.
15. **Lazy-load by route and by weight, with a boundary.** A heavy component that is rarely shown (an editor,
    a chart library, a map) is loaded on demand through the framework's dynamic loading and sits inside a
    Suspense boundary with a real fallback (§10). Lazy-loading a small component adds a request and a flash
    for no saving.
