# § 1 — File layout, naming, order

> Section 1 of `skills/terraform-conventions`. Read it when any configuration is written. These are the
> conventions the vendor's style guide and the community guides agree on; they are cheap and they make every
> later review and every state move easier. `terraform fmt` enforces part of the layout rules mechanically.

1. **Run the formatter and the validator before every commit,** and in the pipeline. The formatter normalises
   indentation and alignment; the validator checks syntax and internal consistency (it does not check that a
   provider will accept a value). Both are safe to run automatically and often, so make them a pre-commit
   check and a first CI step. Add a linter (TFLint is the common one) for the rules the validator cannot know,
   such as provider-specific invalid values.
2. **Split by role, with the conventional file names:** `terraform.tf` (the single block that pins the
   runtime and provider versions), `providers.tf`, `backend.tf`, `main.tf` (resources and data sources),
   `variables.tf` and `outputs.tf` (alphabetical within), `locals.tf`. When `main.tf` grows hard to navigate,
   split resources into files by logical group (network, storage, compute), and keep it obvious where a given
   resource lives. Use override files sparingly: they make the real definition harder to find.
3. **Name resources with a descriptive singular noun, in lowercase with underscores,** never repeating the
   resource type (the address already carries it): `aws_instance.web_api`, not `aws_instance.web_api_instance`.
   The conventional name `this` is for a module that creates exactly one resource of its type, not a default
   for every resource. Use underscores in Terraform names and hyphens inside values a human will see (a DNS
   name). Cloud resources have their own naming limits; this rule is about Terraform's own identifiers.
4. **Order the contents of a resource block consistently:** the repeat meta-argument (`count` or `for_each`)
   first, then ordinary arguments, then nested blocks, then tags if the resource supports them, then
   `depends_on`, then `lifecycle`, with one blank line between groups. A reader then finds the
   repeat/identity-defining argument and the dangerous lifecycle settings without searching.
5. **Order variable and output blocks too:** a variable carries its type, then description, then default,
   then sensitivity, then validation; an output carries description, value, sensitivity. Every variable and every
   output has a description, and every variable has an explicit type: they are the module's documentation and
   its contract (§4.4).
6. **Define things after what they depend on,** so the file reads top to bottom; the order does not affect how
   Terraform builds the graph, only how a human reads it. Put a data source next to the resource that uses it.
7. **Expose a variable only for what changes between deployments.** Over-parameterising makes a configuration
   hard to follow; a value that never differs is a constant or a local. Use input validation where a value has
   a restriction the type cannot express, and no more.
8. **Do not hard-code what can be passed or discovered.** An account identifier, a region, an ami: pass it in
   or read it from a data source, so the same code serves every environment.
9. **Use `count` and `for_each` sparingly, and choose between them deliberately** (§3.1). A conditional
   resource written as a boolean-driven `count` of zero or one is clearer than a length expression.
10. **Comments are for what the code cannot say,** and the idiomatic comment marker is the hash sign. House
    rule: no comments in the code we write; a variable's `description` and a well-chosen name carry the meaning.

**Sources:** the vendor's Terraform style guide (code style, file names, resource naming and order, variables,
outputs, validation, linting), the language reference for the dependency graph, and the community
terraform-best-practices guide (naming, argument order, structure; Apache-2.0), read 2026-10-02. The house
rule on comments in point 10 is ours.
