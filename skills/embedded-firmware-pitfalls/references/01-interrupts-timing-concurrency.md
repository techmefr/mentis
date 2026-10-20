# embedded-firmware-pitfalls §1 — Interrupts, timing and concurrency

Source: own craft knowledge; chip and library behaviour is to be re-read in the datasheet and documentation of the part in use.

## 1.1 Interrupt handlers
1. **A handler sets a flag, copies a sample or advances a counter, and returns.** Parsing, formatting, logging, bus transactions and anything slow belong in the main loop or a task that the flag wakes.
2. **Symptom: serial output garbles, a bus hangs, or the board resets when an input toggles.** Cause: the handler calls something that itself needs interrupts, takes a lock, or allocates. Fix: remove the call; check the platform's list of functions that are safe in a handler.
3. **On some chips, handler code must live in fast memory, and cannot run while flash is being written.** A handler that runs from flash while the flash is busy crashes. Mark it as the platform requires and keep its data in RAM.
4. **Check:** read each handler and list every function it calls. The list should be short and every entry should be documented as handler-safe.

## 1.2 Data shared with a handler
1. **A variable written in a handler and read in the loop must be marked so the compiler re-reads it each time** (the volatile qualifier, or an atomic type). Without it the optimiser keeps a copy in a register and the loop never sees the change; the bug appears only in optimised builds.
2. **Marking is not enough for values wider than the processor's native word.** A 32-bit value on an 8-bit chip is read in several steps, and the handler can change it between them, producing a value that never existed. Read it with interrupts briefly disabled, or use an atomic type, and copy it to a local.
3. **A read-modify-write on shared data (`count++`) is not atomic** even on a native-width value. Use the platform's atomic operation or a short critical section.
4. **Pass bursts through a ring buffer with one producer and one consumer,** and size it for the worst gap the loop can be late. Count overruns instead of dropping silently.
5. **Keep critical sections as short as the handler latency you can afford.** Disabling interrupts for a long operation loses pulses and serial bytes.

## 1.3 Blocking and timing
1. **A busy-wait delay in the main loop freezes everything else,** including input, the watchdog and communication. Use a timestamp comparison against a monotonic clock, or a timer, so the loop keeps running.
2. **Compare elapsed time as a difference of unsigned values,** `now - start >= interval`, so the counter's wrap-around (every few weeks on a millisecond counter) does not break it. Comparing absolute times fails once, at the wrap, a month after launch.
3. **Debounce mechanical inputs in time, not in hope.** A button bounces for a few milliseconds; accept a change only after it has been stable for a chosen period, or filter in hardware.
4. **Do not trust a software delay for precise timing.** Use a hardware timer or peripheral for pulse widths and sample rates; interrupts and the compiler change a delay loop's length.
5. **Check:** run the device through the wrap of the time counter (a build that starts the counter near its maximum) and confirm nothing stalls.

## 1.4 Tasks under a real-time operating system
1. **Share data between tasks through the system's queues, semaphores or event flags, not bare globals.** A global read by two tasks has the same torn-read problem as one shared with a handler.
2. **Give each task a stack sized from a measurement.** Run the worst path and read the minimum free stack the system reports; a task with an unmeasured stack overflows on the one rare path.
3. **Priority inversion hangs systems:** a high-priority task waiting on a lock held by a low-priority task that a medium one keeps preempting. Use the system's mutex with priority inheritance, not a binary semaphore, for resource locks.
4. **Never block inside a critical section or call a blocking function from a handler;** use the handler-safe variant of queue and semaphore calls the system provides.

## Checks
- Handlers are short; every shared variable is marked and read atomically (§1.1, §1.2).
- No busy-wait in the loop; elapsed time uses unsigned subtraction (§1.3).
- Task stacks are measured; resource locks use priority inheritance (§1.4).
