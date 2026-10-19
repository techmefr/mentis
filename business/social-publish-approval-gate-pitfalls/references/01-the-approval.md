# social-publish-approval-gate-pitfalls §1 — The approval

An approval is only worth the precision of what it was shown.

## 1.1 What the person is shown
1. **An exact, fully specified action:** the target account, the final content in full, the schedule time,
   and the media and link details. The source's preview prints exactly these, plus the action name
   (samalyxx socialbu skills, `lib/approval.py`, the preview method).
2. **The time has an explicit offset.** The source rejects a scheduled action whose time has no UTC offset,
   and rejects a publish-now action that carries a time at all.
3. **Show the preview, not a summary of it.** The scheduling skill of the second source lists what, where,
   when and how many (social-media-skills, `scheduling-and-queue`, confirm step).
4. **Own guidance:** if the preview cannot be produced in full, the approval cannot be asked for yet.

## 1.2 The approval belongs to that content
1. **Tie the approval to a fingerprint of the action.** The source hashes the action, target, content,
   time and media together, and refuses to consume the approval if the hash differs at send time
   (`approval.py`, the consume method). The idea carries without the code.
2. **Any change after the yes voids the yes:** content, target, time or media. Ask again with the new
   preview.
3. **Own guidance:** a typo fix is a change. So is a link whose address was altered by a tool.

## 1.3 Expiry, single use, exact text
1. **An approval expires.** The source uses 15 minutes; that is its own choice and not a standard. Pick a
   window and state it (`approval.py`, the gate constructor).
2. **An approval is used once.** After it is consumed, a second use is refused (same file).
3. **The confirmation is an exact string**, tied to the request, not a loose "ok". The source asks the
   person to repeat a phrase containing a one-time token and rejects anything else.
4. **The approval does not publish.** In the source, preparing or confirming only produces a permit; a
   separate, authorised connector does the sending (module docstring). Keep approval and execution
   apart.
5. **A yes is for this action only**; it never covers later ones (social-media-skills, confirm step).
