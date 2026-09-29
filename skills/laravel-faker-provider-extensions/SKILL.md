---
name: laravel-faker-provider-extensions
description: 'Use when a factory definition(), a factory state or a seeder is about to carry generation LOGIC instead of one Faker call per attribute — string concatenation, str_pad/sprintf building a reference, random_int/Str::random/Arr::random, a hand-typed array of domain values, a case-changing wrapper around a Faker call, or a uniqueness retry loop: write a Faker Provider extension instead.'
---

# laravel-faker-provider-extensions

Narrow trigger extracted from `skills/laravel-conventions` §7.47–§7.51, so a factory attribute
carrying generation logic routes here directly instead of only through the whole Laravel block.

## When
Writing or reviewing a factory `definition()`, a factory state, or a seeder, where one attribute's
value needs more than a single generator call to produce.

## Steps
1. **A factory attribute is one Faker call.** The moment it needs logic — concatenation, a retry
   loop, a hand-typed vocabulary array, `ucfirst()`/`strtoupper()` wrapped around a call — that logic
   moves into a `Faker\Provider\Base` subclass, in the project, on the spot.
2. **Register the provider once, through a service provider's `boot()`** (`$faker->addProvider(new
   ...)`), never inside the factory, the seeder, or a test's `setUp()` — registering per-call or
   per-test leaks the provider into every test that runs after the first one in the same process.
3. **Keep helper methods `private`/`protected`.** Every public method on the provider becomes a
   generator (`$faker->yourMethod()`); an internal helper made public is callable, and collidable,
   the same way.
4. **Check the bundled and locale `fakerphp/faker` providers before writing your own.** A value that
   only looks plausible (an unchecked digit string standing in for something with a real check digit
   or format) is a fixture that silently drifts from what the application's own validation rules
   require.
5. **Seeders follow the same rule.** Falling back to an inline string when no provider covers a value
   reintroduces the problem one call site removed from the factory.

## Output / checkpoint
No factory or seeder attribute in the diff builds its value with anything beyond one generator call
and its modifiers (`unique()`, `nullable()`, a regex/format constraint) — every attribute needing
logic resolves to a provider method, registered once.

## Guardrails
- This is the generation-logic half of `skills/laravel-conventions` §7's config/commands/seeders/
  factories section — read §7.47–§7.51 for the full argument and the collision risk.
- `laravel-idempotent-seeders` and `laravel-seed-new-features` cover what a seeder's rows must do;
  this skill covers what generates the values those rows carry.
- A user override ("just inline it, this is a throwaway repro") wins without argument — this is a
  default for new code, not a rule to enforce against an explicit instruction.

## Origin
Mined from an org skill catalogue's Laravel plugin (a `custom-faker-extensions` skill and a paired
`faker-extensions` skill, shipped 2026-09-24), rewritten around the public `fakerphp/faker`
extension mechanism (`Faker\Provider\Base`, `addProvider()`) rather than the source's own internal
Faker fork — that package's kebab-cased-registry-collision and `extra.faker`-composer-key mechanics
are specific to a proprietary package this repo doesn't carry and don't generalise (rule C); the
mechanism kept is the one that transfers to any `fakerphp/faker` project: factories stay a column-to-
generator map, and generation logic lives in a registered provider. The source's explicit behaviour
change — a seeder no longer allows inline generation as a fallback — is kept as point 5. Written
2026-09-29.
