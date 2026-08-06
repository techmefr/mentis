---
name: start-feature
description: Use at the very start of a feature, before coding, creates the isolated worktree via starfleet (create_task + launch_worktree) and kicks off the pipeline. Xefi rewrite of superpowers:using-git-worktrees, wired into starfleet.
---

# start-feature

Starts a feature in an **isolated** space (dedicated worktree), coordinated by starfleet
(unique deterministic port, shared state, dashboard visibility).

## Steps

1. **Identity**: infer the project (git remote `git config --get remote.origin.url`, otherwise
   the repo root) and the target branch.
2. **Register + allocate**: call the starfleet MCP tool **`create_task`** with `project`,
   `branch`, `repoPath`, `runCommand` (the dev command), and `feature`/`role` (front/back) if
   relevant. You get back a **unique port** (no collision with the other
   projects/worktrees).
3. **Create the worktree**: call **`launch_worktree`**, starfleet runs the `git worktree add`
   in a sibling folder, isolated from your current workspace. (First check that the worktree
   folder really is gitignored.)
4. **(optional) Start the server**: `start_server` runs `runCommand` with the injected port;
   the dashboard flips the worktree to "live" and gives you the "Open" link.
5. **Move on**: go to `brainstorm` then `spec`. On every step cleared, `update_checkpoint`.

## Why go through starfleet

Worktree isolation on its own (like superpowers:using-git-worktrees) prevents interference,
but **does not coordinate** ports or multi-project visibility. The seam with starfleet adds:
a deterministic collision-free port, a shared source of truth, the dashboard, and the
post-merge cleanup (`finish_task`).

## End of life

Don't delete the worktree by hand: `finish` (→ `finish_task`) removes it cleanly after the
merge and updates develop.
