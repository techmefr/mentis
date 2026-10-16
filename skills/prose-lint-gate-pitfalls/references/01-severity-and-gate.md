# prose-lint-gate-pitfalls §1 — Severity and the gate

> Part 1 of `skills/prose-lint-gate-pitfalls`. Read it when the gate's behaviour on a pull request is designed
> or argued. Sources: the Elastic Vale rules repository and the Grafana writers' toolkit (Apache-2.0), the alex
> checker (MIT); each rewritten in our own words. Points marked own guidance are ours.

## 1.1 Severity levels decide what the gate means
1. **Use three levels: suggestion, warning, error.** Elastic's rule-authoring notes assign them: error only for
   content that is structurally broken or unsafe to ship (the example is a merge-conflict marker), warning for
   high-confidence issues with a clear fix (spelling, accessibility terms, blocked word choices), suggestion for
   style, tone and context-dependent advice.
2. **Grafana states the reading for its rules page**: errors must be fixed, warnings may need fixing or need
   consideration, suggestions point at a style choice to weigh.
3. **Decide which level fails the build and write it down** (own guidance; neither source states its CI
   threshold in the files read). A gate that fails on suggestions trains people to skip it, and a gate that
   fails on nothing is a report nobody reads.
4. **Show all levels to the author, fail on the one you chose.** Elastic's packaged configuration reports from
   suggestion upward; the failing level is a separate decision.
5. **A level is a promise about confidence.** Do not put a context-dependent rule at error because it matters;
   raise the level only when the rule is rarely wrong.

## 1.2 Overrides in one declared file
1. **Per-repository overrides live in one file** at a known place. Elastic's action looks for an overrides file
   at the repository root or in the `.github` folder, where a repository can enable a rule that is off by
   default, or lower a rule's level.
2. **The merge rule is part of the contract.** Elastic's action replaces the value of an existing key in place
   and inserts a new key into the first file-type section; section headers are ignored except for constrained
   sections such as one that opts YAML files in. Know the merge rule before trusting an override.
3. **Scope the gate to the paths a team owns.** Elastic's action takes a list of paths, with globs and negation,
   so several teams can share one docs folder and one team's backlog does not fail another's pull request.

## 1.3 Scoped disables
1. **Disable a rule around the section that needs it, then enable it again.** Grafana's method is a pair of
   comments that first turn the named rule off and then on, with the rule's name in both.
2. **Name the rule.** The alex checker supports an ignore comment for the next paragraph and a disable and
   enable pair, each taking rule identifiers; it also allows omitting the identifiers to control all messages.
   The blanket form silences findings you never saw (own guidance: do not use it).
3. **Leave a trace of why** in the pull request description, so the comment pair carries only the rule name
   (own guidance). A disable that outlives its reason hides the next real finding.
4. **A page that demonstrates the rules** must break them. Grafana's own rules page starts with a long list of
   disables for that reason; it is the exception, not the pattern.

## 1.4 Skipping a change
1. **A move-only or rename-only change may skip linting.** Grafana lets an author skip the CI check by putting a
   marker in the pull request description, for changes that move files with existing findings or defer the
   content fix.
2. **Say so in the description and state when the findings will be fixed** (own guidance). A skip with no
   follow-up is a permanent exception.
3. **Lint only what the change touched.** The alex checker has a mode that ignores lines not changed in the
   push, so a merge is not blocked by old warnings and the next editor is bothered only by what they added.
   That mode was documented for one CI service; check that your CI supports it before relying on it.
