# rust-conventions — origin and source stamps

> Provenance of `skills/rust-conventions`. Read it when a rule has to be traced back to its source or checked
> for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡, base to be confronted with a real Rust project.** No production Rust experience in house stands
behind this block; the rules are the mechanisms of three published guideline sets, read in their repositories
on **2026-10-02** (shallow clone, pinned commits below), rewritten in the house voice. No text is copied.

| Source | Pinned at | Licence | What was taken |
|---|---|---|---|
| Rust API Guidelines (the language project's library-design checklist) | commit `97a0969`, 2025-07-07 | MIT or Apache-2.0 (both licence files present), rewritten with this credit | naming and conversion conventions, common traits, type-safety (newtypes, builders, flags), dependability (validation, destructors), future-proofing (sealed traits, private fields), predictability, documentation sections, `Debug`, features naming. Read: naming, interoperability, macros, flexibility, type-safety, dependability, debuggability, future-proofing, necessities, predictability, documentation chapters. |
| Pragmatic Rust Guidelines (a software company's public guideline book) | commit `19723b3`, 2026-09-25 | MIT | universal, correctness (unsafe, unsound, panics), library UX, interop, resilience, building, performance, project, macros, FFI, apps, docs, and the AI-specific items. Read: the checklist and the guideline files named in sections 1 to 7 above (several reviewed in full, a few only their first lines). |
| Secure Rust development guide, national cybersecurity agency of France (ANSSI) | commit `3f9e2e2`, 2026-05-18 | Licence Ouverte 2.0 (reuse with attribution), rewritten with this credit | toolchain and cargo rules, errors and panics, integer overflow, dependency vetting and audit, unsafe encapsulation, memory leaks and raw pointers, `Drop`, FFI. The rule list and the body of about forty rules were read. Its **tests and fuzzing chapter is a stub in this snapshot** and is not a source. |

**What was left out, and why.**
- *Rust Design Patterns* (MPL-2.0) and the Rust Book, Reference, Nomicon and style guide: **not read** in this
  pass, so nothing is attributed to them. The block cites the formatter and the linter only by command name and
  defers to the project's own configuration (§6.4).
- Cargo-deny, supply-chain vetting tools and fuzzing tooling: the *categories* come from the guides above; no
  tool-specific rule was invented from memory.
- Async cancel safety, holding locks across awaits, `tokio`-level advice, property-test libraries: no primary
  source read in this pass, so there is no rule; a future pass with the async book and the runtime docs may add
  them.
- One Pragmatic item was reversed on purpose: the guide asks for a *comment* beside each magic value. The house
  rule on comments wins (a named constant, whose name carries the reason); see `skills/code-baseline`.
- Where the strictest source is a security-critical profile (no `mem::forget`, no leaks, no `unwrap`), the
  block says "in a security-critical profile" and does not make it the default for ordinary code (§3.10).

**Volatile content, to re-check at the next pass:** the lint lists and tool names in §6.2, the edition and
minimum-compiler advice in §6.1, the allocator and CPU-target advice in §7.8. These are taken from the
Pragmatic guideline snapshot above and move with each compiler release.

**Crossings with other blocks.** `security-hardening` for the supply-chain background and the
undefined-behaviour classes; `testing-anti-patterns` for the general test doctrine; `observability-
instrumentation` for the logging doctrine; the two C-family blocks (`c-conventions`, `cpp-conventions`) cover
the same hardening ground from the other side, in the section they share.
