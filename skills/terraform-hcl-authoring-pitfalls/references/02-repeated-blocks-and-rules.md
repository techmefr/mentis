# terraform-hcl-authoring-pitfalls §2 — Repeated blocks and rules

A nested block cannot take `for_each` the way a resource can, so repeating one needs a `dynamic` block, and a rule
set can often avoid nested blocks altogether. The two sources read here disagree on the second point; §2.3 states
the decision.

## 2.1 Dynamic blocks
1. **A `dynamic` block generates repeated nested blocks from a collection**, so the number of blocks follows a
   variable instead of the code. Declare the variable with a typed object (list or map), iterate it with `for_each`,
   and read the current element through `<label>.value` (and `<label>.key` for a map) inside `content` (Terramate).
2. **Do not use `dynamic` for one or two fixed blocks.** Write them out; a dynamic block adds complexity and is only
   worth it when the count or the content varies by input or by environment (Terramate; the OpenTofu `dynamic`
   page says the same: overuse hurts readability, use it to hide details for a reusable module, write blocks out
   literally where possible).
3. **An optional block uses `for_each` over a one-element or empty list.** `cond ? [1] : []` creates the block when
   the condition holds and omits it otherwise; the same shape works for "only if a list of CIDRs was provided"
   with a `length()` test (Terramate).

```hcl
dynamic "restore_to_point_in_time" {
  for_each = var.restore_from_snapshot != null ? [1] : []
  content {
    source_db_instance_identifier = var.restore_from_snapshot
    restore_time                  = var.restore_time
  }
}
```

4. **Key an outer `for_each` by something stable when it holds dynamic blocks.** The source's load-balancer example
   builds a map keyed by listener port (`{ for l in list : l.port => l }`) and puts a `dynamic` block for the
   actions inside; a key that is a position in a list brings back the identity problem of
   `terraform-refactor-identity-pitfalls` §1 (Terramate; the link to that problem is our own).

## 2.2 Nested blocks that repeat per environment
1. **Put the varying part in a typed variable.** Ingress rules, listeners and container lists are inputs; the
   `dynamic` block (or the `for` expression of `terraform-hcl-authoring-pitfalls` §1.1) turns them into blocks, so a
   new rule is a new element and not a code change (Terramate).
2. **A default list of open rules is an input to review, not a safe default.** The source's samples open the web
   ports to every address by default; keep the default empty or closed and require the caller to widen it (our own
   guidance).

## 2.3 Security-group rules: separate resources
1. **Prefer separate rule resources to inline `ingress` and `egress` blocks.** Babenko's security reference lists
   the costs of inline rules: a rule change recreates the whole group (with downtime, in the source's words), mixing
   inline and separate rules on one group makes them conflict and overwrite each other, dynamic rules need complex
   `dynamic` blocks where separate resources take a plain `for_each`, and the rules are buried in the group's state
   where separate resources are tracked one by one (Babenko; the recreate claim is the source's, not tested).
2. **Use the individual rule resources the provider offers.** The source prefers
   `aws_vpc_security_group_ingress_rule` and `aws_vpc_security_group_egress_rule` (AWS provider major version 5 and
   later) and accepts `aws_security_group_rule` as older but still supported. **Version-bound, re-check** against
   the provider version in use (Babenko).
3. **Decision where the sources disagree.** The Terramate dynamic-blocks rule builds a security group's rules with
   `dynamic "ingress"` inside the group; Babenko's reference says to avoid inline rules. Use separate rule
   resources with `for_each` over a keyed map for security groups, and keep `dynamic` for nested blocks that have no
   separate resource, such as a listener's default actions (our own decision from the two sources).
4. **Never mix inline and separate rules on one group** (Babenko).

```hcl
variable "web_ingress" {
  type = map(object({
    port = number
    cidr = string
  }))
}

resource "aws_vpc_security_group_ingress_rule" "web" {
  for_each = var.web_ingress

  security_group_id = aws_security_group.web.id
  description       = each.key
  cidr_ipv4         = each.value.cidr
  from_port         = each.value.port
  to_port           = each.value.port
  ip_protocol       = "tcp"
}
```

5. **Scope egress too.** Babenko's example scopes outbound traffic to the ports needed and notes avoiding an
   all-protocols rule to every address where possible (Babenko).
