# code-baseline §7 — Customising a third party

> Section 7 of `skills/code-baseline`. Read it when a vendor file, template or component needs changing. The other sections and the guardrails stay in `SKILL.md`.

1. **Changing a package's, framework's or generator's behaviour by copying and editing its file, or
   replacing it outright, is the last resort — not the first move.** Narrowest first: a single config
   key/flag, a documented config file, a documented file-override hook, a wholesale file replacement,
   forking/patching the vendor code. Stop at the first tier that reaches the goal.
2. **The ladder is ordered by what the next upgrade costs.** A config key is read by whatever version is
   installed, so an upgrade carries it forward for free; a copied file was written against one specific
   upstream version, so every upgrade is a manual merge somebody has to notice is due. That is rule B in
   `CONVENTIONS.md` — the third party's breaking change should hit one file, and each tier down the ladder
   widens the surface it hits.
3. **Investigate before overriding, every time**: identify the exact package and version, read its docs
   for config keys/env vars/lifecycle hooks/extension points, and if the docs are thin, read the source
   — how it loads user config, at which layer a default applies (build vs runtime, merge vs whole-file
   replace). Skipping straight to "just replace the file" is usually a config key not yet found.
4. **Compose before you change.** Where the goal is to add behaviour rather than alter it, the vendor object
   goes inside one of yours and the extra work happens around it. That keeps the upstream code untouched and
   the addition greppable, and it is available at every tier — including the ones where an override would
   otherwise look necessary.
5. **A whole-file override that only replaces part of the upstream file is a latent bug**: it silently
   drops whatever else the package's default provided, surfacing far from the edit that caused it. A
   whole-file replacement reproduces the upstream file faithfully and changes only what's needed.
6. **A copied file is a fork of whatever guarantee that file carried** (§8.4). It freezes at the moment it
   was copied, so an upstream security fix, an accessibility correction or a bug fix inside it never
   arrives — and nothing anywhere reports that. The copy keeps working, which is precisely why nobody
   revisits it.
7. **An override by copy pins the version it was written against.** Left on a floating constraint, the
   upstream file moves underneath the copy and the two silently disagree; the override then either stops
   having an effect or reintroduces a behaviour the upgrade removed. Pin it, and treat the pin as the
   reminder that the override exists.
8. **Never edit inside the dependency directory.** That tree is not versioned and is rebuilt by the next
   install, so the change works on the machine that made it, disappears in CI, and reappears as a bug that
   only one person cannot reproduce. If the vendor code genuinely must change, it is a tracked patch or a
   fork — something the install reproduces.
9. **Runtime monkey-patching is the invisible tier.** Reassigning a method or replacing a class at boot does
   change the behaviour and leaves no trace in the file whose behaviour changed, so the next person
   debugging that file cannot find the cause from the file. Where a language makes it easy, it is still the
   tier below a fork, not above a config key.
10. **The cheapest override is the one that stops being an override.** Where the project takes
    contributions, the missing config key or hook is often a small change upstream, and once released the
    local workaround is deleted rather than maintained. That is worth ten minutes of assessment before
    committing to carry a patch indefinitely.
11. **When wholesale override genuinely is the answer** (confirmed from the docs or source that no
    narrower hook exists), say so in the code or the PR — the sentence that proves the investigation
    happened is what stops the next reader from re-deriving it, or reflexively "fixing" it back to a
    config key that was already ruled out. Name the **version** you read, because "no hook exists" is a
    statement about one version and stops being true without warning.
12. **A fork or patch needs its exit condition written down.** Record what upstream change would let it be
    dropped, and check that on each upgrade; without it the fork is permanent by default, and the reason it
    was taken leaves with whoever took it.
13. **Assert the behaviour the override buys.** A config key that stops being read, a hook that is renamed,
    a copied template whose upstream contract moved — each fails silently, and the thing that notices is a
    test on the *outcome*, not on the setting. That is §8's asymmetry in a dependency: a declared override
    that no longer does anything is worse than none, because it answers the question nobody re-asks.
14. **Generated code you were meant to own is not an override at all.** Where a tool's contract is
    "scaffold once, then it's yours", editing the output is the intended path — but it is then application
    code, on this repo's rules, and no upstream fix will ever reach it either (point 6 applies unchanged).
15. **The tells that this rule was skipped**: copying a default/template file verbatim to change one
    line; editing a file inside a package/dependency directory directly; a duplicated upstream template
    that will drift the moment the package updates; reaching for "replace the whole thing" without having
    checked for a config key first.
