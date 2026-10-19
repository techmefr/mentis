# redis-security-and-observability-pitfalls §1 — Authentication, ACLs and network exposure

Sources: the `redis-security` skill of redis/agent-skills at a84871d (`SKILL.md`, `references/auth.md`, `references/acls.md`, `references/network.md`), read 2026-10-16. The files give no Redis version. The source's point is that authentication, access control and network exposure are covered together, since any one of them alone leaves a gap.

## 1.1 Authenticate, and encrypt
1. **Never run a production Redis without a password.** The source pairs authentication with TLS so credentials and data do not travel in clear text; its server settings are `requirepass`, a `tls-port`, and the certificate and key files, and its client example turns TLS on and requires certificate verification.
2. **`requirepass` is effectively the legacy shortcut for the `default` user.** When ACL users can be used instead of the single password, use them (§1.2).
3. **Connecting with only a host and a port is the failure the source shows,** in Python and in Java: no password, no TLS.
4. **Own guidance:** the source's examples write the password into the code. Read the credential from the deployment's secret store (`security-hardening`), and keep it out of the repository.

## 1.2 One ACL user per application
1. **The `default` user with a shared password is for development.** For production give each application a dedicated ACL user with only the commands and key patterns it needs, and never use one shared password for all access.
2. **The source's three shapes**, with the password replaced by a placeholder:

```
ACL SETUSER app_readonly on >REPLACE_ME ~cache:* +get +mget +scan
ACL SETUSER app_writer on >REPLACE_ME ~* +@all -@dangerous
ACL SETUSER admin on >REPLACE_ME ~* +@all
```

3. **Read them as follows.** The reader may touch only keys under the `cache:` prefix and only `get`, `mget` and `scan`. The writer reaches every key and every command except the `@dangerous` category. The admin has everything, is used sparingly, and never carries application traffic.
4. **Command categories the source names:** `@read` (for example `GET`, `MGET`, `HGET`), `@write` (`SET`, `DEL`, `XADD`), `@dangerous` (`FLUSHALL`, `DEBUG`, `KEYS` and others) and `@admin` (administrative commands). Own guidance: the category contents are the server's, so check them against the server version in use before relying on a category as a boundary.
5. **The point of the tight user is the leak.** If application credentials leak, a narrow ACL bounds the damage: whoever takes a cache reader's password cannot run `FLUSHALL`.
6. **Own guidance, not run:** after creating a user, connect as that user and try one command it must be refused, so the boundary is tested and not assumed.

## 1.3 Restrict who can reach the server
1. **The source's most common breach is a Redis reachable from the internet without authentication.** It layers three defences: bind to specific interfaces, keep `protected-mode` on, and put a firewall in front that allows only the application subnets and drops the rest.
2. **The anti-pattern is binding to all interfaces with `protected-mode` off.** It exposes the instance to the whole network with no protection.

```
bind 127.0.0.1 192.0.2.10
protected-mode yes
```

## 1.4 Destructive commands
1. **The source also shows disabling destructive commands with `rename-command` to an empty name** (its examples are `FLUSHALL`, `DEBUG` and `CONFIG`), as an optional but recommended step, so a compromised client cannot trash the database.
2. **That directive could not be confirmed as current guidance for this block.** The Redis documentation was not read (it is idea-only for this programme). Prefer the ACL command categories of §1.2 to restrict what a client may do, and treat `rename-command` as something to verify against the documentation of your server version before adding it or relying on it. If an existing configuration already uses it, leave it and verify before changing it.
3. **A `-@dangerous` rule also removes `KEYS`** (the source lists it in that category), which agrees with never calling it in production (`redis-client-and-cluster-pitfalls` §2).

## 1.5 Checks (own guidance)
1. Every application has its own ACL user, and the list of users on the server matches the list of applications plus one admin.
2. The instance is not reachable from a network that has no business with it, tested from outside, and `protected-mode` is on.
3. The admin credential appears in no application configuration.
4. A refused command was tried as each application user.
