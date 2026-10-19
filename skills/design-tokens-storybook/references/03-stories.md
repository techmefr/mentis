# design-tokens-storybook §3 — Stories

> Section 3 of `skills/design-tokens-storybook`. Read it when a story is written, the workshop is configured, or a
> component is documented or tested through it. The other sections and the guardrails stay in `SKILL.md`.

1. **A story is a component plus a set of arguments.** The arguments (args) are one serialisable object that
   sets props, slots or styles; they can be defined for a story, for the component's whole file, or globally.
   Define shared arguments at the narrowest level that covers them: when most stories of a file repeat the same
   value, it moves to the file level, and a story spreads another story's arguments instead of copying them.
2. **Args are serialisable, so complex values are mapped.** A node, a function result or an instance cannot go
   through the controls panel or the address bar. Expose a string option and map it to the complex value in
   the argument type definition; the mapping need not be exhaustive, an unmapped value passes through.
3. **One story per state a reader or a test needs to see,** named for the state, not for the implementation.
   A component with many variants can show them in one grid story for the reader and still test each alone: the
   single-variant stories drop the sidebar and documentation tags (so they only run as tests) and the grid
   story drops the test tag (so it is only read).
4. **Hierarchy is the title, or the folder.** The sidebar tree comes from each file's title with slashes for
   grouping, or from the file's location when the title is left implicit. Pick one rule project-wide. A
   component with a single story whose name equals the component name is hoisted into the parent in the
   sidebar, so name it deliberately.
5. **Tags decide where a story appears and what runs on it.** Built-in: shown in the sidebar, included in the
   machine-readable manifests, included in test runs; `autodocs` (not applied by default) generates the
   component's documentation page when at least one story carries it. Remove a built-in tag with a leading
   exclamation mark. Use custom tags for status (experimental, deprecated) or ownership, and define them in the
   workshop configuration when they need a default sidebar filter. A documentation-only story is `autodocs`
   kept and the sidebar tag removed.
6. **Drive behaviour in a play function, with the queries a user would use.** It runs after render, receives a
   canvas scoped to the story, and uses the same role- and label-based queries as a component test (see
   `skills/frontend-testing`). Query outside the canvas only for content rendered outside the story root, such
   as a dialog in a portal. Compose a long flow from smaller stories' play functions.
7. **Themes are applied by a decorator, driven by a toolbar global, not by a story argument.** A theme is a
   global setting the reader switches, not a property of the component. The themes addon ships three decorators:
   one for a provider component, one that sets a class on a parent element and one that sets a data attribute.
   Use the one that matches how the application selects its theme, import the same global stylesheet the
   application imports, and use the same attribute name as the token build's theme selector (§2.8) so the
   story shows exactly what ships. The page describing the addon in the docs is marked draft: confirm the
   decorator names against the addon's own README before relying on them.
8. **Check every story for accessibility, and decide the severity once.** The accessibility addon runs an
   automated rule engine on the rendered story and groups results as violations, passes and items to confirm
   by hand. It defaults to the WCAG 2.0 and 2.1 level A and AA rules plus best-practice rules, with the region
   rule off because a component is not a page; widen it to a later WCAG version or to AAA through the run-only
   option. Automated checks catch only a part of all issues (the docs cite up to 57 percent): a clean panel is
   not a conformance claim, and keyboard and screen-reader behaviour still need `skills/accessibility`.
9. **The test parameter has three levels with a meaning each.** Off: not run. Todo: run, and violations show as a
   warning in the workshop only, with no output in CI. Error: run, and a violation fails the test locally and in
   CI. Set the project default to error, and mark a known problem as todo with the reason in the pull request, so
   the todo is a debt a reviewer can count. Off is for a story that demonstrates an anti-pattern on purpose.
   Excluding an element from the check is done through the context option and is the narrowest suppression.
10. **Run the stories as tests in CI.** The test addon runs stories through the project's test runner, which
    needs a Vite-based framework; a Webpack project migrates first. Add a script that runs the runner restricted
    to the workshop project, and run it in a container image whose browser version matches the one the runner
    pins. Interaction results and accessibility results come from the same run.
11. **Visual regression is a separate, hosted service in the official docs** (a cloud snapshot service from the
    maintainers). It is optional and other snapshot tools were not read. Do not describe a story as
    visually tested without naming the baseline it is compared with.
12. **Configuration files are modules.** The workshop's main configuration must be valid ESM from the tenth major,
    local addons are referenced by a resolved path and relative imports in plain JavaScript configuration carry
    their extension; the major requires a recent Node (20.19 or 22.12 and later) and a TypeScript module
    resolution that understands package export conditions (`bundler`, `node16`, `nodenext`).
