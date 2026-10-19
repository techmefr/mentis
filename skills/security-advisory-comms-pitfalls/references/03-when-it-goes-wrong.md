# security-advisory-comms-pitfalls §3 — When it goes wrong

The failure this section prevents is a plan that only works if everything goes to schedule.

## 3.1 The fix is not ready when the embargo ends
1. **Get more help first**: a contributor who knows the area, a specialist, colleagues in a response team.
2. **Release the partial fix that breaks the exploitation chain**, meaning one that makes the exploit much
   harder, rather than nothing, and keep working on the full one.
3. **Say plainly that the fix is partial**, and what exposure remains, so users understand their risk after
   patching.
4. **Update the earlier announcements** to point to the latest information when the full fix lands, for
   example a line in the later release notes naming the identifier.

## 3.2 No fix is possible
1. **Disclose with workarounds.** The guide says users are better off knowing, and that obscurity is a weak
   defence because any existing flaw can be found.
2. **Document it well, including workarounds for common environments, and keep working on it in public.**

## 3.3 It was disclosed without you
1. **Treat it as a high-priority public issue**, since it already is one.
2. **Tell users you are aware, how it is being handled and where updates will appear.** The guide notes that
   handling it in public lowers the communication burden, because people find the answer instead of writing to
   you.

## 3.4 The reporter has gone quiet
1. **Try more than once to reach them.** If you cannot reproduce the issue, send one polite final note saying
   so and that you will not issue an advisory.
2. **Invite them to reopen** if they can reproduce it later.

## 3.5 Exploitation in the wild
1. **Notify users and release remedies quickly.** The guide says it intends to add resources on this and gives
   little detail; the rest of this block applies with less time. Do not invent a separate procedure here.
2. **Regulatory reporting duties are not covered.** Whether any applies to you is a question for your legal
   owner; nothing in this block says that one does or does not.
