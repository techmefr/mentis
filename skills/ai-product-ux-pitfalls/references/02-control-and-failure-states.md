# ai-product-ux-pitfalls §2 — Control and failure states

All points in this file are own guidance.

## 2.1 Control
1. **Editing must be cheaper than redoing.** Symptom: users regenerate five times or copy the text into another
   tool. Fix: edit in place, regenerate one part, and keep previous versions one click away.
2. **Every automatic action has an undo or a preview.** A change applied across many records needs a dry run
   and a way to revert the whole batch; see `agent-run-limits-and-guardrail-pitfalls` for gating agent actions.
3. **The human gate lands where the harm lands.** Approval of "send" is useful; approval of fifty small
   intermediate steps trains people to click through. Gate the irreversible step, and make that screen
   show exactly what will happen.
4. **Let the person override and say why** in one tap (wrong, outdated, not relevant, unsafe). The override is
   data for the team (§3), not a failure of the user.
5. **Keep the manual path.** A form the model autofills stays editable and submittable without the model.

## 2.2 Waiting
1. **Streaming shows progress but also half-formed answers.** Symptom: users act on the start of a response that
   later changes. Fix: stream text, but enable actions (copy, send, apply) only when the response is complete; let
   the person stop it.
2. **Long tasks need steps, not a spinner.** Show what is happening (searching, reading, drafting), allow
   cancel, and say what happens to partial work.
3. **Time out visibly.** After the budget set in the design, show what failed and the options, rather than an
   endless spinner. Timeouts and retry limits are in `llm-cost-latency-control-pitfalls`.

## 2.3 Failure states, each designed
1. **Slow:** progress, cancel, and the manual path.
2. **Wrong:** a report button next to the output, and the corrected value stays corrected in the session.
3. **Refused:** say it was refused, whether the cause is policy or capability, and what to try; never show a raw
   provider error.
4. **Empty or irrelevant:** suggest rephrasing, show what was searched, offer a person or the search page.
5. **Down or rate-limited:** a plain message, the manual path, and no loss of what the person typed.
6. **Partial:** if a batch half-succeeded, list what did and did not, and let the person retry the rest.

## 2.4 Feedback that arrives
1. **A thumbs-up with no context is low value.** Capture the output, its inputs and the version of the prompt and
   model (`prompt-versioning-and-change-gating-pitfalls`), with consent and minimisation
   (`llm-pii-and-data-handling-pitfalls`).
2. **Feedback needs an owner and a loop.** A weekly read, a route into the evaluation set
   (`llm-eval-regression-pitfalls`) and a visible fix; otherwise people stop giving it.

## 2.5 Checks
1. Each consequential action has undo or preview, and an approval on the irreversible step only.
2. Actions are disabled until streaming ends.
3. The six failure states in §2.3 each have a screen that leaves the task doable.
4. Feedback records carry versions and reach a named reader.
