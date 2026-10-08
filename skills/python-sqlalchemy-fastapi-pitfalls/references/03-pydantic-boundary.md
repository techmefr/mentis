# python-sqlalchemy-fastapi-pitfalls §3 — Pydantic at the boundary

Pydantic turns untrusted input into typed objects and typed objects back into output. Used elsewhere it
costs flexibility and hides two silent behaviours: coercion and serialising by declared type.

## 3.1 Use it where the data is untrusted
1. **Pydantic models belong at the edge:** request bodies, configuration, file and message input. The
   Pydantic repository's own guidance is that it is generally not recommended for classes your code
   instantiates itself, because you lose flexibility (types it does not support, post-init changes) and a
   type checker already catches mismatches there. Use a plain class or a standard-library dataclass inside.
2. **Convert once at the boundary** and pass the plain object inward, so the core does not depend on the
   validation library; this is our layering advice, not a Pydantic rule.

## 3.2 Constraints and validators
1. **Prefer built-in constraints over a custom validator:** `Field(gt=1)`, an `annotated_types` constraint,
   `StringConstraints(strip_whitespace=True)` for string normalisation. They are declarative, show up in the
   schema and cost nothing in review.
2. **When a validator is needed, prefer an after-validator.** It runs after Pydantic validation, so the value
   already has the field's type; a before-validator receives arbitrary input, and a model-level one may
   receive something that is not even a dict.
3. **Prefer the annotated form** (`Annotated[int, AfterValidator(fn)]`) so the validator sits next to the
   field. The decorator form makes validator order on subclasses unclear.
4. **Field-specific metadata (alias, deprecated) goes on the whole annotated type,** not on one member of a
   union inside it; it only applies at the top level of the annotation.

## 3.3 Coercion
1. **By default input is coerced:** a string `"123"` is accepted for an `int` field, and a `list[str]`
   field also accepts tuples and sets. A client that sends the wrong type is silently fixed, which is only
   acceptable if you meant it. Use strict mode for fields where it must be an error.
2. **Do not use a union such as `int | str` to coerce a string to an integer through a validator,** and do
   not use abstract collections such as `Sequence` to accept both lists and tuples: the first makes every
   user of the field check both types, the second is inefficient.

## 3.4 Serialisation follows the declared type
1. **A subclass instance under a base-class annotation is serialised as the base class.** The extra fields
   are dropped silently, and validating a dict against the base type does not produce the subclass
   either. A `Main(model=Sub1(...))` dumps without `sub1_field`.
2. **Use a discriminated union** when you can add a literal type field to tell the models apart, or a
   generic model parameterised on the subclass. Polymorphic serialisation (from Pydantic 2.13) and
   serialising as `Any` (before 2.13) are last resorts; the repository names both.
3. **The same applies to a FastAPI return type** (§2.3.5): the declared type decides what leaves, not the
   object you return.

## 3.5 Forward references and aliases
1. **Avoid `from __future__ import annotations` in a module that defines models.** It turns every
   annotation into a string that Pydantic must evaluate later. Quote only the names not yet defined
   (`'Model'` for a self-reference). From Python 3.14 annotation evaluation is deferred, and string
   annotations should not be used at all.
2. **A recursive alias cannot be a quoted `TypeAlias`;** Pydantic generally cannot evaluate it. Use the
   `type` statement (Python 3.12 and later) or `TypeAliasType` for the older versions.

## Verification
- A subclass instance was serialised through the declared field and the output compared with the
  expectation.
- Wrong-typed input (`"1"` for an integer, a tuple for a list) was sent where strict behaviour was intended
  and was rejected.
- The core package has no import of the model library, or the exception is named.
