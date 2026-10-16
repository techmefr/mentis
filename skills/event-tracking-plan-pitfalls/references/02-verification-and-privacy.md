# event-tracking-plan-pitfalls §2 — Approval, verification and privacy

A plan fails after it is written: the wrong account is selected, a plan nobody approved is generated, a preview
is misread, or free text is captured with nobody having decided what it contains.

## 2.1 No automatic choices, explicit approval
1. **Never auto-pick the account, the container or the workspace.** At each selection step show the options and
   wait for the person's explicit answer. A matching domain, an environment name or one option that "looks like
   production" is not a reason to choose (jtrackingai, vendor).
2. **After an interrupted or wrong selection, redo it and confirm each step again** before going on
   (jtrackingai).
3. **The plan is approved as a whole, including its properties.** The reviewer sees the events and the full
   property list of each, because names, values and descriptions often need adjusting. A request such as "do the
   whole workflow" is not approval of the schema, and the approval is not recorded on the person's behalf
   unless they confirm in that turn (jtrackingai).
4. **Nothing downstream starts before approval**: no configuration generated, no synchronisation, no preview, no
   publish (jtrackingai).
5. **Where a live baseline exists, the review says** which existing events are reused, which gaps are filled,
   which current problems the plan fixes and what it gains (jtrackingai).

## 2.2 Reading a preview
1. **A preview that saw no hit is not automatically a broken configuration.** Three false negatives are named by
   the source: a same-origin single-page link that fires its event only after the router changes, a root URL
   with and without a trailing slash treated as two pages, and external, new-tab or mail links that need
   preview-safe handling to avoid losing the browser context (jtrackingai).
2. **Check manual preview or the tag assistant before rewriting a trigger**, especially on navigation-heavy sites
   (jtrackingai).
3. **Classify every miss** as one of three, in the source's report template: a selector problem (not found, too
   broad or ambiguous), a runtime problem (the interaction happened and the event really did not fire), or a
   preview limitation (it fires in manual preview but automated preview did not attribute it).
4. **Known expected failures** are named, not hidden: the source gives a form behind a challenge or a login that
   an automated browser cannot submit.
5. **Rule out the environment first**: a browser that cannot run or reach the network produces hangs and empty
   results that look like configuration faults (jtrackingai).
6. **A selector that matches nothing is fixed in the plan** and the configuration regenerated, not patched by
   hand in the tag manager (jtrackingai's troubleshooting steps). That the corrected plan goes back through
   the approval is own guidance.

## 2.3 The gate before publish
1. **A release decision comes from the verification**: blockers, expected failures, selector mismatches,
   unexpected events outside the approved plan, and an overall readiness verdict (jtrackingai).
2. **Publish stops by default when the health report is missing, manual-only or has blockers**; overriding it
   needs the person's explicit request (jtrackingai).
3. **High-priority events that are still real conversion entry points block**; events that are no longer live
   entry points or are out of scope are taken out of the decision, and the rest is reassessed (jtrackingai's
   report guidance).
4. **Publishing is its own request.** Stopping after the QA verdict when only QA was asked is the source's
   default.

## 2.4 QA checklist
1. **Per event**: where to go, what to do, and which properties to check (product-on-purpose).
2. **Per property**: its type, when it must be present and its allowed range.
3. **Edge cases**: a slow network, a session timeout and re-login, a page refresh mid-flow, events that must not
   fire when a condition holds, and no duplicate event when the user navigates back and forward
   (product-on-purpose's worked example).
4. **Say how to see the event stream** in the product's debug tool so QA has a way to check (product-on-purpose).

## 2.5 Personal data
1. **Flag every property that holds personal data** and write what happens to it: hashed, encrypted or not sent
   (product-on-purpose).
2. **Record consent requirements and retention** in the same section.

## 2.6 Traces of model inputs and outputs
This applies whenever any model input, output, retrieval context or tool call is captured, whoever wrote the
text. A feature with no direct user input can still write a customer's document into a trace store
(product-on-purpose). A trace is not an event: an event holds properties chosen in advance, a trace holds free
text that can contain anything.
1. **Name the data classes**: user text, retrieved documents, system prompt, tool arguments and results, file
   contents, model output. "The trace" is not an answer.
2. **Minimise at both boundaries**: what is dropped or masked before the trace leaves the process, and
   separately before it is stored. A redactor that only runs at storage has already sent the raw text out.
3. **Decide what happens when minimisation fails**: fail closed, drop the trace or block the request; never
   send or write it raw. Anything that buffers or replays a failed trace is itself a durable sink and needs the
   same controls.
4. **Access**: who can read traces, how that grant is removed when someone leaves, and whether reads are logged.
   "Every read is recorded" and "the record names the reader" are two separate claims that fail independently.
5. **Retention and deletion**: how long, what deletes them, and how a deletion request reaches a trace copied
   into an evaluation set.
6. **Consent and opt-out**: whether the subject agreed and what the feature does when they decline.
7. **Sampling**: the fraction captured and how it is chosen. A uniform sample is a poor instrument for finding
   rare failures; oversample the cases a check already flagged and say so.
8. **Every claim needs a test that could fail**, on a normal path and on a failure path, and the test must show
   the pipeline was exercised, so "nothing forbidden found" cannot be satisfied by nothing captured
   (product-on-purpose's template).
