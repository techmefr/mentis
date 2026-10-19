# helm-chart-pitfalls §2 — Values

`values.yaml` is the interface of the chart. Its shape decides whether a template can read a value safely,
whether the value keeps its type, and whether a user can override it from the command line.

## 2.1 Names, and keys with dashes
1. **Start a value name with a lowercase letter and separate words in camelCase** (`chicken`,
   `chickenNoodleSoup`). An initial capital may collide with Helm's built-ins, which all start with an
   uppercase letter (`.Release.Name`, `.Capabilities.KubeVersion`); do not use hyphens in a name (§2.1 point 2 says why).
2. **A dashed key cannot be read with dot notation**, because the template parser reads `-` as subtraction.
   Prefer camelCase in your own charts. When you must read a dashed key, for example a dependency chart named
   `gitlab-runner`, use the `index` function:

```yaml
checkInterval: {{ index .Values "gitlab-runner" "checkInterval" }}
```

## 2.2 Flat or nested
1. **Favour flat values over nested ones in most cases**: `serverName` and `serverPort` rather than
   `server.name` and `server.port` (Helm's values page). It is simpler for the template author and for the
   user.
2. **A nested value must be checked at every level.** Reading `.Values.server.name` safely needs a check that
   `server` exists first; each extra level adds another check, and a flat key needs none.
3. **Nesting is acceptable when many values are related and at least one of them is non-optional**, because
   readability then wins over the extra checks.

## 2.3 Make types clear
1. **YAML coercion is not intuitive.** `foo: false` is not `foo: "false"`, and a large integer such as
   `12345678` is converted to scientific notation in some cases.
2. **Be explicit about strings and implicit about everything else: quote all strings.**
3. **Store large integers as strings** and convert them in the template with `int` (`{{ int $value }}`)
   when the number is needed.
4. **Do not rely on an explicit YAML type tag.** `foo: !!string 1234` is respected in most cases, but the
   parser consumes the tag, so the type information is lost after one parse.

## 2.4 Layout for `--set`
There are three sources of values: the chart's `values.yaml`, a file passed with `-f` to install or upgrade,
and `--set` or `--set-string`. `--set` is the least expressive, so the page's first rule is to make a value
easy to override from `--set`.
1. **Structure repeated entries as maps, not lists.** With a list of servers, `--set servers[0].port=80`
   addresses a position, which is harder to work out and breaks when the order changes. With a map keyed by
   name, `--set servers.foo.port=80` says what it means:

```yaml
servers:
  foo:
    port: 80
  bar:
    port: 81
```

2. **The page notes that the list form could not be set from `--set` at all before Helm 2.5**, and that the
   positional form works from Helm 2.5. That is version history; the order-dependence is the reason that
   still applies.

## 2.5 Document each value
1. **Every property in `values.yaml` is documented**, and the comment starts with the property name followed
   by at least one sentence (`serverHost is the host name for the webserver`). Starting with the name makes
   the documentation greppable and lets documentation tools match a comment to its parameter (the values
   page).

## 2.6 Verify
Override one value of each kind with `--set` (a string, a number, a boolean, an entry of a map) and render
with `helm template`: the output must show the value with the intended type.
