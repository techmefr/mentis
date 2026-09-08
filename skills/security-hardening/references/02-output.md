# § 2 — Output: the escaping depends on the destination

> Section 2 of `skills/security-hardening`. Read it when a value reaches a query, a template, a shell,
> a filesystem path or an outbound HTTP call. Point 4 is the SSRF rule added by the 2026-08-10 OWASP
> coverage check.

1. **Never build a query by concatenation.** Parameterised queries or the ORM's binding, always,
   including for the parts that "can't" contain user data. Column and table names can't be
   parameterised at all, which is exactly why they go through a whitelist (§1.3). The "can't contain
   user data" cases are where this fails in practice, because the value is internal today and becomes
   a request parameter in the change that adds a filter.
2. **Escape for the context you're writing into.** HTML, an HTML attribute, JavaScript, a URL and SQL
   all escape differently; the framework's default usually covers HTML text and nothing else. The
   moment you reach for the "render this unescaped" facility, the value has to be sanitised or come
   from a trusted source.
3. **Never pass user data to a shell.** Use the API that takes an argument array; string interpolation
   into a command is not fixable by escaping. The shell has more metacharacters than any quoting
   routine covers, and the argument-array form removes the shell entirely rather than trying to outrun
   it.
4. **A user-supplied URL fetched server-side is SSRF, not just injection.** The trust boundary named at
   the top of this block ("an HTTP call") means an allowlist of destinations/schemes, a block on
   internal/link-local/loopback and cloud-metadata IP ranges (`169.254.169.254` and equivalents), and no
   blind following of redirects — a redirect can retarget an already-validated URL to an internal one
   after the check has passed.
5. **A value interpolated into a template is code, whichever template it is.** The rule extends past
   HTML: a value placed into an SQL fragment, a shell string, a log format, a regular expression, an
   LDAP or a NoSQL filter, or a header, is being interpreted by something. Ask what parses the result,
   and use that parser's parameter mechanism rather than its string form.
6. **Escaping happens where the value is written, not where it arrives.** Sanitising on input and
   storing the escaped form gives you a database whose contents are correct for exactly one
   destination — so the same row is double-escaped in the HTML page and raw in the CSV export or the
   API response. Store the value; escape at each output.
7. **A path built from a value the caller supplied is a traversal.** Joining a filename onto a
   directory does not confine it, since the value can climb out, and the check has to be that the
   *resolved* path is inside the intended directory — after resolution, not before. The reliable answer
   is not to use the caller's string as a path at all (§4.1).
8. **A redirect target is an output too.** A location taken from a parameter sends the reader to
   wherever the attacker wants under your domain's authority, which is what makes it useful in a
   phishing chain; the target comes from a whitelist of known destinations, or it is a path within the
   application and nothing else.
9. **Never place a secret or an internal identifier into a URL.** Query strings are logged by every hop
   — the browser's history, the proxy, the access log, the referrer sent to the next site — so a token
   or a signed value in a path or a query has been copied into places with different retention and a
   different audience. Bodies and headers are where those go.
10. **An outbound call carries whatever credentials it was given.** A request whose target is
    influenced by user input and whose headers carry a service token is a way to spend that token on
    someone else's behalf, which is the half of SSRF that survives an IP allowlist. Scope the
    credential to the destination, and never attach it to a call whose target was not fixed by you.
11. **A response you fetched is untrusted input.** What comes back from a third-party or internal call
    goes through §1 before it is parsed, rendered or trusted for a decision — including its size, since
    a streamed response with no cap is a way to exhaust memory through a request that looked ordinary.
12. **The unescaped-render facility is a decision, not a shortcut.** Every framework has one and every
    codebase ends up with occurrences of it; each is a place where a future value reaches a parser
    directly, so each is worth a named reason at the call site and a sanitiser rather than a trusted
    source assumed. Reaching for it to fix a display bug is the guardrail this block states absolutely.
