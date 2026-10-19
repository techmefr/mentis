---
name: dotnet-container-runtime
description: "Use when a .NET service is packaged or tuned to run in a container: a Dockerfile for an ASP.NET Core or worker app (runtime versus SDK image, restore layer caching, non-root user and port, cross-architecture builds, runtime and SDK images), memory limits and garbage collector settings (heap limit default, Server versus Workstation GC, DATAS, hexadecimal environment values), and globalization, ICU and time zone data in slim images."
---

# dotnet-container-runtime

Step 6 of the pipeline (`WORKFLOW.md`), for the layer between a .NET app and the machine: the image, the
memory and GC settings it runs under, and the culture and time zone data it needs. The premise: **the
runtime reads its limits from the container, so the image and the limit are one design, not two**. General
publish and trim rules are in `dotnet-conventions` §9; image scanning and registry policy belong to
`devops-conventions`; the equivalent block for Node is `node-container-runtime`.

## When
- Writing or reviewing a Dockerfile or a compose service for a .NET app.
- A container is OOM-killed, uses far more memory than expected, or is slow under load.
- Changing GC settings.
- An image fails with a culture or time zone error, or uses an invariant-culture switch.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Image build: runtime image, restore caching, non-root user and port, cross-architecture, certificates and secrets | a Dockerfile or image build is written or reviewed | [`01-image-build.md`](./references/01-image-build.md) |
| 2 | Memory and GC: heap limit, GC mode, DATAS, setting syntax | a container is killed, bloated or slow | [`02-memory-gc.md`](./references/02-memory-gc.md) |
| 3 | Globalization and time zones: ICU, invariant mode, tzdata | a slim image is chosen, or a culture or time zone error appears | [`03-globalization-tzdata.md`](./references/03-globalization-tzdata.md) |

## Output / checkpoint
The image was built and run: the final image holds no SDK and the app ran as the non-root user (§1), the
container ran under its real memory limit and the heap stayed inside it (§2), and the app was started in
the final image with the same culture and time zone calls the code makes (§3). A Dockerfile that was only
linted is not verified.

## Guardrails
- Never use the SDK image as the final stage (§1.1).
- Never run the container as root (§1.2).
- Never set a GC value in an environment variable as if it were decimal (§2.3).
- Never turn on invariant globalization to silence an ICU error without checking what the app formats (§3.2).
- Versions: the user and port defaults apply to .NET 8 and later images; each other rule names its
  version. Nothing was built or run while writing this block.

## Origin
Rewritten from the .NET Docker samples (MIT) and the .NET runtime configuration and GC documentation
(CC-BY-4.0), read 2026-10-08. 🟡: never run by us; open points are in
[`references/origin.md`](./references/origin.md).
