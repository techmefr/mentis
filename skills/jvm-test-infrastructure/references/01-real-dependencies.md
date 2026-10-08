# jvm-test-infrastructure §1 — Real dependencies with Testcontainers

A test that passes against an engine production does not run proves little about the query. Testcontainers
starts the real thing in a container for the test. Names and packages are as in the Testcontainers for Java
documentation and the Spring Boot 4.1 testing pages.

## 1.1 Use the real engine for anything that touches the database
1. **Do not test data access on an embedded database of another dialect.** Spring Boot's data slices default
   to an in-memory database when one is on the classpath, and the Testcontainers documentation lists, as a
   reason to use it, database features the embedded one does not emulate; a real database in a container gives
   full compatibility at the price of speed.
2. **Tell the Boot slice to keep the container's database.** For `@DataJpaTest` (and the JDBC slices) the
   Spring Boot page shows `@AutoConfigureTestDatabase(replace = Replace.NONE)` to stop it replacing the
   configured data source.
3. **Pin the image to the version production runs,** not `latest`, so the migrations and the queries run
   against the same engine that serves them.

## 1.2 Wire the container without fixed ports
1. **Never hard-code the host or port.** Testcontainers maps a container port to a random free port on the
   host, so the address is only known once the container is running. Ask for it with `getHost` and
   `getMappedPort`, and let the framework pass it on.
2. **Prefer a service connection when Spring Boot supports the service.** Annotate the container field with
   `@ServiceConnection` and Boot creates the connection-details bean for it; those details take precedence
   over connection properties in the configuration. It needs the `spring-boot-testcontainers` module as a
   test dependency, and for a generic container the `name` attribute tells Boot which service the image is.
3. **Otherwise register the properties dynamically.** A static method annotated `@DynamicPropertySource` adds
   values to the Spring environment from the running container. It is more verbose but more flexible.

## 1.3 Share the container
1. **A static `@Container` field is shared by the methods of one test class.** With the JUnit 5 extension a
   static container stops after the class, and a non-static one after each test method; shared containers
   cannot be declared inside nested test classes.
2. **To share across classes, start it once.** The documented singleton pattern starts the container in a
   static initialiser of a common base class; the cleanup container stops it at the end of the suite.
3. **With Spring, prefer containers as beans or an imported declaration** when the context stays cached
   (`@ImportTestcontainers`, or a `@Bean` method on the test configuration). Spring then creates the
   container before other beans and stops it after they are destroyed, once per cached context; a container
   managed by Testcontainers alone gives no guarantee of that shutdown order and the beans can throw on a
   lost connection.

## 1.4 The cleanup container
1. **Leave it on.** The resource reaper removes containers and cleans up dead ones when the JVM exits, and it
   is what stops a singleton container at the end of a suite.
2. **Turn it off only where the environment already cleans up and cannot start privileged containers,** by
   setting the environment variable `TESTCONTAINERS_RYUK_DISABLED` to `true`. Testcontainers still cleans up
   at JVM shutdown unless the process is killed hard.

## 1.5 Reuse
1. **Reusable containers are experimental and opt-in per machine.** They keep running after the tests and
   are reused only when the configuration is identical. The documentation says they are not suited to CI.
   Use them, if at all, for a developer's inner loop, never in a pipeline.

## 1.6 Checks
- The test fails if the container is pointed at a different engine version than production (the image tag
  is read from one place).
- Search the test configuration for a fixed database host and port: none is left, and the suite passes.
- After a full run no test container remains (`docker ps` is empty), including after a failed run.
