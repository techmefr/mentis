# § 2 — Hyrum's law: whatever is observable will be depended on

> Section 2 of `skills/api-design`. Read it when deciding what an interface exposes, and before
> changing anything a consumer can observe.

1. Every observable behaviour (field order, default value, error format) will sooner or later be
   depended on by a consumer, even an undocumented one: handle that risk at design time, don't
   discover it by breaking a consumer later. The mechanism is that consumers write code against what
   they *observe*, not against what we documented, and they have no way to tell the two apart — so
   every accident of the implementation is a de facto part of the contract from the first integration.
2. Internal/technical fields never exposed "because it's handy": only what is a genuine public
   contract is. Handy costs nothing today and is permanent tomorrow: the field cannot be removed
   without breaking somebody, and it now constrains the internals it was a window onto.
3. **The surface is everything a consumer can see, not the fields.** Response times, ordering, the
   number of results returned by default, whether an operation is synchronous, the status code chosen
   for a case, the exact wording of an error, whether two requests can be issued in parallel: each has
   been depended on somewhere, and none of them is in the schema.
4. **An unspecified detail is not a free choice, it is a choice you will make once by accident.**
   Ordering is the clearest case: a list with no stated order comes back in whatever order the query
   produced, a consumer paginates or displays it as if the order were stable, and the day an index
   changes their output changes with no error anywhere. Specify it or randomise it, but do not leave it
   to the database.
5. **The narrower the surface, the cheaper the interface is to keep.** Every field, parameter and
   behaviour not exposed is one nobody can depend on, which is the only real freedom to change we get.
   That is why this section is a design rule and not a warning: it is decided when the contract is
   written, and it cannot be recovered afterwards.
6. **A field nobody uses still cannot be removed without knowing.** "Nobody uses it" is a claim about
   consumers we can see, and an API with any external consumer has consumers we cannot — which is what
   makes usage data, not reasoning, the input to that decision (`skills/observability-instrumentation`
   §1).
7. **Anything undocumented but reachable is reachable.** An endpoint left in place after its feature
   was cut, a parameter that still works, a debug field behind no flag: each is a live part of the
   surface, and its authorisation, its cost and its compatibility are all real (`security-hardening`
   §3.1).
8. **Loosening is compatible, tightening is not.** Accepting a value you previously rejected breaks
   nobody; rejecting one you previously accepted breaks whoever was sending it, including the consumer
   whose payload was always technically invalid. So a validation rule added later is a breaking change
   even though it makes the contract stricter and more correct.
9. **A default value is part of the contract.** Changing it changes behaviour for every consumer who
   never sent the parameter, which is most of them, and the change is invisible in their code — so it
   is indistinguishable from a bug on their side. A default is chosen once, and changed through the
   same path as removing a field (§3.2).
10. **Consumers depend on failures too.** A retry loop keyed on a status code, a client treating one
    error as permanent and another as transient, a caller relying on an operation being idempotent
    after a timeout: each is a dependency on our failure behaviour, and changing which code a case
    returns can turn a client's careful handling into a duplicated write.
11. **Design what you will not promise, and say so.** A field marked as informational, a shape stated
    as unstable, an ordering documented as arbitrary: an explicit non-promise is the only thing that
    makes a later change defensible, and it has to be there from the first release rather than added
    when we want to change the thing.
