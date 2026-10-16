# semantic-layer-metric-pitfalls §3 — Answering a question from the layer

> Part 3 of `skills/semantic-layer-metric-pitfalls`. Version-bound: dbt Core 1.12 and the tools of dbt's MCP
> server named by the source. Read it when a business question must be answered with data. Source: dbt Labs'
> answering-natural-language-questions skill (Apache-2.0); points marked own guidance are ours.

## 3.1 Order of approach
1. **Try the semantic layer first.** The source's order is: query a metric; modify the compiled SQL of a metric;
   explore models and write SQL; analyse the manifest and catalog files. Each step is used only when the one
   before cannot answer.
2. **With semantic-layer tools available**: list the metrics, check that the dimensions needed exist, then query
   the metric with filters. If a dimension is missing or custom logic is needed, move to the compiled SQL.
3. **Writing fresh SQL before checking for a metric produces a second definition of the number** (own
   guidance, a consequence of the layer's purpose). When the layer answers, the answer carries the shared
   definition.
4. **A dimension that "does not exist in the data" may only be missing from the semantic config**, the source
   warns; check the config before reporting the gap.

## 3.2 Modified compiled SQL
1. **Use it for small changes**: a missing dimension (join and group), a custom filter that is not a dimension,
   a case expression for a custom category, or a different aggregation.
2. **Get the compiled SQL of the metric, edit it, and run the result.** The compiled SQL has resolved table
   names, not `ref` calls; work with the raw SQL as returned.
3. **Say that the answer comes from modified SQL** (own guidance): the number no longer carries the metric's
   definition untouched.
4. **Suggest adding the change to the semantic model** whenever the modification would be reusable.

## 3.3 Models, then files
1. **Without a semantic layer, discover the marts first**, not staging, because marts carry business logic.
2. **Without any tool server, read the manifest and catalog files in the project** if they exist. They can be
   large: filter with a query tool before reading, and look only at the nodes and columns needed.
3. **When SQL cannot be run**, say so, for example that it should run in the warehouse and has not been
   executed (the source's wording is to state that it cannot execute without database access).

## 3.4 Suggestions and limits
1. **Suggest changes at the semantic-layer level**: add a metric, add a dimension, add a semantic layer. Do not
   suggest database schema changes, pipeline changes or "ask the data team".
2. **Check which tools are available before choosing an approach**, and do not answer "cannot answer" before
   the four approaches were tried.
3. **This is for answering questions, not for validating models**: the source excludes checking model logic,
   running tests and building models from this flow.
