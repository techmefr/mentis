---
name: a11y-lint-wiring-pitfalls
description: "Use when accessibility lint rules are added to a JSX or Vue project or a lint run is quiet for the wrong reason: wrapper components the rules cannot see until they are declared, polymorphic components, label rules and their component and depth options, flat-config scoping and globals, presets that leave rules off, label association by nesting versus for and id, deterministic ids, anchors that act as buttons, click handlers without key handlers, autofocus, and deprecated rules not to enable."
---

# a11y-lint-wiring-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for the lint half of an accessibility check. `accessibility` §2.12 says that
what a tool can check is a fraction of what matters; this block is about making that fraction real, because a
rule that cannot see a component reports nothing and a green run then proves nothing. The three sections share
one premise: **a lint rule only judges the elements it recognises, so the wiring (which components stand for which
elements, which files, which options) decides what a green run means**. The component-level accessibility rules
themselves are in `accessibility`; this block does not restate them.

## When
- Adding `eslint-plugin-jsx-a11y` or `eslint-plugin-vuejs-accessibility` to a project, or upgrading it.
- A project has its own `Button`, `Input`, `Label` or `Link` components and the a11y rules never fire.
- A rule fires on correct code, or a pattern passes that should not.
- Choosing which rules to turn on, and what to do about rules that conflict between plugins.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Making wrappers visible: component and attribute maps, polymorphic props, label and link options for both plugins | custom components wrap native elements | [`01-wrappers-and-options.md`](./references/01-wrappers-and-options.md) |
| 2 | Scope and presets: static analysis limits, flat config files and globals, what the presets leave off | a config is written or a green run is trusted | [`02-config-scope-and-presets.md`](./references/02-config-scope-and-presets.md) |
| 3 | Rules that encode a decision: label association, ids, anchors, click handlers, autofocus, rules not to enable | a rule fires, or two plugins disagree | [`03-rules-that-decide.md`](./references/03-rules-that-decide.md) |

## Output / checkpoint
Each rule was exercised, not read off the file: a deliberately wrong usage of every wrapper component (an input
without a label, a link without `href`, a click handler on a `div`) was written and the run failed on it, then the
usage was fixed and the run passed (§1, §3); the config was run on a file of each extension in scope, with the
globals the code uses (§2). A rule that was never seen failing is not known to be wired.

## Guardrails
- Never read a green lint run as an accessibility pass; pair static rules with an audit of the rendered DOM and a
  manual check (§2.1).
- Never leave a project component that wraps a label, an input or a link out of the plugin settings (§1.1, §1.3).
- Never generate an id at render time to associate a label (§3.2).
- Never use an anchor without a real destination as a button (§3.3).
- Never enable a rule the plugin itself marks deprecated, and never copy a passing example that hides a focusable
  element from assistive technology (§3, last subsection).
- This block states plugin behaviour as of the repositories read on the date in
  [`references/origin.md`](./references/origin.md), bound to eslint-plugin-jsx-a11y 6.10.2 and
  eslint-plugin-vuejs-accessibility 2.6.2. Nothing was run while writing it.

## Origin
Rewritten from the README and two rule pages of eslint-plugin-jsx-a11y (MIT) and six rule pages of
eslint-plugin-vuejs-accessibility (MIT), read 2026-10-16. 🟡: never run by us; open points are in
[`references/origin.md`](./references/origin.md).
