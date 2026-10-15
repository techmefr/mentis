---
name: release-notes-writing-pitfalls
description: "Use when release notes or a CHANGELOG file are written from commits and pull requests: reducing the history to net outcomes, selecting entries by what a consumer can observe, working from the diff and not from titles, entry wording, breaking entries (what breaks, who is hit, what to do), keeping the version number honest, announcing deprecations, tiering a release by reader impact, a verification gate that maps each claim to a diff, small note files kept with the code, and the Keep a Changelog baseline."
---

# release-notes-writing-pitfalls

The premise: **release notes answer one question, "does this release cost me work?", and a commit log answers
a different one**. Generated lists fail in two directions, entries with no source and shipped changes with no
entry, and the damage that is hard to undo is a sentence describing a change the code did not make.

`business/release-communication` is the short overview of who needs to be told what. This block is the
writing craft: selecting, wording, versioning and checking. The mechanics of removing something that is in use
are `deprecation-migration`; observable behaviour as an API contract is in `api-design`.

## When
- Writing the notes for a release, or a `CHANGELOG.md`, from a messy history.
- Reviewing notes that read like a git log, hide a breaking change, or contradict the code.
- Deciding how much announcement a release deserves.
- Setting up how a team with many contributors collects notes.

## Steps

**Read only the section the task meets.**

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Reducing to net outcomes, selecting by consumer effect, working from the diff | the raw history is in front of you | [`01-select-and-reduce.md`](./references/01-select-and-reduce.md) |
| 2 | Entry wording, ordering, breaking entries, honest versions, deprecations | an entry is being written | [`02-entries-and-breaking.md`](./references/02-entries-and-breaking.md) |
| 3 | Tiering, the verification gate, note files kept with the code, hand-off | the notes are about to be published | [`03-tier-and-gate.md`](./references/03-tier-and-gate.md) |
| 4 | The Keep a Changelog baseline for the file | a changelog file is created or repaired | [`04-changelog-file.md`](./references/04-changelog-file.md) |

## Output / checkpoint
The notes; a table mapping each entry to a commit or pull request in the range; the list of changes seen and
deliberately left out, with the reason; and the open items for a human (an unmeasured number, a missing
migration link). Notes without the mapping are a draft.

## Guardrails
- Never write one entry per commit; reduce to the net outcome first (§1.1).
- Never decide inclusion from a file path (§1.2).
- Never trust a commit or pull request title as the claim; check the diff (§1.3).
- Never put marketing adjectives or ticket identifiers in an entry (§2.1).
- Never bury a breaking change mid-list, and never write one without what breaks, who is hit and what to do
  (§2.2, §2.3).
- Never ship a "Removed" entry in a minor release (§2.4).
- Never include a number that is not from a measurement in the source material (§3.2).
- Never dump the commit log into a changelog (§4.1).
- The source of the wording rules is one author's skill and a changelog convention; its cited studies, tool
  notes and statistics were not checked and are not carried (see [`references/origin.md`](./references/origin.md)).

## Origin
Rewritten from the changelog-writing skill in Samuel Berthe's developer-relations-skills (MIT) and the Keep a
Changelog source page by Olivier Lacan (MIT), read 2026-10-15. Details, removed content and open points are in
[`references/origin.md`](./references/origin.md). 🟡: never run by us.
