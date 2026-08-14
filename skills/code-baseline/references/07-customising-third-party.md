# code-baseline §7 — Customising a third party

> Section 7 of `skills/code-baseline`. Read it when a vendor file, template or component needs changing. The other sections and the guardrails stay in `SKILL.md`.

1. **Changing a package's, framework's or generator's behaviour by copying and editing its file, or
   replacing it outright, is the last resort — not the first move.** Narrowest first: a single config
   key/flag, a documented config file, a documented file-override hook, a wholesale file replacement,
   forking/patching the vendor code. Stop at the first tier that reaches the goal.
2. **Investigate before overriding, every time**: identify the exact package and version, read its docs
   for config keys/env vars/lifecycle hooks/extension points, and if the docs are thin, read the source
   — how it loads user config, at which layer a default applies (build vs runtime, merge vs whole-file
   replace). Skipping straight to "just replace the file" is usually a config key not yet found.
3. **A whole-file override that only replaces part of the upstream file is a latent bug**: it silently
   drops whatever else the package's default provided, surfacing far from the edit that caused it. A
   whole-file replacement reproduces the upstream file faithfully and changes only what's needed.
4. **When wholesale override genuinely is the answer** (confirmed from the docs or source that no
   narrower hook exists), say so in the code or the PR — the sentence that proves the investigation
   happened is what stops the next reader from re-deriving it, or reflexively "fixing" it back to a
   config key that was already ruled out.
5. **The tells that this rule was skipped**: copying a default/template file verbatim to change one
   line; editing a file inside a package/dependency directory directly; a duplicated upstream template
   that will drift the moment the package updates; reaching for "replace the whole thing" without having
   checked for a config key first.
