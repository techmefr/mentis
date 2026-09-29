---
name: laravel-layer-owned-config
description: Use when adding or changing configuration in an OSDD Laravel project (layer-package scaffolding) — a new settings file, a third-party package override, publishing a vendor config, or wondering where a config/ file belongs. There is no config/ at the project root; every layer carries its own, and an override posted from a provider's register() lands after the package already read its own settings, so it's silently dropped.
---

# laravel-layer-owned-config

Narrow follow-on to `skills/laravel-conventions` §7 and `skills/no-catch-all-layer` for an OSDD
Laravel project: this is the configuration half of the catch-all problem. Triggers on
`php artisan vendor:publish`, a new file under `config/`, `mergeConfigFrom`, a package setting that
looks ignored, and "où je mets ce config".

## When
Adding a settings file to an OSDD Laravel project, overriding a third-party package's config, or a
package setting that seems to have no effect even though the value was set correctly.

## Steps

### 1. Configuration lives inside the layer that answers for it
1. **No `config/` at the project root.** Each layer carries its own `config/`, including its own
   overrides of third-party packages — the authentication layer's `config/` carries `auth.php` and
   `jwt.php`, the tenancy layer's carries `tenancy.php`, and so on. The keys read exactly as before:
   `config('crm.sla.default_minutes')` doesn't change because the file moved.
2. **A root `config/` is settings living outside every layer** — the configuration form of the
   catch-all layer (`skills/no-catch-all-layer`): a layer that depends on a file that doesn't travel
   with it is not actually liftable on its own, and a root folder accumulates entries nobody answers
   for the same way a transverse layer accumulates classes nobody owns.
3. **A layer that carries its own config declares nothing** — no provider call registers it. The file
   is read because it exists in the layer's directory.

### 2. The load order is the part that isn't guessable
1. Layer config files are loaded from the bootstrap sequence, hooked to run right after the
   framework's own configuration load and **before any service provider is registered**.
2. **That ordering is why it works for third-party overrides, and why the opposite ordering fails
   silently.** A third-party package typically reads its own settings inside its own provider's
   `register()`. An override posted from *this project's* provider `register()` runs after that —
   the package has already read the old value, the new one is dropped, and nothing errors. The
   package simply runs on its defaults, which looks exactly like a bug in the package rather than a
   timing mistake in the override.
3. Two consequences: never override a package's config from a layer provider's `register()` or
   `boot()` — put the file in the layer's own `config/` instead; and the loader itself must resolve
   nothing from the container, because at that point the bindings a config loader would need don't
   exist yet.

### 3. Merge semantics don't change
1. A layer's config file **replaces** its top-level key, with the same exception the framework
   itself makes for a handful of arrays it merges rather than replaces (`auth.guards`/`providers`,
   `database.connections`, `filesystems.disks`, `cache.stores`, `logging.channels`, `mail.mailers`,
   `queue`/`broadcasting` connections) — two layers can each add their own entry to one of those
   without clobbering the other's.
2. The loader steps aside entirely once configuration is cached (`config:cache`), since everything
   has already been resolved into one file by then.

### 4. Guard it with a test, and test the values
1. **Assert there is no `config/` at the project root.** One line, and it's what keeps the rule from
   quietly decaying.
2. **Assert that the value a layer declares is the value the application actually reads — and
   compare values, not key presence.** Presence proves nothing: the framework posts its own defaults
   for `auth`, `database`, `queue`, `filesystems` and `cors` as soon as the root config is gone, so a
   layer whose config stopped loading would still show those keys present, backed by the framework's
   defaults rather than the layer's own. Compare the declared values against what `config()` actually
   returns, and serialize both sides of the comparison — a file returning a fresh object on each read
   (or a `DateInterval`, which the language itself refuses to compare) will otherwise report a
   mismatch that isn't real.

## Output / checkpoint
No `config/` directory exists at the project root. Every settings file sits under the layer it
belongs to, including third-party overrides, and a test compares declared values against what the
application reads rather than only checking key presence.

## Guardrails
- `vendor:publish` still writes to the project root by default — move the published file into the
  owning layer's `config/` immediately, don't leave it where the command put it.
- Never override a third-party setting from a layer provider's `register()` or `boot()` — it's too
  late, and the failure is silent.
- Don't recreate a root `config/` "just for the app-wide settings" — an application-wide setting
  still belongs to the technical layer that owns that concern.
- A key-presence test is not a passing test here — see §4.2.

## Origin
Mined from the org catalogue's `laravel` plugin, `layer-owned-config` (new file, commit shipping
2026-09-21, alongside the OSDD layer-naming and multi-tenancy work). Mechanism kept: no root
`config/`, per-layer config directories including third-party overrides, the exact load-order
argument (before providers register, so a provider-`register()` override is dropped silently), the
merge-semantics table, and the two-part test discipline (root-absence plus value comparison rather
than key presence). Genericised: the concrete PHPUnit test body from the source (a `glob()` over
declared layer buckets comparing `serialize()`d arrays) is described rather than reproduced verbatim,
since the exact bucket-configuration key it reads (`osdd.layers.paths`) depends on the specific
scaffolding package's own config surface, which this skill doesn't otherwise assume is installed.
Nothing else needed genericising — the source contained no internal names. Prose rewritten
throughout; no text copied from the source file.
