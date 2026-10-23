---
name: scaffolded-code-updates
description: "Use when code was copied into the repo by a generator or a copy-in component registry (a project scaffold, a starter template, shadcn-style components the project owns line by line) and the upstream source has moved on: a new version, a security fix, a breaking change. Records where each copy came from, detects drift between the copy and its source, applies upstream changes by codemod or three-way diff, and spreads a security fix to every project already generated."
---

# scaffolded-code-updates

Cross-cutting, used at step 6 (`code`) and step 10 (`ship`) of `WORKFLOW.md`. A dependency is updated by
bumping a version; scaffolded code is not, because once copied it is ours. That is the point of the model
and its cost: the generator or registry ships a fix, and nothing tells the copies. This block is how the
copies stay reachable.

## When
- A generator, starter or copy-in registry is used to add code to a repo.
- The upstream of code already copied releases a new version, a breaking change or a security advisory.
- A review finds a file that looks generated and nobody knows from which version.

## Steps
1. **Record the origin at copy time.** For each scaffolded unit (a component, a module, a whole project),
   keep in the repo a manifest entry: source, version or commit, date, and the list of files. Most copy-in
   registries write a configuration file; keep it committed. Without the version, step 3 has no base and
   every later update is a guess.
2. **Keep the pristine copy reachable.** Either commit the generated output alone first, then the local
   edits in later commits, or keep the upstream version recorded in step 1 so it can be regenerated. Local
   edits sit on top of a known base, never mixed into the generation commit.
3. **Detect drift mechanically.** Regenerate the recorded version into a scratch directory and diff it
   against the repo: what differs is the local edits. Regenerate the new version and diff it against the
   recorded one: that is the upstream change. A unit whose local diff is empty is replaced outright.
4. **Apply upstream changes as a three-way merge or a codemod, never by retyping.**
   1. Three-way: base = the recorded version, ours = the repo, theirs = the new version. Conflicts are where
      a local edit met an upstream change, and each one is read.
   2. Codemod: when upstream publishes one for a breaking change (a renamed prop, a moved import), run it
      on the repo, then review its diff like any other change. A codemod is code that rewrites code; its
      output is not trusted unread.
   3. Update the manifest entry of step 1 in the same change.
5. **Spread a security fix to every copy.** When an advisory hits a generator or registry version, the fix
   in upstream reaches nobody. List every repo whose manifest records an affected version (a search across
   the organisation's repos for the manifest file and version), open one change per repo with step 4, and
   track them to merge. A repo with no manifest is searched by a distinctive line of the vulnerable code.
6. **Prefer a dependency when nothing is edited.** A unit kept byte-identical to upstream across several
   updates is a dependency in disguise: moving it to a package makes the next fix a version bump.

## Output / checkpoint
The manifest entry per scaffolded unit (source, version, files), and for each update the drift diff of
step 3 and the merged change of step 4, attached to the `code` checkpoint. For a security fix, the list of
affected repos with the status of each change. No new checkpoint.

## Guardrails
- Record the version at copy time; never copy generated code into a repo without its manifest entry.
- Never regenerate over a modified copy: local edits are lost without a trace. Diff first (step 3).
- Review a codemod's output as a diff; never commit it unread.
- The agent prepares the changes; it does not run a generator that downloads from the network on its own
  (`CONVENTIONS.md`, no-install rule): the operator runs it and the agent works on the output.
- 🟡: written from the documented update model of copy-in component registries and project generators, not
  run on a real update yet.

## Origin
No external text taken. The idea comes from public documentation of copy-in component registries (the
"you own the code" model and its diff command) and of project generators that ship codemods for upgrades;
the manifest, three-way merge and security fan-out are an internal synthesis.
