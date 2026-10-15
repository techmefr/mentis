# otel-collector-config-pitfalls §3 — Exporters, queues and exposure

An exporter that is wired and validated can still drop data on a restart, ship it to the wrong port, or sit on a
volume that corrupts its queue. And the receiving side can listen on the wrong interface.

## 3.1 Pick the exporter
1. **`otlp` is OTLP over gRPC (default port 4317); `otlphttp` is OTLP over HTTP (port 4318).** Match the backend's
   protocol and port (otelcol-doctor).
2. **The `prometheus` exporter is pull**: the Collector exposes an endpoint for Prometheus to scrape. **The
   `prometheusremotewrite` exporter is push**: the Collector sends to a remote-write endpoint. They are not
   interchangeable (otelcol-doctor).
3. **`debug` is the console exporter**; raise its verbosity while debugging (otelcol-doctor).
4. **Removed or renamed components, as otelcol-doctor states them** (no Collector version is given; check the
   current documentation before relying on any of these):
   - the `logging` exporter is removed or deprecated in favour of `debug`;
   - the dedicated `loki` exporter was removed from contrib: send OTLP over `otlphttp` to the backend's native OTLP
     endpoint;
   - the `jaeger` exporter is gone: send `otlp` or `otlphttp`. The `jaeger` receiver still exists for ingesting
     legacy spans during a migration and is not removed;
   - bare `${VAR}` environment expansion is deprecated in favour of `${env:VAR}`.

## 3.2 Queues and durability
1. **A production exporter needs retry and a queue.** The defaults drop data on a transient backend failure
   (otelcol-doctor).
2. **The queue key is per exporter.** `otlp` and `otlphttp` use `sending_queue`, with `storage: file_storage/...`
   added when losing data on restart is unacceptable. `prometheusremotewrite` uses `remote_write_queue` and
   rejects `sending_queue` at startup (otelcol-doctor).
3. **If validation rejects a queue key, look up that exporter's own key**; do not conclude it has no queue and
   ship it with retry only (otelcol-doctor).
4. **`remote_write_queue` is memory-only**: it takes no `storage:`, so a restart loses the backlog. That does not
   mean the exporter has no on-disk option: `prometheusremotewrite` has its own `wal:` (with `directory`,
   `buffer_size` and `truncate_frequency`), or the path can move to `otlphttp` with `sending_queue.storage` against
   an OTLP-capable backend (otelcol-doctor).
5. **A `file_storage` queue goes on a `ReadWriteOnce` block-backed volume, never on NFS, EFS, CephFS in a network
   mode or any `ReadWriteMany` volume.** `file_storage` uses bbolt, which needs byte-level `flock(2)` locking those
   filesystems do not provide reliably, and the database can be corrupted on a multi-writer or failover (o11y-dev).
6. **Shape of an exporter queue with persistent storage** (Dash0's pattern):

```yaml
exporters:
  otlphttp:
    endpoint: https://backend.example.test:4318
    sending_queue:
      enabled: true
      queue_size: 5000
      storage: file_storage

extensions:
  file_storage:
    directory: /var/lib/otelcol/queue

service:
  extensions: [file_storage]
```

## 3.3 What listens where
1. **A receiver bound to `localhost` misses traffic from other containers**, which need `0.0.0.0`; bound to
   `0.0.0.0` it is a security concern where the network is shared (otelcol-doctor).
2. **`pprof` (port 1777) and `zpages` (port 55679) on `0.0.0.0` let any workload on the network extract runtime
   data or profile the Collector.** Bind them to `localhost` or leave them out in production (o11y-dev).
3. **The Collector's own metrics endpoint is a separate case.** Dash0 binds it to `0.0.0.0:8888` because
   Prometheus cannot scrape `localhost` inside a pod. The two sources pull in different directions, so decide per
   endpoint what must reach it, bind accordingly, and record it.
4. **`hostPort` on a horizontally scaled gateway Deployment is fragile**; it suits a DaemonSet agent with one pod
   per node. Use a Service for a gateway (o11y-dev).
