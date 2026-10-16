# release-changelog-pitfalls §2 — What the Keep a Changelog 2.0 text adds

Sources: `source/en/2.0.0/index.html.md` of olivierlacan/keep-a-changelog at 08d0df5, read in full 2026-10-16. It is one maintainer's published convention, not a standard (the text says so). The baseline file layout (the six headings, newest first, ISO dates, an Unreleased section) is already in `release-notes-writing-pitfalls`, part 4; this part keeps only what the 2.0.0 text adds or sharpens.

## 2.1 A changelog is curated, a generated one is raw material
1. **Drafting and curating are different jobs.** The text's line is that machines can draft and humans curate. A tool that reads commits (it names semantic-release, release-please, Changesets and git-cliff) gives a starting point, because a commit and a changelog entry are written for different readers.
2. **Two assumptions fail in a generated changelog:** that every commit belongs in it, and that the right entry is a reworded commit message. Many commits do not matter to a reader, and the changes that do often span several commits and need to be described from the reader's side. Sorting commits by type shortens the list and does not make that shift.
3. **So read and edit the section the tool wrote before the release goes out.** For release-please the README documents one correction route, the override section in the body of a merged pull request (1.2, point 4); editing the changelog by hand in the release pull request before merging it is own guidance and was not checked against the tool.
4. **Curation is not sorting every commit into a type as it is made.** Write the changelog as a summary for readers, not as a record of commits. A changelog lists notable changes only, since version control already records all of them.
5. **If a language model drafts it,** the text's brief is: summarise notable user-facing changes, do not paste a git log, sort each into one of the six types, explain the reason in the text, mark breaking changes, drop what is not worth reading, then read the result before anyone else does.

## 2.2 Types
1. **The six types are listed in order of urgency:** Security, Removed, Changed, Deprecated, Fixed, Added. The reason given: readers skim to find what affects them, and starting with new features buries security fixes and removals. A different order is allowed if it is the same in every release.
2. **Omit a section with no entries,** and order entries inside a section by usefulness to readers.
3. **Decide Fixed versus Changed by asking whether the old behaviour was a bug.** A bug becomes Fixed; behaviour that worked as intended and now works differently is Changed. Security is for a change that addresses a vulnerability, even though it could fit either, because the urgency and the audience differ.
4. **A Security entry that has a CVE identifier starts with it,** so readers and security tools can match it to the advisory. The entry is a short summary with a link to the advisory (a CVE record, a database entry or the project's own page) where affected versions, severity and fix live. A changelog does not replace a formal disclosure the project owes elsewhere.
5. **Six types on purpose.** What kind of change it is goes in the type; why it matters goes in the wording. "Rewrote the parser; three times faster on large files" goes under Changed, not a new Performance heading. `Improved` and `New` are `Changed` and `Added`; internal or housekeeping changes are rarely notable at all.
6. **Dependencies are not a type of change.** A bump can be harmless, a fix or breaking: if it matters to users, describe its effect under the right type, and otherwise leave it out. **Known issues are not a type either:** note them on the affected version or in the tracker, and put the fix under Fixed when it comes.

## 2.3 Breaking entries
1. **Mark the break inside the entry,** with a short `**Breaking:**` marker, because the version number is easy to miss. Keep the entry under its own type (usually Changed or Removed) and do not collect breaks into a separate section, so a reader scanning Changed sees them in place.
2. **Say which interface breaks:** a command line, a library API, a network protocol, a file format or a configuration schema, and which one the versioning scheme covers. "Breaking" means little until readers know that.
3. **A short upgrade note may sit in the entry** (rename one option); a long procedure is linked, not written out, since it would turn a scannable record into a how-to. The three-part wording of a breaking entry is in `release-notes-writing-pitfalls`, part 2.

## 2.4 Structure the text adds
1. **Each version heading carries a bracketed version and a date, and the bracket is a link reference resolved at the bottom** to a comparison with the previous version; the oldest version links to its tag. The Unreleased link compares the latest tag with the current head, so it always shows what changed since the last release.
2. **At release time:** rename Unreleased to the new version in the heading and in its link, then add a fresh empty Unreleased section pointing at the head.
3. **Open the file with a fixed preamble** that says it records notable changes and names the format and the versioning scheme, with the format link pinned to the version followed. A version that is not Semantic Versioning (calendar versions, a date) is fine if stated; a project that releases continuously keeps dated entries under Unreleased.
4. **Adopting a newer version of the format does not mean rewriting history.** Leave old entries as they are, apply the new rules from the next release, update the link, and say so in a short summary line.
5. **Optional extras:** name the area an entry touches when the project has distinct parts, grouped under a fourth-level heading below a type, consistently; a short summary sentence at the head of a version; linking to issues sparingly and preferring prose to bare numbers, since numbers belong to one host.
6. **A release pulled for a serious bug or a vulnerability stays in the file,** marked with a bracketed yanked tag after the date. An entry added or corrected after release is allowed, and the text suggests noting the date of the correction.

## 2.5 Changelog, release notes and CI
1. **The changelog is the source and release notes are drawn from it.** At release time the version's section is the draft of the release text. Because every version sits under a predictable heading, a small script can extract it and create the release without retyping.
2. **A release page on a code host is not a substitute for the file:** it lives in the host's database and does not travel with the repository.
3. **CI may do the mechanical parts:** move Unreleased into a dated version, check the file's format, and optionally remind a contributor that a change may need an entry. **Do not make a changelog edit a required check on every change.** The text's reason is that people then add a line to pass the check and the file fills with noise.
4. **Conflicts on a shared Unreleased section:** keep entries short and on the branch that makes the change; if conflicts are frequent, use a union merge setting in the attributes file; if they stay frequent, keep one small file per change in a directory and combine them at release. The text advises starting with the shared section and evolving only when it hurts.
5. **A monorepo** keeps one changelog per unrelated project. A single product made of many parts may keep one per component but must also keep one central changelog, so a reader does not read a dozen files to understand a release.
6. **A very long file is usually fine;** if it must be split, link the main file and the archives both ways and do not delete old entries.

## 2.6 Checks (own guidance)
1. Take the section a tool generated for the next release and mark every entry a user would never notice; the section is not ready until those are removed or rewritten.
2. Pick one entry of each type and apply the bug question to Fixed and Changed.
3. Search the file for a Security entry without an identifier or a link, and for a dependency bump listed as its own heading.
