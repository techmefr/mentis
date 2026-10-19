# dotnet-blazor-conventions §3 — State, parameters, forms, errors, services

Applies to Blazor on .NET 8 and later.

## 3.1 State and lifetime
1. **No per-user state in a singleton service on Blazor Server.** A singleton lives for the app, so every
   circuit shares it (our inference from DI lifetimes); the documentation scopes per-user state to the
   circuit with scoped services.
2. **A scoped service lasts for the circuit,** not the request, so scoped and disposable transient services
   can live much longer than in a normal ASP.NET Core app. For a `DbContext`, the documentation recommends
   one context per operation from a factory (`IDbContextFactory<T>`) when several threads may touch the
   code, and notes that a scoped context is shared between components of the same user.
3. **Unsubscribe from service events in `Dispose`.** The documentation's state-container examples do this
   in the component's `Dispose`.

## 3.2 Parameters
1. **Do not write to a component's own parameters after the first render.** The documentation says
   parameters are a channel from parent to child and points to its page on overwriting parameters; copy the
   value to a private field and edit the copy.
2. **Use `EventCallback` and `EventCallback<T>` for event handling and binding component parameters.**

## 3.3 Forms
1. **A static server-rendered form needs a unique form name:** the `@formname` attribute, or the
   `EditForm.FormName` property. The model comes from the form through `[SupplyParameterFromForm]`.
2. **A plain `<form>` adds the `AntiforgeryToken` component;** an `EditForm` includes the antiforgery
   support for you.
3. **Add `DataAnnotationsValidator` when you validate with data annotations,** and repeat validation on
   the server side of any API the form calls; the browser is not a trust boundary. This is our own
   guidance.

## 3.4 Errors
1. **In production, do not render framework exception messages or stack traces in the UI.** They can
   expose sensitive information.
2. **Turn on detailed errors only in Development.** The Razor components option defaults to `false`; tie
   it to the environment.
3. **Use error boundaries** around components that can fail independently, so one fault does not take the
   page down.
4. **Show a stable message and log the detail** with a correlation id. This is our own guidance.

## Verification
- Open the app in two browsers and change state in one; the other is unchanged.
- Submit the static form with an empty required field; the validation message shows.
- Throw in a service and see the stable message, with the detail only in the log.
