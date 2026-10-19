# jvm-test-infrastructure §2 — Spring Boot slices and the context cache

Spring Boot 4.1 and Spring Framework 7.0 documentation. Annotation names and packages differ in earlier
major versions, so check the version in use; the mock-bean annotation named here is the framework's
`@MockitoBean`.

## 2.1 Pick the narrowest test that proves the thing
1. **A slice loads one layer, a full context loads the application.** The Boot documentation offers
   `@WebMvcTest` for controllers (it scans controllers, advice, converters, filters and similar web beans,
   not regular components), `@DataJpaTest` for JPA, and `@JsonTest` for serialisation, each with its own
   auto-configuration. When a test only needs the web layer, use `@WebMvcTest` instead of starting the whole
   application.
2. **Use a full `@SpringBootTest` for wiring** and for flows that cross layers; do not use it to check
   one controller's validation.
3. **A slice does not scan your regular components or configuration properties,** so a collaborator is
   supplied by a mock bean or imported explicitly. If a slice test fails for a missing bean, the test
   caught a hidden dependency; do not widen the slice to the full context to make it pass.
4. **A slice that unexpectedly scans your components** is the symptom of a `@ComponentScan` placed on the
   `@SpringBootApplication` class, which overrides the default scan for every slice. The Boot page's fix is
   to move the custom scan to a separate configuration class.

## 2.2 How the context cache works
1. **A context is built once and reused for every test with the same configuration key,** within one test
   suite in one process. The key is built from the context configuration (locations, classes, initialisers),
   context customizers, the loader, the parent, the active profiles and the test property sources.
2. **Bean overrides and dynamic properties are part of the key.** The framework page lists, among the
   customizers, `@DynamicPropertySource` methods and bean overrides such as `@MockitoBean`, plus several Boot
   test features. Two classes that differ in any of those do not share a context.
3. **The cache is bounded.** The default maximum is 32 contexts with least-recently-used eviction (set
   `spring.test.context.cache.maxSize` to change it); an evicted context is closed, and with it any
   container the context manages.
4. **Forking defeats the cache.** The cache is a static variable, so tests run in separate processes each
   start from empty. Do not configure the build to fork a new JVM per test class.
5. **`@DirtiesContext` removes the context** and the next test needing it rebuilds it. The framework calls
   corruption "unlikely"; it is for a test that really breaks the context, not for cleaning data.

## 2.3 Keep the key stable
1. **Put shared mocks and properties on a common base class or configuration,** so most classes have one
   key. A mock bean declared on one class for convenience is a new context for that class.
2. **Drive state through the data, not through the context.** Reset the database between tests by
   transaction rollback or an explicit cleanup, not by dirtying the context.
3. **Read the cache statistics.** Set the log level of the `org.springframework.test.context.cache` category to
   debug and count the contexts built in a full run; a number that grows with the number of test classes
   is the problem.
4. **JMX is off in cached contexts by default,** to avoid identical components registering in the same domain;
   a test that needs it must dirty its context, which is exactly the cost to know about.

## 2.4 Checks
- Run the suite twice from cold and compare the number of contexts built against the number of distinct
  mock and property combinations.
- Remove one `@MockitoBean` or `@DynamicPropertySource` from a class and see the count drop.
- Each slice test lists only the layer's beans; none loads a repository when it tests a controller.
