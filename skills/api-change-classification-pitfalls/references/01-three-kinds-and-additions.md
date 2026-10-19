# api-change-classification-pitfalls §1 — Three kinds of compatibility and additions

> Part 1 of `skills/api-change-classification-pitfalls`. Read it when a change adds something to a shipped
> contract. Sources: Google AIP-180 and the Microsoft Graph guidelines, both CC-BY-4.0, rewritten in our own
> words; points marked own guidance are ours.

## 1.1 Three kinds of compatibility
1. **Source compatibility**: code written against the previous version still compiles against the new one and
   runs with the new client library.
2. **Wire compatibility**: code written against the previous version still talks to the new server correctly.
   Inputs and outputs match, and so do the serialisation and deserialisation expectations.
3. **Semantic compatibility**: old code keeps receiving what a reasonable developer would expect. The source
   admits this is the hard one and that deciding what users expect can be a judgment call.
4. **A change is classified against all three.** A change can be wire-compatible and still break generated
   code (source) or break expectations while the bytes are valid (semantic).
5. **The scope assumption matters.** AIP-180 assumes many consumers, in several languages, with no control over
   when they update. Where producer and consumer are one team and updates can be forced, the source says to
   consider the compatibility requirements carefully rather than assume the strict rules.
6. **The guidance is indicative.** The source says it is not a complete list of changes and that an expansive
   reading could forbid every change, which is not the intent. A case outside it is written down with the
   reasoning (own guidance on recording it).
7. **The transport assumption**: the specific guidance assumes protocol buffers and JSON; other formats may
   have slightly different rules.

## 1.2 Adding components
1. **New components may be added in the same major version**: interfaces, methods, messages, fields, enums and
   enum values. The condition is that code unaware of them must be treated exactly as before.
2. **A new required field must not be added** to an existing request message or resource. The Graph guidance
   says the same from the other side: adding a non-nullable property to an existing type, a required request
   header, or a parameter not marked optional or nullable to an existing action or function is breaking.
3. **A field the client populates needs a default that reproduces the old behaviour.** The source's example is
   adding pagination after the fact where everything was returned before: if the new page size defaults below
   what used to be returned, an old client wrongly assumes it received everything.
4. **A field the server used to populate must keep being populated**, even if it becomes redundant.
5. **Additive Graph changes**: adding a property that is nullable or has a default value is non-breaking; the
   order of properties may change. Adding a member to an enum is non-breaking only where the enum was declared
   open to additions (see part 2).
6. **A new component closely related to an existing one can collide in generated code**, for example a value
   field next to a field of the same stem. The source asks owners to know the quirks of the tooling their users
   run.
7. **An addition still needs the consumer to tolerate it** (own guidance, echoing the additive-only rule in
   part 3 of `api-design`): classifying a change as additive assumes clients ignore what they do not know; say
   so in the contract.
