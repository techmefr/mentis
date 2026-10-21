# embedded-firmware-pitfalls: origin and source stamps

> Provenance of `skills/embedded-firmware-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from the author's own craft knowledge, with part of the claims checked against the Zephyr and MCUboot documentation on 2026-10-20. Never dogfooded; no firmware was built or run on hardware.

## Sources (read 2026-10-20)

| Source | Licence | What it gave |
|---|---|---|
| Zephyr documentation: interrupts, threads, non-volatile storage, device management | Apache-2.0 (`LICENSE` of the Zephyr repository read 2026-10-20); rewritten, nothing copied | Short handlers and hand-off (§1.1), thread-only calls, zero-latency handlers (§1.1.2), stack measurement (§1.4.2), erase sectors, wear formula, write order and unchanged-write skip (§2.3.1, §2.3.2) |
| MCUboot documentation: design | Apache-2.0 (`LICENSE` of the MCUboot repository read 2026-10-20); rewritten, nothing copied | Two slots, test versus permanent swap, confirmation, revert, signature check (§2.3.3) |
| Zephyr source files `doc/kernel/services/interrupts.rst`, `threads/index.rst`, `synchronization/mutexes.rst`, `other/atomic.rst`, `doc/services/storage/nvs/nvs.rst`, `doc/hardware/peripherals/hwinfo.rst` (re-read 2026-10-20); `LICENSE` of the Zephyr repository re-read | Apache-2.0, no holder named in the text | Handler rules, zero-latency rule, stack measurement and MPU alignment, mutex semantics, atomic services, wear and write order, reset-cause flags vary |
| MCUboot repository `docs/design.md` and `LICENSE` (read 2026-10-20) | Apache-2.0, no holder named; the repository bundles a BSD-licensed crypto library, not used here | Slots, swap modes, hash and optional signature, swap resume, overwrite-only and rollback counter |
| FreeRTOS-Kernel `LICENSE.md` (read 2026-10-20) | MIT, no holder named | Licence only: the mutex documentation page returned truncated text and nothing was taken from it |
| PlatformIO documentation repository | Apache-2.0 (`LICENSE` read 2026-10-20) | Not used: tool documentation, §2.5 stays generic |
| FreeRTOS documentation (mutex page) | not checked | Page returned no text; nothing taken |

## Removed
- Board-, chip- and library-specific API names, pin tables, register values, endurance and current figures, protocol stacks and certification topics: not covered.

## Not verified
1. **Checked in one RTOS's documentation:** short handlers and thread hand-off, thread-only calls, stack measurement, erase blocks and wear, write order for power-loss safety, two-slot update with confirmation. **Also checked 2026-10-20:** mutex priority inheritance and handler restriction (Zephyr mutex page). **Also checked 2026-10-20:** atomic operations shared with handlers, interrupt-lock latency cost, mutex ownership and unlock behaviour, reset-cause flag support varies, MCUboot swap resume, overwrite-only and rollback counter. **Corrected:** the MCUboot signature is optional and signs the hash (earlier text said the signature covers the parts directly); the mutex ceiling and the ignore-invalid-metadata remark were not found again and are no longer asserted. **Unverified:** fast-memory handlers during flash writes (the interrupts page does not discuss it), torn reads on narrow chips, the volatile rule, ring buffers, watchdog feeding patterns (the watchdog page URL was not found at the source path), brown-out symptoms, heap fragmentation, power and radio, flash-string mechanisms. Re-read the datasheet of the part in use.
2. **PlatformIO and vendor toolchains** are not described; §2.5 is generic build advice.
3. **Safety-critical and regulated devices** (medical, automotive) need their own standards; this block is not one.

## Related blocks
`c-conventions`, `cpp-conventions`, `cpp-build-and-lifetime-pitfalls`, `source-freshness`.

Independent verification 2026-10-21: 29 checked, 27 matched, 2 corrected, 0 unverified
