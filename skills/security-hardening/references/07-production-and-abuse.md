# § 7 — Production configuration and abuse resistance

> Section 7 of `skills/security-hardening`. Read it when a diff touches environment configuration,
> error handling, a public or authentication endpoint, a queue of expensive work, or the dependency
> manifest. Nothing here is specific to one framework; each point names the setting by what it does,
> and the last paragraph maps it to two common stacks.

A configuration that is safe in development is usually the opposite of safe in production, and the
difference is invisible in the code because it lives in the environment. This section is the list of
settings that have to differ, and of the limits that keep a correct endpoint from being used as a weapon.

1. **Debug mode is off in production, and the build proves it.** A debug flag turns every unhandled
   error into a page of stack trace, configuration values, environment variables and sometimes source
   lines, served to whoever caused the error. It is the single most expensive misconfiguration to leave
   on, and the commonest because the development default is the on position. Make the production value
   the default and the development value the explicit override, never the reverse.
2. **Configuration is validated when the process starts, not when it is first used.** A missing secret,
   a malformed URL or an unset required value should stop the boot with a message, because the
   alternative is a service that starts, serves traffic, and fails on the first request to touch that
   value, or worse falls back to a default. Read each variable once, in one module, with a type and no
   silent default for anything secret (§4.2).
3. **The environment file is a deployment artefact, never a repository one.** It stays out of version
   control and out of the image build context, a template with placeholders is what gets committed, and
   the deployed value comes from the platform's secret store. A file that exists on the production host
   with broad read permissions is a second copy of every secret in it.
4. **Rate-limit by what an attacker gains, not by what the server can bear.** Authentication,
   password reset, one-time-code verification, signup, search that fans out, anything that sends an
   email or a message, anything that triggers paid work: each gets its own budget, keyed on the right
   thing. The key matters as much as the number: per account for credential guessing (per address alone
   lets one attacker rotate addresses, per account alone lets one attacker lock a victim out), per
   address for scraping, per tenant for fairness. Return the refusal the protocol defines (status 429
   with a retry hint) so well-behaved clients back off.
5. **A limit must hold when the application runs more than one copy.** A counter kept in the memory of a
   single process is multiplied by the number of processes; keep it in a store they share, and decide
   deliberately what happens when that store is unreachable. Failing open is usually right for a general
   API and wrong for a login or a code-verification endpoint.
6. **Make cost proportional to the request, then bound it.** Cap page size, upload size, request body
   size, nesting depth, the number of items in a batch, query complexity and the time any one request may
   take. A limit that is only a rate counts how often a user asks and not how much each ask costs, so a
   single expensive request evades it.
7. **Errors reach the user as a category, and reach the log as detail.** The response says that something
   failed and gives a correlation identifier; the stack, the query and the parameters go to the log
   (`skills/observability-instrumentation`). The same applies to the *difference* between errors: a
   login that answers differently for an unknown user and a wrong password has published the list of
   accounts, and a 403 versus a 404 can say whether a record exists (§3).
8. **Never expose more of a record than the caller is entitled to.** An endpoint that returns the whole
   row and relies on the client to ignore the columns it should not show has published them: the
   password hash, internal flags, other tenants' identifiers, notes. The serialiser lists the fields it
   returns; a model that is serialised wholesale is a leak waiting for the next column (§3.8).
9. **Secure transport is enforced by the application as well as by the edge.** Redirect plain requests
   to the secure scheme, generate absolute links with the secure scheme, mark session cookies secure
   (§6.16) and send the strict-transport header from the secure origin (`skills/devops-conventions`
   §5). When the application sits behind a proxy, trust the forwarding headers only from that proxy's
   address; trusting them from anywhere lets a client assert that its own request was secure, or choose
   the client address your rate limit (§7.4) and your audit log record.
10. **Administrative and operational surfaces are not on the public site.** A metrics endpoint, a health
    page that prints versions, a queue dashboard, a database console, a debug toolbar, an API
    documentation page for internal routes: each is either removed in production, bound to a private
    network, or put behind the same authorisation as the data it reveals. Default credentials on any of
    them are a finding on arrival.
11. **Known-vulnerable dependencies are a gate, and the report is read.** Run the package manager's
    audit against the lock file in the pipeline (§4.9), for production dependencies at least, and read
    what it prints: a report about a development-only tool, or about a path your code never reaches, is
    still worth a recorded decision, and an ignored advisory carries a reason and a date to look again.
    A green audit is a floor (§5.9): it knows only the vulnerabilities somebody has published.
12. **Logs are a data store with a different audience.** Request bodies, authorisation headers, cookies,
    tokens, reset links and personal data do not belong in them, and the redaction list is maintained
    next to the code that handles those fields, because a new field is unredacted by default.
13. **Security events are logged where someone will read them.** Failed and successful logins, privilege
    changes, authorisation refusals, rate-limit trips and configuration changes, with who, what, from
    where and when, and with no secret in the record. An incident without these is reconstructed from
    guesses (`skills/observability-instrumentation`).
14. **The deployment is checked as a deployment.** The headers of §6, the debug flag of §7.1, the
    redirect of §7.9 and the absence of the surfaces of §7.10 are observed against the running
    environment, because every one of them can be correct in the repository and wrong where it runs.

**Mapping, for two common stacks** (names current at time of writing; check the framework's documentation
for the release you use). *PHP with Laravel*: the debug flag is the application debug setting and the
environment name decides which defaults load; configuration is cached for production so that the
environment file is read only at build time; rate limits are declared as named limiters and attached by
route middleware; trusted proxies are configured explicitly; `composer audit` is the dependency check.
*Node*: the environment name controls the framework's error detail, a schema validator over the
environment at startup covers §7.2, the limiter needs a shared store to satisfy §7.5, and the package
manager's `audit` command is the dependency check.

**Sources:** OWASP Top 10 (security misconfiguration, vulnerable components, logging and monitoring
failures); OWASP ASVS (configuration, error handling, anti-automation); OWASP Cheat Sheets (Error
Handling, Logging, Denial of Service, Authentication); RFC 6585 (status 429); RFC 9110 (status
semantics); the documentation of each stack for the release in use.
