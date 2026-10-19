# c-conventions §5 — Hardening flags, sanitizers and annotations (shared with C++)

> Section 5 of `skills/c-conventions`, **also the hardening section of `skills/cpp-conventions`** (which
> cites it instead of repeating it). Read it when build flags, a Makefile, a CMake file, a CI job, a sanitizer
> or fuzzing run, or a function annotation changes. **Everything here is volatile**: flag availability depends
> on the compiler and library version and the source guide is revised several times a year. Before applying a
> flag, check the project's compiler and libc versions and the current text of the guide named in
> `references/origin.md` (`skills/source-freshness`). The other sections and the guardrails stay in `SKILL.md`.

**The model.** Hardening flags do two things: they make the compiler warn about constructs that often hide a
defect, and they make the produced binary integrate with the operating system's run-time mitigations
(address-space randomisation, non-executable stacks, read-only relocations, stack canaries, fortified libc
calls). They reduce the chance a defect becomes an exploit; they do not remove the defect, they apply only to
code compiled with them, and a pre-built third-party binary is not covered.

1. **Staged adoption.** In a new project, turn everything on before the first line of code, so every problematic
   construct is reported the day it is written. In an existing project the warning count is overwhelming and
   some run-time mitigations can expose latent bugs: enable options in groups, fix the warnings of each group
   to zero, and then hold the line (any new warning is then a signal). Treat "the code does not build with
   these options" as a bug in the code. A build that omits a hardening option does so by a recorded decision,
   not by neglect, since a binary that was shipped without it cannot be hardened afterwards.
2. **Warning set.** Always compile with the general warnings, the format-function warnings (basic and level 2),
   the implicit-conversion warnings and the implicit-fall-through warning. The conversion warnings are noisy in
   third-party headers: silence them around that one include with the compiler's diagnostic push/pop, not
   globally, and fix your own implicit casts by making them explicit after a range check (§1.2). With GCC add the
   trampoline warning (an executable stack is needed to take the address of a nested function) and, where the
   source is written only left to right, the warning on bidirectional control characters in source.
3. **Warnings as errors, in two forms.** The blanket form is for development, with a zero-warning policy. Do not
   ship it in distributed source: it makes the build depend on one vendor's and one version's set of
   warnings. Ship the selective form, which names the warnings that must never occur: the format-security
   error (a non-literal format string without arguments, §3.7), and, for C code that wants obsolete
   constructs refused, implicit declarations, incompatible pointer types and int-to-pointer conversions.
4. **Library fortification.** Build with optimisation at level 2 or higher and with the source-fortification
   macro at its highest level, first undefining any value the toolchain predefines to avoid a redefinition
   warning. Fortification turns an overflow in `memcpy`, `strcpy`, `sprintf` and their relatives into an abort
   when the compiler can estimate the destination size (so annotations in §5.10 help). It is incompatible
   with the memory sanitizer: build instrumented test binaries without it. In C++, also define the
   standard-library precondition checks: the assertion macro for libstdc++ and the fast hardening mode for
   libc++ in production; the debug modes only in non-production test builds, since libstdc++'s debug mode
   changes the layout of containers and cannot be mixed across translation units.
5. **Stack and bounds.** Use the strictest trailing-array setting so a structure's last array is bounds-checked
   at its declared size (this breaks the old one-element-array trick, which §2.8 already forbids); the
   stack-clash protection, which splits large stack allocations into probed steps so one allocation cannot
   jump the guard gap; and the strong stack protector, which puts a canary in the frame and checks it on
   return. On 64-bit Arm use a GCC recent enough to place buffers below the saved registers, otherwise
   variable-length arrays and `alloca` buffers can be overflowed undetected.
6. **Control flow and registers.** On x86-64 enable full control-flow protection; on aarch64 the standard branch
   protection. Zero the call-used registers that were used on return, which shortens the life of secrets held
   in registers and removes many return-oriented-programming gadgets. With GCC also request zero-initialisation
   of padding bits in automatic aggregates. For multi-threaded C code on the GNU C library, enable
   exception-propagation unwind tables, so thread cancellation does not spill an unprotected function pointer
   onto the stack.
7. **Production semantics.** For production builds keep the compiler from "optimising away" safety: do not
   delete null-pointer checks (a dereference before a test lets the compiler assume the pointer is non-null
   and drop the test), define signed and pointer overflow as wrapping, and do not assume strict aliasing.
   Initialise automatic variables to zero by default, which turns a logic bug that reads an uninitialised
   value into a deterministic one; the compiler's own uninitialised-use analysis still reports the variable.
   These flags make the program behave the way the author probably thought it did; they are a safety net for
   defects, not licence to write the undefined behaviour of §1.1.
8. **Linking and loading.** Build executables as position-independent (so address-space randomisation applies)
   and libraries as shared position-independent code; link with full relocation read-only (both the relro and
   now options, since partial relro leaves the lazy-binding table writable), a non-executable stack, only the
   libraries that are used (as-needed) and no implicit transitive dependencies. Mark shared objects that
   should never be loaded dynamically with the no-dlopen option. Do not hard-code run-time library search
   paths into the binary.
9. **Sanitizers in debug and test builds, never as production hardening.** Address (heap, stack and global
   overflows, use-after-free, use-after-return, initialisation order, leaks), undefined-behaviour, thread (data
   races) and leak sanitizers each need their own build and cannot all be combined: the address and thread
   sanitizers exclude each other, and so does the leak sanitizer with either; the GCC and Clang runtimes cannot
   be mixed. Use low optimisation, debug info, frame pointers and no tail-call optimisation for readable
   traces. Run the whole automated test suite under the address and undefined-behaviour sanitizers at least in
   CI, and the thread sanitizer for any multi-threaded code. The single production exception is the
   undefined-behaviour sanitizer with its minimal, trap-only runtime, which exposes no extra attack surface.
   Sanitizers read operational parameters from environment variables, so they never go in a set-user-id
   binary.
10. **Annotate for the compiler.** Describe allocators and deallocators (the malloc attribute with its
    deallocator, the allocation-size attribute taking the size or the two factors), the access mode and size
    of pointer parameters, file-descriptor parameters, functions that never return, and, in a structure, the
    field that counts a flexible array's elements (the counted-by family). They improve diagnostics, extend
    fortification to your own functions, and enable bounds checks on flexible arrays. For the entry points that
    take untrusted data, mark them with the tainted-arguments attribute so the static analyser follows the
    data to sizes, indices, divisors and offsets. Use the standard double-bracket attribute syntax where the
    language version has it (C23, C++11), guard each use with a feature test, and declare in the header what
    is attached to a declaration, placing the attribute before the function name in a definition.
11. **Fuzz the parsers.** Any code that decodes an input format, a protocol or a file from outside is run
    against a fuzzer under the address and undefined-behaviour sanitizers: they turn a corrupted-memory input
    into a crash the fuzzer can report. The corpus and the fuzz target live in the repository.
12. **Separate debug information, and check that the flags took effect.** Debug information can be larger than
    the code and makes reverse engineering easier (though security must never depend on its absence): keep it
    in a separate file, strip the shipped executable and add a debug link, so a debugger can still load the
    symbols for a field crash. A build system can drop a flag silently, and a flag in the Makefile proves
    nothing about the binary: inspect the produced binary with a tool that reports position independence,
    relocation protection and stack executability, and fail the CI job when one is missing. The source guide
    names no verification tool; choosing one is the project's decision.
