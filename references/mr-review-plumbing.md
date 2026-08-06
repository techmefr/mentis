# MR review plumbing (GitLab)

> **Single source for the mechanism every review reader shares.** How to read an MR, how to batch, how the two
> modes work, how to handle existing discussions, and how to post an inline comment without it silently
> landing as a general note. The *judgement* — what counts as a finding, the comment register, the per-stack
> rules — stays in each agent. This file is the transport layer, and it does not vary by stack.
>
> Cited by: `aragorn`, `gimli`, `legolas`, `frodo`, `boromir`, `theoden`, `samwise`, `faramir`. When the
> mechanism changes, it changes **here**, once.

**Host and scripts.** Commands below assume `glab` is authenticated against the project's host. On a
self-hosted instance, `glab` falls back to `gitlab.com` unless the host is explicit — **pass
`--hostname <host>` on every `glab api` call** against a self-hosted project, or the response comes back from
the wrong instance and the failure looks like a permissions problem. The helper scripts
(`prefetch_mr.py`, `search_blobs.py`, `post_mr_comments.py`) live in the operator's own scratch folder, outside
this repo, and take the host as a default they set themselves.

## 1. Reading the MR: API first, no clone

The time cost is fetching the project, not the reasoning. By default you fetch **nothing** — everything is
read through the API.

- **One mandatory first call**: `python3 <scratch>/prefetch_mr.py <ns/repo> <N>`. It dumps, in parallel, into
  `<scratch>/mr<N>/`: `mr.json` (metadata, `diff_refs`, source branch), `diffs.json` (every hunk),
  `discussions.json`, and `files/` (each touched file on the head side, path flattened with `__`). After that,
  **everything is read locally from the dump** — no further API call for the diff, the files or the
  discussions.
- **Cross-references outside the touched files** (other callers, an interface definition, a config key):
  `glab api "projects/<ns%2Frepo>/search?scope=blobs&search=<term>&ref=<source-branch>"`, grouping a turn's
  searches. **That search is basic** — no regex, tokenised — so a "no caller left" or "already handled
  elsewhere" finding must rest on results you actually saw. If they look incomplete or ambiguous, fall back to
  the clone rather than asserting.
- **A single file outside the diff** (the matching test, a parent interface, a consumer):
  `glab api "projects/<ns%2Frepo>/repository/files/<url-encoded path>/raw?ref=<head_sha>"`, several in one
  turn. One call per file is not a reason to clone.
- **Clone fallback, only when needed**: a lot of files (order of magnitude > 15) or broad greps the search API
  can't express. Then a **warm clone at a fixed path** `<clones>/<repo>` — never `/tmp`, never a dated folder.
  First time `git clone --depth 1 <url> <clones>/<repo>`; per MR
  `git fetch --depth 1 origin <source-branch>` then check out `FETCH_HEAD`. If the base is missing in shallow
  mode, `git fetch --depth 50` and widen, rather than a full clone. Once that path exists the fetch is nearly
  free, which makes the fallback acceptable sooner.

## 2. Batching: cut the round trips
- Every tool call is a slow round trip. **Group them**: read what you need in parallel in one turn, never
  re-read a file you already read.
- **Batched searches**: `python3 <scratch>/search_blobs.py <ns/repo> <source-branch> term1 term2 term3 …`
  runs them all in parallel in ONE call and returns `path:line` plus context. Accumulate the terms and fire
  once; one call per term is the pattern to avoid.
- On a local clone, one multi-pattern grep (alternation `a|b|c`) rather than N greps.

## 3. Restricted scope: parallelised review
When the instruction hands you a ready dump (`<scratch>/mr<N>/` exists) **and** a scope (a list of files):
- Do **not** redo the prefetch; start from the dump.
- Review **only** the files in your scope. The rest of the diff belongs to a twin agent — you may read those
  files to understand or verify, but you produce **no finding** on them.
- Write your payloads to the file the instruction names (e.g. `<scratch>/mr<N>_payloads_a.json`), never into
  another scope's file.

