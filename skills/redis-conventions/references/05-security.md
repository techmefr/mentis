# § 5 — Security

> Section 5 of `skills/redis-conventions`. Read it when a server is deployed or reviewed, or credentials are
> created. The vendor's stated model is that the server is for trusted clients inside a trusted network, so
> every rule below is a layer that makes that true, and none of them replaces the others.

1. **The port is reachable only by the application that uses it.** Bind to the interfaces that are needed, not
   to all of them, and firewall the rest. An exposed instance with no authentication lets any stranger read
   and delete the whole dataset with one command, and instances left exposed this way are the common breach.
   The server's protected mode refuses outside clients when it runs with default binding and no password;
   treat it as a last net that an operator can switch off, not as a design.
2. **Untrusted users never talk to the server directly.** A web application sits between browsers and the
   store, validates input and decides which operation to run. Never forward a user-supplied command name or
   key pattern to the server.
3. **Authenticate every client, with named users.** Access control lists (since version 6) give each
   application its own user; the single shared password is the legacy method. A shared password in a
   configuration file also has to be long enough to resist guessing, because the server answers guesses very
   fast. Authentication is a second layer behind the network rule, not a substitute for it.
4. **Encrypt the transport with TLS** on client connections, on replication links and on the cluster bus,
   since the authentication command and the data otherwise cross the network in clear text.
5. **Give each application the least access that works.** One user per application, restricted to the key
   patterns it owns (the tenant or service prefix of `01`'s key naming makes this expressible) and to the
   command categories it needs, with the dangerous and administrative categories off. A leaked
   cache-reader credential then cannot flush the dataset. Keep the administrative user out of
   application configuration.
6. **Do not use renamed or disabled commands as the control.** The vendor marks the command-renaming
   directive deprecated and points to access rules instead; remove dangerous commands from the application
   user's categories rather than renaming them.
7. **The injection surface is narrow but not zero.** The protocol is length-prefixed and binary-safe, so a
   normal client library cannot be injected through a value. The exceptions are the ones you create: a script
   body assembled from untrusted strings, and a command name or key built from user input. Pass data as
   arguments, never as part of the script text or the command (`skills/security-hardening` §1).
8. **Run the server as an unprivileged user,** never as root. A client able to change the server's
   configuration can redirect where it writes its data files, which turns a network exposure into code
   execution as the server's user; this is why the configuration command is among the things an application
   user must not hold.
9. **Treat data in the store as sensitive as the database it mirrors.** A cache of personal data is a copy of
   personal data: it is subject to the same retention, deletion and access rules (`business/data-protection`),
   and an expiry (§2.1) is also a retention control. Backups and snapshot files hold the same data and need the
   same protection.

**Sources:** the vendor's security documentation (security model, network security, protected mode,
authentication, TLS, command disallowing, injection, code security) and its development skill on security
(MIT), read 2026-10-02. The instance-versus-version caveats: access control lists need version 6 or later.
