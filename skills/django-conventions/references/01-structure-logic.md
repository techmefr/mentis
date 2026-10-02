# § 1 — Where behaviour lives

> Section 1 of `skills/django-conventions`. Read it when a model, a view, a form, a serializer, a signal or a
> task is written and the question is "where does this rule go". The ORM and transaction rules are §2, the
> schema ones §3. The structure comes from a style guide that is an opinion, not the framework's own position;
> it is marked where it is a preference. Read 2026-10-02.

1. **Behaviour that writes lives in services, behaviour that reads lives in selectors.** A service is a plain
   function in the app's `services` module that takes keyword-only arguments (unless it needs zero or one),
   is type-annotated, touches the database and the outside world, and holds the rule; a selector is the same
   shape for fetching. The point is that the same behaviour is reachable from a view, a command, a task and a
   test without constructing a request. If the split into two layers does not suit the team, one service layer
   for both is acceptable; two competing places are not.
2. **Name services after the entity and the action** (`user_create`, `course_cancel`) and group them by entity in
   a module. The cost is an odd-looking name; the gain is that everything that can happen to an entity is found
   by one search and sorts together.
3. **Views and API handlers do not hold business logic.** They parse the input, fetch the objects the call
   needs, call one service or selector, and shape the output. Likewise forms, serializers and form tags. One
   handler per operation keeps each of them simple and keeps permissions and documentation per operation.
4. **Models describe the data and little else.** A model carries its fields, constraints, a derived value as a
   property when it is cheap, and a `clean` that validates across the model's own plain fields. Everything that
   spans relations, fetches extra data or is non-trivial moves to a service or a selector; a property that
   walks a relation is an N+1 waiting for a serializer to call it (§2.3).
5. **Do not put business logic in `save()`, in custom managers or querysets, or in signals.** `save` is bypassed
   by the queryset `update` and `delete` and by `bulk_create`, so a rule living there holds only on some paths;
   signals give the look of loose coupling and in practice code that is hard to follow, adjust and debug: call
   the handling code directly instead. Where a signal is genuinely needed (a reusable app reacting to a
   framework event), connect the receiver in the app configuration's `ready()` from a `signals` submodule, take
   `sender` and `**kwargs`, and remember that receivers are held weakly.
6. **Validate in layers, each at what it can see.** Constraints in the database for what must always hold
   (`CheckConstraint`, `UniqueConstraint`, foreign keys): they hold on every write path. `clean` for simple
   rules across the model's own non-relational fields, called through `full_clean()` in the service right
   before `save()`, which also makes the admin run it. Rules that are complex or need other rows live in the
   service. Duplicating a rule at two layers is acceptable; leaving it only at the one that a path can bypass
   is not.
7. **A base model carries the shared columns** (`created_at`, `updated_at`) as an abstract class, so every table
   has them without anyone remembering to add them.
8. **Tasks are another entry point, not another place for logic.** A background task loads what it needs by id,
   calls a service, and handles retry and failure at the task level; it takes ids, not model instances. The
   failure handler calls a service, like any other caller. Split large task modules by domain the way services
   are split (`skills/background-jobs-conventions` for idempotency and delivery guarantees).
9. **Check the version before relying on a feature.** The documentation read for this block is the development
   branch (Django 6.2 alpha at the time), which describes things a supported release does not have yet; a rule
   that depends on a recent feature (a fetch mode for related objects, for instance) carries the version it
   needs, and a project on an LTS reads it as "not yet".
