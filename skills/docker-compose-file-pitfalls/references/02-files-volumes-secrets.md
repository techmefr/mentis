# docker-compose-file-pitfalls §2 — The file itself: names, volumes, overlays, secrets

What the Compose file contains decides what ends up in version control and what can be changed from outside
the container in production.

## 2.1 Naming and pinning
1. **`compose.yaml` is the canonical file name.** Docker's skill calls `docker-compose.yml` and
   `docker-compose.yaml` legacy names, and the Compose documentation agrees: `compose.yaml` wins when several
   exist, and the old names are accepted only for backward compatibility. Own guidance: an existing project keeps its name until someone migrates
   it on purpose; do not rename in a drive-by.
2. **Pin every image tag to a version.** Never `latest`, never no tag.
3. **Name services for their role** (`web`, `db`, `cache`, `worker`) and add `container_name` only when
   something outside Compose needs a predictable name; otherwise let Compose generate it.
4. **A restart policy is a production decision.** Docker's production page lists a policy such as
   `restart: always` among the changes to make for production; the skill uses `restart: unless-stopped` for
   long-running infrastructure and non-development deployments. Choose one and state why.

## 2.2 Volumes and overlays
1. **Named volumes for data that must outlive a container** (database data, uploads), all declared under
   the top-level `volumes:`.
2. **Bind mounts only for development-time source sync**, and in `compose.override.yaml`, which Compose
   loads automatically next to `compose.yaml`. Debug ports and development variables go there as well.
3. **Production removes the source bind mounts**, so that code stays inside the container and cannot be
   changed from outside (Docker's production page). Do it with a second file that holds only the
   differences, applied over the base:

```console
docker compose -f compose.yaml -f compose.production.yaml up -d
```

4. **Keep production-oriented settings in the base file** and override only what differs for development
   (the skill's rule); that makes the common path the safe one.
5. **Prefer `develop.watch` to hand-written bind mounts for development** where supported: `action: sync`
   for source files, `rebuild` for dependency manifests, `sync+restart` for configuration that needs a
   process restart.
6. **Other production changes the page lists**: different host ports, quieter logging and settings for
   external services, and extra services such as a log aggregator.

## 2.3 Variables and secrets
1. **No secret in `compose.yaml`.** Docker's skill says to use `env_file:` or Docker secrets, and Docker's
   environment-variable page says to be cautious with sensitive data in environment variables and to
   consider Compose secrets. Prefer a secret to an environment variable for anything whose leak is costly: the Compose
   secrets page says environment variables are visible to every process in the container and can land in
   debug logs, while a secret is one file at `/run/secrets/<name>` granted per service (Linux containers only;
   several official database images read a `_FILE` variable pointing to it).
2. **Defaults go through substitution**: `${DB_PASSWORD:-postgres}`. Never a bare plaintext value for a
   password field.
3. **Add `.env` to `.gitignore`.**
4. **Know the precedence**, highest first: a `run -e` flag; a value interpolated from the shell or a `.env`
   file; the literal `environment:` entry; `env_file:`; and last the image's own `ENV` and `ARG` defaults. A
   command-line setting overrides everything, which is useful for a test and a trap when forgotten.
5. **Use `environment:` for a few non-sensitive values and `env_file:` for a longer list.**
6. **A secret is not granted by declaring it.** It must be defined at the top level and listed under each
   service that reads it. In the long form, `uid`, `gid` and `mode` apply only to a secret whose source is an
   environment variable and are silently ignored for a file source: a file secret keeps the permissions of the
   host file, so an unreadable host file means an unreadable secret.
7. **A short-syntax bind mount creates a missing host directory.** A typo in the host path therefore starts the
   service on an empty directory, with no error. Use the long syntax with
   `create_host_path: false` to make it fail instead.

## 2.4 Redeploying and validating
1. **Redeploy one service** after a code change with `docker compose build web`, then
   `docker compose up --no-deps -d web`. The build makes the new image; `up` recreates only `web`, and
   `--no-deps` stops Compose from recreating the services it depends on.
2. **Validate with `docker compose config --quiet`.** Plain `docker compose config` prints interpolated
   values and `env_file` credentials, which then land in a terminal, a log or a transcript; Compose warnings
   and errors may still contain sensitive details.
3. **Do not create custom networks without a reason.** For a single application the default network is
   enough; add networks for isolation between service groups, with descriptive names, defined under the
   top-level `networks:`. Host port collisions across projects are in `docker-multi-project-dev-environment`.

## 2.5 Verify
Run `docker compose config --quiet` in CI, search the repository and `docker compose config` output (in a
safe place) for any password-like value, and start the production overlay once to confirm that no source
directory is mounted (`docker compose ... config` shows the volumes of each service).
