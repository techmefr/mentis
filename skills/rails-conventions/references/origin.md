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
