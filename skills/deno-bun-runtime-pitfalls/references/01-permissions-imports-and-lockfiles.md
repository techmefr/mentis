# deno-bun-runtime-pitfalls §1 — Permissions, imports and lockfiles

Source: own craft knowledge; flags and defaults are to be re-read in the documentation of the runtime version in use.

## 1.1 Deno's permission model
1. **Deno denies file, network, environment, subprocess and native-library access until a flag grants it.** Grant each flag with a scope: read and write limited to named directories, network limited to named hosts, environment limited to named variables. A bare grant covers everything of that kind.
2. **Symptom: a script that "needs all permissions to work".** Cause: someone added the allow-all flag during development and it shipped. Fix: run once with prompts or the runtime's audit output, record what was requested, and replace the flag with the exact list.
3. **Permissions apply to the process, so a dependency inherits them.** A transitive package with network access can send what the process can read. Keep read scope away from secret directories and key files, and review which hosts the network scope allows.
4. **Subprocess and native-library permissions are near-equivalent to full access,** since the child process is not sandboxed. Do not grant them for code you do not control.
5. **Check:** the production start command and the task definitions contain no allow-all flag, and each scoped flag has a reason you can state.

## 1.2 Bun has no permission model
1. **A Bun process runs with the user's full rights,** like Node. Do not assume a sandbox; use a container user, filesystem permissions, and network policy for isolation, as for Node.
2. **Scripts from dependencies can run at install time under the package manager's rules, which differ from npm's.** Check which install scripts the manager runs by default and which it blocks until trusted, and keep the trusted list short.
3. **Never run untrusted code on either runtime for convenience of the flags.** Isolation for hostile input is a container or a virtual machine, not a flag.

## 1.3 Imports, resolution and lockfiles
1. **Deno resolves URL, registry and package specifiers, and a mapping file can alias them.** Pin versions in every specifier or in the mapping, never "latest" or an unversioned URL; an unpinned remote import changes under you.
2. **Commit the lockfile and install from it in CI** (a frozen or locked install mode). Without that, the pipeline resolves new versions and a green local build turns red, or worse, ships different code.
3. **A lockfile can be ignored by an option or an environment setting.** Confirm CI really reads it: change a dependency without updating the lockfile and see the install fail.
4. **Bun's lockfile format has changed between versions** (binary to text). Pin the Bun version in the project and CI so every environment reads and writes the same format.
5. **Do not mix package managers in one repository.** Two lockfiles disagree silently; keep one and delete the other.
6. **Module resolution rules differ from Node's.** File extensions, directory indexes, conditional exports and type-only imports behave differently; a path that resolves in one runtime can fail in the other.

## 1.4 Tasks, workspaces and configuration
1. **Define tasks in the project file** so the permission flags and arguments live in one place and are reviewed, not retyped in shell history.
2. **For a monorepo,** use the runtime's workspace feature or a task runner, and pin versions per workspace; see `monorepo-task-graph-and-cache-pitfalls` for cache and task-graph issues.
3. **Read environment variables through one validated config module,** not scattered calls; on Deno the environment permission is then a short, named list.
4. **Keep type-checking in CI even if the runtime strips types.** A runtime that runs TypeScript by removing types does not check them.

## Checks
- No allow-all flag; each scope has a reason (§1.1).
- Isolation relies on the container or VM where code is untrusted (§1.2).
- Imports are pinned; the lockfile is enforced; one package manager (§1.3).
- Tasks hold the flags; type-checking runs in CI (§1.4).
