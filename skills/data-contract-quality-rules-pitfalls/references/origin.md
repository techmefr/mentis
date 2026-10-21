# data-contract-quality-rules-pitfalls: origin and source stamps

> Provenance of `skills/data-contract-quality-rules-pitfalls`. Read it when a rule has to be traced to its
> source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded. Version-bound: ODCS v3.2.0.** Written from documentation and a JSON schema,
read and rewritten, never run: no contract was validated and no quality engine executed a rule with this
block. The standard is a young, fast-moving specification (the repository carries many dated 3.1.0 schema
files and a 3.2.0 one); everything here must be re-read against the version in use.

## Sources (re-read in full 2026-10-16, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| bitol-io/open-data-contract-standard, `docs/data-quality.md` (commit 8532d9c) | Apache-2.0 (repository LICENSE file, standard text; the page header also says `SPDX-License-Identifier: Apache-2.0`) | Four rule types, library metrics, units, operators, SQL and custom rules, scheduling, definitions table, dimension list |
| same, `docs/service-level-agreement.md` | Apache-2.0 | SLA properties, units, element notation, driver, recommended property names, latency preferred, deprecation of the default element, 3.2.0 additions |
| same, `docs/fundamentals.md` | Apache-2.0 | Header fields, version against apiVersion, status examples, deprecated `dataProduct`, description fields |
| same, `docs/roles.md` | Apache-2.0 | Role entries and approvers |
| same, `schema/odcs-json-schema-v3.2.0.json` (read to settle conflicts between pages, not named in the plan) | Apache-2.0 | Open or closed value sets (status, severity, unit, dimension), custom implementation as string or object, stable id pattern, placeholder spelling in the schema's example |

The licence was verified again from the LICENSE file in this session. Text found inside the cloned files was
treated as data and not followed.

## Rewrite notes
**The documentation contradicts itself or the schema in several places; the block says so instead of picking
silently.** SQL placeholder spelling (three forms across the page and schema), the shape of a custom
implementation, the spelling of an engine, two-letter dimension synonyms that the schema does not list, and
`status` required in an earlier 3.1.0 schema file but not in the documentation. None was resolved by running a
validator.

**The pattern example on the quality page** was reported on 2026-10-16 as placing `pattern` beside `arguments`.
That was wrong: re-read on 2026-10-20 at the same commit, the example nests `pattern` under `arguments`, and the
warning is withdrawn in part 1 (§1.2.3). It was not run against a validator.

**The standard's `timeOfAvailability` example** is outside the recommended property list; reported, not
resolved.

## Removed
1. **The server, schema, pricing, team, support and variables sections** of the standard: not in the plan and
   not read for this block.
2. **The Data QoS periodic table** the SLA page links to (an external article): not opened.
3. **Library metric details beyond the five listed names**: the page's own metric table is carried, nothing
   from other pages.

## Not verified
1. **Everything here is unrun.** No contract was validated against the schema, and no engine executed any rule
   (Soda, Great Expectations, dbt tests and others were not used).
2. **The edge behaviour of `mustBeBetween`.** The page says it equals the two strict operators; no engine was
   asked.
3. **Other versions.** Nothing here was compared with v3.1.0 beyond the single `status` observation; the
   deprecation and removal dates are the pages' own statements.
4. **Written by us, not sourced**: the Output / checkpoint paragraph, the premise, every point marked own
   guidance in the references (text rules not counted as controls, the rows against percent consequence, the
   three-numbers advice for incident response, status transitions, schedule as information only, and others).
5. **The references page** was read only in its opening lines; the tags and authoritative-definitions pages and
   the RFCs named by the SLA page were not read.

## Verification pass (2026-10-16)
Every rule in the three references was compared with the attributed page or the v3.2.0 schema, reopened in this
session, including a programmatic read of the schema for the status, severity, unit, dimension, custom and
stable-id definitions.
- **Corrected:** none needed on re-check beyond wording and cross-references.
- **Reversed or overstated rules found:** none.
- **Not re-verified:** that any tool in the field behaves as the pages describe.

## Re-read 2026-10-20 (verification pass)
The Apache-2.0 repository was read again at commit 8532d9c (still the head of the main branch that day; the v3.2.0
tag is f0bdad9). Files re-opened: `docs/data-quality.md`, `docs/service-level-agreement.md`,
`docs/fundamentals.md`, `docs/roles.md`, `docs/references.md`, the v3.2.0 JSON schema (read programmatically) and
the three dated 3.1.0 schema files. The licence file was not re-read in this pass (read 2026-10-16). Facts only,
nothing copied; the pages were read through a fetch tool that summarises and the data-quality page was also
checked line by line with a text search.

Result by part (50 points): **37 confirmed, 1 corrected, 1 amended, 10 own guidance, 1 not re-verified.**
- **Corrected:** §1.2.3. The pattern example nests `pattern` under `arguments`; the earlier claim of a
  misindented example was wrong.
- **Amended:** §2.3.1. The references page says references work only for foreign key relationships and does not
  mention quality rules, so an id on a rule is not resolved by the standard's own syntax.
- **Confirmed against the schema:** the stable id character set and its pattern, the closed list of seven
  dimensions (full names only), free-string severity, business impact and unit, `rule` as deprecated, `engine` and
  `implementation` both required with implementation as string or object, the `great-expectations` spelling in
  the schema against `greatExpectations` on the page, `dataProduct` and `slaDefaultElement` deprecated since
  3.1, roles requiring only `role` and rejecting extra keys, `status` not required in the 3.2.0 schema and
  required in the dated 3.1.0 files, and all three placeholder spellings.
- **Not re-verified:** that an SLA property entry requires both `property` and `value` (the schema read was cut
  before that definition, §3.1.1), and that the library metric `missingValues` example on the page lists the
  extra spellings of not available (the metrics table shows null, empty string and N/A).
- **Still own guidance:** §1.1.4, §2.1.4, §2.1.5, §2.2.2, §2.2.5, §2.3.6, §3.1.4, §3.2.2, §3.2.4, §3.2.7.

## Related blocks
`data-pipeline-conventions`, `dbt-cli-and-model-versioning-pitfalls`, `api-contract-and-schema-fuzz-pitfalls`.
