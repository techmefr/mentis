# search-engine-index-settings-pitfalls §2 — Meilisearch keys and deployment

Sources: the Meilisearch documentation of meilisearch/documentation at 944814e, pages `resources/self_hosting/security/basic_security.mdx` and the first half of `resources/self_hosting/deployment/running_production.mdx` (installation, system user, configuration file, service file), read 2026-10-16. The second half of the deployment page (reverse proxy and TLS) was not read, so nothing is taken from it.

## 2.1 The master key
1. **A self-hosted instance is only protected once a master key is set** (the page presents the key as the first step of securing a project). Start it with a master key, through the command-line option or the environment variable; the start-up log then confirms that requests need a key. The managed cloud service generates one per project.
2. **The key must be at least 16 bytes of valid UTF-8,** and should come from a random generator (the page lists UUID, OpenSSL and hash tools). A weak key makes the instance print a warning and propose a generated one.
3. **Keep it out of public places.** The deployment page puts it in a configuration file next to the production environment setting and warns against exposing it.
4. **Own guidance:** read the key from the deployment's secret store (`security-hardening`) and restrict the permissions of any configuration file that holds it.

## 2.2 Which key goes where
1. **The master key is for managing API keys only.** The page's warning: never use it to search or for other everyday operations.
2. **A protected instance creates four default keys:** a search key, an admin key, a read-only admin key and a chat key.
3. **Only the search key and the chat key may reach a frontend.** The search key allows searching; the chat key allows searching and chat completions. The page states in so many words that admin keys must not be exposed on a public frontend.
4. **The admin key can do everything except manage keys;** the read-only admin key can read across the database. Use the admin key from the backend that configures indexes and adds documents.
5. **Send keys in an authorisation header as a bearer token.**
6. **Own guidance:** each key in the listing carries a list of allowed actions, a list of indexes, and an expiry (null in the page's sample). For a production frontend, create a dedicated key limited to the indexes the page searches, with an expiry, instead of the default one that covers every index.

## 2.3 Run as a dedicated user
1. **Do not run the engine as root.** The deployment page creates a system user with no login shell and a home directory for its data, and gives that user ownership of the binary.
2. **Give it its own data, dump and snapshot directories** with ownership set recursively and mode 750 on the parent.
3. **Run it as a service that restarts on failure,** under that user, started at boot (the page's service file sets the user, the group and `Restart=on-failure`).
4. **Use the vendor's managed service where it fits:** the page itself calls it the recommended way to run in production.

## 2.4 Checks (own guidance)
1. Call the search endpoint with no key, with the search key, and with the master key; only the second should be what an application uses.
2. With the search key, try to add a document and to read the key list, and confirm both are refused.
3. Check the process owner on the host (`ps` shows a non-root user) and the mode of the data directory.
