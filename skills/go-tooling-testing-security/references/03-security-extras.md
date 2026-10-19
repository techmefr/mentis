# go-tooling-testing-security §3 — Security extras

The general policy is `security-hardening`; this section is the Go standard-library half.

## 3.1 Confine file access with `os.Root`
**Go 1.24 and later.** `os.OpenRoot(dir)` returns an `os.Root`, and the methods on it operate inside that
directory and refuse paths that point outside it, **including ones that follow a symbolic link out of the
directory**. `Root.FS()` returns an `fs.FS` with the same guarantee. When a file name comes from a request,
an archive or a config value, open it through a `Root` instead of cleaning the string and joining it to a
base path. The package documentation points to the `Root` type for details and limitations: read them
before relying on it for a case the docs do not mention (hard links and mount points were not covered in
what was read). On older toolchains the scanner flags the manual pattern instead (gosec G304 for a tainted
file path, G305 for path traversal while extracting a zip, G703 by taint analysis).

## 3.2 Randomness for secrets
1. **Take tokens and secrets from `crypto/rand`,** never from a pseudo-random package. gosec G404 reports
   an insecure random source.
2. **`rand.Read` never returns an error and always fills the buffer;** if the system source fails it
   crashes the program irrecoverably, so there is no error branch to write.
3. **Go 1.24 and later: `rand.Text()`** returns a cryptographically random string over the RFC 4648 base32
   alphabet, meant for a secret string, token or password.
4. **Go 1.26:** several key-generation and signing functions in the crypto packages now ignore their
   `random` parameter and always use secure randomness; for deterministic tests the release notes name
   `testing/cryptotest.SetGlobalRandom`, with `GODEBUG=cryptocustomrand=1` as a temporary escape. A test that
   passed a fixed reader to those functions breaks on 1.26.

## 3.3 Compare secrets in constant time
`subtle.ConstantTimeCompare(x, y)` returns 1 for equal contents and 0 otherwise; if the lengths differ it
returns 0 immediately, and its running time depends on the length, not the contents. Use it, not `==` or
`bytes.Equal`, for a token, a MAC or a password hash. If the length is itself secret, compare fixed-length
digests of both values (own guidance, a consequence of the length behaviour).

## 3.4 Templates and queries
1. **Render HTML with `html/template`, never `text/template`.** The documentation says it should be used
   whenever the output is HTML, that it escapes by context (HTML, CSS, JavaScript, URI), and that it trusts
   the template's author but not the data passed in. `text/template` writes data out unescaped. gosec flags
   server-side template injection through `text/template` (G708) and cross-site scripting by taint (G705).
2. **Pass values to SQL as arguments to the placeholder form of the query, never by building the SQL
   string.** Own guidance: no page read in this pass states the rule in those words; gosec reports SQL
   injection by taint analysis (G701). Context and pooling rules for the database are
   `go-conventions` and `sql-conventions`.

## 3.5 Run the static security analyser
**gosec** inspects the AST and the SSA form and includes taint analysis for SQL and command injection, path
traversal, SSRF, XSS, log injection and unsafe deserialisation. Its rule list also covers hard-coded
credentials (G101), weak hashes (G401, G505), TLS settings (G402), insecure `rand` (G404), a missing
`ReadHeaderTimeout` (G112), and secrets exposed through JSON or YAML marshalling (G117). Its README shows a
CI run with the argument `./...`. Run it beside `govulncheck` (§1.5): one reads your code, the other your
dependencies. Triage each finding; a suppression needs a stated reason (own guidance), and the scanner
reports patterns, so a clean run is not a security review.
