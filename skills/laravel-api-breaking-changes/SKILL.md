---
name: laravel-api-breaking-changes
description: "Use when removing a field, renaming one, or narrowing a type on an HTTP API: it's breaking even when every in-repo caller is updated — go through the additive-then-remove path, never one commit."
---

# laravel-api-breaking-changes

Narrow trigger extracted from `skills/laravel-conventions` §6.14, so a change to an API Resource or
response shape routes here directly instead of only through the whole Laravel block.

## When
Removing a field from an API Resource, renaming one, or narrowing its type (making it non-nullable,
changing its shape) on an endpoint that isn't brand new.

## Steps
1. **An HTTP API has consumers you do not deploy.** Removing a field, renaming one, or narrowing a
   type is breaking even when every in-repo caller is updated.
2. **This goes through the additive-then-remove path**, not one commit that changes the shape
   directly — add the new field, let both exist for a deprecation window, remove the old one only
   after that window closes.
3. `skills/deprecation-migration` owns the mechanics of that path (Expand/Contract, the announcement,
   the removal date).
4. **What counts as breaking, from public API guidance (AIP-180):** removing a field; renaming one (it is a
   removal plus an addition, so the old name has to stay); changing a field's type, even to a wire-compatible
   one; making accepted input stricter, or changing the format or construction of an existing value; changing a
   documented default; stopping to populate a field the server used to populate; adding a required field to an
   existing request. Adding an optional field that defaults to the old behaviour is the compatible move, and
   an enum that responses can return should be documented as extensible before a value is added.
5. **Announce on the wire as well as in prose.** Two standard response headers exist: `Deprecation` (RFC 9745
   section 2.1, a date that may be past or future; it changes nothing about how the resource behaves) and `Sunset`
   (RFC 8594 section 3, when the resource is expected to stop answering; it must not be earlier than the deprecation
   date, RFC 9745 section 4). Both are hints: clients may not read them, and a consumer must not assume behaviour is
   unchanged once the deprecation date has passed (RFC 9745 section 7).

## Output / checkpoint
Any breaking field change on a shipped API endpoint lands as an addition first (new field alongside
the old), never as a single commit that removes or narrows the old field outright.

## Guardrails
- "Every in-repo caller is updated" is not the bar — an external consumer you don't control or can't
  see is exactly who this rule protects.
- This is the contract question; `skills/laravel-conventions` §10 holds the separate layer question of
  where the endpoint's logic itself lives.

## Origin
Extracted from `skills/laravel-conventions` §6.14 (2026-09-09). Checked on 2026-10-20 against Google's API
Improvement Proposal 180, "Backwards compatibility" (sections Adding components, Removing or renaming
components, Changing the type of fields, Semantic changes; read for facts, our words; its licence file could not
be fetched, so it is credited as an official public guide, not copied), RFC 9745 (Deprecation header, section 2.1, section 4,
section 7) and RFC 8594 (Sunset header, section 3), IETF texts used for facts only, and Stripe's API versioning page (monthly
releases without breaking changes, majors twice a year; vendor documentation, facts only). Neither AIP-180 nor
the RFCs speaks of a deprecation window length or of Laravel API Resources: the additive-then-remove path is
the usual practice those sources support, the window and the "unseen consumers" argument are our own
reasoning. Mechanisms only, rewritten in our words.
