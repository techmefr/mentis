# nestjs-node-conventions §2 — DTOs and validation: the HTTP boundary

> Section 2 of `skills/nestjs-node-conventions`. Read it when an input shape, a pipe or a typed exception is written. The other sections and the guardrails stay in `SKILL.md`.

1. One DTO per input shape (`CreateUserDto`, `UpdateUserDto`), decorated with `class-validator`
   (`@IsString()`, `@IsEmail()`, `@IsOptional()`...). Never an `any` or an untyped object as a controller
   parameter.
2. A global `ValidationPipe` (`app.useGlobalPipes(new ValidationPipe({ whitelist: true,
   forbidNonWhitelisted: true }))`) rather than a pipe placed route by route. Add `transform: true` as
   soon as any DTO validates query params (a paginated list's `page`/`limit`, for instance): Express
   delivers query values as strings, so a `@IsInt()` field paired with `@Type(() => Number)` only
   converts before validation when `transform` is on — without it, every such route fails validation
   permanently, not just on bad input.
3. Typed HTTP exceptions (`NotFoundException`, `ConflictException`, `BadRequestException`...) are thrown
   on the service side, never on the controller side; the service knows the business rule that justifies
   the status, the controller doesn't.
4. **Schema validation is a first-class alternative in Nest 12.** A `StandardSchemaValidationPipe` validates
   with any Standard Schema library (Zod, Valibot, ArkType) and passes the schema's output (coerced, defaulted,
   transformed) to the handler; it only touches parameters that declare a schema, so binding it globally is
   safe. A project chooses classes with `class-validator` or schemas, per module or globally, not both for one
   shape. How unknown keys are treated is the schema's decision, not the pipe's.
5. **Transformation is what converts path and query strings.** With `transform` on, primitives are converted by
   the declared type; with it off, convert explicitly with `ParseIntPipe`, `ParseBoolPipe`, `ParseUUIDPipe`,
   `ParseEnumPipe`, `DefaultValuePipe`. There is no string pipe, since the values already are strings.
6. **An exception thrown by a pipe never reaches the handler** and is handled by the exceptions layer: the
   pipe is the right place to reject data at the system boundary.
7. **Production may hide validation detail**: the pipe's option to disable error messages avoids describing
   the schema to a caller. Decide it per environment and record it.
