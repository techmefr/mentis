# symfony-conventions — origin and source stamps

> Provenance of `skills/symfony-conventions`. Read it when a rule has to be traced back to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

Block created 2026-10-02, every rule from a document **read that day**. A fact not found in a read source was
left out rather than recited.

| Source (public repository, read 2026-10-02) | Licence | Used for |
|---|---|---|
| Symfony documentation (`symfony/symfony-docs`): the best-practices article, the security chapter (login CSRF, login throttling, access control, role hierarchy; read by search of the chapter, not end to end), the deployment chapter, the messenger chapter (worker sections only) | CC BY-SA 3.0 (the repository `LICENSE`, read) | §1 and §2. **Idea only**: the share-alike licence would carry over to any reused wording, so every rule is restated in the house voice and no sentence, example or structure is copied. |

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
