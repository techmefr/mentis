# security-hardening §12 — Auditing an AI-generated or scaffolded app

> Section 12 of `skills/security-hardening`, and the checklist `agents/seraph` follows when the repo was built
> mostly by a coding assistant or a scaffold. Read it when the audit target looks finished, runs, and was
> produced fast. The depth for each item stays in the blocks it points to; this is the order of looking and the
> reporting discipline.

1. **The failure set is small and repeated.** An assistant optimises for the demo: it inlines the key so the
   example runs, leaves the data store open because the happy path worked, and concatenates the user's text into
   the prompt because the tutorial did. Look for these first, name each as a scaffold default rather than blame,
   and do not report a generic "possible issue" in place of a located one.
2. **Secret reachable by the client.** Check variables with a client-exposed prefix (the framework's "public"
   convention), keys compiled into the shipped bundle, and any privileged service key imported where client code
   can reach it. **Symptom:** a provider key in a browser-visible variable. **Fix:** move the call behind a
   server route and use a server-only variable (`skills/react-nextjs-conventions` §9, `skills/react-native-expo-pitfalls` §2).
3. **Separate the secret from the designed-to-be-public.** A publishable or anonymous client key is meant to be
   in the browser; flagging it teaches people to ignore the report. **Check:** read the provider's description of
   the key before classing it; if the safety of the key depends on a data-store rule, the finding is the rule
   (item 5), not the key.
4. **A leaked secret is finished only with a rotation step.** Deleting it from the file does not un-leak it, and
   history keeps it. Every such finding names the provider-side rotation and the secrets that probably travelled
   with it, since an assistant that inlined one key often inlined others (`skills/secret-leak-response-pitfalls`). Report
   the type, the place and a redacted preview, never the value.
5. **"Access rules on" is a claim to verify.** A table with row-level rules enabled and no policy denies everyone;
   one with an allow-all policy admits everyone; a table with the rules off is open to anyone holding the public
   key; a storage bucket can be world-readable; a policy can test a role string the user controls instead of the
   authenticated identity. **Check:** read the migrations, not the dashboard summary. **Fix:** a policy scoped to
   the authenticated user's identity (`skills/postgres-operations-and-exposed-api-pitfalls`).
6. **No authorisation from a client-editable field.** In several managed auth services a signed-in user can edit
   their own profile metadata through the public auth interface, so a role read from it can be self-granted;
   privileged logic reads the server-only counterpart. **Re-read before relying:** which metadata field is
   user-editable depends on the provider and version; confirm in its current documentation
   (`skills/source-freshness`). Applies equally to a role in the request body or a header the client sets.
7. **Backend functions and routes with no auth check.** Edge or serverless handlers scaffolded for the demo often
   answer anyone. **Check:** every handler either authenticates or is listed as public on purpose
   (`skills/security-hardening` §3).
8. **Untrusted input reaching a model's instructions: rate by position.** Trace request input from source to
   the model call. Lowest risk: the text in its own user-role message, no tools. Higher: concatenated into the
   system prompt or into a single instruction string with no role boundary. Highest: any call that also grants
   tools or actions, since a successful injection then performs something (excessive agency) rather than only
   saying something. The heuristic is conservative on purpose: an ambiguous flow gets a labelled low-confidence
   note or silence, and the documented-safe pattern is never reported (`skills/llm-app-prompt-injection-and-exfiltration-pitfalls`).
9. **Permissions live in code, not in the prompt.** An instruction in a system prompt is not an access control; a
   tool that can move money, delete or send needs a server-side check and a confirmation step of its own.
10. **Severity by what an attacker gets, in order.** Secret or privileged key reachable, open data store,
    model-with-tools fed from the request, no-auth handler, then the rest. Say each in plain language before the
    standard identifier: who can do what, from where.
11. **Be honest about coverage.** State what was read, what could not be read (an encrypted config, a dashboard
    setting not in the repo) and the confidence of each heuristic finding. Never give a compliance statement or a
    "percent secure" figure; give the denominator of what was checked.
12. **A rescan is the only proof of a fix.** Key every finding to a stable fingerprint (rule, file, normalised
    snippet), re-run after the change and report three lists: resolved, still present, newly introduced. A fix
    not rescanned is a claim, not a result (`skills/gate`, claims and proof). The audit itself writes nothing;
    the fixes go through the normal pipeline.
