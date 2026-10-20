# embedded-firmware-pitfalls §2 — Memory, resets, storage and power

Source: own craft knowledge; limits, endurance figures and register behaviour are to be re-read in the datasheet of the part in use.

## 2.1 Memory
1. **Symptom: the device runs for days, then resets or misbehaves, and the fault is never in the same place.** Cause: heap fragmentation from allocate and free in a loop, a string class that grows, or a stack that overflows into data. Fix: allocate fixed buffers once at start-up, use fixed-size arrays and formatted writes with a length, and keep dynamic containers out of long-running paths.
2. **String literals can occupy scarce RAM on some architectures** because they are copied from flash at start-up. Use the platform's flash-string mechanism for large constant text and tables.
3. **Check the free-memory figure at boot and after a day.** Log the minimum free heap and the minimum free stack; a figure that only goes down is a leak, and a low minimum is a crash waiting for a rare input.
4. **Bound every buffer write.** `sprintf` into a fixed array with an unbounded string is the classic overflow; use the length-limited form and check its return value for truncation.
5. **Make the linker map part of the review.** A change that moves RAM use by a large step is visible there and not in the code.

## 2.2 Watchdog and resets
1. **A watchdog is a proof of progress, so feed it only where progress is proven.** Feeding it from a timer handler or at the top of the loop keeps it quiet while a task is deadlocked. Feed it after every critical task has checked in during the cycle.
2. **Read and log the reset cause at every boot** (power-on, brown-out, watchdog, software, exception). A field device with no reset history cannot be debugged; keep a small counter per cause.
3. **A brown-out reset loop on a weak supply looks like a software bug.** Check the supply under load (radio transmit, motor start) with a scope or a logged supply reading before changing code.
4. **Make start-up idempotent.** After a reset in the middle of an operation, outputs and peripherals come up in a defined safe state, and a half-finished action is detected and either completed or rolled back.
5. **Do not hide a crash with a watchdog reset and ship it.** Log it, count it, and treat a rising count as a defect.

## 2.3 Flash and non-volatile storage
1. **Flash and emulated storage have limited erase cycles and erase in blocks.** Writing a counter or a log line on every event wears a sector out in the field. Write on a change that matters, batch writes, and use the platform's wear-levelling store.
2. **Never write from a place that can lose power mid-write without a plan.** Write a new copy with a version or a checksum, then switch to it, so a power cut leaves either the old or the new record valid, never half of each.
3. **A firmware update is a write too.** Keep two image slots or a recovery path, verify the image before switching, and confirm after boot that the new image is healthy, otherwise roll back.
4. **Settings need a schema version.** A new firmware reading an old record meets a missing field; apply defaults and migrate by version, as in any data store.
5. **Check:** simulate power loss at random moments during a write in a test and confirm the device boots with a valid record each time.

## 2.4 Power and radio
1. **Battery life is decided by sleep, not by code speed.** Measure current in each state, put the chip and peripherals to sleep between work, and wake on an interrupt or a timer, not on a polling loop.
2. **A radio transmit draws a burst that can sag the supply and reset the chip.** Size the capacitor and regulator for the peak, and keep the burst short.
3. **Connection handling is a state machine, not a call.** Handle disconnects, retry with growing backoff and a ceiling, time out every wait, and keep the device useful (local control, local logging) while the link is down.
4. **Set time from a source and expect drift.** A cheap oscillator drifts by seconds a day; resynchronise periodically and never use device time as the only ordering of records.
5. **Secrets on the device are extractable from flash unless the chip protects them.** Enable the chip's flash protection and encryption options where the product needs them, and never ship one shared credential in every unit.

## 2.5 Build and test without the board
1. **Keep logic that does not touch hardware in a plain library and test it on the development machine.** Parsing, state machines, scaling and protocols need no board; the code that talks to pins stays thin behind an interface.
2. **Pin the toolchain and library versions in the project file.** A library update that changes timing or memory use is a regression a board test finds late.
3. **Run a hardware-in-the-loop check for what the host cannot test** (timing, interrupts, power), and record the board revision with the result.
4. **Build with warnings as errors and run the static analyser,** since a type mix-up on an 8-bit chip does not crash on a host.

## Checks
- Buffers are fixed; minimum free heap and stack are logged (§2.1).
- The watchdog is fed on proven progress; the reset cause is logged (§2.2).
- Flash writes are counted, bounded, power-loss safe and versioned (§2.3).
- Current is measured per state; radio loss is handled (§2.4).
- Pure logic is tested on the host; toolchain versions are pinned (§2.5).
