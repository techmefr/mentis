# social-publish-approval-gate-pitfalls §2 — Around the approval

## 2.1 Batches and irreversible actions
1. **One confirmation per batch action.** A bulk plan is validated in full first, then confirmed once with
   a summary table (social-media-skills, `scheduling-and-queue`, rules and edge cases).
2. **Publish-now and delete are irreversible; confirm each explicitly and separately** (same file).
3. **To change a scheduled post in a tool that cannot edit in place, the change is a delete and a new
   post**, so it needs both confirmations (same file, edge cases).

## 2.2 Time
1. **Pin the timezone before scheduling.** "9am" is ambiguous; "tomorrow" or "this evening" gets turned
   into an exact date, time and zone (same file).
2. **Show the offset in the preview** (part 1).

## 2.3 Validate first, then ask
1. **Check each post against the platform's constraints before asking for the confirmation**, and list
   every failure: unsupported media, length, missing fields (same file, validate step). Never ask a person
   to approve something that cannot be sent.
2. **Own guidance:** the platform constraints belong to the reference file of `business/social-publishing`,
   which says they change.

## 2.4 After sending
1. **Report exactly what happened:** which posts, to which accounts, for when, with the identifiers the
   tool returned (same file, results step).
2. **On failure, show the real error and do not retry blindly.** After a partial success, re-attempt only
   what failed; never repeat what went through (same file).

## 2.5 Pause the queue
1. **In a crisis or at a sensitive news moment, scheduled promotions can fire at the wrong time.** Pause
   or reschedule queued posts before they go out (social-media-skills, `crisis-and-moderation`,
   escalation reference).
2. **Confirm with the human which posts to hold and for how long**, using the same confirmation as for
   scheduling, and resume deliberately (same file).
3. **`business/social-publishing` already says to re-read scheduled posts.** This adds the pause as a named
   action.

## 2.6 No connection
1. **If the tool is not connected, produce a schedule table** (post, platform, date and time, timezone)
   for someone to act on, and say plainly that nothing was posted (same scheduling skill, connection step).
2. **A platform that is not connected is flagged, never skipped silently** (same file, edge cases).
