---
name: go-tooling-testing-security
description: "Use when setting up or reviewing the Go checks that run in CI and in tests: formatter, go vet, race detector, pinned tools via the go.mod tool directive, vulnerability and security scanners; goroutine-leak checks, table tests, testing/synctest for time-dependent code, fuzzing; and the standard-library security pieces (os.Root, crypto/rand, constant-time comparison, html/template)."
---

# go-tooling-testing-security

Steps 5 and 7 of the pipeline (`WORKFLOW.md`), for the Go checks that decide whether a change is allowed to
merge: the tool gate, the test additions that catch what the race detector cannot, and the standard-library
calls that replace hand-written security code. General Go rules are `go-conventions`; the generic test
anti-patterns are `testing-anti-patterns`; security policy is `security-hardening`; the CI workflow itself is
`ci-workflow-hardening`.

## When
- A Go CI job, a Makefile target or a tool list is created or changed.
- A test touches goroutines, timers or a parser, or a table test is written.
- Code reads files by a name that comes from outside, generates a token, compares a secret, or renders HTML.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Tool gate: formatter, vet, race detector, `tool` directive, vulnerability scanner | a CI job, Makefile or tool list is written or reviewed | [`01-tooling-gate.md`](./references/01-tooling-gate.md) |
| 2 | Test extras: leak check, table tests, synctest, fuzzing | a test uses goroutines, time or a parser, or a table test is written | [`02-test-extras.md`](./references/02-test-extras.md) |
| 3 | Security extras: os.Root, crypto/rand, constant-time compare, html/template, scanner | files, tokens, secrets, SQL or HTML are handled | [`03-security-extras.md`](./references/03-security-extras.md) |

## Output / checkpoint
The gate ran and was green on the changed code: format, `go vet ./...`, tests with the race detector, and
the vulnerability scanner (§1); new concurrent or time-dependent code has a test that would fail on a leak or
a race (§2); and a security scanner run shows no new finding for the diff (§3). A gate that was only added to
a config file and never run is not verified.

## Guardrails
- Never let the race detector or a scanner stand in for a test of the behaviour; each only reports what
  executes or matches (§1.3).
- Never use `math/rand`-style randomness for a token or a secret (§3.2).
- This block names tools and the user installs them; it installs nothing (`CONVENTIONS.md`).
- Versions: each rule names its Go version or tool. Nothing was run while writing this block.

## Origin
Rewritten from the Go release notes, command and package documentation, the fuzzing and vulnerability
guides, the race detector article (CC-BY-4.0 text, BSD-3 code), the goleak README (MIT), the gofumpt README
(BSD-3), the gosec README and rule list, and the Uber Go Style Guide (Apache-2.0), read 2026-10-08. Meant to
be folded into `go-conventions` when the extended version of that block lands. 🟡: never run by us; open
points are in [`references/origin.md`](./references/origin.md).
