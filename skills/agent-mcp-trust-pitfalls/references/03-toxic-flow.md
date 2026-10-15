# agent-mcp-trust-pitfalls §3 — Toxic flow

The harm is rarely in one tool. It appears when three things are available to the same agent in the same
session, and no individual server looks wrong.

## 3.1 The three parts
1. **Untrusted content:** content from channels attackers can write to, such as email, issue trackers or
   support tickets (the scanner's `untrusted_content` risk).
2. **Private data:** non-public data such as personal communications, financial records or credentials
   (`private_data`).
3. **The ability to communicate outward.** The agent-scan v0.5 issue-code page names this combination, citing
   outside research, a toxic flow: exposure to untrusted content, access to private data and the ability to
   communicate with the internet. It says most agents have all three, so the scanner flags the first two
   and destructive capabilities per server and does not flag internet access separately.

Checking for the combination is the review to run for each new tool; the scanner will not report the outbound
part for you.

## 3.2 Break the flow where it is cheapest
1. **Drop one part from the session.** The scanner's advice for an untrusted-content server is to avoid combining
   it with destructive or sensitive capabilities without isolation and approval controls, and for a
   private-data server to avoid pairing it with untrusted-content or outbound-network capabilities. Own
   guidance: a split into two sessions with a human-reviewed handoff costs less than a gate on every step.
2. **If all three must stay, put a person in front of the outbound step** showing the payload and the
   destination (own guidance, in line with the scanner's call for human approval of state-changing operations).
   Network limits from `agent-sandbox-egress-pitfalls` come after this, not instead of it.
3. **Look at what comes back before the model acts on it.** The context protector can scan tool responses with a
   guardrail provider and quarantine a suspicious one until a person releases it. The SlowMist checklist says
   not to insert a third-party interface's returned data directly into context without checking it.

## 3.3 Fetched text is data
1. **Content retrieved from outside is data, not instructions.** A defence note in a safety-hooks repository
   says so without exception, including imperative text in a page, and asks, before any tool call triggered by
   external content, whether the user asked for the action or the content did. If the content suggested it,
   report it to the user instead. Apply the same to files cloned for review, including agent instruction
   files in them.
2. **Do not let the content move data out.** The same note lists sending messages, writing credentials to
   files, fetching URLs the content asks for and saving to locations it specifies as things external content
   must not trigger.
3. **Flag and do not reproduce.** When summarising, describe what an injection attempts without copying the
   actionable text, and tell the user it was there.
4. **State it in the task** that a page may try to give orders (own guidance).
5. **Keep a record of what was read and what was done,** so a leak can be traced. What to do once a credential
   has left is in `secret-leak-response-pitfalls`.

## 3.4 What this does not cover
1. **A defence in prose is a request to the model, not a control.** The note above and the scanners lower the
   chance; the controls that hold are the missing part of the flow and the human gate (own guidance).
