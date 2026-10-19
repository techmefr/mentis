---
name: api-change-classification-pitfalls
description: "Use when a change to an API that already has consumers must be classified as breaking or not, before it ships: source, wire and semantic compatibility, new required fields or headers, new client-populated fields keeping their old default behaviour, server-populated fields that must keep being populated, rename as remove plus add, type changes, changed defaults, value formats and string lengths, serialising a default, enum values in requests against responses, pagination and performance changes."
---

# api-change-classification-pitfalls

Not a step of the pipeline: a craft block for the question "is this change breaking?", asked of a diff against a
contract that consumers already use. The three parts share one premise: **breaking is decided by what an
existing consumer experiences, not by what the schema diff looks like**, so the pitfalls are changes that pass
a schema comparison and still break someone, and sources that disagree on where the line is. The shape of
extension, renaming and deprecation (optional fields, the one-version rule, announcing deprecation) is in part
3 of `api-design`, and what a contract should expose in part 2 of the same block; this block adds the
classification checklist those parts do not hold.

## When
- A pull request changes a response, a request, a default, an error code or a limit of a shipped API.
- A reviewer must say whether a change needs a new version or a deprecation path.
- Two teams disagree on whether "just a new field" is safe.

## Steps

**Read only the part the task meets.**

| Part | Covers | Read it when | File |
|---|---|---|---|
| 1 | Three kinds of compatibility, adding components, what old clients and old servers must keep getting | a change adds something | [`01-three-kinds-and-additions.md`](./references/01-three-kinds-and-additions.md) |
| 2 | Changing what exists: names, types, formats, lengths, defaults, serialisation, enums, errors, pagination, performance | a change alters something that shipped | [`02-changing-what-exists.md`](./references/02-changing-what-exists.md) |
| 3 | Where the two sources disagree, the stricter reading chosen, what follows a "breaking" verdict | a verdict is contested or must be acted on | [`03-disagreements-and-verdict.md`](./references/03-disagreements-and-verdict.md) |

## Output / checkpoint
A change is classified when each altered element is listed with the kind of compatibility it touches (source,
wire, semantic), the verdict (breaking, additive, or breaking by the stricter reading with the reason), and, for
a breaking verdict, the path chosen (a new element beside the old one, a new version, or a deprecation). Read
the list once looking for an element judged only by its type. Nothing here was run against a real API or a
diff tool: the check is a read of the text. No pipeline checkpoint.

## Guardrails
- Never call a change additive because the schema diff only adds; check the old client's behaviour (part 1).
- Never add a required request field or header to an existing operation (part 1).
- Never give a new client-populated field a default that changes the old behaviour (part 1).
- Never treat a rename as cosmetic; it is a removal plus an addition (part 2).
- Never change a default, a value format or whether a defaulted field is serialised within a version (part 2).
- Where the sources disagree, take the stricter reading and say which source it came from (part 3).
- The guidance is indicative, not a complete list; a case not covered is a judgment call to write down, not a
  pass (parts 1, 3).

## Origin
Rewritten from Google's API Improvement Proposals on backwards compatibility and versioning (CC-BY-4.0) and
from the Microsoft Graph REST API guidelines (CC-BY-4.0), read 2026-10-16. Attribution to both is in
[`references/origin.md`](./references/origin.md). 🟡: never run by us on a real API; open points are there too.
