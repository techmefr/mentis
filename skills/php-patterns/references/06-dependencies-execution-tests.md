# § 6 — Dependencies, the execution surface and the test runner

> Section 6 of `skills/php-patterns`. Read it when a package is added, updated or removed, when code
> builds a database statement, a shell command or an include path outside a framework's layer, or when the
> test runner's configuration is touched. Uploads, secrets handling and the audit of a dependency's trust
> are `skills/security-hardening` §4; this section is the PHP and Composer mechanics.

1. **The lock file is committed for an application and not for a library, and CI installs from it.** An
   install from the lock gives every machine the versions that were tested; an update resolves anew and
   produces a different tree from one day to the next. A deploy runs the install command, never the update
   command, and a changed lock in a diff is read like code (what moved, by how many versions, and why).
2. **A new dependency gets a look before it is required.** Who maintains it, when it last released, whether
   its repository matches the name (a one-letter difference in a vendor name is how a typosquat works), how
   many people depend on it, and what its install does. Download counts show popularity, not trust. A package
   that is a thin wrapper over a dozen lines is a dozen lines you own and read.
3. **Composer plugins and scripts execute code at install time.** The `allow-plugins` setting lists each
   plugin that may run, and a new entry in a diff is a review item. Auditing or inspecting an unfamiliar
   package is done with scripts disabled, in a disposable environment.
4. **Version constraints state a decision.** A caret constraint on a stable major, a pinned version for a
   package that breaks in minors, and never a wildcard, an open range or a development branch in an
   application. The platform setting in the manifest names the PHP version production runs, so the lock is
   resolved for production's interpreter and extensions and not the developer's.
5. **The audit runs in CI and on a schedule.** The package manager's audit lists known advisories and
   abandoned packages for the locked set. New advisories appear without any change to the repository, so a
   job that only runs on pushes is silent exactly when a vulnerability is published. An abandoned package is
   replaced; a fork patched in place is a dependency with one maintainer.
6. **Production installs exclude development packages and optimise the autoloader.** The no-dev flag keeps
   test tools and debuggers off the server, where they are attack surface and sometimes expose a dashboard.
   The optimised or classmap-authoritative autoloader removes filesystem lookups per class; with the
   authoritative option a class created at run time is not found, which is the behaviour to want.
7. **Database statements are prepared, and the connection is configured to fail loudly.** Values go through
   bound parameters; a column or table name cannot be bound and comes from a closed list in code. Set the
   error mode to throw exceptions (the default of silent warnings hides a failed query behind a `false`) and
   turn off emulated prepares, so the driver prepares the statement natively and types are not coerced into
   strings on the way.
8. **An include path, a class name and a function name are never built from input.** `include` or `require`
   on a request-derived path executes whatever file that resolves to; a variable class or callable name
   chosen from input instantiates or calls what the caller names. Map an input value to a known entry in a
   table, and use that. `eval`, `extract` and variable variables have no place in application code.
9. **A shell command takes an argument list, or escaped arguments, from validated values.** Anything
   assembled into a command string and passed to a shell is injection waiting for a value with a space or a
   semicolon. Prefer the process component that takes arguments as an array without a shell; where a shell
   string is unavoidable, each variable part goes through the argument-escaping function, and the command
   name is a constant. Paths from users are resolved and checked to be under the intended directory before
   use.
10. **Output is escaped for its context at the point of output.** The HTML escape function with the quote
    flag and an explicit encoding is for HTML text and attribute values only; a URL, a script block and a CSS
    value each need their own treatment. A template engine escapes by default, so the escape function appears
    in application code only outside one, and raw output in a template is a justified exception.
11. **One test framework per project, configured to be strict.** The runner's configuration fails the build
    on warnings, on risky tests (a test with no assertion) and on deprecations, treats unexpected output
    during a test as a failure, and runs in random order where the suite allows it. A suite that tolerates
    all four reports green with debt the next upgrade collects. The popular higher-level layer sits on top of
    the same runner, and the two styles are not mixed in one file.
12. **Data providers carry named datasets.** The provider returns an array keyed by a description of the
    case, so a failure reads "negative amount" and not "dataset 3". One provider per behaviour, declared with
    the runner's current attribute form rather than a docblock annotation, which newer major versions no
    longer read.
13. **Coverage uses the lightest driver that answers the question.** A line-coverage driver is fast and
    sufficient to find untested branches; the debugger extension is slower and needed for path coverage. Enable
    either only in the job that reports coverage, since the debugger extension loaded by default slows every
    local run by a large factor and gets disabled "just this once", permanently. A threshold, if the project
    has one, lives in CI configuration where everyone can read it (`skills/laravel-verification` step 5).
14. **A double replaces a boundary, not a collaborator of your own.** The runner's built-in mocks and
    prophecy-style libraries are for the outbound edge (a gateway, a clock, a mailer). A test that verifies
    that a method on your own class was called with certain arguments restates the implementation and fails
    on any refactor (`skills/testing-anti-patterns`).
