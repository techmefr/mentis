---
name: design-tokens-storybook
description: "Use when writing or reviewing a design-token source and its build (token file shape, types, aliases, themes, generated output) or the component stories that document and test the result: how a token is declared, resolved and shipped, and how a story is written, themed, checked for accessibility and run in CI."
---

# design-tokens-storybook

Step 6 of the pipeline (`WORKFLOW.md`), next to `skills/tailwind-conventions` (the utility framework that consumes
tokens as theme variables), `skills/accessibility` (contrast, focus, motion) and `skills/frontend-testing` (what a
component test proves). This block owns two things those do not: the **source of truth for design values** (a
platform-neutral token file and the build that turns it into stylesheets and constants) and the **component workshop**
(stories as living documentation and as tests). **Status: a base to confront with real work**, no in-house project
behind it yet (same status as `go-conventions`). Pinned to **Style Dictionary 5.5** reading the **Design Tokens
Format Module 2025.10** (a community-group draft, not a W3C standard) and **Storybook 10.6**, read 2026-10-02
(`references/origin.md`).

## When
As soon as a token file, a token build configuration, a generated token stylesheet, a story file or the workshop's
configuration is written or modified, during `code` (6).

## Steps

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | The token file: shape, names, types, aliases, deprecation | a token or group is added, renamed, retyped or removed, or an alias is written | [`01-token-file.md`](./references/01-token-file.md) |
| 2 | The build: pipeline, transforms, references in output, themes | the token build is configured, a platform output is added, or a theme or brand is introduced | [`02-token-build.md`](./references/02-token-build.md) |
| 3 | Stories: shape, args, tags, themes, accessibility, CI | a story is written, the workshop is configured, or a component is documented or tested through it | [`03-stories.md`](./references/03-stories.md) |

## Output / checkpoint
A token source that parses, resolves every alias and builds without a warning, and stories that render in every
theme and pass the accessibility checks at the severity the project set. No dedicated checkpoint: `gate` (7) and
`review` (8).

## Guardrails
No comments in the code produced. Never an install: name the package, the person runs the install command
(`CONVENTIONS.md`). Never edit a generated token file: change the source and rebuild. Never put a raw colour,
size or font in a component when a token expresses it. Never silence an accessibility rule on a story to make a
check pass without saying which rule and why. Do not adopt the draft token format's newest features before the
build tool in use reads them: check the tool, not the specification.

## Origin
Rewritten from the Style Dictionary and Storybook documentation and the Design Tokens Community Group format
report, read 2026-10-02; see [`references/origin.md`](./references/origin.md). Read it when checking freshness,
not when applying a rule.
