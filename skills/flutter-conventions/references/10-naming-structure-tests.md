# flutter-conventions §10 — Naming, structure, tests

> Section 10 of `skills/flutter-conventions`. Read it when a file is placed or named, or tests are written. The other sections and the guardrails stay in `SKILL.md`.

1. House casing per artefact kind (files, folders, classes, widgets, state holders, states, events, entities,
   gateways, use cases, data sources, variables, constants, enums, tests), applied without exception.
2. Separate **technical/shared** layers from **functional/business** ones, one folder per feature, and no
   technical layer importing a functional one.
3. **Widget tests** for a component's behaviour: pump it, locate by key or type rather than by rendered text
   where the text is translated, drive the interaction, then assert. Match the pump to what you're testing —
   pump once for static rendering; pump again after an interaction for a state change; advance time explicitly
   for animations and async updates; and scroll an off-screen item into view before expecting to find it,
   because a lazy list hasn't built it yet.
4. **Integration tests** for the journeys that must not break, run on a real device or emulator.
5. A test that awaits a frame settles deliberately: an unconditional settle on a screen with a repeating
   animation never returns.
6. For *what* to test — plan first, exhaustive rather than happy-path, the permission matrix, the coverage
   floor — see `skills/tdd`.
