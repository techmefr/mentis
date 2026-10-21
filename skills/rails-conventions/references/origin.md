# rails-conventions — origin and source stamps

> Provenance of `skills/rails-conventions`. Read it when a rule has to be traced back to its source or checked
> for freshness (`skills/source-freshness`), never to apply a rule.

Block created 2026-10-02, every rule from a document **read that day** (rule B: mechanisms rewritten in the
house voice, no prose copied). A fact not found in a read source was left out rather than recited.

| Source (public repository, read 2026-10-02) | Licence | Used for |
|---|---|---|
| The community Rails style guide (`rubocop/rails-style-guide`) | CC BY 3.0, stated in its README | §1 routing and controllers, §2 models and queries, §3 migrations, §4 config/time/i18n/mail, §6 testing points. Rewrite with credit. |
| The community Ruby style guide (`rubocop/ruby-style-guide`) | CC BY 3.0, stated in its README; headings read in full, the sections cited read | §6 Ruby judgment calls only; the formatting chapters deliberately left to the linter. Rewrite with credit. |
| The rubocop-rails cop reference (`rubocop/rubocop-rails`) | MIT | The cop descriptions behind §1 to §4 and §6 (flash before render, after_commit override, transaction exit, unique validation without index, not-null column, add_column index key, default scope, env access, output safety). Rewrite with credit. |
| The Rails guides (security, action controller, active record querying, migrations, active job, testing, configuring), `main` branch, examples showing 8.x | Code MIT; the guides are CC BY-SA 4.0 | **Idea only**: mechanisms and facts restated in our own words (strong parameters `expect`, N+1 and `strict_loading`, `enqueue_after_transaction_commit`, session fixation, forgery, uploads, headers, credentials). No sentence reproduced. |
| PostgreSQL documentation for `CREATE INDEX` (the `postgres/postgres` repository) | PostgreSQL licence (permissive) | §3.10: concurrent index build, invalid index, no transaction block. |

**Verification pass 2026-10-20.** Re-opened: the community Rails style guide README (CC BY 3.0, licence line
re-read), the rubocop-rails cop reference and one cop source (MIT, `LICENSE.txt` re-read, copyright holder
named there), and the Rails API reference for strong parameters, Active Job enqueuing, retries, transactions,
`where` chain, redirecting, strict loading and application configuration (framework code under MIT; the API pages
read for facts only). The share-alike guides were not re-opened. Confirmed: §1.1 to §1.3 and §1.4 (skinny
controllers, one method, few instance variables), §1.6 (`expect` is type-strict and raises `ParameterMissing`),
§1.7 (cop), §1.9, §1.11 (cop), §2.4 to §2.6, §2.8 to §2.9, §2.11 to §2.13 (callback dedup by method name),
§2.15 to §2.20, §2.22 to §2.24, §3.3, §3.4, §3.6 (cops), §3.8, §4.1, §4.2, §4.5 (`Rails.env.local?`, cop marker
7.1), §4.6, §4.7, §4.8 (the `enqueue_after_transaction_commit` switch, a boolean class attribute), §4.10 (retry
defaults). Corrected: §2.21 (`where.not` with several attributes is a negated AND since 6.1, the block had the
direction reversed), §2.14 (the exit-statement rollback exists only on 7.0 and 7.1; 7.2 restored commit, per the
cop source note and the 7.2 changelog), §1.8 (`redirect_back_or_to` follows the referer cross-host unless
`allow_other_host: false`), §4.10 (the documented backoff name is `:polynomially_longer`; the page lists no
`:exponentially_longer`). Not found on any page read, so unverified: `prepend: true` for a vetoing
`before_destroy` (§2.13), the `strict_loading_by_default` / `:log` action (§2.26), `config_for` and the
"keeps the defaults of the version it started on" statement (§4.1, §4.3), the claim that a job with no
`retry_on` goes straight to failed on the database queue (§4.10), global id serialisation and the
deserialisation error (§4.9), `deliver_later` advice (§4.11), the `safe_join`/`concat` advice (§1.11),
`inverse_of` guidance beyond the cop, `exists?` advice (§2.19), `add_column` and `change_table bulk` version
details (§3.6). Sections 5 and 6 were not re-opened in this pass.

**Read but not used as a source of rules:** Brakeman's licence is restrictive (the veille marks it idea-only) and
its documentation was not read; the OWASP Ruby on Rails cheat sheet (CC BY-SA) was not read; the thoughtbot guides
(no licence) were not read. The Rails guides' sections on views, Action Cable, Active Storage and caching were not
read: no rule is claimed for them.

**Version stamp.** Rails guides at `main` (examples in the migrations guide use `Migration[8.2]`), style guide as fetched on
2026-10-02, cop reference with `Requires Rails version 8.0` markers read as such. Expiry: when the
project's Rails major changes (`skills/source-freshness` §2.1), re-read §1.6 (strong parameters), §4.8 to §4.10
(jobs) and §6 first: they are the fastest-moving.

**Status.** 🟡, "base to confront with the real thing", like `go-conventions` for a technology new to the repo.
Nothing here was run against a Rails project; the checkpoint depends on RuboCop being present in that project.
