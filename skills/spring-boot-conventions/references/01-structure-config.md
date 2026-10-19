# § 1 — Package layout, injection, configuration

> Section 1 of `skills/spring-boot-conventions`. Read it when a class is placed, a bean is wired, a property is
> read or an environment-specific difference is introduced. Read 2026-10-02 from the Spring Boot reference
> (4.2.0-SNAPSHOT): structuring your code, beans and dependency injection, externalized configuration, profiles.

1. **Never use the default package; put the application class in a root package above the rest.** Scanning
   starts from the package of the annotated class, so a class in the default package scans the whole
   classpath. A root-package main class lets every feature package sit below it and be found without extra scan
   configuration.
2. **Constructor injection with `final` fields.** With a single constructor no annotation is needed; when there
   are several, mark the one the container must use. Field injection hides dependencies from the constructor
   and from tests.
3. **Read configuration through a typed properties class, not `@Value`.** A class bound to a prefix gives
   hierarchy, a type per field, validation and a place to document each property; `@Value` scatters string
   keys. When a placeholder must name a property, use the canonical kebab-case lowercase form so relaxed
   binding applies.
4. **Prefer constructor binding (a record works) for properties.** The class is immutable and a missing value
   is visible at construction. It requires the class to be registered through properties scanning or an
   explicit enabling annotation, not created as an ordinary bean, and the code compiled with parameter names
   kept. Give defaults on the parameter, not in the consumer.
5. **Validate properties at startup.** Put the validation annotation on the properties class and constraint
   annotations on its fields (and the cascade annotation on nested objects). A service that starts with a
   blank URL fails at the first request instead of at boot.
6. **Know the override order before adding a source.** Environment variables, command-line arguments and
   external files override the packaged file; profile-specific files override the non-specific ones, and with
   several active profiles the last wins. The `env` and `configprops` endpoints show why a property has its
   value (§3.1 for exposing them safely). Operating-system variables use underscores for dots, so name
   properties so that the mapping stays unambiguous.
7. **Everything that varies by environment is a property, not a profile-guarded class.** Profiles select whole
   beans or whole files; they are for deployment shape (a test double, a development database), not for
   secrets or hostnames, which come from the environment. A bean that exists only under a profile is code the
   other environments never exercise.
8. **`spring.profiles.active` is set only in a non-profile-specific document;** setting it inside a profile
   file is invalid. Activate by environment variable or argument at deploy time, and keep `default` for what a
   developer needs to run the service with no setup.
