# decision-proposal-review-pitfalls §1 — Process and stages

A proposal process is a set of stages with a named exit for each. These rules make the stages visible, so
nobody has to guess. For the record of the final decision see `documentation-adr`.

## 1.1 Before writing
1. **Socialise the idea first.** The Rust RFC process warns that a hastily proposed RFC can hurt its own
   chances: low quality proposals, ones for previously rejected ideas and ones that do not fit the near-term
   plan can be rejected quickly, which is demotivating for an unprepared author.
2. **Get feedback from long-standing contributors beforehand**, in the project's chat, forum or a
   "pre-proposal" post. Encouraging feedback from people on the relevant team is a rule of thumb that it is
   worth continuing (Rust).
3. **Know what needs a proposal and what does not.** Rust lists "substantial" changes as needing one and
   says reorganising without changing meaning, or changes only noticed by the project's own developers, do
   not. What counts as substantial is each team's call; own guidance: write the threshold down.
4. **A sponsor is required.** Kubernetes' template says an enhancement proposal should not be checked in
   without a sponsoring group that wants the problem.

## 1.2 Stages made explicit
1. **Name each stage and who may move a proposal out of it.** Kubernetes requires that moving a proposal to
   its "implementable" status, or significantly changing it afterwards, is approved by every named approver.
2. **A merged proposal is not an approved one by default.** Kubernetes says a merged proposal is not
   complete or approved, and a "provisional" one is a working document. Rust calls a merged one "active".
   Define what your own word means.
3. **Discussion happens in the proposal's thread.** Rust asks that offline discussion be summarised back on
   the pull request, and that when the reasoning of a decision is not clear from the thread, the team adds a
   comment giving the rationale.

## 1.3 The final comment period
1. **Open the last stage with a stated disposition**: merge, close or postpone (Rust). Do it when the
   trade-offs have been discussed and the argument for the disposition has been laid out; it does not need
   consensus among all participants, which is usually impossible, and there should not be strong consensus
   against it outside the deciding team.
2. **Precede it by a summary comment** when the discussion is long: the current state, the main trade-offs
   and the open disagreements (Rust).
3. **All team members sign off before the period opens**; Rust notes this is often the first time many of
   them read the proposal in depth.
4. **Make the period long enough to object.** Rust uses ten calendar days so that at least five business
   days are open, and advertises it widely. Both numbers are one project's choice, an example.
5. **A substantial new argument cancels the period** and returns the proposal to development (Rust).
6. **Merge or close at the end, with a reason.** The usual outcome is quiet.

## 1.4 Postponed is not closed
1. **"Postponed" means: not now, and not evaluated now.** Rust uses it when the project neither wants to
   think about evaluating nor implementing the idea until later and can afford to wait.
2. **If the answer to "would we ever consider this" is no, close it.** Rust says closing, not postponing, is
   the right response then. Using postponed to avoid saying no leaves a zombie proposal.
3. **Say how a postponed one comes back.** Rust has no formal process and tells authors to ask the team; own
   guidance: state it, or the proposal is effectively dead.
