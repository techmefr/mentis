# § 2 — Stack patterns: Laravel and Nuxt

> Section 2 of `business/data-protection`. Read it when the checklist in `SKILL.md` and
> `references/01-cnil-france.md` has settled *what* is required, and the question becomes *how* to
> build it in a Laravel backend or a Nuxt/Vue frontend.

**These are illustrative patterns to adapt, not a certified implementation.** Written without
internal legal expertise, same as the rest of this block (`business/README.md`): they show one
concrete way to wire a requirement into code, not the only way, and not one a DPO/legal sign-off can
be skipped on the strength of. Adapt the shape to the project's actual schema, stack version and
threat model before trusting it.

1. **Anonymising/pseudonymising a user record (Laravel).** A deletion request (step 3 of the router `SKILL.md`) often can't be a hard `DELETE` — foreign keys from orders,
invoices or audit trails point at the row, and removing it breaks referential integrity or destroys
records you're legally required to keep for accounting purposes. Anonymising in place — overwriting
the identifying fields while keeping the row and its relations intact — is the common answer. A
model method plus an Artisan command wrapping it, so it's both callable from code (a queued job
reacting to a deletion request) and runnable manually:

```php
final class User extends Model
{
    public function anonymise(): void
    {
        $this->forceFill([
            'name' => 'Deleted user #' . $this->id,
            'email' => 'deleted-' . $this->id . '@anonymised.invalid',
            'phone' => null,
            'address' => null,
            'date_of_birth' => null,
            'avatar_path' => null,
            'password' => Hash::make(Str::random(40)),
            'anonymised_at' => now(),
        ])->save();

        $this->notifications()->delete();
        $this->sessions()->delete();
        $this->tokens()->delete();
    }
}
```

```php
final class AnonymiseUserCommand extends Command
{
    protected $signature = 'users:anonymise {user : ID of the user to anonymise}';

    public function handle(): int
    {
        $user = User::query()->findOrFail((int) $this->argument('user'));

        if ($user->anonymised_at !== null) {
            $this->comment("User {$user->id} is already anonymised.");

            return self::SUCCESS;
        }

        $user->anonymise();

        $this->comment("User {$user->id} anonymised.");

        return self::SUCCESS;
    }
}
```

Two things this sketch leaves for the real implementation to settle, deliberately not answered here:
what "identifying field" means for the project's actual schema (free-text fields — support tickets,
order notes — routinely carry a name or an email that this method won't touch unless it's taught to),
and whether the search index / cache / analytics events already emitted for that user also need a
matching purge — the CNIL guidance in §1 (`references/01-cnil-france.md`) treats "the record survives
elsewhere" as the normal way a deletion fails silently.

2. **Cookie/tracker consent (Nuxt).** The CNIL rule in `references/01-cnil-france.md` point 3 — refuse as easily as accept, no script fires
before consent, revocation stays reachable — translates into three concrete requirements on a Nuxt
app: a categorised list of trackers (not a single accept/reject toggle), a load gate that keeps
non-essential scripts out of the DOM until their category is granted, and a persistent way back into
the choice.

```ts
export type ConsentCategory = 'necessary' | 'analytics' | 'marketing'

export const useConsent = () => {
  const consent = useState<Record<ConsentCategory, boolean>>('consent', () => ({
    necessary: true,
    analytics: false,
    marketing: false,
  }))

  const hasDecided = useState<boolean>('consent-decided', () => false)

  const load = () => {
    const stored = localStorage.getItem('consent')

    if (stored) {
      consent.value = { ...consent.value, ...JSON.parse(stored) }
      hasDecided.value = true
    }
  }

  const save = (categories: Partial<Record<ConsentCategory, boolean>>) => {
    consent.value = { ...consent.value, ...categories, necessary: true }
    hasDecided.value = true
    localStorage.setItem('consent', JSON.stringify(consent.value))
  }

  const revoke = () => {
    hasDecided.value = false
    consent.value = { necessary: true, analytics: false, marketing: false }
    localStorage.removeItem('consent')
  }

  return { consent, hasDecided, load, save, revoke }
}
```

