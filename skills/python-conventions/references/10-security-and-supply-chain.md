# python-conventions §10 — Security surface and supply chain

> Section 10 of `skills/python-conventions`. Read it when Python code loads data in a serialised format,
> runs a subprocess, handles a secret, a file path from outside, a temporary file, XML or an archive, or
> when a dependency is added or audited. The background (what each class of attack is) is
> `skills/security-hardening`; the web layer is §9. The other sections and the guardrails stay in `SKILL.md`.

1. **Secrets come from the environment or a secret store, read once at startup.** A missing required
   secret fails the process at boot with the name of the variable, and that is why it is read with a lookup
   that raises (§5, config) and not one that defaults to an empty string. A secret never appears in a
   default argument, a test fixture that is also used in a real environment, a log line or an exception
   message. The file that holds local values is excluded from version control and a template of the keys is
   committed instead.
2. **A serialised format that can run code is never loaded from an untrusted source.** The standard object
   serialiser executes code while loading, and so does the unsafe mode of the common YAML loader and the
   binary formats of several numerical and machine-learning libraries. Untrusted input uses a data-only
   format (JSON, or YAML through the safe loader) and is validated into a typed model (§1). A pickle file
   that arrives from another system is untrusted, even when it came from "our" bucket.
3. **A subprocess takes a list of arguments and no shell.** The argument-list form passes each element as
   one argument with no interpretation; enabling the shell and building a command string from a value
   reintroduces every metacharacter. The executable is a constant or a resolved path, the input is
   validated, a timeout is set, and the exit status is checked (the check parameter) so a failure is not
   treated as success.
4. **`eval`, `exec` and dynamic imports from data do not appear.** A name, a plugin or an operator chosen by
   input is looked up in a dictionary of known implementations. Template engines used to render user-supplied
   templates run in their sandboxed mode, or not at all.
5. **A path from outside is resolved and confined.** Join it to the intended base, resolve it, and verify the
   result is still inside the base before opening it; a `..` segment, an absolute path replacing the base and
   a symbolic link all escape a naive join. Archives are the same problem in bulk: extracting a zip or tar
   from outside can write anywhere, so the extraction uses the library's safe filter where it exists or
   checks every member's destination, and bounds the total size and member count against decompression bombs.
6. **Temporary files are created by the library that makes them safely.** The function that creates and
   opens a temporary file atomically, with restrictive permissions and an unpredictable name, replaces a
   hand-built path in a shared directory, which is a race and a predictable target. The file is removed by
   the context manager, not by a cleanup that an exception skips.
7. **Randomness for a secret comes from the secrets module.** Tokens, reset codes, session identifiers and
   keys use the secrets module or the operating system's source; the general random module is deterministic
   by design. A secret comparison uses the constant-time comparison function from the standard library, not
   an equality operator that returns early at the first differing byte. Passwords are hashed with a memory-
   hard algorithm through a maintained library, with a per-password salt and a work factor stored with the
   hash so it can be raised.
8. **XML from outside is parsed by a hardened parser.** The standard XML parsers expand entities, which
   enables entity-expansion bombs and, on some, external entity reads. Use the hardening library's drop-in
   parsers, or disable entity resolution and network access explicitly, for any document the program did
   not produce.
9. **Outbound HTTP calls to a user-influenced URL are an SSRF.** Fixed base address from configuration,
   scheme and host checked against an allow-list, redirects disabled or re-checked at each hop, private and
   link-local ranges refused after DNS resolution (the check is on the resolved address, since the name
   can change between check and use), a timeout and a response size limit (`skills/security-hardening` §2).
   The TLS verification flag is never turned off; a failing certificate is fixed.
10. **SQL values are bound; identifiers are chosen from a closed set.** The database API's parameter
    substitution handles values for every driver and ORM; string formatting into SQL does not, whatever
    escaping is attempted. A sort column or table name from a request is mapped through an allow-list.
11. **A static security scan runs in CI, and its suppressions are findings.** A Python security linter
    reports the patterns above (shell use, unsafe loaders, weak hashes, hard-coded passwords, temp-file
    misuse, disabled TLS verification). A suppression comment on a flagged line states a reason in the review,
    and a blanket suppression of a rule class is a configuration decision made once and written in the
    project file, not scattered (`skills/code-baseline` on comments applies: the justification lives in the
    review and the configuration, not in the line).
12. **The dependency set is audited on a schedule, from the lock file.** A vulnerability audit tool reads the
    locked, hashed requirements and reports known advisories for the exact versions installed; a pass last
    month says nothing about today, so it runs weekly as well as on each push. Requirements are installed with
    hash checking where the tooling supports it, so a replaced artefact fails to install (§8, point 3).
13. **A new package is read before it is added.** The name is checked against the intended one (typosquatting
    targets the install command, not the code), the maintainer and the release history are looked at, and the
    package's install-time behaviour is considered: a source distribution runs its build backend on install.
    A package with a handful of lines of value is those lines in the repository (`skills/security-hardening` §4).
14. **Private index configuration is explicit.** A package name that exists on both an internal index and the
    public one is resolved to whichever the installer prefers, which is the dependency confusion attack. The
    internal packages are namespaced, the installer is told which index owns which name, and the extra index
    option is not used to mix trust domains.
15. **Debug facilities are off outside development.** An interactive debugger, an auto-reloader, a verbose
    error page and a server bound to all interfaces by default are development conveniences; production
    configuration turns them off and binds to what the platform expects, and a test asserts the setting.
