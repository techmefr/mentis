# § 1 — Errors: say what happened, and what to do now

> Section 1 of `business/ux-writing`. Read it when a diff adds or changes an error message, a validation
> message, or any text shown on a failure path.

1. **Name what went wrong in the user's terms**, not the system's. "Request failed with status 422" is
   a log line, not a message. The status code is the one part of it the reader cannot act on, and it is
   the part that ends up pasted into a support conversation instead of the description of what they were
   doing — so the ticket arrives with no reproduction and the code has to be traced back to a rule.
2. **Every error gives a next action.** If there's nothing the user can do, say who can, or that it's
   been reported. A dead end with no route forward is what turns an error into a support call. The
   default behaviour with no stated action is to reload the whole application, which discards anything
   unsaved elsewhere on the screen, and then to try the same thing again in case it works.
3. **Never blame the user.** "Invalid input" for a date typed in a format you didn't accept is our
   parser's problem stated as the user's failing. The practical consequence is not offence, it is that
   the message contains no information: the reader retypes the same value because nothing told them
   which part was unacceptable.
4. **Be specific about which field and why.** "Some fields are invalid" makes the user hunt. On a long
   form the hunt usually ends in abandonment, and where the message appears at the top of the page a
   keyboard or screen-reader user has no way to reach the offending field at all
   (`skills/accessibility`).
5. **Don't leak internals**: stack traces, table names, internal ids. That's a security habit as much
   as a writing one (`skills/security-hardening`). What leaks is not only the string: an error naming a
   table, a class or a framework hands an attacker the stack and the schema for free, and the version in
   the message is what a scanner matches against a known advisory.
6. **A validation message names the rule, not the verdict.** "Password too weak" cannot be satisfied
   without guessing; the rule that was broken can be. State it before the attempt where you can, and
   after it in the same words — a requirement that only appears on failure is a requirement the reader
   discovers by failing.
7. **Say what happened to the reader's work.** After a failed save the reader's first question is
   whether their input survived, and the message is the only thing that can answer it. Silence on that
   point is read as loss, so the careful ones retype from scratch and the rest leave.
8. **Distinguish "you cannot" from "it did not work".** A permission failure is not retryable and a
   network failure is; presenting them identically means somebody spends ten minutes retrying something
   they will never be allowed to do. Where the distinction itself is sensitive — whether a record exists
   at all — that is a security decision made deliberately, not by wording accident.
9. **A message the reader cannot keep is a message they will need again.** A toast carrying the only
   copy of a reference number or a failure detail is gone before it can be written down, and the support
   conversation then has nothing in it (`business/interface-design` §2.1). Anything a reader might have
   to quote belongs somewhere that persists.
10. **One failure, one message.** Several messages for one cause — a field error, a banner and a toast
    all firing together — reads as several problems, and the reader starts fixing things that were never
    wrong. Where a single cause has several consequences, the message names the cause once and lists
    them.
11. **Never let humour into an error path.** The person reading it is already having a problem, and the
    joke is read as the product not taking their situation seriously — which is exactly the sentence that
    gets screenshotted. The same string also has to survive translation and a reader whose first language
    it is not, which a joke rarely does.
12. **A generic fallback message is still written on purpose.** Every application ends up with a
    catch-all for the unforeseen, and shipping the framework's default text there is a decision made by
    omission. Write it: say that something unexpected failed, that it was reported, and what the reader
    can do next — and give it a reference the reader can quote, which is what makes the fallback usable
    rather than merely polite.
