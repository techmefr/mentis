# § 3 — Phoenix: contexts, access, web vulnerabilities, tests

> Section 3 of `skills/elixir-phoenix-conventions`. Read it when a context function, a controller, a plug, a
> query fragment, an outbound request or a test is written. Read 2026-10-02 from the Phoenix guides (contexts,
> cross-context boundaries, API authentication, security, testing, main branch). The scope points reflect the
> current generator line.

1. **Phoenix is the web interface to an Elixir application; the application lives in contexts.** A context is a
   module that encapsulates data access and validation for one area (it talks to the database or to an HTTP
   client), exposing a small API the web layer calls. Controllers and LiveViews call contexts; they do not
   build queries.
2. **Contexts are a starting point: write purpose-built, well-named functions** for the real operations rather
   than keeping the generated CRUD names. Name a context after its business area (accounts or identity for user
   management), not after a table.
3. **Cross-context links are deliberate.** One context may depend on another's data (a cart item belonging to a
   catalog product); make that dependency an explicit association in one place, and keep each context
   responsible for its own rules. Let the database enforce referential integrity with delete rules, rather
   than cleaning up in application code across contexts.
4. **Scope every query to the caller.** The authentication generator provides a scope struct holding the current
   user, assigned on the connection; context functions take the scope and filter by it, so a user reaches only
   their own records. Authentication says who the user is; the scope decides what they own.
5. **Authorise from the authenticated user, never from submitted values.** Take the user from the connection's
   assigns (or the scope); an email or id coming from the request body lets the caller act as anyone.
6. **Cast only the fields a user may set.** Changesets list permitted parameters explicitly; a field like an
   admin flag in a public sign-up cast lets anyone create an administrator.
7. **API authentication reuses the session token table.** Issue API tokens from the same store as the generated
   authentication with a distinct token kind and its own validity period, verify them in a plug, and return
   distinct statuses for "not found" and "invalid"; such tokens expire when the email changes.
8. **Never pass untrusted input to code evaluation or command execution functions.** The unexpected route is
   deserialising external binaries: the safe option of the Erlang decoder only prevents atom creation, not
   executable terms; use the Plug-provided non-executable decoder for untrusted data.
9. **Query fragments take arguments, not interpolation.** The query DSL parameterises values passed as arguments
   (and refuses a non-literal fragment string at compile time); building a raw SQL string from user input and
   passing it to the repo's query function is injection. Use parameters.
10. **An outbound request built from user input is a request forgery risk,** not only against cloud metadata
    addresses but against any internal service the app can reach. Avoid user-controlled URLs; a base URL set in
    client configuration is not a barrier, since it can be overridden by an absolute URL in the request.
11. **List allowed CORS origins by name;** a policy that allows any origin lets a hostile site read data for a
    logged-in visitor.
12. **Templates escape by default; the raw-output function bypasses it.** Never pass user input to it. HTML built
    from user input in a controller response, or a content type chosen by the uploader, is the same hole: restrict
    the content types you serve to the ones you intend.
13. **State changes go through POST (or another unsafe method) with the CSRF check, never GET.** The default browser
    pipeline includes the forgery-protection plug; a GET route that reaches an update action lets a link trigger
    the change.
14. **Run a security scanner in CI and read its confidence levels.** Sobelow's README describes checks for
    insecure configuration, vulnerable dependencies, XSS, SQL and command injection, code execution, directory
    traversal and unsafe serialisation; a low-confidence finding means "needs a human look", not "safe". Credo is
    the code-consistency linter. Neither was run for this block.
15. **Database tests use the SQL sandbox: each test runs in a transaction rolled back at its end.** Mark a test
    case async when it only uses the sandbox so cases run in parallel (tests within a case still run serially).
    Context tests call the context functions and assert on their results; they sit beside controller tests, not
    inside them.
