# agent-sandbox-egress-pitfalls §4 — Generated code

## 4.1 Executing code a model wrote
1. **Running model-written code is risky even without an attacker.** The smolagents guide lists plain model
   error, a compromised model, prompt injection from a page the agent browses, and misuse of publicly exposed
   agents. By default its code agent runs the generated code in your environment.
2. **A restricted local interpreter is not a sandbox.** Its local executor disallows imports unless
   authorised, disables submodule access unless authorised, caps operation counts and rejects undefined
   operations, yet the guide says no local Python sandbox can be completely secure and that the only way to
   get robust isolation is remote execution such as E2B or Docker.
3. **Authorise imports one by one.** The guide notes that harmless-looking packages can expose harmful
   submodules (its example reaches `os` through `random`), and that an allowed imaging library could be used
   to fill the disk.

## 4.2 Where to run it
1. **Two approaches, with a trade-off the guide states.** Running only the code snippets in a sandbox is
   simpler, keeps API keys out of the sandbox and protects the local environment, but does not support
   multi-agent setups and still passes state across. Running the whole agentic system in a sandbox isolates
   more and supports multi-agent, but needs more setup and may need sensitive credentials inside.
2. **Choose by threat, not by convenience** (own guidance): where the agent loops over generated code and
   needs keys inside, give the sandbox a scoped, short-lived credential and no ambient one.
3. **The guide's sandbox options** are Blaxel, E2B, Modal and Docker; its Docker example drops all
   capabilities, sets no-new-privileges, limits memory, CPU and process count and runs as an unprivileged user.

## 4.3 Limits and cleanup
1. **The guide's best practices:** set memory and CPU limits, execution timeouts and resource monitoring; run
   with minimal privileges; disable unnecessary network access; pass secrets through environment variables
   only as needed; keep dependencies minimal with fixed versions; update base images; always clean up
   containers.
2. **Treat files that come out as untrusted** (own guidance): output written by sandboxed code is read by
   something else later; inspect it as you would an upload.
