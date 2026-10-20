---
name: settings-and-preferences-page-pitfalls
description: "Use when a settings or preferences page is designed, written or reviewed in a business application, whatever the framework: autosave against explicit save, defaults and where they live, per-user against per-workspace or per-organisation scope and precedence, reset to default, dangerous settings with confirmation and audit, settings search and structure, plus states, accessibility, performance and the tests that catch them."
---

# settings-and-preferences-page-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for the page every application grows and nobody designs. The premise: **a
setting is a stored decision with a scope, a default and an owner, and every defect hides one of those three**: a
toggle that looks saved and is not, a personal choice that silently overrides an organisation rule, a "reset" that
wipes more than it says, a dangerous switch one click from the safe one. Long forms in general (validation timing,
drafts, dirty state, two editors) are in `long-and-multistep-form-pitfalls`; list-style screens follow
`data-table-ui-pitfalls`; field-level access is in `field-and-row-permission-ui-api-pitfalls`; admin surfaces and
dangerous-action patterns are in `admin-back-office-pitfalls`; flags as a product mechanism are in
`feature-flag-lifecycle`; widget accessibility in general is in `accessibility`.

## When
- A settings, profile, preferences or workspace-administration page is built or changed.
- A user reports "I changed it and it came back", "my setting is ignored", "I cannot find the option", "reset deleted my other choices".
- A new setting, a new scope (per team, per device) or a default change is introduced.

## Steps

**Read the section the task meets.** Each ends with checks.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Save model, defaults, scope and precedence, reset, dangerous settings, versioning of the schema | the storage, the save behaviour or the meaning of a setting is written | [`01-save-scope-defaults.md`](./references/01-save-scope-defaults.md) |
| 2 | Structure and search, states, accessibility, performance, tests, framework pointers | the page, its navigation or its tests are written | [`02-structure-states-tests.md`](./references/02-structure-states-tests.md) |

## Output / checkpoint
A change is done when: each setting has one declared scope, default and owner in a registry; the save model is the
same across the page and the user is told what is saved; the effective value and its source can be shown; reset says
what it resets; dangerous settings are gated server-side and audited; and the tests in §2.6 exist. No checkpoint is
written: a craft block, 🟡, nothing here was run in an application.

## Guardrails
- Declare scope, default and owner for each setting in one registry (§1.3). Never scatter defaults across the interface, the API and the database.
- Pick one save model per page and show its state (§1.1). Never mix silent autosave and a Save button on the same screen.
- Resolve the effective value server-side with a fixed precedence and say where it came from (§1.4). Never let a client merge layers on its own.
- Make reset explicit about its target and reversible where possible (§1.5). Never reset the whole page behind a button named for one section.
- Gate dangerous settings server-side, with confirmation and an audit entry (§1.6). Never rely on the toggle being hidden.
- Facts about a library are for the date stamped in `references/origin.md`; re-read before relying.

## Origin
Own craft knowledge; no permissive source on settings pages was read. Details in
[`references/origin.md`](./references/origin.md).
