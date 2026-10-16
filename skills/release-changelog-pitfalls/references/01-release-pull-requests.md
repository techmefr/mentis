# release-changelog-pitfalls §1 — Release pull requests with release-please

Sources: the README and `docs/troubleshooting.md` of googleapis/release-please at fa67225, read 2026-10-16. The files describe the tool's behaviour at that commit; label names and the list of releasable prefixes are the files' own.

## 1.1 What the tool does, and what it does not
1. **It reads the Conventional Commit messages in the git history and keeps one release pull request open.** The request stays up to date as more work lands; merging it is the act of releasing.
2. **On that merge it updates the changelog and the language-specific version files, tags the commit with the version, and creates a GitHub release from the tag.**
3. **It does not publish to package registries and does not manage complex branch layouts.** Publishing is a separate step in a separate job (own guidance: trigger it from the tag or the release event, not from the pull request merge).
4. **The release pull request carries a status label:** pending before the merge, tagged after the tag exists, snapshot for a snapshot version bump, and published, which the tool does not add itself but recommends as a convention for publishing tooling. The pending and triggered labels are what the tool consults before opening another release pull request (1.4).
5. **The release pull request itself may be merged by squash or by a merge commit.** That is a statement about the release pull request only; 1.2 is about the pull requests that feed it.

## 1.2 Merge feature pull requests by squash
1. **The README strongly recommends squash-merge for the pull requests that feed the release.** A linear history sorts commits by merge date without mixing pull requests, makes bisecting bugs easier, and keeps main clean.
2. **The reason that matters for notes:** inside one pull request a `feat` commit can be followed by a `fix` commit for a bug that never existed on main. Merged commit by commit, both reach the notes, and the fix entry describes a bug no user ever met.
3. **Red-green development has a second cost:** a failing-test commit followed by its fix leaves points on main where the tests do not pass, if the commits are merged or rebase-merged individually.
4. **A correction to the notes of an already merged pull request** goes in the body of that pull request, in a marked override section; the next run uses it in place of the original message. The README says this works only when the pull request was squash-merged, because with a plain merge the tool cannot tell which commits the override replaces.

## 1.3 Writing the commit
1. **The prefix decides the bump:** `fix` is a patch, `feat` a minor, and a `!` after the type (`feat!`, `fix!`, `refactor!`) marks a breaking change and gives a major.
2. **One commit can carry several changes** by adding further messages as footers at the bottom of the commit message. The README's example yields three entries from one commit: one for the main message and two from the footers, one of them flagged as breaking by a breaking-change footer line. The README marks as important that the extra messages go at the bottom of the commit.
3. **To force a version, put `Release-As: x.y.z` in the body of a commit on the main branch** (case does not matter). The tool then opens a release pull request for that version. The README's way to do it without a code change is an empty commit with that line in its body.

## 1.4 No release pull request appeared
1. **Check that a releasable unit was merged since the last release.** A releasable unit is a commit prefixed `feat`, `fix` or `deps`. A `chore` or `build` commit alone is not one, so a chore-only history opens nothing. Some language strategies add prefixes; the README's example is `docs` for Java and Python.
2. **Look for an old release pull request still labelled pending or triggered.** A failed API call may have left the label behind, and the GitHub app does not open a new release pull request while one is labelled pending. If that pull request is not going to be released or was already released, remove the label, and only then re-run the tool.
3. **Re-run to force it.** With the GitHub app, add the force-run label to the merged pull request; with the action, retry the failed workflow run.
4. **A release pull request closed by mistake and reopened** is labelled closed and is not labelled pending again, so the tool does not act on it. Remove the closed label, add the pending label and the force-run label (the troubleshooting page's recipe).
5. **Own guidance:** record the label state in the incident notes before changing any label, since the labels are the tool's only memory of what is in flight.

## 1.5 Test the configuration where the tags are
1. **Debug with the command-line tool in dry-run mode,** which says what it would do without opening a pull request or tagging, and with the debug or trace log levels for detail. It needs a token with access to the repository.
2. **Test a configuration change on a branch of the real repository, not on a fork,** and point the tool at it with the target-branch option. The tool depends on pull requests, releases and tags, and a fork does not copy them.

## 1.6 How the previous release is found
1. **Use a manifest config.** The tool then reads the latest released version from the manifest file, a map from component path to version (the path is a dot for a single component), and finds the matching commit from recent releases or the expected tag name.
2. **Without a manifest the lookup is fragile.** The troubleshooting page lists a search through the last 250 commits on the target branch for a release pull request, then the latest releases, then the latest tags, each matched against those commits, at the cost of more API calls. Own inference: a last release further back than that window may not be found.
3. **In a monorepo, give each independently released module a component name.** Releases and tags then carry the component as a prefix, so two modules can both be at the same version number.
4. **A repository with existing releases is best bootstrapped from a manifest** (the README's advice) instead of leaving the tool to infer the history.

## 1.7 Checks (own guidance)
1. Squash-merge a `feat` pull request containing a `fix` fixup commit and confirm the notes carry one entry.
2. Merge only a `chore` commit and confirm no release pull request opens; then merge a `fix` and confirm it does.
3. Run the dry-run on a test branch and read the version it intends to propose before merging the real release pull request.
