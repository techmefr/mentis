# node-container-runtime §3 — Running TypeScript

There are three ways to get TypeScript to run: Node strips the types itself, a tool compiles ahead of time,
or a loader compiles on the fly. They differ in what syntax they accept, whether they type-check, and how
the framework in use reads metadata. Choose before writing the start command.

## 3.1 Node type stripping: what it is
1. **Node can run `.ts` files directly** by deleting the type annotations and doing nothing else. It is on by
   default from v23.6.0 and v22.18.0, prints no experimental warning from v24.3.0 and v22.18.0, and is
   stable from v25.2.0 and v24.12.0; `--no-strip-types` turns it off.
2. **It does not type-check.** Run the compiler in no-emit mode in CI for that.
3. **It ignores `tsconfig.json`.** Nothing in the file changes how the code runs.
4. **Only erasable syntax works.** Features that need generated code are not supported by stripping alone:
   enums, namespaces with runtime content, constructor parameter properties, and import aliases. The
   transform flag that once covered them was removed in Node 26 (v26.0.0): do not plan around it.
5. **Decorators are not supported**: they are a parse error, not a warning.
6. **Import specifiers must name the real file** with its extension (`./x.ts`), since there is no
   resolution step.

## 3.2 What that means for a Nest app
A Nest application depends on decorators, on `emitDecoratorMetadata` to get constructor parameter types for
injection, and conventionally on parameter properties for injected dependencies. Type stripping supports
none of the three. So:
1. **Build a Nest app with the Nest CLI** (tsc by default, SWC or Rspack optionally) and run the output.
   Do not run it through Node's type stripping.
2. **Do not enable `erasableSyntaxOnly` in a Nest project**: it forbids parameter properties and enums
   that the codebase uses.
3. **Type stripping is a good fit for** scripts, small tools, a migration runner, test helpers, and Node
   services that avoid decorators and injection by metadata.

## 3.3 SWC with Nest
1. **Fast, but unchecked.** `nest start -b swc` compiles with SWC and does no type-checking; add
   `--type-check` (runs the compiler in no-emit mode next to it) and keep the type check in CI.
2. **The SWC builder is preconfigured for Nest;** a custom `.swcrc` must keep `decorators: true` in the parser
   options, and the Jest transform needs the `legacyDecorator` and `decoratorMetadata` options as well.
3. **Circular imports behave differently.** The Nest recipe says SWC does not handle circular imports well:
   the reflection metadata saves the type of a property, so two files that import each other can hit a class that
   is not defined yet. Wrap the type with the documented wrapper type (the `Relation<>` pattern, a type alias
   of the type itself) so the type is not saved in the metadata; the recipe asks for the same wrapper on circular
   dependency injections.
4. **The CLI plugins** (Swagger introspection and similar) run under SWC only through `--type-check`, which
   produces a metadata file the application loads, or through the plugin metadata generator the recipe describes
   for the webpack builder and for Jest; see `nestjs-integration-patterns` §2.4.
5. **Newer Nest projects** use ES modules and Vitest by default and, as of Nest 12, monorepos default to the
   Rspack builder (the recipe says so); the SWC builder emits ES modules when `package.json` sets `"type":
   "module"`. Whether the scaffold also adds `.js` extensions to relative imports is not stated on the page read;
   check what the scaffold produced before copying an older config.

## 3.4 tsconfig flags worth setting
Pick a maintained base preset for the Node major (module `nodenext`, a `lib` matching the runtime, `strict`,
`skipLibCheck`) instead of writing one from scratch. Then consider, by project type:
1. **Plain Node code run by type stripping:** `rewriteRelativeImportExtensions`, `erasableSyntaxOnly` and
   `verbatimModuleSyntax` (TypeScript 5.8 or later); they make the compiler reject exactly what Node cannot
   run.
2. **Strictness beyond `strict`**, where the codebase can take it: `noUncheckedIndexedAccess` (an index read may
   be `undefined`), `exactOptionalPropertyTypes`, `noImplicitOverride`, `noPropertyAccessFromIndexSignature`,
   `noImplicitReturns`, `noFallthroughCasesInSwitch`. Turn them on one at a time; each one finds a class of
   bug, and `noUncheckedIndexedAccess` produces the most edits.
3. **`isolatedModules`** whenever a transpile-only tool (SWC, esbuild, Node itself) sits in the chain: it
   makes the compiler reject files that cannot be compiled one at a time.
4. **Do not copy a preset's `target`/`lib` above the runtime's support.** A newer `lib` type-checks calls the
   runtime does not have.

## 3.5 Verification
- The exact start command from the Dockerfile was run on a clean checkout and the service answered.
- CI runs a type-check separate from the build when the build tool (SWC, esbuild, stripping) does not check.
- For Nest on SWC: the app was started with a circular-import pair present and injected, and the DI
  resolved.

## 3.6 Nest mapping
Everything in §3.2 and §3.3 is the Nest mapping. See `nestjs-di-traps` for the injection mistakes metadata
makes visible, and `typescript-patterns` for type-level practice that is unrelated to how the code runs.
