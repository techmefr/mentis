# webperf-measurement-and-budget-pitfalls §3 — Budgets in CI

A budget that fails at random is turned off within a month. The settings below are about making a check fail
for the right reason: a real change in a fact, on hardware that does not add noise of its own.

## 3.1 Runs and noise (Lighthouse CI)
1. **One run is noise.** Lighthouse CI collects three runs per URL by default; `collect.numberOfRuns` raises
   it. The troubleshooting page lists, as the usual remedies for run-to-run variance: more runs, dedicated hardware,
   removing non-determinism, and avoiding external dependencies.
2. **Use dedicated hardware.** The page recommends dedicated machines with at least two cores and 4 GB of
   memory, and names underpowered and burstable CI instances as the thing to avoid.
3. **Remove what varies on its own**: random timers, A/B tests, and variable third-party content such as ads,
   embedded video and analytics.
4. **Before comparing two environments, compare their settings.** The page lists the usual differences: device
   form factor, throttling (its note: the desktop mode in DevTools and PageSpeed Insights changes throttling as
   well as form factor), storage clearing, authentication state, headless versus headful Chrome, hardware,
   and geographic location.

## 3.2 Assertions and presets
1. **Assert facts before conclusions.** The troubleshooting page's advice is to start with assertions on the
   number and size of JavaScript requests rather than on the value of Time to Interactive. Resource budgets use
   the form `resource-summary:<type>:size` or `:count`, with third-party counts available.
2. **Know what the aggregation does.** Assertions default to `{"aggregationMethod": "optimistic", "minScore": 1}`.
   The four methods are `median`, `optimistic` (the run most likely to pass), `pessimistic` (the run least
   likely to pass) and `median-run` (the run found most representative on key metrics, which may not be the run
   where your audit is best). The median is a common assumption, but the default
   is optimistic, and the page's own "complete" example sets it explicitly. Own reasoning: optimistic means one
   good run in a set passes the check, so a regression that only appears in some runs can be hidden; choose the
   method on purpose and write it in the configuration.
3. **Three levels: `off`, `warn`, `error`.** An audit not listed is off. `warn` prints the result but does not
   change the exit code; only `error` fails the build.
4. **The recommended preset is deliberately soft on performance.** `lighthouse:recommended` asserts a perfect
   score on every non-performance audit, that no resource was flagged as a performance opportunity, and only
   warns when a metric score falls below 90, which the page says avoids hard failures for flaky audits.
   `lighthouse:all` asserts every audit perfect and the page calls that extremely difficult; use it only on very
   high-quality greenfield projects.
5. **Start with the audits you pass and switch off the ones you fail.** The "next level" setup in the page
   asserts the recommended preset and turns off the failing audits one by one, rather than failing on day one.
6. **Different URLs, different assertions.** `assertMatrix` pairs a URL pattern with its own assertions, for
   instance a first-paint limit on every page and a stricter one under a path.
7. **Mind the units.** In Lighthouse CI assertions a size limit is in bytes; in a `budget.json` file it is in
   kilobytes, and a `budgetsFile` cannot be combined with other assert options.

## 3.3 Collecting and running in CI
1. **`staticDistDir` is for a static site served from localhost.** The page says not to use it when the URL
   points to another origin or when a separate server is started; with it, URLs are rewritten to the local
   server's port, and without it they are used as given. When it is not set, `autorun` looks for built HTML in
   `dist`, then `build`, then `out`, then `public`.
2. **Child options of `autorun` need the `=` form** (`--collect.numberOfRuns=5`, not with a space).
3. **An upload failure under `autorun` is only a warning by default**, so a pipeline can look green with nothing
   stored; `failOnUploadFailure` makes it fatal.
4. **A shallow clone breaks the ancestor lookup.** When the Lighthouse CI server cannot find the base ancestor,
   the cause given is a shallow checkout. The page's example for GitHub Actions sets `fetch-depth: 20` and
   fetches the base branch head; it calls 20 a good default that might not suit every repository. The page's
   example uses `actions/checkout@v3`; check the options of the version you use.
5. **A rerun of the same build is refused by the server.** The documented workaround is an empty commit.
6. **URLs that change between builds need replacement patterns.** `urlReplacementPatterns` masks random parts
   such as ports and UUIDs; setting your own removes the default two, so copy them over.
7. **Flag names are version-bound.** The repository's last commit read here is dated June 2025; check a flag
   against the installed version.

## 3.4 Where reports go
1. **`temporary-public-storage` publishes the report.** The configuration page's list: anyone with the link can
   read it, it is deleted after a few days, it is stored on a cloud storage service, and you should have read
   the terms and privacy policy first. The `lhci` target with your own server keeps reports longer and controls
   access; `filesystem` keeps the raw files for your own processing.

## 3.5 A JavaScript size budget (size-limit)
1. **It measures cost with dependencies.** size-limit's README says it calculates the real cost of the JavaScript
   for end users, including all dependencies and polyfills, as minified and Brotli-compressed size by default
   (Gzip or none are options), and fails when it exceeds a limit.
2. **Set the first limit from the current size.** For an application, add 25 percent to the measured size, or to
   the measured time, and use that; for a small library, add a little, such as a kilobyte. Own guidance: a limit
   that sits right on the current size fails on the first harmless change and gets raised without thought.
3. **A time limit is less stable than a size limit.** The `time` plugin compares the machine to a low-priced
   Android device to compute a CPU throttling rate, then runs headless Chrome to measure compile and run time;
   the README warns that these measurements depend on available resources and may be unstable. It also
   says time is a more understandable metric than bytes. Own guidance: gate on size on a shared CI runner and
   report time next to it.
4. **Test the size after tree-shaking with the `import` option**, for example one named export (the
   README's option for ES modules). Own reasoning: without it the measured entry includes exports you never import.
5. **For a CSS file, turn the bundler off.** With webpack the `style-loader` runtime of about 2 kB is added
   to the number; set `webpack: false` (or `rolldown: false` for the rolldown plugin).
6. **Wire the check into the test script and CI**, as the README does, so a pull request that adds a large
   dependency fails. `--why` explains where the size comes from; `--ignore-missing` skips configured paths
   that a changed-only workspace build did not produce.
