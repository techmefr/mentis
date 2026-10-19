# § 10 — Assurance level: decide it once, review against it

A review that asks every possible security question of every application produces a long list nobody
closes. The mechanism that keeps the list honest is to **state the assurance level the application
needs, once, in the spec, and review only against that level.**

1. **The spec names the level.** One line, owned by whoever owns the risk, chosen from the levels the
   security standard in use defines (a web or mobile verification standard, or the organisation's own
   baseline). The default for an ordinary application is the standard's base level; an application handling
   money, health data or similar is raised deliberately and the reason is written down.
2. **The level is a property of the application, not of the diff.** A diff never lowers it. A change that
   would need a higher level than the one declared (a first payment feature in an application declared at
   the base level) stops and asks for the declaration to be revisited before the code is written.
3. **The review checklist is the chosen standard's controls for that level and the ones below it, nothing
   else.** Do not mix in the controls of a higher level as findings: raise them as one question about the
   declared level. Do not drop a base-level control because the application is "internal".
4. **Controls that raise the cost of attacking the binary (tamper detection, obfuscation, root detection)
   are an optional extra profile, never a substitute for a base control.** They slow an attacker and
   protect nothing by themselves; this block already treats them as advice (§8).
5. **Record the level in the checkpoint.** The verification summary (§5) names the level it was checked
   against, so a later reviewer knows which controls were in scope.

**Sources:** the verification standards for web and mobile applications published by OWASP (read as a
taxonomy of control groups and levels, 2026-10-02; the text is share-alike licensed and none is reproduced
here); the mechanism of declaring the level once is the part kept.
