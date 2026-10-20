---
name: embedded-firmware-pitfalls
description: "Use when writing or reviewing microcontroller firmware (Arduino-style, ESP32, PlatformIO projects, bare-metal or RTOS): interrupt handlers and shared variables, blocking delays, stack and heap limits, watchdog and reset causes, flash and non-volatile writes, power and radio behaviour, and testing without the board."
---

# embedded-firmware-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for code that runs on a chip with kilobytes of memory and no operating system
to forgive mistakes. The premise: **the program works on the bench for ten minutes and fails in the field after
three days**: an interrupt changes a value halfway through a read, a heap that fragments runs out in week one, a
flash cell is written to death, a blocking delay starves the watchdog. Language rules are in `c-conventions` and
`cpp-conventions`; this block covers what the hardware adds.

## When
- An interrupt handler, a timer, a DMA transfer or a shared variable is written.
- Memory is allocated, a library with dynamic allocation is added, or a board runs out of RAM.
- Settings, counters or logs are written to flash or an emulated store.
- The device resets, hangs, drains a battery or loses its radio link without a clear reason.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Interrupts, shared data, blocking, timing, debounce, concurrency under an RTOS | an interrupt, task or timer is touched | [`01-interrupts-timing-concurrency.md`](./references/01-interrupts-timing-concurrency.md) |
| 2 | Memory, watchdog and resets, flash wear, power, radio, build and test | memory, reset, storage, power or the build setup is the question | [`02-memory-resets-storage-power.md`](./references/02-memory-resets-storage-power.md) |

## Output / checkpoint
For a change touching this block: interrupt handlers only set flags or copy data, every variable shared with
one is marked and read atomically, nothing blocks longer than the watchdog allows, no allocation happens after
start-up, writes to non-volatile storage are counted and bounded, and the reset cause is logged at boot.

## Guardrails
- Keep handlers short and flag-setting (§1.1). Never call blocking, allocating or slow functions from one.
- Read multi-byte shared values atomically (§1.2). Never read them bare while an interrupt can change them.
- Allocate buffers once at start-up (§2.1). Never allocate and free in a long-running loop.
- Feed the watchdog from the code that proves progress (§2.2). Never from a timer that fires regardless.
- Count and bound every flash write (§2.3). Never write a counter to flash on every event.
- Pin limits, register behaviour and library details come from the chip's datasheet and the board's documentation; re-read them for the part in use (🟡, nothing here ran on hardware).

## Origin
Written from our own craft knowledge of firmware practice. No source text was taken. See
[`references/origin.md`](./references/origin.md).
