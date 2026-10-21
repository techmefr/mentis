# docker-compose-file-pitfalls §3 — The Docker socket and commands that delete data

Two things in a Compose workflow cost the most when they go wrong: giving a container the Docker socket,
and running a "clean restart" that removes volumes.

## 3.1 The Docker socket is root on the host
1. **Do not mount `/var/run/docker.sock` unless the service genuinely needs it** (Docker's skill).
2. **Access to the socket can mean root access to the host, or to a whole swarm** (the socket proxy project's
   rationale). Some tools (reverse proxies that react to container events) need it; for those, put a
   filtering proxy in front instead of the raw socket.
3. **A socket proxy returns `403` for the API sections you leave revoked.** The Tecnativa proxy is
   configured by environment variables where `0` revokes and `1` grants access to an API section.
   `EVENTS`, `PING` and `VERSION` are granted by default; `AUTH`, `SECRETS` and `POST` (without it only `GET`
   and `HEAD` are allowed, so the API is read-only) are revoked by default and are called security-critical.
   Grant only the sections the consumer needs.
4. **Never publish the proxy's port to a public network.** Put it on a Docker network that contains only the
   proxy and the one service that uses it. The image has no TLS (it is plain HTTP to the Unix socket by
   design), so the network boundary is the protection.
5. **The proxy container itself holds the socket**, so it is a privileged container (its documentation runs
   it with `--privileged` for SELinux and AppArmor contexts). Treat it as part of the trusted base.

```yaml
services:
  dockerproxy:
    image: tecnativa/docker-socket-proxy:${PROXY_VERSION}
    environment:
      CONTAINERS: 1
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    networks:
      - proxynet
  watcher:
    image: example/watcher:1.4.0
    environment:
      DOCKER_HOST: tcp://dockerproxy:2375
    networks:
      - proxynet
networks:
  proxynet:
```

   The tag comes from a variable so that a released version is chosen on purpose (§2.1); the project's
   documentation says `latest` is the latest released version and `edge` the master branch. Whether to also
   mark the network `internal` is not covered by the sources read.
6. **Do not use the socket proxy as a way around the rule in point 1.** It narrows the socket, it does not
   make it safe.

## 3.2 Commands that delete data
1. **Name the loss and confirm before** `docker compose down -v` (or `--volumes`: deletes the named volumes
   including database data), `docker compose rm -v` (deletes anonymous volumes attached to removed
   containers), and `docker volume rm` or `docker volume prune` aimed at a project's volumes.
   `docker compose down` alone removes containers and networks but keeps named and anonymous volumes;
   `--remove-orphans` removes containers of services no longer in the file, which surprises someone who
   renamed a service.
2. **A volume declared `external: true` is not managed by the project**, so `down -v` leaves it alone. Treat
   removing it as the standalone case: `docker volume rm` without `-f` first, and a confirmation.
3. **"Restart" and "clean up" do not mean those commands.** To restart services, or reclaim containers and
   networks, use `docker compose down` without `-v`, or `docker compose restart`: named volumes survive.
4. **Do not run one as a side effect of debugging.** The data it removes is usually the thing that made the
   bug reproducible.

## 3.3 Verify
Before an uncertain cleanup run `docker volume ls` and note which volumes belong to the project; after a
`down` without `-v`, check that the same volumes are still listed and that the database starts with its old
data.
