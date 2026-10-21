# cloud-iam-network-and-cost-pitfalls: origin and source stamps

> Provenance of `skills/cloud-iam-network-and-cost-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation-style skill files, never run by us against a cloud account. No
resource was created, no policy applied, no price queried while writing it.

## Sources (read 2026-10-20, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| awslabs/agent-plugins at commit fbefb37: `plugins/deploy-on-aws/skills/deploy/SKILL.md`, `elastic-beanstalk/SKILL.md`, `plugins/aws-serverless/skills/aws-serverless-deployment/SKILL.md` | Apache-2.0 (`LICENSE` read 2026-10-20) | Estimate before generating, dev-sized default, private subnets behind a balancer, outbound path for workers, least privilege derived from SDK calls, template scan, stateful and stateless stacks, termination protection, logical-name tests, preview in CI, bootstrap, pipeline for production |
| huggingface/skills at commit c3ff942: `skills/hf-cloud-sagemaker-iam-preflight/SKILL.md` | Apache-2.0 (`LICENSE` read 2026-10-20) | Discover an existing role before creating, rank by last use then by creation date, single-sign-on callers cannot create roles, no full-access managed policy, trust check |
| Official AWS pages: NAT gateway pricing, S3 Block Public Access, CloudWatch Logs log groups | product documentation, facts only, rewritten, read 2026-10-20 | NAT billing basis and endpoint advice (§2.2.3-4), account-level public-access block (§1.4.2), indefinite default log retention and tags for cost (§2.2.5, §2.4.4) |
| Official AWS page: IAM security best practices | product documentation, facts only, rewritten, read 2026-10-20 | Temporary credentials for workloads and people, second factor on root and long-lived users (§1.1.3, §1.5.4) |
| Official AWS pages: S3 default encryption, CloudFormation termination protection, CDK bootstrapping, AWS Budgets | product documentation, facts only, rewritten, read 2026-10-20 | Later encryption leaves existing objects (§1.3.5), protection scope (§2.3.1), per-environment bootstrap (§2.3.5), budget refresh lag (§2.4.5) |
| Official Azure pages: managed identities overview, NAT gateway overview | product documentation, facts only, rewritten, read 2026-10-20 | Azure identity equivalent (§1.1.4), private-by-default networks and explicit outbound (§2.2) |
| Official Google Cloud page: service-account best practices | product documentation, facts only, rewritten, read 2026-10-20 | Dedicated accounts, no keys, no default editor (§1.1.4) |
| Official AWS page: EC2 on-demand pricing | product documentation, facts only, rewritten, read 2026-10-20 | Internet data-out is charged with a monthly free allowance (§2.2.4) |
| Official Google Cloud page: IAM service-account overview | product documentation, facts only, rewritten, read 2026-10-20 | Default compute identity gets the editor role (§1.1.4) |
| MicrosoftDocs/architecture-center | CC BY 4.0 (`LICENSE` first line read 2026-10-20) | Not opened: no Azure page was needed for a point still open (below) |

## Removed (stated in the sources, not carried)
- Service-selection matrices, the choice between Beanstalk modes, platform detection and every product-specific command, flag and configuration key.
- Approximate prices and the note that one managed service is in maintenance mode: version-bound and unverified.
- The tool-server setup, write-access defaults and hook wiring of the plugins.
- All code samples and the helper scripts of the role-discovery skill.

## Not verified
1. **Prices and limits.** None is recited. The gateway charging basis is now confirmed; internet egress charging is now confirmed (tiered, with a monthly free allowance); cross-zone charging beyond the gateway is still own knowledge (the EC2 pricing page read 2026-10-20 does not show the same-region rate) and must be re-read against the provider's current price list.
2. **Azure.** Managed identities and the NAT gateway outbound change were read; Azure storage exposure, price and cost traps were not. GCP is confirmed for identities and keys (§1.1.4), not for network or cost.
3. **Own guidance, still labelled in the text:** private databases, scanners finding public resources within hours, expiry on experiments, budget alert, every "Checks" section.
4. **Scanner names** are the source's; their rule sets were not checked.
5. **No command, flag or template key was executed.**

## Related blocks
`terraform-conventions`, `terraform-state-and-secrets-pitfalls`, `kubernetes-access-and-exposure-pitfalls`,
`serverless-edge-worker-pitfalls`, `credential-lifecycle-pitfalls`, `production-readiness-review`.
