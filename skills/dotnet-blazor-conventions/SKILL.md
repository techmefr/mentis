---
name: dotnet-blazor-conventions
description: "Use when writing or reviewing Blazor components (Server, WebAssembly or Auto): lifecycle methods and prerendering that runs OnInitializedAsync twice, JavaScript interop and DotNetObjectReference disposal, StateHasChanged from other threads, per-user state and circuits, component parameters and EventCallback, static server-rendered forms with antiforgery and validation, error display, and what HttpContext and DbContext can be used where."
---

# dotnet-blazor-conventions

Step 6 of the pipeline (`WORKFLOW.md`), for Blazor components. mentis has no other Blazor block, so this
one is new, not an extension. The premise: **a Blazor component runs in more places than it looks (the
server during prerendering, a circuit, the browser) and its lifecycle is driven by the framework, so code
that is correct on one render path is wrong on another**. General C# rules are in `dotnet-conventions`;
ASP.NET security configuration is in `dotnet-aspnet-efcore-pitfalls`.

## When
- Writing or reviewing a `.razor` component or its code-behind.
- Calling JavaScript from a component or .NET from JavaScript.
- A component loads data and flickers, or loads it twice.
- A form is rendered statically, or state is shared between users.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Lifecycle and prerendering: where to load data, double initialisation, render modes, async updates | a component loads data, or runs on more than one render mode | [`01-lifecycle-prerender.md`](./references/01-lifecycle-prerender.md) |
| 2 | JavaScript interop: timing, object references, invokable methods, call cost | a component touches the DOM, a JS library or a .NET callback | [`02-js-interop.md`](./references/02-js-interop.md) |
| 3 | State, parameters, forms, errors, services | state is shared, a parameter is changed, a form is posted, an error is shown | [`03-state-forms-services.md`](./references/03-state-forms-services.md) |

## Output / checkpoint
The component was run in its real render mode: refreshed once with prerendering on and the data loaded a
single time (§1), the page navigated away and back and the JavaScript handle was released (§2), two
browsers opened at once and neither saw the other's state (§3). A component that compiles is not verified.

## Guardrails
- Never call JavaScript before the first render completes (§2.1).
- Never keep per-user state in a singleton service on Blazor Server (§3.1).
- Never assign to a `[Parameter]` property inside the component (§3.2).
- Never show `exception.Message` to the user (§3.4).
- Versions: this block targets .NET 8 and later (render modes); each rule names a later version where it
  needs one. Nothing was run while writing it.
- Authentication and authorisation setup beyond the points here belongs to `dotnet-conventions` §3 and
  `security-hardening`.

## Origin
Rewritten from the Blazor documentation in the ASP.NET Core docs (CC-BY-4.0) and from MIT Blazor skill
files (read 2026-10-08). 🟡: never run by us; open points are in
[`references/origin.md`](./references/origin.md).
