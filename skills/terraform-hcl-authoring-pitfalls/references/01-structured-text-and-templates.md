# terraform-hcl-authoring-pitfalls §1 — Structured text and templates

A heredoc is a string, and Terraform does not know it is meant to be JSON. A value built as a string is only
validated when the provider or the remote API rejects it, which is at apply time.

## 1.1 Encode, do not concatenate
1. **Do not write JSON, YAML or an IAM policy as a heredoc.** The problems are the same for all three: no syntax
   validation until apply, hard to maintain once the structure grows, interpolation that can break the syntax, and
   no editor help for the structure (Terramate).
2. **Use `jsonencode()` for JSON.** Write the document as an HCL object, with the interpolated values as ordinary
   expressions, so the structure is built by the function and not by string concatenation (Terramate).
3. **Use `yamlencode()` for YAML**, for example the value of a config-map key built from variables (Terramate).
4. **Use a policy-document data source for IAM policies where the provider has one**, and pass its `json` attribute
   to the policy resource: the AWS provider's `aws_iam_policy_document` is the source's example, with several
   `statement` blocks that each take `effect`, `actions` and `resources` (Terramate). For another provider, look for
   the equivalent before falling back to `jsonencode()`.

```hcl
data "aws_iam_policy_document" "reader" {
  statement {
    effect    = "Allow"
    actions   = ["s3:GetObject"]
    resources = ["arn:aws:s3:::${var.bucket_name}/*"]
  }
}

resource "aws_iam_role_policy" "reader" {
  name   = "reader"
  role   = aws_iam_role.app.id
  policy = data.aws_iam_policy_document.reader.json
}
```

5. **Build a list of structured items with a `for` expression inside the encoder.** The source's ECS example turns a
   typed list variable of containers into the JSON container definitions, with nested `for` expressions for the
   port mappings and the environment, instead of repeating a block (Terramate).

```hcl
resource "aws_ecs_task_definition" "app" {
  family = "app"

  container_definitions = jsonencode([
    for container in var.containers : {
      name  = container.name
      image = container.image
      portMappings = [
        for port in container.ports : {
          containerPort = port
          protocol      = "tcp"
        }
      ]
    }
  ])
}
```

## 1.2 Templates and heredocs
1. **Use `templatefile()` for a real template**, a script or a document with variables, with the template in its own
   file under `${path.module}/templates/` and the values passed as a map. Turn a list into a string with `join()`
   before passing it (Terramate).
2. **A heredoc is fine for plain text.** The source allows an indented heredoc (`<<-EOT`) for plain-text
   descriptions, for shell scripts when `templatefile` is overkill, and for multi-line strings without structure,
   such as the instructions in an output (Terramate).
3. **An instance bootstrap belongs in `user_data` with the template rendered by `templatefile()`**, not in a
   provisioner (Babenko; §3.4).
4. **Keep secrets out of what you encode.** An encoded policy or template is still a value in state and in the
   plan. Anything secret that reaches it follows `terraform-state-and-secrets-pitfalls` §2 (our own guidance).
