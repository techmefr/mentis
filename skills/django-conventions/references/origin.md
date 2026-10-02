# django-conventions — origin and source stamps

> Provenance of `skills/django-conventions`. Read it when a rule has to be traced back to its source or checked
> for freshness (`skills/source-freshness`), never to apply a rule.

Block created 2026-10-02, every rule from a document **read that day** (rule B: mechanisms rewritten in the house
voice, no prose copied). A fact not found in a read source was left out rather than recited.

| Source (public repository, read 2026-10-02) | Licence | Used for |
|---|---|---|
| The Django documentation, development branch (`django/django`, `docs/`; version file reads 6.2 alpha): deployment checklist, security topic, database-optimization topic, transactions topic, migrations topic, signals topic, QuerySet reference, CSRF reference, middleware reference, testing overview, `django-admin` reference, raw SQL topic | BSD-3-Clause (the repository `LICENSE`, read) | §2 to §4, and the test points of §5. Rewrite with credit. |
| A public Django style guide (`HackSoftware/Django-Styleguide`): services, selectors, models, APIs and serializers, URLs, settings layout, error handling, Celery, testing | MIT (its `LICENSE`, read) | §1 and §5 and the settings layout in §4. Rewrite with credit; the structure is flagged as one team's preference in the block. |
| PostgreSQL documentation for `CREATE INDEX` (`postgres/postgres`) | PostgreSQL licence (permissive) | §3.6: concurrent index build, invalid index, not inside a transaction block. |

**Read but not used for rules:** the Django REST framework documentation was not read, so no rule here is claimed
for it beyond what the style guide's API chapter says about serializers in general. The cookiecutter project
template (BSD-3) and the version-upgrade tool (MIT) from the veille were not read. The OWASP Django cheat sheet
(CC BY-SA) was not read. The style guide's long error-handling "approach 1 / approach 2" comparison was read for
its principles only (§5.4, §5.5); its code is not reproduced. Left out: caching, internationalisation, the admin,
authentication backends and password-hashing policy (a separate topic: `skills/auth-session-conventions`).

**Version stamp.** Development docs at Django 6.2 alpha. Features marked recent in the block (a fetch mode for
related objects, the mailer setting in the deployment checklist, which is deliberately not cited) exist only there.
Expiry: when the project's Django major changes (`skills/source-freshness` §2.1) re-read §2.3, §3 and §4.1 first.

**Status.** 🟡, "base to confront with the real thing", like `go-conventions` for a technology new to the repo.
Nothing here was run against a Django project.
