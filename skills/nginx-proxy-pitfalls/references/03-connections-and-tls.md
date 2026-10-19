# nginx-proxy-pitfalls §3 — Connections and TLS

Connection limits and TLS settings are trade-offs between capacity, latency and client compatibility. The
boilerplate states the trade-off next to each value; the points below keep it.

## 3.1 Worker and descriptor limits
1. **The maximum number of connections is `worker_processes` times `worker_connections`** (h5bp's main
   file). The boilerplate sets `worker_processes auto`, so it follows the CPU count.
2. **Keep `worker_connections` below `worker_rlimit_nofile`**, the number of open files per worker. The
   boilerplate sets 8000 connections and 8192 descriptors. A proxy holds a descriptor for each client and each
   upstream connection; own reasoning for why the file limit must leave room.
3. **The boilerplate's comment on the connection count**: needing more than that means tuning the operating
   system next. Treat the numbers as a starting point for your host, not a capacity figure.

## 3.2 Keepalive
1. **`keepalive_timeout` is a pool trade-off.** Longer values are better for each client, particularly over
   TLS, but tie up worker connections for longer. The default is 75 seconds; the main file sets 20 seconds.
2. **The TLS file sets a higher value (300 seconds)** to cut repeated handshakes, with the warning that this
   should only be done when you serve mostly HTTPS.
3. **The two files give different values and the files do not say which one wins.** Own note: if you include
   both, check which value is in effect with `nginx -T`, and state the one you chose.

## 3.3 Sessions and cipher preference
1. **Cache TLS sessions** to cut expensive handshakes. The boilerplate keeps them for 24 hours in a shared
   cache of 10 megabytes; the file says one megabyte holds about 4000 sessions, so this holds about 40000.
   The `10m` is a size, not a time.
2. **Turn session tickets off unless you rotate their keys.** Ticket keys are not rotated automatically:
   only a reload signal or a restart does it, and a restart loses the previous key and resets all earlier
   sessions. Enable tickets only with a manual rotation mechanism (h5bp's TLS engine file).
3. **Let the client choose the cipher** (`ssl_prefer_server_ciphers off`) when the TLS 1.2 and 1.3 ciphers
   in the policy are not considered dangerous. The boilerplate's changelog shows this moved to `off` in its
   5.0.1 release (July 2023), so older copies of the boilerplate had a different setting.

## 3.4 Choose a TLS policy and re-read it
1. **TLS settings are version-bound.** The boilerplate points at Mozilla's server-side TLS recommendations;
   use a maintained profile and re-read it when you upgrade, rather than copying a value from an old
   article or from this block.
2. **Two profiles in the boilerplate, as a worked example.** Balanced, for a wide range of clients: TLS 1.2
   only in the boilerplate's version, a cipher list, and the curves `X25519`, `prime256v1`, `secp521r1`,
   `secp384r1`. Strict, for services that do not need backward compatibility: TLS 1.2 and 1.3, the same
   ciphers, and `X25519` only. The strict file warns that old clients may get errors, and that you can add
   the other curves back to support Microsoft Edge and Safari.
3. **The boilerplate calls the NIST curves "known to be weak and potentially vulnerable"** and keeps them in
   the balanced profile only because Microsoft Edge and Safari require them (its comment, relayed here; the
   claim itself was not checked).
4. **TLS 1.3 and 0-RTT need nginx 1.15.4 or later and OpenSSL 1.1.1 or later**, per the strict file
   (version-bound to that file).
5. **Do not enable `ssl_early_data` blindly.** Requests sent in early data are subject to replay attacks.
   The boilerplate ships the directive commented out, and says to pass the `$ssl_early_data` variable to the
   application with a request header, which should answer `425 Too Early` for anything that could contain
   user-supplied data.

## 3.5 Certificate and stapling
1. **The default certificate is served to clients that do not support SNI** (the boilerplate's
   certificate file). The certificate file may contain the intermediate certificate.
2. **With OCSP stapling on, load the intermediate** through `ssl_trusted_certificate` if the certificate
   file lacks it (the same file).
3. **Stapling needs a `resolver`.** The boilerplate sets `ssl_stapling` and `ssl_stapling_verify` on, a
   60-second validity and a 2-second resolver timeout, and lists three public DNS operators as alternatives.
   Choose the resolver your network policy allows; do not copy the list by default.

## 3.6 Verify
Run `nginx -t` and `nginx -T` and read the effective keepalive, protocols and ciphers. Handshake from the
oldest client you support and from a current one; if the old one is refused on purpose, say so in the
change.
