# mobile-crash-symbolication-pitfalls §1 — Reading the report

> Part 1 of `skills/mobile-crash-symbolication-pitfalls`. Read it when a crash file has just been opened, or an
> identifier is missing. Sourced from `plugins/dotnet-diag/skills/apple-crash-symbolication/SKILL.md` and its
> `references/ips-crash-format.md`, and `plugins/dotnet-diag/skills/android-tombstone-symbolication/SKILL.md` in
> `dotnet/skills` (commit `6364668`), read 2026-10-16. The libraries named are the .NET runtime's, used as the
> example. Sentences marked "own guidance" are ours.

1. **Check the format before anything else.** The Apple skill says the `.ips` file must start with a line of
   valid JSON; if the file is plain text (an Android tombstone with numbered pc frame lines, or the older Apple
   text crash format) the Apple workflow does not apply and the report is to be returned with the format
   mismatch, without trying other tools. The Android skill's frame lines look like a numbered pc offset, a
   library path, an optional symbol and a build id. Own guidance: say in the ticket which of the two formats
   the file is, so the next reader does not repeat the check.
2. **An `.ips` file is two JSON documents.** Line 1 is a metadata header (app name, bundle id, OS version and
   similar); the remaining lines are the crash body, a separate JSON document. Parse them separately. The
   source adds a parsing trap: some files have case-conflicting duplicate keys (`vmRegionInfo` and
   `vmregioninfo`), so rename the lowercase one in the raw text before parsing, and the application-specific
   information field may be missing.
3. **Compute an Apple frame's address from its image.** In the crash body the loaded binaries are listed with
   a name, a base (load) address, a UUID and an architecture, and each thread frame carries an image index and
   an offset. The frame's address is the image's base plus the offset. The app's own binary can appear twice
   in the image list with different UUIDs, which is why the UUID, not the name, picks the symbol file (part 2).
4. **Read the cause fields before the stack.** The source starts with the application-specific information
   field, which for the .NET case often holds the managed exception's type and message, then the faulting
   thread (its index is in the report), and explains frames 0 and 1 before looking at other threads; other
   threads are context, such as garbage-collection state, and not evidence of cause. It also points to the
   last-exception backtrace for the path of the exception that triggered the crash.
5. **Know what to skip.** Both skills filter to the runtime's own libraries (for the .NET case the CoreCLR or
   Mono runtime and its native base-class libraries, which on Apple platforms ship as framework bundles, so
   match the name by substring) and skip system libraries and frameworks unless asked. Own guidance: the
   point generalises to "the code you own or ship"; the platform's own frames are not yours to symbolicate
   without the platform's symbols.
6. **An Android offset is already library-relative.** The tombstone's pc value is an offset into that library
   and the Android skill says never to add or subtract a library base address, which is the opposite of the
   Apple case where the load address is passed to the tool.
7. **Take every thread, not only the crashing one.** The Android skill symbolicates all threads by default
   because background threads such as garbage collection and finalizers often hold useful frames; the
   crashing thread's backtrace comes first and the rest follow after separator lines. The Apple skill has an
   option to limit output to the crashing thread.
8. **Logcat output loses build ids.** The Android skill says tombstones captured from logcat often omit the
   build id, which is a 32 to 40 character hex string on the frame line. Ways to recover it: read it from the
   library on the device with the ELF notes reader, take it from CI build artifacts, or take it from the
   runtime package. It prefers pulling the raw tombstone file from the device, which always has the ids.
   Own guidance: make "attach the raw file, not a pasted excerpt" part of the crash-ticket template.
9. **A paste can corrupt the frame lines.** The Android skill notes that issue trackers may turn `#1 pc` into
   a link to an issue, so replace the mangled form with the original before saving the text to a file.
10. **Getting the Apple file from a device.** A connected iOS device's crash reports can be copied with the
    libimobiledevice tool `idevicecrashreport`; they are also visible in Xcode's device logs, in the crash
    reporter directory for Mac Catalyst apps and in the diagnostic reports directory on macOS.
