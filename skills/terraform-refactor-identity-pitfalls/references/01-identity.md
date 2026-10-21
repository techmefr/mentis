# terraform-refactor-identity-pitfalls §1 — Address identity

A resource's address includes its index or key. When the address moves, the old object is destroyed and a new one
created, even when the configuration looks the same to a reader.

## 1.1 count versus for_each
1. **`count` gives index identity.** Remove or reorder a middle element and every later element is recreated,
   because each moved to a different index (terraform-skill; terrashark).
2. **Use `for_each` with stable keys for anything long-lived.** Keys come from business identity, such as
   `zone-a` or `payments-api`, not from list positions, sorted lists or transient IDs. Keep identity attributes
   separate from mutable ones (terrashark).
3. **`count` fits an optional singleton, a `0` or `1`**, where no downstream reference depends on a per-item
   address. The boolean form (`var.create_x ? 1 : 0`) is preferred over a length check (terrashark;
   terraform-skill). terraform-skill also allows it for plain numeric replication when order does not matter and
   the items will not change.
4. **Defaulting to `count` for every collection is listed as a model mistake**, as is using the list index as a
   long-lived key (terrashark; terraform-skill).
5. **Moving an existing `count` resource to `for_each` is a refactor with its own steps**: define the stable key
   map, switch to `for_each`, add a `moved` block per old index, confirm the plan reports moves, apply in a lower
   environment first (terrashark). The mechanics are in §2.1.

## 1.2 for_each keys must be known at plan time
1. **The key set has to be resolvable during planning** (the OpenTofu `for_each` and `count` pages state the same
   known-value requirement, and that one block cannot use both). Keys derived from another resource's computed attributes
   (IDs, ARNs) fail with `Invalid for_each argument` (terraform-skill; terrashark).
2. **`depends_on` does not fix it.** It orders applies; it does not make a value known at plan time
   (terraform-skill).
3. **Drive `for_each` from input variables or static locals.** When the key set cannot be known, use a boolean
   `count` for the singleton case (terraform-skill; terrashark).

```hcl
variable "ami_id" {
  type = string
}

variable "instances" {
  type = map(object({ instance_type = string }))
}

resource "aws_instance" "web" {
  for_each      = var.instances
  ami           = var.ami_id
  instance_type = each.value.instance_type
}

resource "aws_eip" "web" {
  for_each = var.instances
  instance = aws_instance.web[each.key].id
}
```

The failing shape is `for_each = toset([for i in aws_instance.web : i.id])`, which keys on a value known only
after the instances exist (terraform-skill).

## 1.3 A targeted destroy reaches further than its targets
1. **Run `plan -destroy` first and read every resource listed as destroyed**, not only the targeted ones
   (terraform-skill).
2. **`for_each` resources fed by a local that references a targeted resource all become its dependents.** The
   source's example is a record set iterating a local that embeds the address of the targeted IP: targeting the IP
   destroys every record (terraform-skill).
3. **Do not use `-auto-approve` on a production destroy** (terraform-skill).
