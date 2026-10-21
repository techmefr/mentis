# symfony-conventions — origin and source stamps

> Provenance of `skills/symfony-conventions`. Read it when a rule has to be traced back to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

Block created 2026-10-02, every rule from a document **read that day**. A fact not found in a read source was
left out rather than recited.

| Source (public repository, read 2026-10-02) | Licence | Used for |
|---|---|---|
| Symfony documentation (`symfony/symfony-docs`): the best-practices article, the security chapter (login CSRF, login throttling, access control, role hierarchy; read by search of the chapter, not end to end), the deployment chapter, the messenger chapter (worker sections only) | CC BY-SA 3.0 (the repository `LICENSE`, read) | §1 and §2. **Idea only**: the share-alike licence would carry over to any reused wording, so every rule is restated in the house voice and no sentence, example or structure is copied. |

**Verification pass 2026-10-20, from framework source only.** The share-alike documentation was not re-opened.
Read instead the Symfony framework source on its 7.4 branch (`symfony/symfony`, MIT, `LICENSE` re-read:
Fabien Potencier, 2004-present): the access map (first matching rule wins, confirms §2.3), the password hasher
factory (the `auto` setting builds a migrating chain starting with the native hasher, not "the strongest
available": §2.2 reworded), the login-throttling factory (defaults 5 attempts, 1 minute, a global limiter at
five times: added to §2.6), the form login authenticator (the CSRF option is off by default and adds the CSRF
badge only when on: §2.6), the role hierarchy voter (hierarchy expansion happens in the voter, confirms §2.5 in
substance), the entity value resolver (a non-nullable argument without a match throws a not-found exception,
a 404: §1.10), the messenger consume and stop-workers commands (memory and time limits exist; the help text says
workers are not restarted automatically and that this belongs to a process control system; stop-workers
finishes the current message then exits: §2.10), and the dependency injection definition class (private and not
autowired by default in the source, which supports §1.6; the default services file that turns autowiring on for §1.5 was not read). Still
unverified from a permissive source and resting only on the earlier share-alike read: §1.1 to §1.4, §1.7 to
§1.9, §1.11 to §1.14, §2.1, §2.4, §2.7 to §2.9 (the deployment order). Nothing was run.

**Read but not used for rules:** the Doctrine chapter was read for migrations only (nothing added beyond
`skills/sql-conventions`); the controller, configuration and testing chapters were not read end to end. Not read:
PHP-CS-Fixer, PHPStan and its Symfony extension, Psalm, the Symfony Demo application, the Doctrine ORM
documentation. No rule here is claimed for them, so static analysis and code-style tooling are not covered; write
the section when those sources are read.

**Version stamp.** The documentation repository was read on its default branch; its pages track the current
Symfony release and the page text does not carry the version, so none is pinned. The attribute names, the
default hasher and the name of the entity resolver have moved between majors; check against the installed
version before applying a point. Expiry: at each Symfony major (`skills/source-freshness` §2.1) re-read §1.7
to §1.10 and §2.2 first.

**Status.** 🟡, "base to confront with the real thing", like `go-conventions`. Nothing here was run against a
Symfony project.

Independent verification 2026-10-21: 10 checked, 10 matched, 0 corrected, 0 unverified. All ten against the 7.4 framework source (hasher chain order native, sodium, pbkdf2; throttling 5 per 1 minute and a global limiter at five times; form login CSRF off; first-match access map; 404 on a missing entity; worker limits; private services by default)
