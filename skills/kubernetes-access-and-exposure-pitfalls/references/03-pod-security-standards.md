# kubernetes-access-and-exposure-pitfalls §3 — Pod Security Standards

The Pod Security Standards define three cumulative policies, from permissive to restrictive. This section
restates the field-level rules of the Baseline and Restricted policies from the Kubernetes page "Pod Security
Standards" (read in full on 2026-10-16; attribution at the end of this file). The page is revised with
Kubernetes releases, and several rules carry a version, so re-read it for the cluster version you run.

## 3.1 The three profiles
1. **Privileged**: unrestricted, with a known path to privilege escalation. It is meant for system and
   infrastructure workloads run by privileged, trusted users; a pod under it can bypass container isolation,
   for example by using the node's host network.
2. **Baseline**: minimally restrictive, prevents known privilege escalations and allows the default,
   minimally specified pod. It targets application operators and developers of non-critical applications.
3. **Restricted**: heavily restricted, following current pod hardening practice at the expense of some
   compatibility. It targets security-critical applications and lower-trust users, and includes everything
   from Baseline.
4. **A wildcard `[*]` in a field path means every element of the list**, and if any listed container fails
   a rule the whole pod fails validation. Rules for containers apply to `containers`, `initContainers` and
   `ephemeralContainers` alike, so the paths below say "each container" instead of repeating all three.

## 3.2 Restricted: the controls added on top of Baseline
1. **Volume types**: every item of `spec.volumes[*]` must set one of `configMap`, `csi`, `downwardAPI`,
   `emptyDir`, `ephemeral`, `persistentVolumeClaim`, `projected` or `secret`. Anything else (a `hostPath`
   or an NFS volume, for instance) fails.
2. **Privilege escalation** (the page marks it v1.8+): each container sets
   `securityContext.allowPrivilegeEscalation` to `false`. The page's reason is escalation through
   set-user-ID or set-group-ID file mode. Linux only from v1.25 (§3.4).
3. **Run as non-root**: `runAsNonRoot` must be `true`, at the pod level
   (`spec.securityContext.runAsNonRoot`) or on each container. The container fields may be unset if the pod
   level is `true`.
4. **Run as a non-root user** (v1.23+): `runAsUser` must not be 0, at pod level or on each container; any
   non-zero value, or unset, is allowed.
5. **Seccomp** (v1.19+): the profile type must be set explicitly to `RuntimeDefault` or `Localhost`. Both the
   `Unconfined` profile and the absence of a profile are prohibited. It can be set on the pod, on each
   container, or on all containers with the pod level left unset. Linux only from v1.25 (§3.4).
6. **Capabilities** (v1.22+): each container must drop `ALL` capabilities (any list that includes `ALL`),
   and may add back only `NET_BIND_SERVICE`. Linux only from v1.25 (§3.4).
7. **Own illustration built from those allowed values**, a pod spec that meets points 3, 5, 6 and 2:

```yaml
spec:
  securityContext:
    runAsNonRoot: true
    seccompProfile:
      type: RuntimeDefault
  containers:
    - name: app
      image: example/app:1.4.0
      securityContext:
        allowPrivilegeEscalation: false
        capabilities:
          drop: ["ALL"]
```

   With `runAsNonRoot: true` the pod can only run if the image uses a non-root user (own reasoning, check
   it on your cluster; see §3.5 point 5).

## 3.3 Baseline: the controls Restricted inherits
1. **HostProcess**: `windowsOptions.hostProcess` unset or `false` (pod and containers; v1.26 stable
   per the page).
2. **Host namespaces**: `spec.hostNetwork`, `spec.hostPID` and `spec.hostIPC` unset or `false`.
3. **Privileged containers**: `securityContext.privileged` unset or `false` on each container.
4. **Capabilities**: `securityContext.capabilities.add` may contain only `AUDIT_WRITE`, `CHOWN`,
   `DAC_OVERRIDE`, `FOWNER`, `FSETID`, `KILL`, `MKNOD`, `NET_BIND_SERVICE`, `SETFCAP`, `SETGID`, `SETPCAP`,
   `SETUID` and `SYS_CHROOT`.
5. **HostPath volumes**: `spec.volumes[*].hostPath` must be unset.
6. **Host ports**: `hostPort` unset or 0 on each container port; the page recommends disallowing them
   entirely, and says a known list is not supported by the built-in Pod Security admission controller.
7. **Host in probes and lifecycle hooks** (the page marks it v1.34+): the `host` field of `httpGet` and
   `tcpSocket` in liveness, readiness and startup probes and in `postStart` and `preStop` hooks must be
   unset or empty.
