---
name: laravel-filament
description: "Use when writing, reviewing or upgrading Filament code (panels, resources, forms and schemas, tables, actions, relation managers, widgets) in a Laravel app: find the installed major first, apply the version-independent rules, and verify every signature against that version's documentation instead of writing it from memory."
---

# laravel-filament

Step 6 of the pipeline (`WORKFLOW.md`). Filament's API changes between majors, so the same snippet is right
on one and wrong on the next. The discipline of this block is the order: **version first, then rules, then a
signature read from that version's documentation**. It deliberately carries no per-version syntax: that
would be a copy of documentation that goes stale with the next release.

**Special status.** New block, 🟡, "base to confront with the first real change": written from Filament's own
documentation, never run on real work in house. Version
facts below carry a read date; re-read before relying on one (`skills/source-freshness`).

## When
A file under a Filament panel's resources, pages, widgets or relation managers; a question about a Filament
component; an upgrade of the package.

## Steps
1. **Detect the installed major before writing anything.** Read the resolved version (`composer show
   filament/filament`, or the application's `about` output, or the lock file), the constraint only tells the
   intended range. If Filament is absent, ask which major is wanted. If the version cannot be determined, ask:
   never guess.
2. **Read the matching documentation for that major** (`filamentphp.com/docs/<major>.x`) before using a
   namespace, a class or a method signature. Verified here: a path valid on one major can 404 on another.
   State the detected version at the top of the answer, and label code with it.
3. **Know where the real break is.** As of the 2026-10-02 reading, the documentation presents v5 as the v4
   line moved to Livewire 4: requirements PHP 8.2+, Laravel 11.28+, Livewire 4.0+, Tailwind CSS 4.0+, upgraded
   by the vendor's upgrade package and a version-named script, followed by a manual review of what it
   changed. Third-party plugins may lag a major and are removed from the constraint until they catch up. The
   operator runs the upgrade commands themselves (`CONVENTIONS.md`: a block installs nothing).
4. **Authorisation is a policy, not a hidden button.** Filament observes the model's registered policy:
   `viewAny` governs the resource's visibility in navigation, `create`, `view`, `update` and `delete` the
   matching operations, and bulk actions use the `*Any` variants (`deleteAny`, `forceDeleteAny`,
   `restoreAny`) unless per-record authorisation is switched on. Write the policy for every resource and
   test the denied paths (`skills/laravel-permissions-not-roles`: check permissions, not role names).
5. **The base query is the one place to shape reads.** Every query of a resource starts from its Eloquent
   query method: put tenant or visibility constraints and eager loading there, and prefer counts over loading
   a collection for a badge (`skills/laravel-no-queries-in-loops`). Removing a global scope there is a
   decision to be named in review, never a convenience.
6. **Editing is bounded by the form, but exposure is not.** Per the documentation only attributes with a form
   field are editable, so mass assignment is not the main risk here. Model attributes are exposed to the
   browser's component state unless hidden: add secrets and binary or geometry columns to `$hidden`
   (a binary column is reported to break serialisation and the page load: to confirm in the installed version).
7. **Server-side validation lives in the schema.** Field rules are real validation; nothing from client state
   is trusted.
8. **Keep a resource declarative.** It reads as configuration. Logic goes to the model, an action class or a
   service (`skills/laravel-no-fat-models`, `skills/laravel-conventions` §1). Prefer a relation manager to a
   hand-built nested form for one-to-many and many-to-many editing.
9. **Test panels as Livewire components.** Pages, relation managers and widgets are tested through Livewire's
   test helpers (the documentation shows Pest with its Livewire plugin and says to swap in `Livewire::test()`
   for PHPUnit); resources and schema components are non-Livewire classes tested by calling their methods.
   Authorisation and authentication in tests are not covered by that page: write them explicitly.
10. **Match the ecosystem versions.** Each major pins Laravel, Livewire, Tailwind and PHP ranges; a mismatch on the Livewire or
    Tailwind major is the first thing to check when a panel does not render.

## Output / checkpoint
The answer or diff names the detected major, every Filament signature in it was read from that major's
documentation, and each resource has a policy with a denied-path test. Checked at `gate` (7) and `review` (8).

## Guardrails
No comments in the code produced. Never copy a snippet from another major, a blog or a model's memory without
the check in step 2. An upgrade is run in a branch with the vendor's automated script first and the manual list
second, never by hand-editing a hundred files.

## Origin
Version-detection discipline and the stable principles rewritten from the `laravel-filament` skill of
`majdghithan/agent-skills` (MIT, cloned 2026-10-02). Its per-version syntax references are left out on
purpose. Facts re-read from Filament's own documentation on 2026-10-02: the v5 upgrade page (requirements,
upgrade package and script, plugin caveat), the resources overview (policy methods, bulk `*Any` checks, base
query, `$hidden`, the statement on mass assignment) and the testing page (Livewire helpers, Pest or PHPUnit).
That reading contradicts the public skill on one point: it advises guarding mass assignment; the
documentation says form-bound editing is not a mass-assignment problem and warns about exposure instead, so
step 6 follows the documentation. Mechanisms only, rewritten in our words. Reasoning of ours, not a documentation statement: steps 5 (naming a removed global scope in review), 7, 8 and 10; step 6 binary-column remark is unconfirmed.
