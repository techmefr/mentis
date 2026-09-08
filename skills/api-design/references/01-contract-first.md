# § 1 — Contract-first

> Section 1 of `skills/api-design`. Read it before implementing a new endpoint, route or procedure —
> the schema comes before the code, not after it.

1. The typed schema (DTO, tRPC type, OpenAPI/GraphQL schema) is written **before** the
   implementation, not inferred from the code afterwards. Written first, the schema is a design
   decision somebody can disagree with while disagreement is free; generated afterwards, it is a
   description of whatever the implementation happened to do, including the parts nobody chose — a
   nullable field that is nullable because the column is, a shape that mirrors the database, a name
   taken from an internal class.
2. Validation placed **only at the boundaries** (the API entry point): internal code trusts the
   already-validated type, no deep revalidation that duplicates the logic. Duplicated validation is
   worse than absent: the two copies diverge, and the one that matters is whichever runs first, which
   is not the one a reader finds.
3. A single system-wide error format (the same structure for every error returned), never a
   different format per endpoint. A consumer writes error handling once or writes it per endpoint, and
   the second version is the one that silently misses the case nobody tested — so the cost of the
   inconsistency is paid on the client's failure path, where it is least visible to us.
4. **The contract is written for the consumer's question, not for our storage.** A shape that mirrors
   the tables makes every consumer reassemble the answer, and it welds the API to a schema we would
   otherwise be free to change — so a refactor that should be invisible becomes a breaking change
   (§2.1).
5. **Say what is required, what is nullable and what is absent**, and mean three different things by
   them. A field that can be null and a field that may be missing are distinct states for a consumer's
   parser, and a schema that conflates them produces client code that is wrong in exactly one of the
   two cases — usually the rarer one.
6. **Every enumerated value is in the contract, and the contract says what happens when a new one
   appears.** A consumer switching on a closed set breaks the day a value is added, so either the set
   is closed and adding to it is a breaking change, or it is open and consumers are told to tolerate
   the unknown. Silence means the first is assumed and the second is done.
7. **The error format carries a stable, machine-readable code**, not only a message. A consumer
   branching on a human sentence is a consumer broken by a wording change or a translation — which is
   how an interface-text improvement becomes an outage somewhere else (`business/ux-writing` §4).
8. **Validation failures are part of the contract too.** Which field, which rule, and the shape of the
   list when several fail: a consumer building a form against the API has to map them onto its own
   fields, and an error body that names nothing forces the client to re-implement the rules to know
   where to put the message.
9. **Decide the identifier, the units and the time representation once, in the contract.** An id typed
   as a number in one place and a string in another, an amount with no currency, a date with no
   timezone: each is a decision the implementation will make by default if the schema does not, and
   each is expensive to change afterwards because it is in every consumer.
10. **A contract has an owner and a place.** Written first and then left in a chat message, it is not a
    contract — the implementation becomes the reference within a week. It lives where a consumer can
    read it without asking us, which is also what makes the checkpoint's compatibility check possible
    at all.
11. **The contract covers the real need, not a generalised one.** An extra field, an extra parameter
    or an extra level of nesting added for a hypothetical consumer is a promise we now have to keep,
    and Hyrum's law (§2) means we will keep it whether we meant to or not
    (`skills/design-patterns` §1).