## 4. Two modes, inferred from the instruction
- **REPORT (the default)** — and the default as soon as the instruction says "return / list / without posting /
  so I can validate". You post **nothing**. Your final message returns the complete list of findings, ordered
  (bugs first, then conventions, then reuse/architecture, then questions and uncertainties), each with file,
  line, a short description and the suggested fix where you have one. Don't censor yourself, including on the
  points you're unsure about. **On top of the report**, write the ready-to-post comments to
  `<scratch>/mr<N>_payloads.json`:
  ```json
  {"project": "<ns/repo>", "iid": 0, "comments": [{"path": "…", "line": 42, "body": "…"}]}
  ```
  so that a validation posts them without relaunching you:
  `python3 <scratch>/post_mr_comments.py --file <scratch>/mr<N>_payloads.json`. **Name that path at the end of
  your report** — a payload file nobody knows about is a report with a missing half.
- **POST** — only when the instruction explicitly says to post. You review **and** post the inline comments
  directly, without waiting for further agreement: whoever launched you already took that decision. You end
  with a recap of what was posted (`file:line` + subject).
- **When in doubt, REPORT.** On a stack where the reviewer's register is the question rather than the
  statement, stay in REPORT until told otherwise — learning questions should be filtered by a human before
  they appear publicly on someone's MR.

**Before posting from a payload file, re-read it.** A stale file from an earlier run posts duplicates, and its
line numbers are not necessarily the diff's `new_line`. Verify both against the current dump.

## 5. Existing discussions: read them before reviewing
They're already in the dump (`<scratch>/mr<N>/discussions.json`). Note each discussion's `id`, its author, the
file and line, and whether it's resolved.
- If one of your findings overlaps a comment someone already posted, **do not create a duplicate** — propose a
  **reply in that thread**, backing the remark with what you verified in the code.
- Ignore resolved threads, unless the point plainly isn't fixed, in which case say so.
- **REPORT**: list those replies in their own section, with the original author, the `file:line` and the
  proposed text.
- **POST**: reply in the thread —
  ```
  glab api --method POST -H "Content-Type: application/json" \
    "projects/<ns%2Frepo>/merge_requests/<N>/discussions/<discussion_id>/notes" \
    -f body="…"
  ```
A reply follows the same style as a comment, and counts as one in the final recap.

## 6. Posting inline: the four traps
Fetch the refs first: `glab api "projects/<ns%2Frepo>/merge_requests/<N>"` → `diff_refs` gives `base_sha`,
`start_sha`, `head_sha`. Then, per comment, a JSON payload:

```
glab api --method POST -H "Content-Type: application/json" \
  "projects/<ns%2Frepo>/merge_requests/<N>/discussions" --input comment.json
```

```json
{
  "body": "…",
  "position": {
    "base_sha": "…", "start_sha": "…", "head_sha": "…",
    "position_type": "text",
    "new_path": "path/file.ext", "old_path": "path/file.ext",
    "new_line": 42
  }
}
```

1. **The `Content-Type: application/json` header is mandatory** — without it, 415.
2. **Never use `-f position[...]` flags.** The nested fields go out flat, GitLab **silently ignores them**, and
   the comment lands as a general note with no error at all. Always a complete JSON payload through `--input`.
3. **Always check the response returns a non-null `notes[0].position`.** If it's null it went out as a general
   note: delete it (`DELETE …/notes/<id>`) and repost as JSON. Note that a `DELETE` through some helper
   wrappers hangs when no body is passed — send `{}`.
4. **An unmodified context line** (present in the hunk but not changed) fails with a 400
   `line_code can't be blank` when only `new_line` is given. Provide **both `old_line` and `new_line`** so
   GitLab can resolve the line code; read `old_line` from the hunk header (`@@ -old,+new @@`).

For an added line, `new_line` alone is right — to get the exact number, read the file from the source branch
and locate the anchor rather than counting hunk offsets by hand.

## Origin
Extracted 2026-08-06 from `boromir`, which held the canonical copy, after an audit found the same ~150 lines
duplicated across all six full review readers (`samwise` and `faramir` had already resorted to pointing at
`boromir`'s file, which is not a shared mechanism — an agent reading another agent's instructions inherits its
stack bias too). Every trap listed here was hit for real: the flat `position` flags, the general-note fallback,
the context-line 400, the stale payload file, the wrong default host.
