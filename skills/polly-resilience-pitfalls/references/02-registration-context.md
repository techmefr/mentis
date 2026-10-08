# polly-resilience-pitfalls §2 — Registration and context

Applies to Polly v8 with the dependency injection integration.

## 2.1 Services inside a pipeline
1. **Use the `AddResiliencePipeline` overload that gives you the service provider.** The documentation lists
   accessing the `IServiceCollection` instead of the `IServiceProvider` as an anti-pattern: calling
   `BuildServiceProvider` inside the builder builds a new provider before each retry attempt, and the
   alternate overload `(builder, context)` exposes `context.ServiceProvider` and reuses the one already built.
2. **Resolve options through the context helpers** (`context.GetOptions`, `context.EnableReloads`) when the
   pipeline's settings should reload with configuration.

## 2.2 Sharing data between strategies
1. **Use the `ResilienceContext` for per-call data.** It is rented from `ResilienceContextPool.Shared`
   and carries properties for the strategies. The documentation says it is resource-intensive to create, so
   the pool exists to reuse it.
2. **Return the context to the pool when finished.** The documentation calls this recommended, not
   required: it reduces allocations, and skipping it after an exception is acceptable.
3. **Do not share mutable state through a closure between concurrent calls.** This is our own guidance;
   the context carries data per call.

## 2.3 Named pipelines
1. **Register pipelines by key** with `AddResiliencePipeline("key", ...)` and resolve them by that key
   (including through keyed services). One definition serves many callers. The `AddResiliencePipelines`
   method does not support keyed services.
2. **Keep pipeline settings in named options,** so a change of retry count or break duration is
   configuration, not a code edit; dynamic reload is supported through the context.
3. **Pipelines registered through the DI integration are created once per key and reused.** Do not build a
   new pipeline per request. This is our own reading of the registry design; confirm it for your version.

## 2.4 HTTP clients
Attach the pipeline to an `HttpClient` through the resilience handler extensions rather than wrapping each
call site, and do not stack it on top of a second retry handler (`dotnet-conventions` §8).

## Verification
- The service provider is built once in the process.
- Two concurrent calls with different context values each see their own.
