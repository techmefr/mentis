# semantic-layer-metric-pitfalls §2 — Modelling rules

> Part 2 of `skills/semantic-layer-metric-pitfalls`. Version-bound: dbt Core 1.12. Read it when a semantic model
> or a metric is designed or reviewed. Sources: dbt Labs' building-dbt-semantic-layer skill, its best-practices
> and latest-spec pages, and its time-spine page (Apache-2.0); points marked own guidance are ours.

## 2.1 Principles
1. **Prefer normalised models** and let MetricFlow join dynamically for the user, rather than building wide
   denormalised tables.
2. **Compute in metrics, not in rollups.** A calculation defined in a metric stays recomputable at any grouping;
   a rollup frozen in a dbt model fixes one grouping. The best-practices page lists pre-computed rollups as an
   anti-pattern.
3. **Start with simple metrics**, then ratio, derived and cumulative ones, which build on them.
4. **Build in parallel and deprecate gradually**; the source lists refactoring production code directly as an
   anti-pattern.
5. **Do not build a full semantic model on a dimension-only table**; a primary entity is enough there.

## 2.2 Entities and dimensions
1. **Each semantic model has exactly one primary entity.** Name it in the singular (`order`, not `order_id`)
   and point at the column with `expr`; foreign entities are what let semantic models join.
2. **A semantic model with metrics needs a default time dimension.** In the latest spec this is the model-level
   `agg_time_dimension`, placed at model level and not nested under the semantic-model block. A model with no
   time column cannot hold time-based metrics.
3. **Set the granularity once, at the minimum, and let MetricFlow derive the coarser ones.** Do not create
   several time buckets of the same column. In the latest spec the granularity sits on the column, not inside
   the dimension block.
4. **A column in the latest spec is an entity or a dimension, not both.**
5. **Computed dimensions** (a category from thresholds, for example) are written as expressions; the latest spec
   has a separate construct for computed dimensions and entities not tied to one column.
6. **Disambiguate dimension names with a double underscore** (`orders__location`), and give metrics clear
   business-friendly labels for the tools downstream.
7. **A slowly changing dimension of the second type cannot hold simple metrics** in the latest spec, per the
   source.

## 2.3 Metrics
1. **Every metric has a name, a description, a label and a type.**
2. **Where metrics live in the latest spec**: simple metrics on the model; the top-level `metrics:` key only for
   cross-model advanced metrics (derived, ratio, cumulative, conversion). A derived metric lists the metrics
   its expression uses.
3. **Count rows with a constant expression**: `expr: 1` with a sum (legacy and latest) or a count (latest).
4. **A cumulative metric takes `window` or `grain_to_date`, never both**, and needs a time spine. The time
   spine is declared with a `time_spine:` property under the model and a `standard_granularity_column`; the
   source lists a missing standard granularity column as a common mistake.
5. **A conversion metric** measures how often one event leads to another for an entity within a time window;
   `constant_properties` keeps a dimension value the same across both events.

## 2.4 Filters
1. **A filter may reference only dimensions and entities declared in the semantic model.** Raw table columns
   are not allowed, even when they appear in a measure's expression. If the column is needed, declare it.
2. **Filters use Jinja accessors**: `Entity('...')`, `Dimension('entity__name')`, `TimeDimension('name',
   'granularity')` and `Metric('name', group_by=[...])`.
3. **Filters can sit on simple metrics or on the inputs of advanced metrics**, for example on the numerator and
   denominator of a ratio separately.
4. **A filter that validates but returns nothing** is worth a check against the dimension's actual values (own
   guidance; the source does not discuss it).
