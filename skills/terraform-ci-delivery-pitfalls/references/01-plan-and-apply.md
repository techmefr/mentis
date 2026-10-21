# terraform-ci-delivery-pitfalls §1 — Plan and apply

The point of a review is that the thing approved is the thing executed. A pipeline that plans twice has two things.

## 1.1 One reviewed plan
1. **Plan and apply are separate jobs.** The plan job produces a plan file and a JSON rendering for review and
   policy; the apply job runs later, behind an approval (terrashark).
2. **The apply job consumes the exact plan file that was reviewed** (`terraform apply plan.bin`), not a fresh
   `plan`. A plan re-run inside the apply job is listed as a model mistake in both sources (terraform-skill;
   terrashark).
3. **The sources disagree with themselves on this.** terrashark states the rule, and one of its GitHub templates
   downloads the stored artifact in the apply job, while another of its templates re-runs `plan` there. The rule is
   stated here; the second template is not a pattern to copy.
4. **Passing a saved plan file is the approval.** The OpenTofu command reference says applying a saved plan runs
   its actions without a prompt, that `-auto-approve` is ignored for it (so the sources' templates need no such flag
   there), that planning options cannot be added at apply time and that ephemeral variables must be passed again.
   Conversely, `-input=false` on an apply of a new plan blocks the approval prompt and the run fails rather than
   proceeding. The same page does not say what happens if the state changed between the plan and the apply, and
   no claim is made here about it; check the documentation of the tool and version in use.
5. **Plan and apply on different events** (a plan on a pull request, an apply on a push to the default branch)
   make the artifact's lifetime a problem across events. terrashark's note: keep plan and apply in one workflow
   run, or store the plan outside the CI artifact store (it mentions signed plan storage) when "apply the reviewed
   pull request plan" is a hard requirement.

## 1.2 Plan files are sensitive
1. **Plan files and state exports can carry secrets**, so artifact retention and access are restricted, not left
   at the platform default (terrashark; terraform-skill). The OpenTofu references agree: a saved plan holds the
   full configuration, planned values and input variables, with sensitive data in cleartext unless plan encryption
   is on, and `show -json` prints sensitive values in plain text (hidden only in the human-readable form).
2. **Retention is short.** terrashark's GitLab template uses `expire_in: 24h` and terraform-skill's uses one week;
   both are one source's value, so choose the shortest period that still spans the review and approval.
3. **Raw plan JSON does not go to broadly readable CI logs or artifacts**, and sensitive outputs or connection
   strings do not go to pull request comments (terrashark; terraform-skill).
4. **Keep the JSON rendering for the policy engine** (its use in the sources' templates, §2.1) and let people read
   the human plan: the JSON form is the one that prints sensitive values in plain text (OpenTofu `show` page).
5. **Search the exported plan JSON for secret fields before sharing the artifact** (terrashark). Why a value ends
   up there at all is in `terraform-state-and-secrets-pitfalls` §2.

## 1.3 Shape of the two jobs
```yaml
plan:
  stage: plan
  script:
    - terraform init
    - terraform plan -out=plan.bin
    - terraform show -json plan.bin > plan.json
  artifacts:
    paths:
      - plan.bin
      - plan.json
    expire_in: 24h

apply:
  stage: apply
  when: manual
  allow_failure: false
  script:
    - terraform init
    - terraform apply plan.bin
  dependencies:
    - plan
```
This follows terrashark's GitLab layout: the apply job re-initializes and applies the stored `plan.bin`, and a
manual job is the approval gate. The policy stage in between is in §2.1.
