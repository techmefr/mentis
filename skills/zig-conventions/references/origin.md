# zig-conventions — origin and source stamps

> Provenance of `skills/zig-conventions`. Read it when a rule has to be traced back to its source or checked
> for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡. Version pinned: 0.16.0 development tree.** Read on **2026-10-02**.

| Source | Pinned at | Licence | What was taken | Use |
|---|---|---|---|---|
| Language reference in the compiler repository, sections Style Guide and Source Encoding | commit `738d2be9` of 2025-11-26 (stale against the read date: the clone was not updated) | MIT | §1 | rewritten with this credit |

**Not read, so nothing attributed:** the rest of the language reference (memory, errors, comptime), the
standard library, the build system, community style notes.

**Volatile content to re-check:** everything: a pre-1.0 language. Compare with the style guide of the project's
compiler version before applying.

## Source pass 2026-10-20 (every point below was re-opened against the page named, own words, no text copied)

The Style Guide and Source Encoding sections of the published Zig 0.17.0 language reference were re-opened. The repository licence files were read again (MIT, Zig contributors; the website repository is MIT as well). Nothing was compiled or run.

| Source | Licence | What it confirmed or corrected |
|---|---|---|
| Zig 0.17.0 language reference, Style Guide section | MIT (ziglang/zig LICENSE read 2026-10-20) | redundant words list, fully qualified namespace rule, underscore prefix rule, whitespace, naming cases, acronyms, file names, doc comment guidance |
| Zig 0.17.0 language reference, Source Encoding section | MIT (same licence file) | UTF-8, forbidden code points, LF terminator, formatter conversion |
| Zig download index and the 0.17.0 documentation page header | MIT (ziglang/www.ziglang.org LICENSE read 2026-10-20) | 0.17.0 listed with date 2026-10-01 |

### Verified in this pass
1. 01-style items 2 to 8 (namespace rule, whitespace, case table, acronyms, file names, established names win, doc comment guidance) match the 0.17.0 text.
2. Pinned version: the earlier stamp named a 0.16.0 development tree; the content now matches the 0.17.0 release for these two sections.

### Corrected in this pass
1. Item 1: the avoid list also contains "state"; added.
2. Item 9: the earlier text said a carriage return is discouraged and a final newline needed; the reference rejects the carriage return outright (it sits among the forbidden control characters), forbids the byte order mark, and says the formatter can strip both. Rewritten.
3. Item 10 added: the guide's underscore prefix rule was missing.

### Still unverified (no page found that says it, kept as own guidance)
1. No rule here on memory, errors, comptime or build (see `skills/zig-pitfalls`).
2. Nothing was compiled; formatter behaviour is as the reference states it.

### Tally
Points 10. Sourced 8, corrected 2, still unverified 0.