8. **AppArmor**: `appArmorProfile.type`, on the pod or each container, must be unset, `RuntimeDefault` or
   `Localhost`; the legacy annotation `container.apparmor.security.beta.kubernetes.io/*` must be unset,
   `runtime/default` or `localhost/*`.
9. **SELinux**: `seLinuxOptions.type` must be unset or empty, or `container_t`, `container_init_t`,
   `container_kvm_t` (and `container_engine_t` since Kubernetes 1.31); `seLinuxOptions.user` and
   `seLinuxOptions.role` must be unset or empty.
10. **`/proc` mount**: `securityContext.procMount` unset or `Default`.
11. **Seccomp**: the profile type must not be set to `Unconfined`; unset, `RuntimeDefault` and `Localhost`
    pass at Baseline (Restricted, §3.2, requires an explicit value).
12. **Sysctls**: only the safe subset in `spec.securityContext.sysctls[*].name`. The page defines a safe
    sysctl as namespaced in the container or pod and isolated from other pods and processes on the node,
    and lists `kernel.shm_rmid_forced`, `net.ipv4.ip_local_port_range`,
    `net.ipv4.ip_unprivileged_port_start`, `net.ipv4.tcp_syncookies`, `net.ipv4.ping_group_range`, plus
    `net.ipv4.ip_local_reserved_ports` (since Kubernetes 1.27) and four TCP keepalive and fin-timeout
    settings (since Kubernetes 1.29).

## 3.4 Operating system and version notes
1. **The Restricted policy uses `spec.os.name` from v1.25.** Privilege escalation, seccomp and Linux
   capabilities are required only when the OS is not `windows`.
2. **Many `securityContext` fields have no effect on Windows**, as the page says.
3. **Kubelets before v1.24 do not enforce the pod OS field.** With nodes older than that, the page says to
   pin the Restricted policy to a version before v1.25.
4. **The policy definitions carry versions** (v1.8, v1.19, v1.22, v1.23, v1.25, v1.26, v1.34): treat every
   one as the page's statement on 2026-10-16 and re-read it for your cluster version.

## 3.5 Enforcement and what the standards do not do
1. **The page defines the policies, not how they are enforced.** It names the built-in Pod Security
   admission controller, with one namespace example per profile, and mentions the third-party alternatives
   Kubewarden, Kyverno and OPA Gatekeeper. How to configure each of the third-party ones was not read.
   The built-in controller is configured by namespace labels, `pod-security.kubernetes.io/<mode>: <level>`,
   with modes `enforce`, `audit` and `warn` and optional `<mode>-version` pins (Pod Security Admission page).
2. **There is no standard profile between Privileged and Baseline**: privileges above Baseline are
   application-specific, so policies there are defined case by case; the page says that is not a
   recommendation to use Privileged.
3. **A security context is not a security profile.** The security context sets runtime parameters in the
   pod manifest; a profile is a control-plane mechanism that enforces settings, including some outside the
   security context.
4. **Sandboxed pods have no standard definition**, and the need to restrict privileges can differ for them;
   the page recommends no single profile for all sandboxed workloads.
5. **Running as non-root is also an image question.** Own guidance: the image needs a numeric non-root user
   (`dockerfile-build-pitfalls` §3.2) or the pod spec needs a `runAsUser` that the image can run under.
6. **`enforce` judges pods, not Deployments.** `audit` and `warn` also look at workload resources, but
   `enforce` applies only to the Pods a controller creates later: a Deployment can be accepted with a
   warning and then sit at zero replicas, the rejection appearing in the ReplicaSet events. Check there.
7. **Exemptions are wider than they look.** An exempt user covers creating Pods directly, not workloads; an
   exempt controller service account exempts everyone who can create that workload kind, which the page
   advises against. Updates that change only metadata (except seccomp or AppArmor annotations),
   `activeDeadlineSeconds` or tolerations skip the check, so a non-compliant running Pod can still take them.
   The page does not say what happens to Pods already running when `enforce` is tightened: test in a scratch
   namespace.

## 3.6 Verify
Apply the pod spec to a test namespace that enforces the Restricted profile and read the admission result;
then remove one control at a time and confirm each removal is rejected.

*Attribution.* Points 3.5.1, 3.5.6 and 3.5.7 also draw on "Pod Security Admission", © The Kubernetes Authors, from
kubernetes/website, licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). Based on "Pod Security Standards", © The Kubernetes Authors, from kubernetes/website,
licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). Changes: rephrased, condensed and
reorganised; the sample spec is our own illustration; no endorsement by the Kubernetes Authors is implied.
