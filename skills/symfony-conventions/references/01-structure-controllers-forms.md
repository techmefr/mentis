# § 1 — Structure, configuration, controllers, forms, tests

> Section 1 of `skills/symfony-conventions`. Read it when a service, a parameter, an environment value, a
> controller, a form or a test is written. Ideas restated 2026-10-02 from the Symfony best-practices article (no
> wording reused: the source is share-alike).

1. **Keep the default directory layout** unless the project follows a practice that imposes another. It is flat,
   self-explanatory and not tied to the framework, so a newcomer finds things where the documentation says.
2. **Organise your own code by namespace, not by bundle.** A bundle is for code reused as a stand-alone piece
   across projects; internal application logic goes under the application namespace. Reuse across projects is
   the moment to extract a bundle (it can live in a private repository).
3. **Split configuration by what changes it.** Values that differ per machine but do not change behaviour
   (hosts, credentials) are environment variables with one dotenv file per environment; sensitive ones go to
   the secrets mechanism, not a tracked file. Values that change behaviour (a sender address, a feature toggle)
   are container parameters in the services file, overridable per environment. A value that rarely changes
   (a page size) is a class constant, usable in templates and entities where parameters are not.
4. **Name parameters with an application prefix and one or two words** so they cannot collide with a bundle's,
   and keep one separator style throughout.
5. **Autowire and autoconfigure; configure by hand only what is left.** The default services file covers most
   services from constructor type hints. Prefer an attribute next to the code for the odd case, and pick one
   configuration format (YAML or PHP) for the rest.
6. **Services are private.** A private service cannot be pulled from the container at run time, which forces
   dependencies to be declared in constructors and keeps them testable.
7. **Map entities with attributes,** the format that keeps mapping next to the class.
8. **A controller is a few lines of glue.** It reads the request, calls a service, returns a response; the
   business rule lives in a service. Extending the framework's base controller is acceptable for that reason
   (the coupling touches only glue). Configure routing, caching and access with attributes on the action so one
   place describes it.
9. **Inject services as constructor or action arguments;** do not reach into the container from a controller.
10. **Use the entity argument resolver when the lookup is a plain id or slug;** it returns a 404 when nothing is
    found. When resolving the entity takes a real query, call the repository method in the controller instead of
    bending the resolver.
11. **Forms are classes,** reusable across screens and out of the controller. Put the buttons in the template
    (their label and style belong to the screen, not to the form) unless the form has several submit buttons the
    controller must tell apart. One action renders and processes the form.
12. **Put validation constraints on the underlying object, not on the form fields,** so every form and every
    other use of the object gets the same rules.
13. **Templates and translations:** snake_case names for templates and variables, an underscore prefix for
    partials, translation keys that describe purpose rather than location, in a format translators' tools
    read well.
14. **Smoke-test every URL with one data-provider test from the start;** it is a cheap net that no page
    returns an error. Later tests hard-code the URLs they request, so renaming a route breaks them visibly
    instead of silently following it.
