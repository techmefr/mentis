# api-change-classification-pitfalls §2 — Changing what exists

> Part 2 of `skills/api-change-classification-pitfalls`. Read it when a change alters something that already
> shipped. Sources: Google AIP-180 and the Microsoft Graph guidelines, both CC-BY-4.0, rewritten in our own
> words; points marked own guidance are ours.

## 2.1 Names, places and types
1. **Removing a component is breaking** within a major version: interfaces, methods, messages, fields, enums
   and enum values alike.
2. **A rename is a removal plus an addition.** The source allows adding the new name but not removing the old
   one. Where both can then be set, the behaviour for conflicting values must be written down.
3. **A type change is breaking even when the wire format is compatible**, because generated code changes in a
   breaking way. The Graph guidance lists removing, renaming or changing an incompatible type of a declared
   property the same way.
4. **Moving a definition between files** is wire-compatible but breaks generated code for languages that import
   by file (the source names C++ and Python). **Moving a field into or out of a oneof** is breaking in the Go
   protobuf stubs. Both points are specific to schema languages with generated code.
5. **A resource keeps its name**, and the source says this holds even across major versions: a resource created
   under one version must be reachable by the same name under the next. The Graph guidance lists changing the
   URL or the fundamental request or response of a resource as breaking.
6. **Removing or renaming an operation or a parameter is breaking** (Graph).

## 2.2 Strings, formats and identifiers
1. **Do not raise the upper bound of a string's size** if it can reach consumers' storage or URLs. The source
   says to treat an expected increase as incompatible, and gives the reason: consumers store such values in
   limited database columns, and strings in URLs often hit client-side limits.
2. **If a fixed size is needed, pad with filler** and document it; the source allows this explicitly.
3. **The set of valid resource names must not change either.** Making the format stricter makes requests that
   used to work fail; making it looser breaks code that stored names or validated them against the
   documentation. The source cites an example of a vendor giving customers long warning before allowing longer
   identifiers.
4. **Do not change the format or construction of an existing field's value**, even if the field is
   output-only, within an API version; that needs a new version. The source's example is a field holding an
   address in the older internet-address format starting to hold the newer one.
5. **Why**: consumers parse, hash and build tables from the format of a value (source's rationale).

## 2.3 Defaults and serialisation
1. **A static default must not change.** The default behaviour of a resource is set by its defaults, and the
   source says this must not move across minor versions. The rule covers fixed defaults, not dynamic ones such
   as an address assigned at creation. Example: a default category switching from one value to another.
2. **Do not change whether a field with a default value is serialised.** If a field is omitted when it equals
   its default, starting to send it, or the reverse, is not backwards compatible within a major version:
   consumers may treat presence or absence as meaningful.
3. **Check both directions of a presence change** (own guidance, read from the rule above): a field that used to
   be present always and is now omitted at its default is the same break, mirrored.

## 2.4 Enums
1. **Values may be added freely to an enum used only in requests.**
2. **Values may be added to an enum used in responses**, but where new values are expected the contract must
   say so, and caution applies, because client code may not handle an unknown value.
3. **Graph is stricter**: adding a member to an enum that was not declared extensible is breaking; adding a
   member after the sentinel of an extensible enum is not. The practical consequence (own guidance): declare a
   response enum open to additions in its first release, because declaring it later is itself a change.

## 2.5 Behaviour and limits
1. **Any visible behaviour or semantics change** is breaking if it is likely to break reasonable consumer code,
   even behaviour that was never documented (AIP). The Graph guidance states that changing semantics is always
   breaking.
2. **Changing top-level error codes is breaking** (Graph).
3. **Introducing server-side pagination to an existing collection is breaking** (Graph); the AIP example in
   part 1 shows the mechanism.
4. **Significant performance changes are breaking** (Graph): increased latency, changed rate limits or changed
   concurrency. "Significant" is not defined; set the threshold before the change, not after the complaint
   (own guidance).
5. **Changing the order of properties is non-breaking** in the Graph guidance; AIP does not discuss it.
