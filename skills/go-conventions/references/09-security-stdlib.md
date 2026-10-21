# go-conventions §9 — Security with the standard library

> Section 9 of `skills/go-conventions`.

The cross-stack rules live in `security-hardening`; these are the Go equivalents.

1. SQL uses placeholders; a process is started with the executable and its arguments passed separately,
   never through a shell string.
2. HTML goes through `html/template`, never `text/template` or string concatenation.
3. A caller-supplied file name is confined to a root. On a recent toolchain use the root-scoped file API; on
   an older one validate with `filepath.IsLocal` and a relative-path check, and do not rely on cleaning the
   path then comparing a prefix. Those lexical checks only hold when no one can change the directory tree
   between the check and the open: against an attacker who can plant a symlink, check-then-open is a race,
   which is what the root-scoped API closes.
4. Tokens, identifiers and keys come from `crypto/rand`, never `math/rand`. Secret comparison uses
   `crypto/subtle`.
5. A server sets read, write and idle timeouts; a client sets a timeout and uses the context variant of the
   request constructor.
6. Run the vulnerability checker on the module in CI.
