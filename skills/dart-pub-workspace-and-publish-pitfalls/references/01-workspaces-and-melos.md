# dart-pub-workspace-and-publish-pitfalls §1 — Workspaces and Melos

Sources: the pub workspaces page of the Dart website (CC BY 4.0, credit: the Dart authors; code samples
BSD-3-Clause; commit 85d6c72) and the getting-started page of the Melos documentation (Apache-2.0, commit
fb8b35b), both read 2026-10-16, rewritten.

## 1.1 Why a workspace
1. **Without one, each package has its own lock file and resolution.** You run the dependency command once per
   package, you risk different versions of one dependency in each, and an editor opened at the root creates a
   separate analysis context per package, which costs memory.
2. **A workspace gives one shared resolution**, which lowers analysis memory on large repositories.
3. **The trade-off is deliberate**: Dart does not allow two versions of one package, so a shared resolution
   raises the chance of a conflict. For packages used together the page calls that a feature, because the
   incompatibility surfaces between your own packages now, not when a consumer meets it later.

## 1.2 Creating one
1. **The root pubspec has a name, `publish_to: none`, an SDK constraint and a `workspace` list of member
   paths.** Every member has an SDK constraint of at least the workspace minimum (3.6 in the page) and the entry
   `resolution: workspace`. Support starts at that SDK release, and only the members, not their dependencies,
   need the constraint.
2. **One get anywhere in the repository** creates a single lock file and a single package configuration next to
   the root, and deletes the others beside the members.
3. **Glob entries** (such as all subfolders of a packages folder) need a later SDK release (3.11 in the page);
   with an earlier one list explicit paths.
4. **A member can declare its own workspace list** to nest packages; the root lists only the top member and pub
   discovers the rest.

## 1.3 Stray files
1. **After a migration, old lock files and package configurations next to members are deleted by the get**,
   because they would shadow the root ones. This includes such files in directories between the root and a
   member.
2. **A pubspec between the root and a member that is not itself a member makes the get fail**, since resolving
   it would create a shadowing package configuration. Make it a member or move it.

## 1.4 Dependencies between members
1. **Members that depend on each other resolve to the workspace copy whatever the declared source**, but the
   local version must still satisfy the declared constraint.
2. **When a member is published and consumed outside the workspace, the consumer gets the hosted version of
   its sibling.** So declared constraints on siblings must be real, publishable ranges.
3. **Overrides in every member's pubspec and in an overrides file next to it are respected, but a package can be
   overridden only once in a workspace.** Keep overrides in the root pubspec.
4. **To resolve one member alone** (for example to validate its constraints), an overrides file next to it that
   resets the resolution entry gives it an independent resolution; remove it afterwards.
5. **Commands that act on the current package** (adding a dependency, publishing) take a directory option, so
   pass the member's path instead of changing directory. A workspace list command prints all members.

## 1.5 Melos on top
1. **Melos is optional and sits on top of pub workspaces; its own getting-started page tells you to read the
   workspace guide first.**
2. **Put a dependency on Melos in the workspace root pubspec** so every contributor and CI job uses the same
   version; the globally installed one then switches to it.
3. **Keep the workspace root free of an application or package** unless the Melos option for using the root as a
   package is set; the root holds the workspace configuration.
4. **The Melos script, versioning and release documentation was not read**; do not describe those features from
   this block.
