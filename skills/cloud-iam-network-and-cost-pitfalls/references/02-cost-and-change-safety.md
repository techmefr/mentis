# cloud-iam-network-and-cost-pitfalls §2 — Cost and change safety

Sources: the `deploy` skill, the Elastic Beanstalk skill and the serverless deployment skill of awslabs/agent-plugins at fbefb37, read 2026-10-20. Points marked "own guidance" are not from a source. No price is recited; read the provider's current price list.

## 2.1 Price it before you create it
1. **Show a monthly estimate before generating or applying infrastructure,** so the person can change the plan before committing. The source makes this a fixed step between choosing services and writing code.
2. **Estimate from the price list for the region in use, not from memory,** and list every line: compute, load balancer, outbound gateway, storage, database, data transfer, logs.
3. **Separate what scales with time from what scales with use.** An idle load balancer or gateway bills by the hour; storage by what is kept; transfer and requests by traffic. A flat estimate hides the last two.
4. **Say what the estimate does not include,** such as support plans, taxes and the traffic nobody can predict yet.

## 2.2 Defaults that fit the stage
1. **Default to dev-sized (small instances, one zone, no replicas) unless production is stated.** The source says so explicitly; the cost of an over-sized default is paid every hour it runs.
2. **Production differs in availability and in maintenance windows, not only in size:** several zones, rolling deployments with spare capacity, patching in a window.
3. **A managed outbound gateway bills per hour and per gigabyte processed** (own guidance, re-read the current price). A worker that pulls large images or data through it every run can cost more than the instance. Use private endpoints for the provider's own storage and registry traffic.
4. **Traffic between zones and out to the internet is billed** (own guidance): keep chatty components in the same zone when availability allows, and put a content cache in front of heavy downloads.
5. **Logs and metrics cost by volume and by time kept.** Set a retention period on every log group when it is created; the default may be forever.

## 2.3 Stateful resources inside stacks
1. **Keep stateful resources (databases, buckets with data, queues with messages) in a different stack from stateless ones,** and enable termination protection on the stateful stack. The source recommends this for its code-based stacks.
2. **A renamed logical resource is a new resource.** Template tools identify resources by their logical name; renaming one can mean delete-and-create, which empties a database. The source suggests a test that asserts the logical names of stateful resources to catch accidental replacement.
3. **Do not hard-code account identifiers or regions in templates;** read them from the environment of the stack or from references (`this.account` style), so that the same template deploys to another account.
4. **Commit the lookup cache the tool writes** (VPC and zone lookups), so that two machines synthesize the same template.
5. **The tool's bootstrap step must have run in each account and region** before the first deployment; a missing toolkit stack is a common first-deployment failure.

## 2.4 Preview, apply, clean up
1. **Read the change preview before every apply, and in CI on every change.** Look for lines that say replace or delete on anything stateful, and for any new inbound rule or new identity.
2. **Do not deploy to production from a laptop with a direct command;** use a pipeline that runs the preview, the scan and the apply, with an approval for production (the source says to avoid direct production deploys).
3. **Never mix two ways of managing the same resource** (a console edit on a stack-managed resource, two tools claiming one resource), because the next apply silently reverts or conflicts (own guidance).
4. **Tear-down is part of the design.** Name or tag everything with an owner and an expiry for experiments, and list what survives a stack deletion: volumes, snapshots, fixed addresses, log groups, buckets with retained data (own guidance).
5. **Set a budget alert before the first experiment,** at a low amount, to a channel somebody reads (own guidance).

## 2.5 Checks (own guidance)
1. The estimate, with its assumptions, is in the change description.
2. The preview shows no replace or delete on stateful resources, or each one is deliberate and backed up.
3. A new stack has termination protection where it holds data, tags with an owner, and log retention set.
4. After a tear-down, list the account's volumes, snapshots, addresses and gateways: none belong to the deleted work.
