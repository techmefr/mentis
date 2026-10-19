# a11y-lint-wiring-pitfalls §2 — Scope and presets

A lint run is quiet for three reasons: the code is fine, the rule cannot see it, or the config never reached the
file. Only the first is good news, and the other two are decided in the configuration.

## 2.1 What static rules cannot see
1. **The JSX plugin evaluates the source, not the page.** Its README says it spots problems in static JSX, so it
   should be combined with an accessibility test on the rendered DOM (it names the axe React package), and
   always with assistive technology. Own guidance: a label built from a runtime value and a component the plugin
   cannot see through are the usual places where static analysis stops.
2. **A green run is a statement about the wired rules, not about the product.** Own guidance: record in the pull
   request which rules ran, on which files, and what the rendered-DOM and manual checks found, so that
   `accessibility` §2.12 (a tool covers a fraction of what matters) stays visible.

## 2.2 Flat config scope
1. **The shareable flat configs do not scope themselves.** The JSX plugin's `flatConfigs.recommended` and
   `flatConfigs.strict` do not set `files` or `languageOptions.globals`; the README's example adds a `files`
   pattern for the JavaScript, JSX and TypeScript extensions and spreads the browser and service worker globals
   from the `globals` package. Own guidance: a config that omits them either lints no file or lints the wrong
   ones, and either way the run is quiet for a reason that has nothing to do with the code.
2. **Spread the preset's own language options, then add yours.** The README's example keeps the preset's
   `languageOptions` and extends its `globals`. Own guidance: write the same shape rather than replacing the
   object. The example is for the JSX plugin at 6.10.2 (version-bound); the Vue plugin's own README gives no
   configuration and points to a website that was not read.
3. **The legacy format and the flat format name presets differently.** The README gives `plugin:jsx-a11y/recommended`
   and `plugin:jsx-a11y/strict` for the legacy file and `flatConfigs.recommended` and `flatConfigs.strict` for the
   flat file; use the one your ESLint setup reads.

## 2.3 What the presets leave off
1. **A preset does not enable every rule of the plugin.** The README rule table marks which configurations
   enable or disable each rule. In it, `control-has-associated-label` is disabled in both presets,
   `anchor-ambiguous-text` is disabled in `recommended`, `label-has-for` is deprecated and disabled, and
   `no-aria-hidden-on-focusable`, `prefer-tag-over-role` and `lang` carry no preset mark at all.
2. **Read the table once and decide rule by rule.** Own guidance: for each rule marked as disabled or unmarked,
   write in the config either "on, because" or "off, because", so that a quiet rule is a decision and not an
   accident of the preset. `no-aria-hidden-on-focusable` is the case to look at first, since the rule it names
   is already a rule of this repository (`accessibility` §2.7).
3. **Five rules carry options inside `recommended`.** The README lists option objects for
   `no-interactive-element-to-noninteractive-role`, `no-noninteractive-element-interactions`,
   `no-noninteractive-element-to-interactive-role`, `no-noninteractive-tabindex` and
   `no-static-element-interactions`. Own guidance: read them before overriding any of the five, since the effect of
   a partial override on the rest of the options was not checked here.
