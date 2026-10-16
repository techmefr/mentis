# dart-pub-workspace-and-publish-pitfalls §2 — Publishing and advisories

Sources: the automated publishing, publishing and security advisories pages of the Dart website (CC BY 4.0,
credit: the Dart authors; code samples BSD-3-Clause; commit 85d6c72, read 2026-10-16), rewritten.

## 2.1 Credentials
1. **Automated publishing authenticates with temporary tokens signed by the CI host or by the cloud identity
   service**, so no long-lived secret is copied into the deployment environment.
2. **An exported service-account key is the fallback** for environments with no identity service. It is a
   long-lived secret and a larger risk if leaked.
3. **Automation publishes existing packages only.** The first version is published by hand with the publish
   command.
4. **When a service account is the publisher, review who can impersonate it**, through the APIs, by exporting
   keys or by changing permissions in the cloud project.

## 2.2 Tag-triggered publishing from GitHub Actions
1. **pub.dev accepts automated publishing from GitHub Actions only for a workflow triggered by pushing a git tag**
   and rejects other triggers, so events that should never publish cannot.
2. **Enable it on the package's admin tab** (an uploader of the package or an admin of its publisher), giving the
   repository and a tag pattern containing the version placeholder.
3. **The workflow's tag filter must match the pattern on pub.dev**, and the version in the package file must
   match the version in the tag. If nothing triggers, compare the two patterns first.
4. **A repository with several packages gives each its own pattern** (the package name before the version) and
   its own workflow file.
5. **Prefer the Dart team's reusable publish workflow**: it lets them maintain the logic and lets pub.dev know
   how the package was published. A custom workflow is for the case where generated code cannot be checked in;
   the page still prefers checking generated code in, so published files can be compared with the repository.
6. **The job needs the identity-token permission** and nothing more for authentication.

## 2.3 Who can publish
1. **Anyone who can push a matching tag can publish.** Restrict that with tag protection rules, or better with a
   required GitHub environment.
2. **Requiring an environment on pub.dev puts the environment in the signed token**, so a user with push access
   cannot dodge the environment's protection rules by editing the workflow file; required reviewers hold the run
   until approved.
3. **Check the audit log after a publish**: the entry links the workflow run that published it.

## 2.4 Before and after
1. **Run the publish dry run first and read the list of files it would publish**; cancel if an unwanted file
   appears. A publish ignore file is for the rare case the default list is wrong.
2. **Retraction is not deletion.** A version can be retracted within seven days of publication and restored
   within seven days of retraction; it stays listed with a badge. Publish a fixed new version first when you
   can, because retraction affects the package's users.

## 2.5 Security advisories
1. **Pub reads the GitHub Advisory Database**; at resolution the client prints affected versions and links the
   advisory, and the Dart team recommends reading it and strongly considering an upgrade when it affects you.
2. **Ignoring an advisory is a pubspec list of identifiers, honoured for the root package only**; ignored entries
   in your dependencies do nothing for your own resolution. Use it only for an advisory you read and judged
   irrelevant.
3. **To report one, create a draft repository security advisory** on GitHub; GitHub reviews it and ingests it
   into the central database.
