# nestjs-integration-patterns §3 — Dynamic modules, discovery, lazy loading

A reusable module needs options, may need to find other providers by metadata, and may be loaded late. The
principle: **make the options a provider under a token, discover by metadata rather than by name, and
treat lazy loading as a cold-start tool with a lifecycle of its own**.

## 3.1 Dynamic modules
1. **Static `forRoot`/`register`/`forFeature` conventions carry meaning.** `register()` configures a module
   for the caller that imports it (each import gets its own config). `forRoot()` configures it once and
   shares it across the app. `forFeature()` adjusts what `forRoot` configured, for the importing module.
   Each has an `*Async` form taking a factory, a class or an existing provider.
2. **A dynamic module returns** `{ module, providers, exports, ... }`, and the options object is registered as
   a provider (`useValue`) under an injection token that consumers inject.
3. **Do not hand-write the boilerplate.** `ConfigurableModuleBuilder` produces the module class, the options
   token, and the sync and async option types; `setClassMethodName` and `setFactoryMethodName` rename the
   methods, and `setExtras` adds module-level flags such as `isGlobal` that are kept out of the options.
4. **Async options take exactly one of** `useFactory`, `useClass`, `useExisting`; supplying two is an error.
5. **Async registration is how config enters**: options derived from validated configuration (see
   `node-container-runtime` §2) arrive through a factory with injected dependencies, never by reading the
   environment inside the module.
6. **Keep the token private** unless consumers must read the options; export a typed accessor instead.
7. **Global modules are a last resort**: they hide the dependency. Use them for infrastructure every module
   needs (config, logging) and nothing else.

## 3.2 Discovery
1. **When a module must find providers by marker** (every handler decorated for a job, an event, a health
   check), do not maintain a registry by hand. Import the discovery module and use the discovery service to
   list providers or controllers, filtered by metadata.
2. **Create the marker with** the discovery service's decorator factory, then read it back with
   `getMetadataByDecorator`; the decorator's `KEY` is the metadata key when you filter yourself.
3. **Run the scan once at bootstrap** (module init), not per request. Providers are resolved by then.
4. **Scan only what you need**: pass an `include` list of modules when the app is large.
5. **A scanned provider may be non-singleton** (request- or transient-scoped); its instance is not
   available at the scan. See `nestjs-di-traps` for scope behaviour.

## 3.3 Lazy loading
1. **What it is for**: serverless and worker entry points where cold-start time matters, loading a rarely
   used module on first need. Not for a long-lived monolith.
2. **`LazyModuleLoader.load(() => Module)` is cached** after the first call; loading again returns the
   same module reference.
3. **Lifecycle hooks do not run** in a lazy module (`onModuleInit`, `onApplicationBootstrap` and shutdown
   hooks). Initialise explicitly.
4. **Lazy modules cannot be global**, and global enhancers do not apply to them.
5. **Do not put entry points in one**: controllers, resolvers, gateways and middleware in a lazy module do
   not behave: Fastify cannot add routes after it is ready, broker transports must subscribe before the
   connection, and a code-first GraphQL schema needs every class registered up front. Lazy modules hold
   services only.
6. **Libraries that depend on module init fail**, e.g. a per-class injected logger from a library that
   registers at init.

## 3.4 Verification
- The module was imported with `register`/`forRoot` once with literals and once with `forRootAsync` and
  an injected config, and both started.
- Providing both `useFactory` and `useClass` was tried and rejected.
- A lazy module was loaded twice and its initialisation ran as intended (explicitly, once).

## 3.5 Nest mapping
This section is entirely Nest. The transferable idea is "configuration is a dependency, injected through a
token, not read from ambient state".
