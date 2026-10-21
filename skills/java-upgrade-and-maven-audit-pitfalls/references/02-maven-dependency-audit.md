# java-upgrade-and-maven-audit-pitfalls §2 — Maven dependency audit

Source: the Maven dependency audit skill of the claude-code-java repository (MIT, commit 0d98fe9, read
2026-10-16), rewritten.

## 2.1 Order of an audit
1. **Four steps**: list outdated dependencies, analyse the tree, scan for known vulnerabilities, write one
   prioritised report. Run them separately and summarise; do not paste a whole tree.
2. **Run it before a release, after a security advisory and on a regular schedule** (the skill says monthly).
3. **Check plugins as well as dependencies**; the same versions plug-in has a report for plugin updates.

## 2.2 Reading the updates
1. **Categorise by what the change implies**: a security fix first (update at once), a major change (read the
   changelog and test thoroughly), a minor change (usually safe, test), a patch (safe, little testing).
2. **Order security findings by severity band**: critical (9.0 to 10.0) at once, high (7.0 to 8.9) within days,
   medium (4.0 to 6.9) within weeks, low at convenience. The score bands are the standard qualitative ratings of the common vulnerability scoring system (FIRST
   specification, version 3.1); the timings are the skill's own policy.
3. **A scan has three options in the skill**: a dependency-check plug-in producing an HTML report (recommended),
   a dependency report from the analysis plug-in, and the hosting platform's alerting. Add the scan plug-in to the
   build only after the user agrees to the dependency.

## 2.3 Reading the tree
1. **Look for two versions of one library under different parents.** In the tree output, "omitted for conflict"
   means Maven chose one version and dropped the other, and Maven's rule is the nearest definition to your
   project in the tree, not the newest, so an older copy can win over a fixed one; "omitted for duplicate" is the same version and no
   problem. Two versions of a library are a run-time risk because only one is on the classpath.
2. **Filter by the library you are chasing** with the includes option rather than reading the whole tree, and use
   the same filter to find why a transitive dependency is present.
3. **Run the analysis goal for undeclared and unused dependencies.** "Used undeclared" means code relies on a
   library that only arrives transitively; "unused declared" is a candidate for removal. The analysis is a
   candidate list, not an order: check reflection and runtime-only use before removing.

## 2.4 Fixing a conflict
1. **Pin one version in a dependency-management section** when two parents disagree; every module then gets the
   same one. Check that the version you pin is compatible with the parent that wanted the other.
2. **Exclude a transitive dependency** on the declaring dependency when you want it absent (the skill's example
   is a legacy logging artifact). State why in the review, since the exclusion changes what is on the classpath.
3. **Update strategy for production is conservative**: patches freely, minors with basic testing, majors with a
   migration plan. The aggressive "use latest releases" goal is for active development only and is paired with
   the plug-in's commit or revert goals so it can be undone; the selective form takes an includes filter for
   one group.

## 2.5 The report
Fields the skill lists: project, date, dependency count; security issues (dependency, current, advisory
identifier, severity, fixed-in version); major updates with notes; minor and patch updates; conflicts with the
version that won; unused dependencies; recommendations split into immediate, this sprint and planned.
