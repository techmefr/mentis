# flutter-conventions §9 — Text, motion, monitoring

> Section 9 of `skills/flutter-conventions`. Read it when user-visible text, an animation, crash reporting. The other sections and the guardrails stay in `SKILL.md`.

1. No user-facing string hardcoded in a widget: text, dates, numbers and currency go through the
   localisation layer with typed keys. Currency and date formats are locale rules, not string formatting.
2. Implicit animations by default; an explicit animation controller only where the motion genuinely needs
   driving — and it's disposed (§1.2).
3. Crash and error reporting initialised once at startup, with the environment and release stamped, sampling
   configured deliberately, and payloads scrubbed of personal data before they leave the device.
4. Prefer hand-written code over code generation where the project has taken that position, and don't
   introduce a generation step (and its generated files, its build config, its watch mode) for one model.
