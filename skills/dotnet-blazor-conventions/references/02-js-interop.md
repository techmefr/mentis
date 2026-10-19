# dotnet-blazor-conventions §2 — JavaScript interop

Applies to Blazor on .NET 8 and later.

## 2.1 Timing
1. **Call JavaScript from `OnAfterRenderAsync`, guarded by `firstRender` where the call is one-off, and
   from event handlers.** With prerendering, calling into JavaScript is not possible, and an element
   reference passed before the first render arrives in JavaScript as `null`.
2. **A call on a server circuit that has disconnected throws `JSDisconnectedException`.** During component
   disposal the circuit may already be gone; catch the exception in `DisposeAsync` so it is not logged.

## 2.2 Object references
1. **Dispose every `DotNetObjectReference` you create.** The documentation says to dispose it, normally in
   the component's disposal, to permit garbage collection and prevent a memory leak.
2. **Implement `IAsyncDisposable` when disposal calls JavaScript,** and await the call in `DisposeAsync`;
   the documentation's pattern for disposing a JavaScript module reference does this.
3. **Dispose the module reference too,** in the same method.

## 2.3 Invokable methods
1. **A .NET method called from JavaScript carries the `[JSInvokable]` attribute and must be public**
   (the documentation states this for static methods and uses public instance methods in its class-instance
   examples).
2. **Prefer an instance method on a `DotNetObjectReference` to a static one.** A static method is shared by
   every component and every user. This is our own guidance.
3. **Return quickly from an invokable method** and update the UI through `InvokeAsync` (§1.4).

## 2.4 Cost
1. **Batch interop calls coarsely.** The Blazor performance documentation has a page on JavaScript interop
   cost; one call carrying a whole object is cheaper than many small ones. Read it before optimising.
2. **Do not call JavaScript on every render.** Cache the result or call only when the input changed. This is
   our own guidance.

## Verification
- Navigate to the component and away 50 times; the number of live object references stays flat.
- The code has no JavaScript call in `OnInitializedAsync`.
