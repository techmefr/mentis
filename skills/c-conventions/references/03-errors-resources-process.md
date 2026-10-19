# c-conventions §3 — Errors, resources, I/O and the process

> Section 3 of `skills/c-conventions`. Read it when a library call can fail, when a file, socket or other
> handle is acquired, when a format string is built, when the shell, the environment, the file system or
> privileges are touched, or when one function has several exits that all need the same cleanup. Bracketed
> identifiers trace to the published standard in `references/origin.md`. The other sections and the guardrails
> stay in `SKILL.md`.

1. **Every standard-library and system call that can fail is checked** [ERR33, POS54]. An unchecked `malloc`,
   `fopen`, `fread`, `fclose`, `snprintf` or `pthread_*` call is a hidden branch where the program carries on
   with a null pointer, a half-read buffer or a held lock. The check sits on the line after the call, and
   the failure path does something: it releases what was acquired and reports the error to the caller. Casting
   a return value to `void` is not a check.
2. **`errno` is read right after the failing call and only when the call documents setting it.** Its value is
   indeterminate after a successful call and after most other calls [ERR30, ERR32]. Copy it to a local before
   calling anything else (a logging function included). Number conversions that report errors through the end
   pointer and the error indication are checked on both [ERR34].
3. **Return codes, not exceptions, and one convention per code base.** A function returns an error indication
   and passes results through pointers or a result structure; the project picks one convention (zero for
   success, a negative error code, a status enum) and keeps it. Do not return an in-band value that is also
   a valid result without documenting it.
4. **One cleanup path per function that acquires more than one resource.** A function with several exits
   jumps to a labelled cleanup at the end of the function, instead of repeating the cleanup before each
   `return` or nesting an `if` per acquisition. Name each label for what it releases (`out_free_buffer`, not
   `err1`), put the labels in reverse order of acquisition so that falling through them releases in the right
   order, and be careful that the first label never frees something not yet acquired. Initialise every pointer
   the cleanup releases to null. If a function acquires nothing, return directly. Simulate failures in tests so
   every exit path runs at least once.
5. **Close what you open, and never touch it afterwards.** Files and other handles are released when no longer
   needed [FIO42]; a closed stream is never read or written [FIO46]; a `FILE` object is never copied [FIO38].
   Do not switch a stream between reading and writing without an intervening flush or positioning call
   [FIO39], and use positions only from the call that produced them [FIO44]. Do not mistake a character for the
   end-of-file marker by storing it in a `char` [FIO34].
6. **File-system races.** Checking a path and then using it leaves a window in which another process swaps the
   target [FIO45, POS35]. Open the file with the flags that fail if it exists or is a link, then check what you
   opened through its descriptor, instead of testing the name first. Treat symbolic-link resolution with care
   [POS30]. Do not run operations meant for regular files on device files [FIO32].
7. **Format strings are constants.** User input never becomes a format string [FIO30]: a call such as
   `printf(msg)` with an external `msg` lets the sender read and write memory with `%x` and `%n`. Use
   `printf("%s", msg)`. A format string that is not a literal and has no arguments is a build error by
   the flag in §5.3. Arguments match the specifiers in number and type [FIO47, EXP47].
8. **Never hand data to a shell.** `system()` builds a command line that a shell then interprets [ENV33]; any
   metacharacter in an interpolated value is a command-injection. Launch a program directly with an argument
   vector (`execv` and its relatives) with fixed program path and validated arguments. The full treatment of
   injection is `skills/security-hardening` §2.
9. **The environment is global state.** Do not modify the object returned by `getenv`-like calls [ENV30], do not
   keep an environment pointer across a call that can change the environment [ENV31] or store pointers that
   later calls invalidate [ENV34], and do not pass an automatic variable to `putenv` [POS34]. Exit handlers
   return normally and do not terminate the process themselves [ENV32].
10. **Drop privilege in the right order and check that it worked** [POS36, POS37]. A process that sheds root
    drops the group first, then the user, then verifies that regaining privilege fails. After a `fork`, consider
    which descriptors the child inherits [POS38].
11. **Exposing structures.** Clear padding before a structure crosses a trust boundary [DCL39]. Use a defined
    byte order when data goes to another system, and convert explicitly [POS39].
12. **Secrets are not in the source or the binary** [MSC41]. Read them from the environment or a secret store at
    run time; the policy side is `skills/security-hardening` §4.
