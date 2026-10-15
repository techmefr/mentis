# secret-leak-response-pitfalls §1 — Hooks, scans and baselines

> Section 1 of `skills/secret-leak-response-pitfalls`. Read it when a secret scanner is set up, changed or
> trusted. Sources: gitleaks at commit `b58d3f1`, detect-secrets at `5e14193`, git-secrets at `7d6b970`,
> Kingfisher at `8244f7b`, read 2026-10-15. Flag names are version-bound.

1. **A local hook is a convenience, and CI is the control.** Hooks live in each clone and are opt-in:
   git-secrets says in a warning that the hooks must be installed for every repository with
   `git secrets --install`, and offers a git template directory to cover future clones. gitleaks documents
   that its pre-commit hook is skipped by prefixing `SKIP=gitleaks` to the commit, and git-secrets
   documents `--no-verify` for a false positive. Both are the normal way to commit, not an attack. Run the
   same scan in CI on every push or merge request, and turn on push protection where the platform has it
   (`skills/ci-workflow-hardening` §3.5), so a bypassed hook is caught.
2. **No scanner is complete, so none is a guarantee.** The git-secrets documentation says its patterns are
   not guaranteed to catch every instance and are extra insurance. detect-secrets says it is not a
   sure-fire solution and lists what it does not prevent: multi-line secrets, and default passwords that
   do not trigger its keyword detector. Treat a clean scan as the absence of a known pattern.
3. **Scan the history, not only the working tree, and do it before a repository goes public.** git-secrets
   has `--scan-history` for all revisions and documents it under "before making public a repository".
   gitleaks scans past or present commits through `git log -p`; its `git` mode takes `log-opts` for a
   range. A removed secret is still in an earlier commit and in every clone (`skills/security-hardening` §4.6).
4. **The baseline is the list of what is known, and it doubles as the rotation checklist.** detect-secrets
   describes the baseline as the secrets accepted for now so new ones can be blocked, and as a checklist
   of secrets to rotate and move to secure storage. gitleaks accepts any earlier report as a baseline and
   then reports only new findings; Kingfisher's baseline is keyed by repository and fingerprint. Own
   guidance: give the baseline an owner and a date, review it on a schedule, and do not let "baselined" mean
   "accepted forever". The baseline file can itself contain secrets if the scanner writes the match into it,
   so read what yours stores before committing it.
5. **A fingerprint changes when the finding moves.** Kingfisher's documentation says its fingerprints
   include the matched value, the origin kind and byte offsets, so moving a finding within a file can yield
   a new fingerprint and the baseline entry stops matching. Keep scan options (confidence, rules, history
   mode, exclusions) the same between building the baseline and using it, as it also says.
6. **Defaults hide encoded and archived secrets.** gitleaks documents that `--max-decode-depth` and
   `--max-archive-depth` both default to 0: no decoding of percent, hex or base64 values, and no looking
   inside archives. Its decoder handles hex of at least 32 characters and base64 of at least 16, up to the
   set depth. If a base64 environment file or a zipped export is plausible in your repositories, set both.
   Archive scanning applies to both `dir` and `git` scans, and a finding's path shows the nesting.
7. **Inline allow comments are per line and can be audited or ignored.** gitleaks honours `gitleaks:allow` on
   the line of the secret and has `--ignore-gitleaks-allow` to disregard the comments. detect-secrets honours
   `pragma: allowlist secret` on the line, or `pragma: allowlist nextline secret` for the line after, and
   has `--only-allowlisted` to scan only the allowed lines and confirm each exception is a non-secret. A
   comment on the wrong line suppresses nothing, and a comment on a real secret suppresses the one tool that
   would have flagged it. In CI, run the scan once with allow comments ignored or audited so exceptions are
   visible. Own guidance: an allow comment names why in the commit message, not in the comment.
8. **Allow patterns can be too forgiving.** git-secrets says allowed patterns that are too forgiving are as
   bad as prohibited ones that are too greedy. It also notes that a flagged line is matched as
   `path:line:text`, so an allowed pattern containing a file name or line number can match more or less
   than intended. gitleaks allowlists combine criteria with OR by default; check whether you meant AND.
   Test each pattern against a sample with `git secrets --scan <file>` or the scanner's equivalent.
9. **Reports and alert hooks are secrets too.** gitleaks has `--redact` (a percentage, 100 by default) for
   logs and standard output. Kingfisher's documentation says a webhook URL for alerts is a credential:
   keep it in the CI secret store, not in the repository or a job log, and treat an unredacted report as
   sensitive, stored in a protected location. Own guidance: write scan reports with redaction on, and
   upload them as protected artifacts only.
10. **Pass scanner exit codes through.** gitleaks exits 1 on leaks or errors, 126 for an unknown flag, and
    has `--exit-code` to change the code; Kingfisher exits 205 for a validated active finding, 200 for
    findings with none validated, and 0 for none, and says to preserve them in CI policy. A CI step that
    ends in `|| true` turns every one of these into a pass.
11. **Keep the old and new pipelines both while you change scanners.** Own guidance: gitleaks's README
    says it is feature complete and that development has moved to another project, so a change of scanner
    is plausible; run both on the same history once and compare findings before dropping the old one.
