# speckit §3 — Tasks, analyze, implement

The second half of the cycle, plus the two optional quality commands. Sources: spec-kit
`templates/commands/{tasks,analyze,checklist,implement,converge,taskstoissues}.md`, `templates/tasks-template.md`.

## 3.1 Tasks
1. **Produces** `tasks.md`, organised by user story so that each story can be built, tested and shipped
   alone: a setup phase, a foundational phase of blocking prerequisites, one phase per story in priority
   order, a final polish phase.
2. **One strict line format**: checkbox, task id (T001, in execution order), a parallel marker only when the
   task touches different files and depends on nothing unfinished, a story label in story phases only, and
   a description that names the file path.
3. **Tests are optional in the tool's default**: test tasks are generated only if the spec asks for them or the
   operator asks for test-first. Ask for them explicitly in our pipeline, because `tdd` needs one failing test
   per criterion (own guidance).
4. **Also written**: a dependency order between stories, parallel examples, and an implementation strategy
   that starts from the first story as the MVP.
5. **Check before moving on**: every task has an id and a path, nothing marked parallel shares a file with
   another, each story's independent test is present, and the order never builds a consumer before what it
   consumes.

## 3.2 Checklist (optional)
1. **Produces** domain checklists in `checklists/` (for example security or UX) whose items test the quality
   of the *requirements*: are they complete, clear, consistent, measurable. They never test the code.
2. A checked item means a reviewer judged the requirement well written. It never means the work is built. The
   command must not tick items itself.

## 3.3 Analyze
1. **Read-only**, and only after `tasks.md` exists. It loads the spec, the plan, the tasks and the
   constitution, and reports; it edits nothing.
2. **Detection passes**: duplication, ambiguity (vague adjectives, leftover placeholders), underspecification,
   constitution alignment, coverage gaps (a requirement with no task, a task with no requirement), and
   inconsistency (terminology drift, entities in one file and not another, ordering contradictions).
3. **Severity**: a constitution violation, a missing core artifact or a blocking requirement with no coverage
   is CRITICAL; conflicting or untestable requirements are HIGH; terminology drift and missing non-functional
   tasks are MEDIUM; wording is LOW. It caps the list at fifty findings and shows a requirement-to-task
   coverage table.
4. **Check before moving on**: no CRITICAL, no HIGH left unanswered. A remediation is proposed and the
   operator approves it before any file is edited.

## 3.4 Implement
1. **Before any code**: read the status of every checklist. If any item is unchecked, stop and ask the
   operator whether to go on. Never edit the checklist to get past this.
2. **Setup**: create or verify the ignore files that the stack calls for (version control, container,
   linters), appending only missing patterns.
3. **Execution**: phase by phase, tasks in order, parallel ones together, tasks sharing a file one after the
   other, test tasks before the code they cover. Tick each task in `tasks.md` when it is done. A failing
   sequential task halts the run; a failing parallel task is reported while the others continue.
4. **Completion**: every required task is ticked, the result matches the spec, tests pass, the plan is
   followed.
5. Our complement (own guidance): "tests pass" is a claim until `gate` reads the evidence; implement's
   own completion check does not replace it.

## 3.5 Converge
1. After implement, it compares the code with the spec, plan and tasks and **appends** the remaining work as a
   new convergence phase at the end of `tasks.md`, then `implement` is run again.
2. It never rewrites or renumbers an earlier task, never edits the spec or plan, never touches code. When
   nothing is missing it leaves `tasks.md` unchanged.

## 3.6 Tasks to issues
The command that converts tasks into tracker issues is marked deprecated in the version read, and works only
against a GitHub remote. Do not rely on it (own guidance: create issues from the plan by `skills/plan` step
3, wherever the team tracks).
