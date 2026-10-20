# cloud-iam-network-and-cost-pitfalls §1 — Identity and exposure

Sources: the `deploy` and `elastic-beanstalk` skills of awslabs/agent-plugins at fbefb37 and the role-discovery skill of huggingface/skills at c3ff942, read 2026-10-20. Points marked "own guidance" are not from a source.

## 1.1 One identity per workload, scoped to what it calls
1. **Give every workload its own role or service identity, with the actions it needs on the resources it touches.** The source derives the list from the code: find the provider SDK clients in the source and map each call to its action and its resource, rather than starting wide and trimming later.
2. **Do not attach the provider's full-access managed policy for a service,** and do not wait for an access-denied error to learn what is missing. Read the policies the role carries, compare with what the deployment needs, add only the missing actions and scope each to its resource.
3. **Use temporary credentials from a role, not long-lived access keys,** for workloads, CI and people (own guidance). A key committed or logged stays valid until someone revokes it.
4. **A default identity the provider creates for compute (on some providers it carries broad edit rights) should not be left on new workloads**: create a dedicated one and move the workload to it. Checked on one provider: the default compute identity is granted the project-wide editor role when it is created, and the provider recommends turning that automatic grant off and giving each identity only what its workload needs (GCP IAM service-account overview, read 2026-10-20). No Azure page was read.

## 1.2 Discover before you create
1. **Before creating a role for a service, look for one that already exists** and check two things: it exists, and its trust policy lets that service assume it. The source ranks candidates by last use and falls back to the newest creation date when last-use data is empty.
2. **A caller that signs in through a single-sign-on session often cannot create identities at all.** Find this out first, and when it is so, stop and ask the account owner for a role or for the narrow permissions to create one, naming them. Retrying other identity operations is noise.
3. **Never "fix" a failing deployment by widening the role the agent itself runs under** (own guidance). Say what is missing and who can grant it.

## 1.3 Private by default
1. **Put web workloads behind a load balancer in private subnets, and open the instances only to the balancer's group.** The source treats this as the default so that adding capacity later is a setting, not a rebuild.
2. **Terminate TLS with a managed certificate on the balancer** and accept only the secure port from outside.
3. **Databases and caches have no public address** (own guidance). Reach them from the workload's own network, or through a bastion or a session tool, never through an "allow my IP" rule that outlives the day.
4. **Workers with no inbound traffic still need an outbound path** to call APIs and pull images. Private subnets reach out through a gateway, which has a price (§2.2), or through private endpoints to the provider's own services.
5. **Turn on encryption at rest for storage and databases when creating them,** because enabling it afterwards often means copying the data (own guidance).

## 1.4 What is reachable from the world
1. **Treat "anywhere" (all addresses) as a finding in every inbound rule,** except the ports of a public front door. Check the administration ports in particular.
2. **Block public access at the account level for object storage,** and give a bucket public readability only when it is a website, with the reason written down. Checked on one provider: the block exists at organisation, account, bucket and access-point level with four independent settings, the most restrictive combination wins, and the provider recommends turning all four on for the account; the settings do not edit existing policies, so removing one makes a bucket with a public policy public again (S3 Block Public Access page, read 2026-10-20).
3. **A public IP, a public bucket or a public snapshot is found by scanners within hours** (own guidance); do not leave one "for a moment".
4. **Run a template security scan before applying** (the source names two such scanners). It catches missing encryption and open ranges; it does not know your intent, so read the result.

## 1.5 Checks (own guidance)
1. List every identity the change creates or reuses, with its actions and resources. A wildcard in either column needs a reason.
2. List every inbound rule and every public resource. Each has a reason or is removed.
3. From outside the network, try to reach the database and the instances directly. They must not answer.
4. Confirm there is a root or owner login protected with a second factor and not used for deployments.
