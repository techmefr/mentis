# elasticsearch-query-and-triage-pitfalls §2 — Pinning and ranking

Sources: the `elasticsearch-search-relevance` skill of elastic/agent-skills at baa5111 (`SKILL.md`, `references/multi-match-tuning.md`, `references/query-rules-reference.md`), read 2026-10-16. The source states compatibility with Elasticsearch 8.10 or later (query rules), self-managed, Elastic Cloud Hosted and Elastic Cloud Serverless. It covers Query DSL on indices with `text` fields (catalogues, documentation, knowledge bases), not ES|QL, vector or hybrid retrieval.

## 2.1 Choose the lever
1. **A document that must rank first for a given query is a query rule; weak ranking for open-ended text is a tuning problem on the organic query.** Decide which of the two the problem is before touching a query, and make one coherent change at a time, tested before the next.
2. **Do not simulate a pin with an extreme boost, `function_score`, `boosting` or a sort.** The source calls this fragile, and a pin faked by boosting or sorting on a product id breaks when inventory changes.
3. **Do not sort by price or date to fake text relevance, and do not run `term` or `match` on a `.keyword` sub-field for an analysed user phrase.** The first solves merchandising, not relevance; the second skips analysis.
4. **Ground every field name in the mapping** (`GET /{index}/_mapping`): never write `name`, `content` or `body` without checking they exist.

## 2.2 Query rules
1. **Two rule types: `pinned` and `exclude`.** `pinned` rewrites the organic query into a pinned query and lists the documents first, in the given order. `exclude` removes documents. Promote with `pinned`; use `exclude` only when asked to hide documents, never to promote.
2. **Criteria carry a `type` (`exact`, `contains` or `fuzzy`), a `metadata` key and `values`, and all criteria of a rule must match.** The `metadata` key is a label you choose, not an index field. At search time the `rule` query passes `match_criteria` whose keys must equal those `metadata` names; a mismatch means the pin never applies.
3. **Actions take `ids` or `docs`, never both in one rule.** Use `docs` (`_index` plus `_id`) when ids may collide across indices. Pinned queries cap at 100 documents in total across the matching rules.
4. **Creating a ruleset pins nothing.** The search must use a `rule` query with the `ruleset_id`, the `match_criteria` and the normal relevance query inside `organic`; pinned hits are prepended and organic matches follow. `PUT /_query_rules/{ruleset_id}` replaces the whole ruleset body, while `PUT /_query_rules/{ruleset_id}/_rule/{rule_id}` adds or updates one rule.
5. **Test the criteria before searching** with `POST /_query_rules/{ruleset_id}/_test` and the same `match_criteria` payload, then confirm in a search that the target document is first and the organic matches sit below it.

```json
{
  "query": {
    "rule": {
      "ruleset_id": "catalog-sale-pin",
      "match_criteria": { "query_string": "sale" },
      "organic": {
        "multi_match": { "query": "sale", "fields": ["title^2", "description"] }
      }
    }
  },
  "size": 10
}
```

## 2.3 Organic ranking
1. **Classify the fields from the mapping.** `text` fields do full-text retrieval and scoring; `keyword` fields filter, sort and aggregate and are not the primary target for natural-language search. Short `text` fields (title, name) give precision and long ones (description, body) give recall, so search both rather than only the long one.
2. **Use `multi_match` across the mapped text fields and boost the short ones.** The source starts at `title^2` and tunes between `^1.5` and `^3` on tested top hits; `best_fields` is the default for short queries and `cross_fields` treats the fields as one combined field. When no guidance exists the source orders the fields title or name, then summary or headline, then description or body.
3. **Add recall levers one at a time.** `operator` and `minimum_should_match` help multi-word queries where only one term matches; use `operator: "or"` with `minimum_should_match` when a strict AND drops too many relevant documents.
4. **Synonyms are applied through the index analyzer.** The source says creating a synonym set does not change an existing index until the index analyzer references it, and prefers query-time tuning first, proposing synonym sets only when recall gaps persist after field boosting.
5. **Inspect analysis when tokens explain the misses:** `POST /{index}/_analyze` with the field's analyzer on sample query text.
6. **Compare before and after with the same query and `size` of at least 10:** top `_id` values and order, `_score`, key `_source` fields. Use `"explain": true` on a single hit when the score is unclear. Changing a query without re-running the search proves nothing.

## 2.4 Checks (own guidance)
1. A pin is verified with the `rule` query in the request, not with the ruleset alone.
2. The `metadata` names in the criteria and in `match_criteria` were compared character by character.
3. A ranking change comes with two top-hit lists, baseline and candidate.
