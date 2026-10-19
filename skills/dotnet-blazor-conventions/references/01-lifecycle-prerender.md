# dotnet-blazor-conventions §1 — Lifecycle and prerendering

Applies to Blazor on .NET 8 and later, where prerendering of interactive components is on by default for
server-side apps.

## 1.1 Where work goes
1. **Load data in `OnInitializedAsync`** (or `OnParametersSetAsync` when it depends on a parameter that
   can change). Do not block on a task inside a lifecycle method.
2. **Do not touch JavaScript there.** Calling into JavaScript is not possible during prerendering; use
   `OnAfterRenderAsync` (see §2.1).
3. **Keep lifecycle methods awaited.** A method that starts work and returns without awaiting it hides its
   exceptions and renders before the data is there. This is our own guidance.

## 1.2 Prerendering runs initialisation twice
1. **A prerendered component renders twice: once for prerendering and once when it becomes interactive,**
   and `OnInitializedAsync` is called twice. A data or service call in it runs twice, and the page flashes
   from loaded to loading to loaded.
2. **Persist the prerendered state** with `PersistentComponentState`. On .NET 10 and later the
   `[PersistentState]` attribute on a property does this; on earlier versions register a persisting callback
   on `PersistentComponentState` and read the persisted value first, loading only when it is missing.
3. **Avoid non-idempotent work in initialisation** (a request that writes, a started timer): it runs on
   both passes. This is our own guidance.

## 1.3 Render modes
1. **Know the mode a component runs in.** Interactive Server uses a circuit; Interactive WebAssembly runs
   in the browser; Interactive Auto starts on the server and uses WebAssembly on later visits after the
   bundle downloads, and it never switches a component already on the page. Components with the Auto or
   WebAssembly mode are built in a separate client project.
2. **A component that can run in the browser cannot reach server-only services.** Reach server data through
   an HTTP API or through an abstraction with a server and a client implementation. Do not inject a
   `DbContext` into such a component. This is our own guidance following from where the code runs.
3. **`HttpContext` is not available in interactive components.** Use the authentication state and cascaded
   values, or read what you need in a static component and pass it down.

## 1.4 Updating the UI
1. **Call `StateHasChanged` through `InvokeAsync`** when the change comes from outside Blazor's
   synchronisation context, such as a timer or a notification from a service.
2. **Do not discard the task with `_ = InvokeAsync(...)`.** An exception in it is lost. Await it, or wrap
   the body in a try and log. This is our own guidance.

## Verification
- Refresh the page with prerendering on and count the loads in the data service log: one.
- Raise an event from a background task and see the UI update without an exception.
