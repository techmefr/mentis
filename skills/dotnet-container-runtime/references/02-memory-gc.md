# dotnet-container-runtime §2 — Memory and GC

Measure before tuning; most services need no setting beyond the container memory limit.

## 2.1 The limit and the heap
1. **When the process runs under a container memory limit, that limit is treated as total physical
   memory,** and the heap hard limit percent defaults to 75% of it. The percent setting applies to 64-bit
   machines and is ignored if an explicit heap hard limit or per-object-heap limits are configured. The rest
   of the limit is for everything that is not the managed heap, so size the limit for the whole process.
2. **Set a limit on every container.** Without one the runtime sees the host's memory. This is our own
   guidance.
3. **Read the numbers the runtime reports** (`GC.GetGCMemoryInfo`, `dotnet-counters`) before changing a
   setting. This is our own guidance.

## 2.2 GC mode
1. **Workstation GC is the default;** server GC is selected with `System.GC.Server` in `runtimeconfig.json`
   (`ServerGarbageCollection` as a project property). Choose on purpose, and measure, in a small container.
2. **DATAS (dynamic adaptation to application sizes) is enabled by default starting in .NET 9;** the setting
   exists from .NET 8 (`System.GC.DynamicAdaptationMode`, `1` enabled, `0` disabled). It aims to keep the
   heap roughly proportional to the long-lived data size, and the documentation notes the number of gen0 and
   gen1 collections is significantly higher with it. Check the runtime version before assuming a default.
3. **GC settings are per process.** The documentation advises against setting them at machine level.

## 2.3 Setting syntax
1. **Numeric GC settings are decimal in `runtimeconfig.json` and hexadecimal in environment variables,**
   with or without the `0x` prefix. A 200 MiB heap hard limit is `209715200` in the JSON file and `0xC800000`
   (or `C800000`) in `DOTNET_GCHeapHardLimit`. A decimal value pasted into the environment variable means a
   different number.
2. **Prefer the project or runtime-config setting over an environment variable** for a value that belongs to
   the app, so it travels with the build. This is our own guidance.

## Verification
- Run the container with its production memory limit under a load test; it stays below the limit with
  headroom and is not restarted.
- A comparison run with each GC mode shows the memory and latency you chose it for.
