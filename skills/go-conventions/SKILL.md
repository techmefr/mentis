---
name: go-conventions
description: Use when writing or reviewing Go, applies the highest-value concurrency, error handling and context patterns from the golangci-lint meta-linter (govet/staticcheck/errcheck) and the Uber Go Style Guide. No internal production experience behind this block (unlike vue-nuxt-vuetify-conventions/react-nextjs-conventions), content sourced from established market tooling/style guides.
---

# go-conventions

Step 6 of the pipeline (`WORKFLOW.md`). Frames the writing and review of Go code. **Special status**:
unlike the frontend blocks (vue-nuxt-vuetify, react-nextjs), there is no in-house production experience
behind this file yet: the content comes from deterministic tooling (golangci-lint, staticcheck, govet)
and established style guides (Uber), not from real review feedback. To be treated as a solid base to be
confronted with the first real Go project, not as proven doctrine.

## When
As soon as Go code is written or modified, during `code` (6) or `tdd` (5).

## Steps

### 1. Concurrency and goroutines: the most frequent mistake
1. Every goroutine launched has an explicit stop mechanism (`context`, `WaitGroup`, or a `done` channel):
   a goroutine with no way out leaks silently on every call.
2. `sync.Mutex`/`sync.RWMutex` never copied by value (including through a struct that embeds it): the
   zero value is valid, never initialise it or pass a pointer out of reflex.
3. A closure inside a loop capturing the loop variable by reference (a classic bug in Go < 1.22, still
   present in legacy code); check the module's version before judging this point inapplicable.
4. The `cancel` returned by `context.WithCancel`/`WithTimeout` always called (often as a `defer`):
   otherwise a context leak.
5. Concurrent access to a map with no mutex or `sync.Map` panics at runtime ("concurrent map read and map
   write"), not detected statically.

### 2. Error handling
1. No returned error ignored without an explicit `_` or handling.
2. `errors.Is`/`errors.As` rather than a direct comparison (`err == SomeErr`) or a direct type assertion:
   breaks as soon as an error gets wrapped.
3. `%w` to wrap an error (preserves the chain for `errors.Is`/`As`), `%v` only if the obfuscation is a
   deliberate choice, not a default.
4. A `recover()` that swallows the error without rethrowing or logging it hides a real bug: never a silent
   `recover`.

### 3. Context
1. `context.Context` always the first parameter, never stored in a struct.
2. A function propagates the context it received as a parameter, never a `context.Background()` recreated
   deep down, otherwise the upper level's cancellation/timeout gets ignored.
3. HTTP request always with a context (`http.NewRequestWithContext`), never a bare `http.Get`.

### 4. Other correctness
1. An HTTP response's `resp.Body` always closed (`defer resp.Body.Close()`), otherwise a connection leak.
2. `defer` inside a loop accumulates until the end of the function, not of the iteration: resource
   exhaustion (files, locks) on a long loop.
3. An `err` variable redeclared with `:=` shadowing a parent scope's error; check that no error from the
   outer scope is silently lost.
4. `interface{}`/`any` as a catch-all to avoid typing properly: prefer generics or a concrete type.
5. Slices/maps received or returned at API boundaries = a reference to the caller's data, mutable without
   their knowledge: copy if isolation is necessary.

## Output / checkpoint
Code compliant with the four sections above, and `golangci-lint run` (default config: errcheck, govet,
staticcheck, gosimple, ineffassign, unused, plus `contextcheck`/`bodyclose`/`noctx` if enabled) with no
new finding introduced by the diff. Checked by `gate` (7) and `review` (8).

## Guardrails
No comments in the code produced. Don't enable `shadow` (govet) by default: noisy, only if the project
explicitly wants it. This block hasn't been confronted with a real production Go project in house yet: if a
rule here diverges from a real observed need, fix this block rather than treating it as settled.

## Origin
Ideas taken from: golangci-lint (meta-linter, default categories
errcheck/govet/staticcheck/gosimple/ineffassign/unused); staticcheck.dev (the SA/S/ST rules cited);
uber-go/guide (Uber Go Style Guide, copying slices/maps at boundaries, defer for resources, avoiding
catch-all `interface{}`). Mechanisms rewritten, no copied text. Market research, no internal production
feedback at this stage.
