# jvm-resilience-observability §2 — Operating the service on Spring Boot

Spring Boot 4.1 documentation and the Micrometer 1.17 reference unless another source is named. The rules for
what to log and measure are in `observability-instrumentation` §2 and §3; this section is what the framework
does, and the places it does not.

## 2.1 Correlation id and thread hand-offs
1. **Log a correlation id on every line of a request.** When tracing is enabled Spring Boot builds the default
   correlation id from the `traceId` and `spanId` values in the logging context (the MDC) and adds it to the
   log line. You can add your own context entries to the line pattern with `logging.pattern.level`, for
   example a `%X{user}` entry.
2. **The correlation id relies on context propagation,** so a task handed to another thread does not get it
   unless it is forwarded. The Boot documentation uses the Context Propagation library for that: for `@Async` methods on
   the auto-configured executor you opt in with `spring.task.execution.propagate-context`; for an executor
   you configure yourself, register a `ContextPropagatingTaskDecorator` bean; in reactive pipelines set
   `spring.reactor.context-propagation` to `auto`.
3. **Outgoing calls only carry the trace if the client is built from the auto-configured builder.** A
   `RestClient`, `RestTemplate` or `WebClient` created without it does not propagate automatically.
4. **Test it.** Log from an async task in a test and assert the id is present (see the checks below).

## 2.2 Metric tags
1. **Name meters in lowercase dot notation and keep the name meaningful on its own,** so selecting the name
   alone gives a total that can be drilled into by a tag. The Micrometer naming page contrasts a counter
   named for what it counts with a vague `calls` counter that mixes database and HTTP traffic.
2. **Tag values from user input must be normalised and bounded.** The Micrometer page warns that user-supplied
   tag values can blow up the cardinality of a metric, and its example is the URI tag, where not collapsing
   unknown resources to one value makes every missing path a new series. Never tag by id, raw URL or free
   text.
3. **Common tags go on the registry,** with configuration properties or a `MeterRegistryCustomizer` bean, and
   before meters are registered.

## 2.3 Liveness and readiness
1. **Liveness answers "restart me?", readiness answers "send me traffic?".** Spring Boot exposes them as
   health groups on `/actuator/health/liveness` and `/actuator/health/readiness`, built from the
   application's availability state.
2. **The liveness probe must not depend on external systems.** The documentation's reason: if a database, a
   web API or a cache fails and liveness reports it, Kubernetes restarts every instance and creates a
   cascading failure.
3. **Readiness is a judgement call, and Boot adds nothing to it by default.** An external system that is not
   shared between instances may belong there; one the application can degrade around (it has a breaker and
   a fallback) should not; one shared by every instance is a decision between taking all instances out of
   service and handling the failure higher up. Decide per dependency and write it down.
4. **A slow start needs a startup probe,** which uses the liveness endpoint, so that the orchestrator does
   not kill the instance while it is still starting.

## 2.4 Graceful shutdown
1. **It is on by default** with Jetty, Reactor Netty and Tomcat: on shutdown the server stops accepting new
   requests and lets existing ones finish within a grace period.
2. **Set the grace period on purpose** with `spring.lifecycle.timeout-per-shutdown-phase`. A shutdown from an
   IDE may be immediate if it does not send a proper termination signal, so test shutdown with a real
   signal, not by stopping from the editor.
3. **The page covers the web server's drain.** An executor you create yourself has to be shut down by your
   own code; see `java-conventions` §3.

## 2.5 Structured logs
1. **Turn on a structured format in production.** Boot supports JSON formats out of the box (Elastic Common
   Schema and Logstash among them), selected with `logging.structured.format.console` or
   `logging.structured.format.file`; a custom logging configuration must be changed to respect the
   structured-format system properties.
2. **Keep the fields the generic rules ask for** (`observability-instrumentation` §2), and never log
   a token or a whole request body.

## 2.6 Checks
- A log line from an `@Async` task and from a scheduled task carries the correlation id.
- The metrics registry holds a bounded number of series for a tag after a scan of random URLs.
- Probe queries with the database stopped: liveness up, readiness as designed.
- Send a termination signal during a slow request: the response completes, then the process exits.