```vue
<script setup lang="ts">
const { consent, load } = useConsent()

load()
</script>

<template>
  <Head>
    <Script
      v-if="consent.analytics"
      src="https://analytics.example.com/script.js"
      defer
    />
    <Script
      v-if="consent.marketing"
      src="https://ads.example.com/pixel.js"
      defer
    />
  </Head>
  <ConsentBanner />
</template>
```

`ConsentBanner` presents "accept all" / "refuse all" as two controls of identical weight and size —
the symmetry `references/01-cnil-france.md` point 3 asks for is a layout decision as much as a code
one — plus a link into a settings view that calls `revoke()`, reachable from the footer at any time
rather than only on first visit. An accessible, non-color-only way to distinguish the two buttons
matters here too (`skills/accessibility`).
3. **Scheduled purge / retention job (Laravel).** A retention period named in `references/01-cnil-france.md` point 2 needs a mechanism that actually runs, not a comment in a policy
document. The Laravel scheduler plus a command per retention rule keeps each rule visible and
independently testable:

```php
final class PurgeStaleProspectsCommand extends Command
{
    protected $signature = 'gdpr:purge-stale-prospects';

    public function handle(): int
    {
        $cutoff = now()->subYears(3);

        $prospects = Prospect::query()
            ->whereNull('converted_at')
            ->where('last_contacted_at', '<', $cutoff)
            ->get();

        foreach ($prospects as $prospect) {
            $this->comment("Purging prospect {$prospect->id}, last contact {$prospect->last_contacted_at}.");
            $prospect->delete();
        }

        $this->comment("Purged {$prospects->count()} stale prospects.");

        return self::SUCCESS;
    }
}
```

```php
$schedule->command('gdpr:purge-stale-prospects')->daily();
```

The `3 years` cutoff here is the CNIL prospect-retention figure from `references/01-cnil-france.md`
point 2 — written as a named, searchable constant tied to its source in the real project
(`RetentionPeriod::PROSPECT_INACTIVITY` or equivalent), not a bare `subYears(3)` a future reader has
no way to trace back to a regulation. One retention rule per command keeps the `gdpr:*` namespace as
the single place someone audits when asked "what do we actually delete, and when."
4. **Keeping personal data out of logs and exception reporters.** Same reasoning as `SKILL.md` step 3 point 4 and `skills/auth-session-conventions` §2.1/§2.4 for credentials:
logs and third-party exception reporters have wider read access and longer retention than the system
that produced the data, and a serialised request body or a stack trace is exactly where personal
data leaks in without anyone deciding to export it.

**Laravel**: scrub fields before they reach the exception reporter, at the `bootstrap/app.php`
exception-handling configuration (or `App\Exceptions\Handler` on older versions) rather than trusting
every call site to redact manually:

```php
->withExceptions(function (Exceptions $exceptions) {
    $exceptions->dontFlash(['password', 'password_confirmation', 'token']);

    $exceptions->reportable(function (Throwable $e) {
        $e->context = collect(request()->all())
            ->except(['email', 'phone', 'address', 'date_of_birth'])
            ->all();
    });
})
```

**Nuxt**: the same discipline on the client-side error/monitoring integration — a `beforeSend` hook
that strips known personal-data fields from the event payload before it leaves the browser, rather
than relying on the monitoring vendor's own scrubbing defaults:

```ts
Sentry.init({
  beforeSend(event) {
    if (event.request?.data) {
      delete event.request.data.email
      delete event.request.data.phone
      delete event.request.data.address
    }

    return event
  },
})
```

Both sketches need the same follow-up as `SKILL.md` §3.4: check what the framework's own request
logger writes on its own (Laravel's query log, a Nuxt server middleware logging incoming requests)
— the exception-reporter hook above doesn't touch a separate logging pipeline that serialises the
same request.

## Guardrails specific to this section
- **None of the four patterns above is a certified implementation.** Each one needs adaptation to
  the project's real schema, and a DPO/legal review of the resulting behaviour — this section
  shows the shape, not a shippable diff.
- **Never treat "we wrote the purge command" as "the retention rule is enforced.**" A scheduled
  command that isn't wired into the scheduler, or that silently stops running, produces exactly the
  false confidence `references/01-cnil-france.md` point 2 warns about.
- **Never assume the exception-reporter scrub in point 4 above** is the only export path — a query
  logger, an analytics event, a webhook payload can each carry the same data through a different
  pipe.
