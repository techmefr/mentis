# § 4 — Files, secrets and dependencies

> Section 4 of `skills/security-hardening`. Read it when a diff adds an upload, touches a secret, or
> brings in a new dependency.

1. **Uploads**: validate the type from the content rather than the filename or the client-supplied
   MIME type, cap the size, and store outside the web root with a generated name. Never build the
   storage path from user input. The generated name is doing two jobs — it removes the traversal
   (§2.7) and it removes the collision, which is the other way one caller reaches another's file.
2. **Secrets** come from the environment or a vault, never a literal in the code, never a fallback
   default in a config file, and never committed "temporarily". Detail on keeping them out of logs is
   in `auth-session-conventions` §2.4.
3. **A new dependency is a decision**: check that it's maintained and that the functionality genuinely
   isn't in the standard library or in something already installed. Every dependency added is code
   you now ship and don't review.
4. **A file the server will serve back is a stored output.** An uploaded document returned to a browser
   is rendered by it, so the response's content type has to be set by you from the validated type
   rather than inferred, and anything served from user-supplied content is served as a download or from
   a separate origin. Otherwise an upload is a script that runs under your domain's authority.
5. **Never trust an image, an archive or a document to be inert.** These formats are parsed by large
   libraries, and the parse happens before any of your logic: a bomb that expands to fill the disk, an
   archive whose entries escape the extraction directory, a document format that fetches a remote
   entity. Cap the decompressed size, resolve every extracted path, and disable external entity
   resolution where the parser offers it.
6. **A secret committed once is committed forever.** Rotating is the fix; deleting the line is not,
   because the object stays reachable in the history and in every clone and fork already taken. Treat
   the exposure as real from the moment of the push, not from the moment somebody notices.
7. **A secret in an environment variable is still readable by everything in the process.** That is the
   right default and not a vault, so it follows that a crash reporter, a debug page, a subprocess
   inheriting the environment and a log of the configuration at startup are all places the value shows
   up. Whatever prints configuration prints an allow-list of keys.
8. **A secret has a scope and an expiry, or it has neither.** A single credential shared by every
   service and never rotated makes any one exposure a full compromise and makes rotation an outage, so
   the rotation is deferred indefinitely. Separate credential per consumer, least privilege on each,
   and a rotation that has actually been performed once.
9. **The lock file is the dependency inventory, not the manifest.** What ships is the resolved tree,
   including everything transitive that nobody chose, so a dependency review that reads the manifest
   has read the smaller half. Commit the lock file, install from it, and let whatever scans for known
   vulnerabilities read it.
10. **Pin what runs, and know what a version range lets in.** A range means the build is not
    reproducible and that a compromised release can arrive without a change on your side; the same
    applies to a container tag that moves and to a script piped from a URL into a shell, which is the
    shape this repo's own install guard exists to refuse.
11. **A dependency's install step is code that runs on your machine.** Post-install hooks execute with
    your credentials at the moment of installation, before any of your review, which is why an install
    is a deliberate act with a named reason rather than something done to make a command work.
12. **Removing a dependency is part of the decision.** The cost of one is paid continuously — updates,
    advisories, the transitive tree, the build — so a dependency that is no longer used is still being
    paid for and still shipping code. Deleting it is the cheapest security work available
    (`skills/design-patterns` §6).
