# a11y-lint-wiring-pitfalls §1 — Making wrappers visible

The rules reason about native elements. A project that renders every input through its own component presents
the rules with `<AppInput>` and nothing they know how to judge, so they stay quiet. Every wrapper has to be
declared before the rules can see through it.

## 1.1 JSX plugin settings
1. **Map each wrapper to the element it renders.** The plugin's `components` setting pairs a custom component name
   with a DOM element type so that the component is checked as that element; the README's example maps button
   wrappers to `button` and a city field to `input`. Until a wrapper is in the map, it is not checked as the
   element it renders.
2. **Map the property that stands for a DOM attribute.** The `attributes` setting says which JSX property to read
   for a DOM attribute; the README's example accepts both `htmlFor` and `for` when checking label associations.
3. **Tell the plugin how a polymorphic component chooses its element.** With `polymorphicPropName` set to `as`, an
   element written `<Box as="h3">` is evaluated as an `h3`; without the setting it is evaluated as `Box`. A second
   setting, `polymorphicAllowList`, restricts the polymorphic reading to the named components. The README warns
   that polymorphic components can make code harder to maintain; use the setting with caution.

## 1.2 Label rules
1. **The JSX label rule takes the wrappers by option.** `labelComponents` lists the components that render a
   label, `controlComponents` the ones that render an input (both accept glob patterns), `labelAttributes` the
   attributes on a label component that carry its text, and `depth` how deep inside the label the rule looks for
   text content or a labelled element: the default is 2 and the maximum is 25. Own guidance: raise `depth` when
   the label text sits several wrapper levels down, rather than silencing the rule.
2. **The same rule can ask for nesting, `htmlFor`, both or either.** The `assert` option takes `htmlFor`,
   `nesting`, `both` or `either`. §3.1 is about choosing it.
3. **The Vue label-and-control rule takes the wrappers by option too.** `form-control-has-label` accepts
   `labelComponents` and `controlComponents`; labels and the native `input`, `textarea` and `select` are always
   included, and the page presents the options as the way to cover wrappers that render a label or an input.
4. **The Vue `label-has-for` rule has its own options.** `components` for label wrappers and `controlComponents`
   for control wrappers (by default `input`, `meter`, `progress`, `select` and `textarea`), `required` for which
   checks are active (default: both nesting and id), and `allowChildren`, default `false`, which decides whether a
   label whose only content is a default slot is accepted. A wrapper that passes its slot straight into a label
   is flagged by default; set `allowChildren` to `true` only when the slot content cannot be known to the rule.

## 1.3 Link rules
1. **The anchor rule takes link wrappers by option.** In `anchor-is-valid`, `components` lists the elements to
   check besides `<a>`, and `specialLink` the properties to read as a destination besides `href`; the page's
   example is a `Link` component that only renders an `<a>`. The `aspects` option selects the sub-rules (a missing
   `href`, an invalid `href`, an anchor used as a button), all on by default; the page recommends leaving all on
   except where the rule becomes unusable for a well-founded restriction, and the option must name at least one.
