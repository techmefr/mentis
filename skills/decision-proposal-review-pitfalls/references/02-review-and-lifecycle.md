# decision-proposal-review-pitfalls §2 — Review and lifecycle

What to do to a proposal while others are reading it, and what its acceptance means afterwards.

## 2.1 History during review
1. **Do not squash or rebase once changes are visible to reviewers** (Rust, in bold in its text). Reviewers
   need to see what changed since they read it.
2. **Change by new commits and explain each change in a comment.** Rust notes that proposals rarely go
   through unchanged, especially once alternatives and drawbacks are shown.
3. **Be ready to revise.** Rust says a proposal gets design feedback from the wider community and its author
   should expect to change it in response.

## 2.2 Disagreement and size of edits
1. **Mark a live disagreement inline** instead of blocking the merge. Kubernetes wraps the disputed text in
   an "unresolved" marker with optional context or usernames, so the rest can be agreed.
2. **Merge early and iterate.** Kubernetes advises clarifying and merging the goals quickly, then adding
   detail in later small changes, rather than getting stuck on specifics.
3. **Keep edits small and single-topic**, so discussion stays focused; a reviewer who disagrees opens their
   own change with the suggested text (Kubernetes).
4. **One proposal per feature for its whole life.** Kubernetes says moving from beta to stable needs no new
   proposal, only an edit; major changes after the feature is implemented get a new one.

## 2.3 What acceptance means
1. **Accepted does not mean prioritised.** Rust says "active" implies nothing about priority and nothing
   about whether anyone is assigned.
2. **The author is not obliged to implement.** Rust says so, while noting that the author writing the
   implementation is by far the most effective path and that others should not be expected to take it up.
3. **Every accepted proposal gets a tracking item** that can be prioritised like other work (Rust).
4. **Do not change an accepted one substantially in place.** Rust: only very minor amendments, and
   substantial change goes in a new proposal with a note added to the original; the team decides what counts
   as minor. Own guidance: link both ways, and see `documentation-adr` for superseding.
5. **A proposal may not match the end result.** Rust says a merged proposal will not always reflect what is
   finally shipped; follow-up changes can update it.
