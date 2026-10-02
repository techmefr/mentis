# elixir-phoenix-conventions — origin and source stamps

> Provenance of `skills/elixir-phoenix-conventions`. Read it when a rule has to be traced back to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

Block created 2026-10-02, every rule from a document **read that day** (rule B: mechanisms rewritten in the
house voice, no prose copied). A fact not found in a read source was left out rather than recited.

| Source (public repository, read 2026-10-02) | Licence | Used for |
|---|---|---|
| Elixir anti-patterns pages, four of them: code-related, design-related, process-related, meta-programming (`elixir-lang/elixir`, anti-patterns pages, main branch) | Apache-2.0 (repository `LICENSE`, read) | §1 and §2. Rewrite with credit. |
| Phoenix guides (`phoenixframework/phoenix`, `guides/`, main branch): contexts, cross-context boundaries, API authentication, security, testing, testing contexts | MIT (repository `LICENSE.md`, read) | §3. Rewrite with credit. |
| Sobelow README (`nccgroup/sobelow`) and Credo README (`rrrene/credo`) | licence files not read | §3.14 states only what the READMEs say the tools are for. No rule rests on either. |

**Read but not used for rules:** the Phoenix LiveView, channels, deployment, telemetry and asset guides; the
Ecto documentation (its changeset and query pages were not read, so no rule on migrations or on Ecto query
performance is given here: `skills/sql-conventions` covers SQL in general); the Erlang Ecosystem Foundation's
security documents that the Phoenix security guide points to; the Elixir style guide and the process-related
pages of the OTP documentation. Left out: Nerves, umbrella applications, hot upgrades.

**Version stamp.** Elixir and Phoenix documents were read on their main branches and the pages do not carry a
version; the scope-based generators and the scope struct described in §3.4 are those of the current Phoenix
line, so a project on an older Phoenix reads §3.4 as "not yet". The 32-field boundary in §1.13 is a VM
property the page states for the VM version of the day. Expiry: at each Phoenix or Elixir major
(`skills/source-freshness` §2.1) re-read §3 first.

**Status.** 🟡, "base to confront with the real thing", like `go-conventions`. Nothing here was run against an
Elixir project.
