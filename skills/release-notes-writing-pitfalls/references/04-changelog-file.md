# release-notes-writing-pitfalls §4 — The changelog file

Keep a Changelog is one maintainer's published convention, gathered from open-source practice and presented as
his considered opinion, not a standard. It is the baseline here because it is short and widely recognised.

## 4.1 What the file is
1. **A changelog is a curated, chronologically ordered list of notable changes for each version**, written for
   humans and not machines.
2. **Never dump the commit log into it.** A commit documents a step in the evolution of the code; an entry
   documents the noteworthy difference, often across several commits, for users. Merge commits, obscure titles
   and documentation changes are noise.

## 4.2 Structure
1. **One entry for every version, the latest first, with the release date shown.**
2. **Group the same kinds of change under six headings**: Added (new features), Changed (existing
   functionality), Deprecated (soon to be removed), Removed (now removed), Fixed (bug fixes) and Security
   (vulnerabilities).
3. **Versions and sections are linkable.**
4. **Dates are written year, month, day with hyphens**, for example 2026-10-15: largest unit first, no
   ambiguity with regional formats, and an ISO standard.
5. **Say whether the project follows semantic versioning.**
6. **Keep an Unreleased section at the top** so people can see what is coming and so release day moves its
   content into a new version section.
7. **Name the file CHANGELOG.md.** The source's argument: why make users guess where to look.

## 4.3 Bad practice and what the convention insists on
1. **Ignoring deprecations is the failure it names.** Upgrading to a version that lists deprecations, removing
   what is deprecated, then upgrading to the version where they become removals should be possible. If you do
   nothing else, list deprecations, removals and breaking changes.
2. **An inconsistent changelog is as dangerous as none**, since users take it for the single source of truth.
   Trivial changes need not be recorded; any important one must be.
3. **A release pulled for a serious bug or a security problem should still appear**, with a loud marker, and
   the convention suggests a bracketed tag after the date.
4. **A changelog may be rewritten** to add missing releases or to repair an omitted breaking change; the
   source treats the second as obviously necessary.
5. **A hosted release page is not a replacement for the file**: the source argues it is not portable and less
   discoverable than a top-level file.

## 4.4 Example skeleton

```
# Changelog

## [Unreleased]

## [3.0.0] - 2026-10-15
### Changed
- Breaking: client.send() rejects payloads over 1 MB. Affects callers that relied on truncation.

### Removed
- The legacy option TIMEOUT_MS, deprecated in version 2.

## [2.4.0] - 2026-09-30
### Added
- Add stream() for token-by-token responses.
```

## 4.5 Verify
Check the file for the four faults named in §4.3: a deprecation or removal missing from a version that had
one, a version with no entry, a date written in a regional format, and a section that reads like a commit
log. A breaking change found missing is repaired in place (§4.3.4).
