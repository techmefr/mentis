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

## Source pass 2026-10-20 (every point below was re-opened against the page named, own words, no text copied)

The three guideline repositories named above were re-opened at the same pinned commits (still the latest on their default branches at the time of reading: 97a0969, 19723b3, 3f9e2e2) and each rule file below was read again against the points it is credited for. Instruction files inside the cloned repositories were not opened or followed.

| Source | Licence | What it confirmed or corrected |
|---|---|---|
| Pragmatic Rust Guidelines, files under src/guidelines (correctness, universal, libs/ux, libs/interop, libs/building, libs/resilience, docs, ai, performance, project, macros) | MIT (LICENSE.md read), read 2026-10-20 | panic, unsafe, soundness, builders (4 or more permutations, up to 2 optional parameters by inherent methods), wrappers, ladder of dependencies, statics, Send, async fn, yield points, future size, docs sections, first sentence of 15 words, structured logging, features, MSRV, edition, lints, workspace, performance files, macro files |
| Rust API Guidelines, src/checklist.md, naming.md, interoperability, predictability, type-safety, dependability, future-proofing | MIT or Apache-2.0 (both licence files read), read 2026-10-20 | casing, acronyms, crate name suffix, word order, conversions, getters, iterators, common traits, serde feature, Send and Sync, no out-parameters, operators, Deref, sealed traits, private fields, feature names |
| ANSSI secure Rust guide, en/devenv.md and en/integer.md | Licence Ouverte 2.0 (LICENSE.md read), read 2026-10-20 | Cargo.lock tracked (rule DENV-CARGO-LOCK), debug-assertions and overflow-checks not overridden, checked operations |

### Verified in this pass
1. 1: items 1, 3, 5, 7 to 11, 13 to 19. 2: items 1 to 4, 6 to 12. 3: items 1 to 7 and 16. 4: items 1 to 11 and 13. 5: items 1, 2, 3, 4, 5, 7 to 11. 6: items 1, 2, 3, 5, 6, 7, 10. 7: items 1 to 7 and 9 to 11.

### Corrected in this pass
1. 1 item 6: the builder threshold is four or more permutations (two optional parameters can stay inherent methods), the builder is named after the type, setters take the field name and required inputs go to the builder constructor.
2. 7 item 4: building with collect inherits the size hint (added).

### Still unverified (no page found that says it, kept as own guidance)
1. 1: items 2, 4 and 12 (a const panicking constructor, plain numbers at a boundary, weasel words: the files were not read for these points).
2. 2: items 5 and 13 (what panics in library code, discarded results).
3. 3: items 8 to 15 (Send and Sync by hand, Drop, leaks, FFI layers and boundaries): the security guide chapters on unsafe were not re-read in this pass.
4. 4: item 12. 5: items 6 and 12. 6: items 4, 8, 9, 11, 12. 7: item 8.
5. The Rust Book, Reference and standard library pages were not opened for this block.

### Tally
Points 96. Sourced 73, corrected 1, still unverified 22.

Independent verification 2026-10-21: 35 checked, 34 matched, 0 corrected, 1 unverified (API Guidelines naming, interoperability, predictability, flexibility and future-proofing pages; Pragmatic Rust Guidelines builder, docs, features, MSRV, edition, lints, performance and panic files; ANSSI cargo-lock, profile and integer rules; unverified: 1.18 'mark growing enums non_exhaustive' is not on the API Guidelines future-proofing page, the Pragmatic features rule only mentions it for enum variants added under a feature, so it is own guidance).
