# session-retro §1 — Find the struggles

> Section 1 of `skills/session-retro`. The classification and the destinations are §2.

## 1.1 What is read
1. **The record of the session the operator names; the current one when none is named.** Read the primary
   record, not a summary of it: the struggles are exactly what a summary drops.
2. **A long or already-compacted session is read from its stored record**, not from the agent's memory of it.
   Own guidance: what the agent remembers of the middle of a long session is the part most likely to be smoothed
   over.

## 1.2 The seven categories
Look for one candidate per moment, in these categories. Each has the situation that makes it worth looking.

| Category | Question asked of the session | Worth looking when |
|---|---|---|
| Navigation | How easy was it to find the right files? Is there a hidden dependency between files a pointer would expose? | finding one fact took a long time |
| Automated checks | Which mistake could a lint, a type, a test or a hook have caught? | the agent made such a mistake, or the repository has no guardrail at all |
| Coding standards | Should the reviewer be given a new rule, or an existing one clarified or removed? | the reviewer missed a mistake |
| Steering-file size | Is some instruction in a steering file better placed in the standards or turned into a check? | a steering file, in the repository or the operator's global scope, is large |
| Tool economy | Was there an expensive tool call, or a custom tool that returns far more than it is asked for? | one call cost much for what it gave |
| No-ops | Which lines of a steering file change no behaviour? | the steering files are large and unwieldy |
| Information access | Which fact was out of the agent's reach (a server log, a read-only view of a service)? | a crucial fact was missing |

1. **Read the repository's own check command and its CI workflow first** (the scripts the build tool exposes for
   lint and type-check, and the pipeline definition), so that the finding for the "automated checks" category is
   "this check exists and is not wired" or "is broken" when that is the truth.
2. **A repository with no guardrail at all** (no pre-commit hook and no CI job that runs lint, type-check and
   tests) is a finding on its own, not a neutral default.

## 1.3 The discipline on candidates
1. **Each candidate points to the moment it came from.** A candidate that could have been written without reading
   the session is discarded.
2. **The categories are a prompt for looking, not a quota.** A category with no moment behind it is left empty;
   padding it is how the generic advice gets in.
3. **Order by severity, as a first draft.** Own guidance: a quiet expensive mistake can rank below a loud cheap
   one, so the operator's judgement of the order replaces yours.
