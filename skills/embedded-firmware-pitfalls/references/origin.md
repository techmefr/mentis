# embedded-firmware-pitfalls: origin and source stamps

> Provenance of `skills/embedded-firmware-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from the author's own craft knowledge. Never dogfooded; no firmware was built or run on hardware.

## Sources (read 2026-10-20)

| Source | Licence | What it gave |
|---|---|---|
| None opened. The PlatformIO documentation repository (Apache-2.0 per the review, licence file not read in this pass) was not used | n/a | Nothing taken |

## Removed
- Board-, chip- and library-specific API names, pin tables, register values, endurance and current figures, protocol stacks and certification topics: not covered.

## Not verified
1. **All behaviours stated generally** (handler-safe functions, fast-memory handlers, torn reads on narrow chips, wear and erase blocks, watchdog patterns, brown-out symptoms) were not checked against a datasheet or run. Re-read the datasheet of the part in use.
2. **PlatformIO and vendor toolchains** are not described; §2.5 is generic build advice.
3. **Safety-critical and regulated devices** (medical, automotive) need their own standards; this block is not one.

## Related blocks
`c-conventions`, `cpp-conventions`, `cpp-build-and-lifetime-pitfalls`, `source-freshness`.
