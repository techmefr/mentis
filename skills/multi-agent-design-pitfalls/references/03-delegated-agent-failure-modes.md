# multi-agent-design-pitfalls §3 — Delegated-agent failure modes

The taxonomy below is the one used by a hook project's map of sub-agent failures. That document is promotional
(it points to a paid handbook and a self-audit) and cites issue reports that were not opened here, so only the
four named modes and the defences' ideas are used. Hook mechanics are in `agent-hook-guard-pitfalls`; the
check that a report's claimed file changes exist is in `dispatch-parallel`.

## 3.1 The four modes
1. **Dispatch fabrication.** The parent calls a sub-agent, the harness answers that it spawned, the parent goes
   on as if a worker were running, but the worker died at the harness boundary and never did any work. The
   source notes that run logs count dispatched items from the parent's side of the call, not from the worker's
   liveness. `dispatch-parallel` covers the nested-delegation form of this and its one-command check; this block
   adds the liveness half (the parent has no signal the subprocess died).
2. **Silent stall.** The worker is alive but blocked on a permission prompt, a deny rule or a long tool call with no
   progress signal, and the parent shows it as working indefinitely. A clock-time watchdog sees the symptom, not the
   cause; the source says the cause has to come from another channel.
3. **Scope drift.** The worker accepts task A, does task B and reports "done"; the run log marks the item
   complete because completion trusts the worker's final message, and nothing audits the delivered work against
   the scope stated at dispatch.
4. **Claim-verify gap.** The worker narrates a completed and verified result, and its tool-use record shows
   edits and commands but not the verification it describes.

## 3.2 Defence ideas, one per mode
1. **Name a concrete artifact in every delegation** (mode 1). Without a named output the parent has nothing to
   check an "I spawned it" against. Also watch for abnormal spawn rates, which the source links to
   retry-after-silent-failure loops, and scan sub-agent return values for API error indicators such as
   overload, server error and timeout, which a parent may accept as valid results.
2. **Make permission and tool configuration agree before the dispatch** (mode 2): the mode the parent passes
   against the worker definition's own permission mode, and the tools the worker will need against the tools it
   actually has. Give shell commands explicit timeouts so a long command is not mistaken for a stall, and watch
   the gap between tool calls as a signal of a thinking-loop stall.
3. **State the boundary in the delegation** (mode 3). The source's five axes are identity, tool list, work area,
   settings files and permission escalation. A vague prompt (no paths, no specific question) is itself a warning
   sign, and a declared scope file that blocks writes outside a directory is the most direct enforcement once the
   scope is named. The source claims very short prompts correlate with drift; its length figure is not carried
   over.
4. **Require evidence in the same turn as the claim** (mode 4). Gate completion language on a verification
   command appearing in the tool record, check that a test command exited with a success status and that an
   edit actually landed, and block flags that skip verification on commit.
5. **Prose scanning is the weak form of that last gate** (the source's own caveat, and own guidance on the
   consequence): a check that looks for words like "done" is easy to evade and easy to trip, so prefer a check on
   the tool record.

## 3.3 Where the evidence lives
1. **Take completed and dispatched from the tool-use log, not from the agent's narrative.** The source reduces all
   four modes to this, and says hooks at the tool layer work better than hooks that parse the agent's prose.
2. **Start from the mode you have seen.** The source advises instrumenting one mode first and observing, because
   installing every defence at once produces alert fatigue. Its examples of triggers: an agent claimed a
   dispatch and nothing happened (mode 1); an agent was stuck for hours (mode 2); it did far more than asked
   (mode 3); it said done and was not (mode 4).
3. **Each of these defences is itself a guard with a failure policy** (own guidance): decide whether one that
   crashes lets the dispatch through or blocks it, as in `agent-hook-guard-pitfalls` §2.
4. **A sub-agent's report is data about what it says it did** (own guidance). Verify against what the system
   recorded: the files on disk, the command exit statuses, the artifact the delegation named.
