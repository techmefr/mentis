# monorepo-task-graph-and-cache-pitfalls §2 — Tasks, cache and CI

Sources: the `turborepo-caching` and `monorepo-management` skills of wshobson/agents at 0874a27, read 2026-10-20. The source's example uses an older key for the task map; the tool's current reference (turborepo.dev, read 2026-10-20) names it `tasks`. Behaviours below marked "reference" were checked on that page and the run reference; the rest stays as described. Points marked "own guidance" are not from a source.

## 2.1 What a task declares
1. **A cache key comes from the task's declared inputs and the code of its dependencies.** The source's concepts are: what must finish first, whether to cache, which files are outputs, which files are inputs, and whether the task is long-running. Anything the task reads that is not declared is invisible to the key.
2. **"Dependencies first" and "this package's own earlier task" are different edges.** Building a package needs its dependencies built (a caret-style edge in the source's example); a test that needs its own build uses the plain task name. Mixing them runs tasks in the wrong order or too early.
3. **Declare the outputs, and declare all of them.** A hit restores only the listed outputs; a missing one leaves the next task without its files, and the failure looks like a flaky build. Exclude the framework's own cache folder from the list of outputs, as the source's example does.
4. **Declare global inputs:** root configuration files, the lockfile, and environment files that change behaviour. The source puts environment files in a global-inputs list.
5. **Reference:** a caret in a dependency entry means the same task of the package's dependencies; omitting outputs caches no files (only logs); setting inputs replaces the default of tracked files unless the default marker is included; a negated glob keeps a framework cache folder out of outputs; changes to the global variable and file lists invalidate every task.
6. **Narrow inputs for tasks that read little** (a test task that reads sources and its config) so documentation edits do not invalidate it; but a too-narrow list is the most common cause of stale hits (the source names incorrect cache inputs as a pitfall).

## 2.2 Environment variables
1. **A variable that changes the output but is not in the task's environment list does not change the cache key.** Symptom: the build has the old API address after the variable changed. Declare it per task, or globally for ones every task reads.
2. **Pass-through is not the same as hashing:** the per-task environment list changes the key, the pass-through list only makes the variable available at run time (reference). Know which of the two you declared.
3. **Public-prefix variables baked into a front-end bundle are build inputs** (the source's example lists them with a wildcard). Treat them as part of the key, and do not put a secret behind such a prefix (`skills/vite-bundler-conventions`).
4. **Strict environment mode, the default (reference), drops undeclared variables** from the task's process; a task that "suddenly cannot find" a variable in CI has not declared it.

## 2.3 What to cache, what not
1. **Cache deterministic tasks only:** build, lint, typecheck, test. A task that fetches the network, reads the clock or writes a timestamp into its output makes every hit a lie or every run a miss (own guidance).
2. **Never cache the development server or a clean task,** and mark the dev server as long-running so the orchestrator does not wait for it (the source's example does both).
3. **A task must write only inside its own package and its declared outputs** (own guidance). A task that writes to a sibling or to the root changes another task's inputs behind the graph's back.
4. **Debug a suspect hit by running with the cache bypassed and comparing the outputs,** then by asking the tool for the hash inputs of the task and diffing two runs (reference: a dry run lists each task's hash, inputs and environment variables, and a run summary file records hashes and timings; the force flag ignores and overwrites existing cache entries).

## 2.4 Affected-only runs in CI
1. **Run tasks only for packages affected since the base branch,** with a filter that includes dependants of changed packages (the source's CI example filters on a git reference).
2. **The base reference must exist in CI.** The tool's run reference (read 2026-10-20) says the affected mode needs every commit between base and head, defaults to comparing the main branch with HEAD, and treats all packages as changed when the checkout is too shallow; fetch enough history or the base ref explicitly. By default one changed file selects every task of its package.
3. **A change to a global input affects everything,** correctly. If a root file edit does not rebuild all packages, the root file is not declared (§2.1.4).
4. **Compare an affected-only run with a full run at least once and on a schedule** (own guidance): results must match; a difference is a missing edge in the graph.
5. **Install with the frozen lockfile in CI** so the key does not move with a floating resolution (`skills/package-manager-supply-chain-pitfalls`).

## 2.5 Remote cache
1. **A remote cache shares results between machines,** which also shares a poisoned result. Give write access to the main branch's pipeline and read access to the others (own guidance).
2. **The token and team identifiers come from the CI secret store,** never from a committed file (the source passes them as secrets).
3. **A self-hosted cache is a service with authentication, retention and an uptime;** the source shows a small server, which is a demonstration, not a deployment (own guidance).
4. **A cache hit must be reproducible on a different operating system or architecture only if the task is.** Native modules and absolute paths in outputs make cross-machine hits wrong; include the platform in the key for such tasks (own guidance).

## 2.6 Makefile-style graphs (own guidance)
1. **A target that produces no file with its own name must be declared as always-run,** or a stray file of that name makes it silently skip.
2. **A prerequisite you forgot is a stale build:** generate header or dependency lists with the compiler, not by hand.
3. **Parallel builds expose missing edges that serial builds hid;** run the parallel build in CI on purpose.

## 2.7 Checks (own guidance)
1. Delete the cache and build from a clean checkout; then change one declared input and one undeclared file and confirm only the first invalidates.
2. Every task lists inputs, outputs and environment variables, or the absence is stated.
3. The affected-only filter, on a pull request, selects the packages you expect, with history available.
4. The token is a secret, and pull requests from forks cannot write to the cache.
