# go-tooling-testing-security §1 — Tool gate

## 1.1 Formatter
**A stricter formatter than `gofmt` is an option, not a default.** `gofumpt` enforces a stricter format
while staying backward compatible: whatever it accepts `gofmt` accepts, and running `gofmt` afterwards should
change nothing. Its README says it skips `vendor` and `testdata` and does not apply its added rules to
generated files unless they are named explicitly, and that the version read requires Go 1.26 or later. The
choice to adopt it is the team's; the point of the rule is that one formatter decides, in CI, so review
carries no style churn.

## 1.2 `go vet`
1. **Run `go vet ./...` in CI.** The linter set belongs to `go-conventions`; this is the part the toolchain
   ships.
2. **Format strings that are not literals should be constants.** The Uber guide says to declare a
   `Printf`-style format string as a `const` when it is declared outside a string literal, so `go vet` can
   analyse it. Go 1.24's `printf` analyser reports `fmt.Printf(s)` with a non-constant `s` and no other
   arguments, and applies that check only when the module's `go` directive (or a build constraint) is at least
   1.24, so raising the directive can turn on new findings.
3. **New analysers by version:** Go 1.25 added `waitgroup` (a misplaced `sync.WaitGroup.Add`) and
   `hostport` (`Sprintf` used to build a dial address); Go 1.27 runs the `stdversion` check by default under
   `go test`, reporting standard-library symbols too new for the file's Go version, and extends `printf` to
   a `%w` operand whose pointer type's element type implements `error`.

## 1.3 Race detector
1. **Run the tests with `-race` in CI.** The cost the article gives is memory up by 5 to 10 times and
   execution time up by 2 to 20 times for a typical program, which is why it belongs to test and CI jobs and
   is not advised in production.
2. **It only finds races that happen.** The article says it cannot find races in code paths that are not
   executed, so a green run proves only what the tests exercised; `go-conventions` §1.6 notes the same for the
   closed-channel race. Realistic workloads and incomplete coverage both expose more.
3. **Check the platform:** `-race` is supported only on the listed OS and architecture pairs (for example
   linux on amd64 and arm64); a CI image on another pair cannot run it.

## 1.4 Pin tools with the `tool` directive
**From Go 1.24, record a developer tool in `go.mod` with a `tool` directive** instead of a blank import in a
`tools.go` file. `go get -tool <package>` adds the directive and a `require`; `go tool <name>` runs it; the
`tool` pattern covers all of them (`go get tool` upgrades, `go install tool` installs). The tool version then
moves with the module, which is the reason to prefer it.

## 1.5 Vulnerability scanner
1. **Run `govulncheck ./...` as a CI step.** The vulnerability guide says it reports only the vulnerabilities
   whose vulnerable functions your code transitively calls, a low-noise result, and its data comes from the
   Go vulnerability database (curated by the Go security team, OSV format).
2. **Treat a finding as blocking until triaged.** Own guidance: the pages read do not state the exit code, so
   check how the CI step reacts before depending on it. The tool is installed by the user
   (`go install golang.org/x/vuln/cmd/govulncheck@latest` in the guide), or recorded with the `tool` directive described just above.

## 1.6 Modernising
From Go 1.26 `go fix` hosts the "modernizers", which update code to current idioms and library APIs; its old
fixers were removed. Run it as a review aid on a separate commit, not as part of a feature change (own
guidance).
