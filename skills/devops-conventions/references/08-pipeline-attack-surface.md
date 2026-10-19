# § 8 — The pipeline as an attack surface

> Section 8 of `skills/devops-conventions`. Read it when a CI file is written or reviewed for what it
> executes, what it can read and who can make it run. The reproducibility rules are §1; the GitHub
> Actions specifics (aggregator check, workflow analyser, bot pull requests) are in `ci-workflow-hardening`.
> The mechanisms hold on any CI; the setting names below are GitLab's and GitHub's as read, and they move.

1. **Pin everything the pipeline executes by an immutable reference.** A branch, a tag or `latest` is
   whatever its owner last pushed, and your next run executes it with your credentials. Included
   configuration is pinned to a commit, a protected tag or an exact component version, and a verified copy
   kept in the repository is better than a remote include. A container image is referenced by digest, from a
   repository where only a few people can move the tag, and never through a variable, since a variable can be
   made to point at another image. A third-party action is pinned to a full commit hash taken from the
   action's own repository, not from a fork. Dependencies come from the lockfile with exact versions
   (hash checking where the tool offers it), and a tool a job downloads has a stated version and a verified
   checksum.
2. **Untrusted text never becomes part of a script.** A branch name, a merge request title, a commit message
   or an issue body is typed by whoever can open a request. On GitHub, the documentation says to hand such a
   value to the step through an intermediate environment variable (or to an action as an argument) and to
   quote the shell variable, instead of interpolating the expression into the script. The GitLab pages read
   carry no equivalent warning; the same rule applies to its predefined variables by analogy, which is our
   inference and not a statement of that documentation.
3. **A secret reaches only the jobs that need it, and only from refs you control.** Credentials that matter
   most belong in an external secrets manager the pipeline queries, since a CI variable is visible to anyone
   with settings access. A variable that has to exist is protected (available only to pipelines on protected
   branches and tags), masked or hidden, and still treated as readable by anyone who can change what the
   job runs: masking is documented as not a guarantee. Derived values (an encoded or signed token) are
   registered as secrets too, and a structured secret is split so that each value can be redacted. After
   testing, read the job log for a printed value.
4. **A request from a fork runs in the fork, not with your secrets.** By default a fork's pipeline cannot
   read the parent's variables and cannot use protected variables or protected runners. Running it in the
   parent changes that: every variable becomes available to code the fork's author wrote. So a change to the
   CI file is reviewed before anyone triggers a parent-project pipeline for it or merges it, and a reviewer
   who finds code reading the environment stops instead of running it; the interface warning is skipped
   when the pipeline is started through the API or a quick action, so do not rely on it. On GitHub the
   same line is drawn at `pull_request_target`: avoid it unless the workflow needs the privileged context,
   and never check out untrusted code in it or in a workflow it feeds.
5. **The job token gets the narrowest reach.** The job token is valid for the length of the job, but what it
   can touch is decided by configuration: the allowlist of other projects that may use it starts as the
   project alone and gains an entry only when cross-project access is needed (a group entry covers every
   project in the group, including ones created later). Switching the allowlist off is described as a
   security risk and is for a short test only. On GitHub, set the default token to read-only on contents and
   raise permissions per job.
6. **A runner is a machine that runs strangers' code, so decide whom it trusts.** The shell executor runs
   jobs with the runner user's rights and can read other projects' code on the same host, so it fits trusted
   builds only. Privileged container mode gives a job the host's root capabilities, so avoid it or confine it
   to isolated, throwaway machines and to protected branches. A runner shared by several projects and not
   cleaned between jobs lets one repository's job affect another's, and a pull policy that reuses a local
   image can serve a private image to someone without registry access. On GitHub, self-hosted runners on a
   public repository are to be avoided and, elsewhere, are not ephemeral unless you make them so; prefer
   groups that limit the blast radius and clean, just-in-time runners.
7. **Take run-time parameters through typed inputs, not free variables.** The GitLab documentation prefers
   pipeline inputs (typed and scoped) to pipeline variables, which can override predefined ones, and
   suggests turning pipeline variables off once inputs are in use.

**Verification.** A scratch merge request from a fork shows no secret in its job log; the CI file contains no
`latest`, no unpinned include and no expression of a user-typed field inside a script; the list of projects
allowed to use the job token is read and each entry is explained.
