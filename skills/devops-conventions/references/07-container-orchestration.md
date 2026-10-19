# § 7 — Workloads on a container orchestrator

> Section 7 of `skills/devops-conventions`. Read it when a diff writes or changes the manifests that
> run a service on a container orchestrator (Kubernetes is the one assumed; the ideas carry to others).
> It is not a manual: it is the set of defaults that, when absent, turn a deploy into an incident.

1. **Declare the health of a workload with three different probes, because they answer three different
   questions.** *Startup* asks whether the process has finished starting and holds the others off until it
   has; *readiness* asks whether it should receive traffic now; *liveness* asks whether it is wedged and
   should be restarted. Pointing liveness at a check that depends on the database turns a database blip
   into a restart storm of healthy processes. Liveness checks the process alone; readiness may check the
   dependencies it cannot serve without. A slow-starting application gets a startup probe, not a long
   initial delay on the others.
2. **Set resource requests and limits, and know which each one does.** The request is what the scheduler
   reserves, so an absent request packs workloads onto a node until it starves; the limit is the ceiling,
   and a memory limit below real usage is a kill loop. Base both on measurement of the running service,
   not on a guess, and review them when the traffic changes. Treat CPU limits with care: a limit that is
   too tight throttles latency without ever showing as an error.
3. **A rollout updates gradually and can be undone.** Use a rolling strategy that keeps capacity during the
   update, make readiness accurate so the orchestrator does not retire old instances before the new ones can
   serve, and keep enough revision history to roll back. The rollback has to be tested before it is needed
   (§4.1 of this block). A deploy that reports success because the objects were created, not because the
   new pods became ready, is not a verified deploy.
4. **Run more than one copy of anything that must stay up, and keep them apart.** A single replica turns
   every node drain into downtime. Add a disruption budget so maintenance cannot evict them all at once,
   and spread the copies across nodes or zones so one failure does not remove them together.
5. **Handle shutdown on purpose.** On termination the process is sent a signal and given a grace period
   before being killed. The service stops accepting work, finishes what is in flight, and exits inside that
   period; if the load balancer needs a moment to stop sending traffic, a brief pre-stop delay covers it.
   Without this, every deploy drops a handful of requests, and the failure looks random.
6. **Give the workload the least access that works.** A dedicated service account per workload, with a
   role granting only the verbs on the resources it uses; no cluster-wide administrative binding for an
   application; the credentials to the cluster API not mounted into pods that do not call it. Run as a
   non-root user, with a read-only root filesystem where possible, with privilege escalation off and
   unneeded Linux capabilities dropped. These are properties of the pod specification, so they are
   reviewable, which is the point.
7. **Keep configuration and secrets apart, and remember what a secret object is.** Non-sensitive settings
   live in configuration objects, sensitive ones in secret objects, and both are injected by reference.
   A secret object is encoded, not encrypted, unless encryption at rest is configured, and anyone who can
   read it in the namespace can read the value; so access to it is an authorisation decision, and the
   value is sourced from an external secret manager or sealed before it is committed
   (`skills/security-hardening` §4.2). Never bake a secret into the image or put it in an argument list.
8. **Restrict the network by default and open what is needed.** Without a network policy every pod can
   reach every other. Start from a policy that denies traffic into a namespace, then allow the specific
   sources and ports each service has; allow egress deliberately too, since an exfiltrating process needs
   somewhere to send.
9. **Images are pinned and come from where you decided.** Reference an image by an immutable digest or an
   exact version, not a moving tag (`skills/security-hardening` §4.10); pull from a registry you control or
   have vetted; scan images in the pipeline and read the result (§7.11 of security-hardening is the same
   rule for libraries).
10. **Ingress is a security boundary and a reliability one.** TLS is terminated at it with an automated
    certificate (§5), only the routes meant to be public are exposed, timeouts and request-size limits are
    set explicitly, and rate limits live here as well as in the application
    (`skills/security-hardening` §7.4).
11. **Everything is declared, and the cluster matches the declaration.** The manifests (or the chart, or the
    overlay) are in version control; a change made directly on the cluster is drift that the next apply
    overwrites or hides (§2.1 of this block). Read the rendered diff before an apply to a shared cluster, the
    same as a Terraform plan (§2.2), and prefer a reconciling controller to a person running the command.
12. **Label for people who will be paged.** Consistent labels for the application, version, team and
    environment make selection, cost allocation and alert routing possible, and the first incident is the
    wrong time to discover they are missing.
13. **Scale on the signal that matters, with a floor and a ceiling.** Autoscaling on CPU is a proxy;
    queue depth or request rate often tracks the work better. A minimum protects against scaling to zero
    capacity, a maximum protects the database and the bill, and the scale-down is slower than the
    scale-up so the system does not oscillate.

**Debugging order when a workload will not run:** the object's events and status first (they usually name
the cause: unschedulable, image pull failure, probe failure, out of memory kill), then the previous
container's logs when it is restarting, then the rendered manifest against what you meant, and only then
the node.

**Sources:** the Kubernetes documentation (workloads, configure probes, resource management, security
context and Pod Security Standards, RBAC, network policies, disruption budgets, secrets good practices,
termination of pods); the 12-factor app (disposability, config); CIS Kubernetes benchmark as a checklist
for the hardening points.
