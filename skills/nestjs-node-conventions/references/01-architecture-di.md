# nestjs-node-conventions §1 — NestJS: module, controller and service architecture

> Section 1 of `skills/nestjs-node-conventions`. Read it when a module, a controller, a service or its injection is written or reviewed. The other sections and the guardrails stay in `SKILL.md`.

1. One module per business domain (`UsersModule`, `OrdersModule`...), declared with its explicit
   `providers`/`controllers`/`exports`. No business logic in the module itself.
2. The controller only routes and serialises: it receives the validated DTO, calls the service, returns
   the result. No business rule, no direct Prisma access in a controller.
3. Dependency injection through the constructor only (`constructor(private readonly usersService:
   UsersService) {}`). Never a `new Service()`: it breaks the Nest lifecycle and the DI graph becomes
   unverifiable.
4. `forwardRef()` as a last resort only, when a circular dependency between two modules really is
   unavoidable. Before reaching for it, check whether splitting a module removes the cycle.
5. Tests through `Test.createTestingModule({...}).compile()`, never a manual service instantiation in a
   unit test, so the DI graph stays the same as in production (mock the injected providers, not the
   service under test).
6. The current Nest CLI scaffold (`@nestjs/cli new`) ships as ESM (`"type": "module"`,
   `moduleResolution: "nodenext"`): every relative import needs its explicit `.js` extension
   (`from './users.service.js'`), including between `.ts` files — the extension is a TypeScript/Node
   module-resolution requirement, not a build artifact to strip. And with `isolatedModules` +
   `emitDecoratorMetadata` both on by default, a non-class type (an interface, a type alias) used in a
   decorated method's signature — most often a controller's return type — must be brought in with
   `import type`, or the build fails with `TS1272`; a DTO class doesn't need this since it exists at
   runtime.
