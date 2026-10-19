# elasticsearch-mapping-and-reindex-pitfalls: origin and source stamps

> Provenance of `skills/elasticsearch-mapping-and-reindex-pitfalls`. Read it when a rule has to be traced to
> its source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from skill documents, never run by us against an Elasticsearch cluster. No index was
created and no reindex was run.

## Sources (all read in full 2026-10-15, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| elastic/agent-skills at commit baa5111 (2026-09-10): `skills/elasticsearch/elasticsearch-index-design/SKILL.md`, `references/field-type-decisions.md`, `references/multi-field-patterns.md`, `references/mapping-explosion.md` | Apache-2.0 (`LICENSE` re-read 2026-10-15, Apache License Version 2.0 text) | Explicit mapping, type by access pattern, multi-fields, `ignore_above`, `flattened`, `doc_values`, `scaled_float`, new index for type changes |
| elastic/agent-skills at baa5111: `skills/elasticsearch/elasticsearch-reindex/SKILL.md`, `references/tuning.md`, `references/troubleshooting.md`, `references/api-reference.md` | Apache-2.0 (same file) | Destination preparation, async copy and task polling, slicing, throttling, remote reindex limits, overwrites, `version_type`, Serverless differences |
| elastic/agent-skills at baa5111: `skills/elasticsearch/elasticsearch-ingest/SKILL.md`, `references/mapping-design.md`, `references/ndjson-bulk-format.md`, `references/troubleshooting.md` | Apache-2.0 (same file) | Typed bulk JSON, action and source lines, `errors: true`, count checks, wrong-mapping recovery |

Not read for this block: `references/patterns.md` of the reindex skill (485 lines, multi-step recipes; only
`SKILL.md` links into it). The OpenSearch documentation (Apache-2.0 sparse clone) was not opened.

## Version bounds stated in the sources
- Compatibility line of all three skills: Elasticsearch 8.x or 9.x, self-managed, Elastic Cloud Hosted or
  Elastic Cloud Serverless. The reindex skill carries a self-managed against Serverless table, reproduced in
  prose in §3.5; the remote-reindex line there is marked Tech Preview by the source. No finer version is given
  and none is claimed.

## Removed (in the sources, not carried)
- The `elastic` CLI commands, the "Operations" tables and the instructions telling an agent not to call the HTTP
  API or to guess credentials: tool usage of the source, treated as data.
- The `eval-*` index names, CSV fixtures and evaluation-style examples.
- The review's wording "settings" for what `_reindex` does not copy: the source says mappings, shard counts and
  analyzers, which is what §3.2 states.
- The source's `_cat/count` and `_cluster/settings` logging recipes beyond the one-line mentions in §3.4 and
  §3.5.

## Not verified
1. **Defaults and limits** quoted from the files (`source.size` 1000, scroll keep-alive 5 minutes, the 100 MB
   remote buffer, the 32 KB term limit, `ignore_above` 256, bulk batches of 500 to 5,000) were not checked
   against Elasticsearch release documentation.
2. **A string in a `long` field as a mapper parsing exception** is taken from the ingest skill's troubleshooting
   page; Elasticsearch's own coercion rules were not read.
3. **Serverless behaviour** is taken from the reindex skill's table, not from Elastic documentation.
4. **Own guidance, labelled in the text:** the delete-or-reindex remark in §4.4 and every "Checks" section.
5. **Multi-source id collisions** (§3.4): the script that appends the index name was described in the source's
   `patterns.md`, which was not read; only the sentence in the troubleshooting page is relied on.

## Related blocks
`nestjs-integration-patterns` §5 (index synchronisation, outbox, lag), `data-pipeline-conventions` §1
(idempotent re-runs), `source-freshness`. Query tuning, relevance and cluster triage are a separate, unwritten
block.
