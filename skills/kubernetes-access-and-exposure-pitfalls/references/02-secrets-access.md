# kubernetes-access-and-exposure-pitfalls §2 — Who can read a Secret

A Secret is only as protected as the weakest path to it: an API verb, a pod that mounts it, a manifest in a
repository, or the storage behind the API. The points below are rephrased and condensed from the Kubernetes
page "Good practices for Kubernetes Secrets" (attribution at the end of this file). Whether a workload reads
its secret from a file or from an environment variable, and how rotation reaches the process, are in
`kubernetes-availability-config-pitfalls` §2.3 and are not repeated.

## 2.1 Access to Secret objects
1. **Components**: restrict `watch` and `list` on Secrets to the most privileged, system-level components,
   and grant `get` only if the component's normal behaviour requires it.
2. **Humans**: restrict `get`, `watch` and `list`, including read-only access, and let only cluster
   administrators reach `etcd`. For finer control, such as limiting access by annotation, the page points
   to third-party authorization mechanisms.
3. **`list` on Secrets implicitly lets the subject fetch their contents.** The page puts this in a caution
   box; the same point is in §1.3 here.

## 2.2 A pod that mounts a Secret exposes it
1. **A user who can create a pod that uses a Secret can see the Secret's value**, even when policy does not
   let them read it directly, because they can run a pod that exposes it.
2. **Detect or limit the impact** of Secret data being exposed, on purpose or not: the page recommends
   short-lived Secrets, and audit rules that alert on events such as one user reading several Secrets
   at the same time.
3. **Use separate namespaces to isolate access to mounted Secrets** (the page's one-line advice under
   "Restrict Access for Secrets").

## 2.3 Containers, manifests and what the application does
1. **Give a Secret only to the containers that need it.** In a pod with several containers where one needs
   the Secret, define the volume mount or environment variable on that container only.
2. **Protect the value after reading it.** The application must not log it in the clear or send it to an
   untrusted party.
3. **A Secret manifest with base64 data is readable by everyone who can read the file.** Sharing it or
   committing it to a source repository exposes the value, and the page states that base64 encoding is not
   an encryption method and adds no confidentiality over plain text.

## 2.4 What the cluster stores
1. **Secrets are stored unencrypted in `etcd` by default.** The page tells cluster administrators to
   configure encryption of Secret data at rest.
   The task page adds the traps: with the default `identity` provider nothing is encrypted; the first provider
   in the list encrypts new writes, so `identity` listed first keeps writing plain text, and listed after an
   encrypting provider it only lets the server read old plain-text data; turning encryption on does not
   rewrite existing Secrets, you must replace each one (for example by piping the list of all Secrets
   through a replace) before they are encrypted. KMS v2 is the stable form from v1.29, v1 being deprecated.
2. **If `etcd` runs on several instances, encrypt the traffic between them** with TLS to protect Secret data
   in transit, and consider wiping or shredding the storage of an `etcd` that is no longer in use.
3. **An external secret store can hold the data outside the cluster.** The page names the Secrets Store CSI
   Driver, a DaemonSet that lets the kubelet fetch Secrets from external stores and mount them into the pods
   you authorise; it marks that as third-party content.
4. **Object limits and updates.** A Secret holds at most 1 MiB. `immutable: true` cannot be reverted and
   means delete and recreate, then restart the pods that kept the old mount; it also relieves the API
   server. A Secret mounted as a volume updates after a delay of up to the kubelet sync period plus the
   cache delay, and never through a `subPath` mount; the page describes automatic updates for volumes only.
   Legacy service account token Secrets are long-lived and non-expiring: prefer short-lived tokens from the
   TokenRequest API (since v1.22).

## 2.5 Verify
With `kubectl auth can-i list secrets` as each subject, in each namespace, confirm that only the intended
components and administrators can. Search repositories for `kind: Secret` manifests with a `data` or
`stringData` block. Confirm in a multi-container pod that each Secret appears only where it is used.

*Attribution.* The encryption traps and point 2.4.4 are based on "Encrypting Confidential Data at Rest" and
"Secrets", © The Kubernetes Authors, from kubernetes/website, licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). Also based on "Good practices for Kubernetes Secrets", © The Kubernetes Authors, from
kubernetes/website, licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). Changes:
rephrased and condensed; no endorsement by the Kubernetes Authors is implied.
