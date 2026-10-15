# nginx-proxy-pitfalls §4 — A label-driven container proxy (caddy-docker-proxy)

caddy-docker-proxy is a Caddy plugin that reads Docker labels, generates a Caddyfile in memory and reloads
Caddy when a container changes, without downtime. It removes the proxy file and adds a layer in which a
mistake is invisible until you read what it generated.

## 4.1 Only containers on an ingress network are served
1. **Only containers and services connected to the Caddy ingress networks are used** as upstreams, so a
   container on another network is not routed even with correct labels (the README's `upstreams`
   function).
2. **The proxy detects the ingress networks automatically, as a best effort, and the README says that logic
   fails in some scenarios** (it links an issue). By default the ingress networks are those attached to the
   controller container.
3. **Set them explicitly.** Use the `ingress-networks` option or the `CADDY_INGRESS_NETWORKS` environment
   variable, or give one container or service a `caddy_ingress_network` label naming the network:

```yaml
services:
  caddy:
    image: lucaslorentz/caddy-docker-proxy:${PROXY_VERSION}
    ports:
      - 80:80
      - 443:443/tcp
      - 443:443/udp
    environment:
      - CADDY_INGRESS_NETWORKS=caddy
    networks:
      - caddy
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - caddy_data:/data

  app:
    image: example/app:1.4.0
    networks:
      - caddy
    labels:
      caddy: app.example.com
      caddy.reverse_proxy: "{{upstreams 8080}}"

networks:
  caddy:
    external: true

volumes:
  caddy_data: {}
```

   The tag comes from a variable so that a released version is chosen on purpose (§4.4).
4. **Create the network with IPv6 if clients use it.** The README notes that without the `--ipv6` flag on
   `docker network create`, Caddy and its upstreams see Docker's gateway address instead of the real client
   address for IPv6 clients.

## 4.2 Labels become a Caddyfile
1. **Quote upstreams only in YAML.** The README warns about quotes around `{{upstreams}}` and says they
   should only be added when using YAML (own reasoning: an unquoted template is not valid YAML, while
   other label sources need no quotes). It shows that a quoted value produces one quoted argument holding
   all the addresses. The page does not say more, so read the generated file (§4.3) after any change to quoting.
2. **Directive order is rearranged after generation.** Caddy sorts directives by its own default directive
   order when it parses the generated Caddyfile. Within the labels, directives are first ordered
   alphabetically.
3. **Control order with a numeric prefix.** `1_name` gives a custom order (mainly inside `route` blocks), and
   directives without a prefix go last. A suffix `_0`, `_1` keeps otherwise grouped directives apart.
4. **Where you define the labels decides what is proxied.** For a Swarm service, labels go inside `deploy`;
   for a plain container they go outside it (the README's services versus containers section). Own
   reasoning: labels on the wrong level target the wrong kind of object, so confirm with §4.3.
5. **A label with no value produces a directive with no arguments.** Some tools cannot set an empty label,
   and the README offers a template that renders to an empty value for that case.
6. **Global options come from labels that have no value for `caddy`**, from any container or service,
   including the proxy itself; so a label on an unrelated container can change the global configuration.
   Own reasoning from the README's statement that they can be set in any container or service.

## 4.3 Read what was generated
1. **The generated Caddyfile is saved as `Caddyfile.autosave` in Caddy's config directory** whenever it
   changes, typically `/config/caddy/Caddyfile.autosave` in Docker; its full path is logged at startup.
2. **Read it with `docker exec <caddy-container> cat /config/caddy/Caddyfile.autosave`** to troubleshoot
   the conversion, as the README suggests, rather than inferring the result from the labels.

## 4.4 State and images
1. **Keep Caddy's data folder on persistent storage.** Without a volume on `/data`, Caddy re-issues
   certificates at every restart and can exceed the certificate authority's quota (the README's warning for
   production). Several replicas can share the folder, and then coordinate issuing among themselves.
2. **The default image has only the Caddy executable, so it has no shell, `curl` or `dig`**: small and safe,
   but hard to troubleshoot. The `alpine` variant adds a shell and basic tools and trades some security and
   size for easier troubleshooting. Own guidance: use the alpine variant to troubleshoot, and decide
   deliberately whether to ship it.
3. **Pin a full version number.** The README calls the full version the safest and says a partial one pulls
   the newest matching release automatically.
4. **Images with the `ci` suffix track the master branch** and their stability is not guaranteed.

## 4.5 The Docker socket
1. **Controller instances need access to the Docker host socket; server instances do not.** In the
   distributed mode, a controller generates configuration and pushes it to servers, which can run on any
   node and do not mount the socket; the README warns that controller mode needs servers to serve traffic.
2. **The standalone mode used in the sample mounts the socket.** What that grants and how a filtering proxy
   narrows it are in `docker-compose-file-pitfalls` §3.1.

## 4.6 Verify
Read `Caddyfile.autosave` after every label change, request each hostname, and restart the proxy once to
confirm certificates are not re-issued.
