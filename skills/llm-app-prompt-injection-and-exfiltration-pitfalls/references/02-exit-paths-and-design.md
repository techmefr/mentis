# llm-app-prompt-injection-and-exfiltration-pitfalls §2 — Exit paths and design

## 2.1 Markdown images and links
1. **A rendered image is an outbound request carrying data.** The garak web-injection probes test whether a
   model writes a markdown image or link whose address includes conversation text, possibly encoded; the
   client fetches the image on display and the data arrives at the attacker's host with no click. Symptom:
   nothing odd in the chat, a request in someone else's logs.
2. **There are many spellings.** The garak detectors cover inline image and link forms and the reference
   style, where the address sits in a definition elsewhere in the text, and the probes build the address
   from pieces so no single string looks like a link. A check that matches one pattern misses the others.
3. **Close it where the data would leave:** do not render images or links from model text unless the host is on
   an allowlist you own; proxy or drop the rest; show links as inert text with the destination visible
   (own guidance). A content security policy that limits image and connect sources is the backstop, see
   `csp-and-sanitiser-pitfalls`.
4. **Query strings are the payload channel.** Drop or ignore parameters on allowed hosts where the feature does
   not need them (own guidance).

## 2.2 Links that run code
1. **A markdown link can carry a script scheme or an HTML fragment** that runs when the surface renders it. The
   garak probes include cross-site-scripting tasks and markdown-link variants for this. Fix: render model
   output through a sanitiser that allows a short list of schemes and tags, as for any user-supplied markup
   (`csp-and-sanitiser-pitfalls`).
2. **Model output is user input to everything downstream.** Symptom: a generated string reaches a shell, a SQL
   statement, a template, a file path or an API call unchanged. Fix: validate against a schema, parameterise,
   and apply the same escaping as for text typed by a stranger (own guidance).

## 2.3 What the model can reveal
1. **The system prompt will be extracted.** garak includes a probe that combines collected system prompts with
   extraction techniques and checks whether the model gives it up. Put nothing in it you could not publish:
   keys, internal hostnames, rules that rely on secrecy.
2. **Private data in context can be asked for.** Symptom: one user's record appears for another. Fix: retrieve
   only what the current user may see (`rag-retrieval-quality-pitfalls` §1.2); never rely on an instruction
   to withhold text that is already in the prompt.
3. **Scan output for sensitive values** (personal data, secrets) as a last layer. llm-guard has output scanners
   for sensitive entities and for secrets in input, and a vault that swaps placeholders back into the answer;
   that swap-back reintroduces the values, so apply it only after the output checks and only for the user
   who owns them (own guidance).

## 2.4 Tools and authority
1. **Give the model the least capability that serves the task.** A summariser needs no send, write or delete
   tool; a tool that fetches a URL is an outbound channel. Split into steps with different tool sets
   rather than one session with everything (own guidance, in line with the toxic-flow advice in
   `agent-mcp-trust-pitfalls` §3).
2. **Authority is carried by the session of the user, not by text.** A tool call that came after reading
   outside text runs with the rights of the asker at most, and the application checks them, not the model.
3. **Put a person in front of the irreversible step,** showing the real payload and destination, as the toxic
   flow guidance advises. A confirmation that displays the model's description of the action instead of the
   action itself fails.
4. **Bound the damage:** rate limits per user on tool calls, size limits on outbound payloads, and logs of
   what text was read before each action so a leak can be traced (`secret-leak-response-pitfalls`).

## 2.5 Order of defences
1. **Remove the capability first** (no outbound tool, no remote render), then **gate it**, then **filter**.
   Filters (§3.3) come last because they can be bypassed by rephrasing and by encodings the filter was not
   trained on (the garak documentation says the same of guardrails and hidden characters).
2. **Write the residual risk down.** If the product keeps a risky combination on purpose, record who accepted
   it, what monitors it and when it is re-tested.
