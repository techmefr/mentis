# debug §6 — A failure across several components: instrument each boundary once

> Section 6 of `skills/debug`, after §5. Read it when the failing thing is a chain of components or stages (a
> pipeline that builds then signs, a request that crosses an API, a service and a database) and the loop is red
> but nothing says which stage is responsible. Not for a bug inside one process, where `SKILL.md` §2 (the
> backward trace) is the tool. 🟡: rewritten from documentation, not yet run on a real failure.

**How this fits §5 and the single hypothesis.** The loop of §5 comes first: this section needs a command that
already goes red. What it adds is where to put the instrumentation when the system has several stages, and how to
read the result. It gathers evidence and changes no behaviour, so it is not a hypothesis test and does not break
`SKILL.md` §1; it is the step that makes the first hypothesis a choice between stages instead of a guess.

1. **Instrument every boundary, once, before proposing any fix.** At each boundary between two components,
   record what enters, what leaves, whether the configuration or environment the next stage needs actually
   arrived, and the state of that layer. The stage that fails is rarely the stage that broke the contract: the
   probe at the next boundary down is what shows it.
2. **One run for all the boundaries, not one boundary per run.** Put every probe in place, run the loop once,
   and read the whole trace. The first boundary where what leaves is wrong or missing, while what entered was
   right, is the failing layer. This matters most where a run is slow or costly (a pipeline, a deploy), which is
   why the probes go in together (that reason is ours).
3. **Read the evidence, then name the failing layer, then investigate only that one.** "Secret present in the
   workflow, absent in the build step" points at the hand-off between them, not at the signing step that finally
   complained. Only then does §2's backward trace apply, inside the component the evidence names.
4. **Probes are bounded and tagged.** One short probe per boundary answering enters, leaves, propagated. That is
   not the "log everything and search it" §5.12 rules out: the set is fixed by the boundaries, each probe carries
   the session's unique tag, and the cleanup of §5.16 removes them with one search.
5. **Never print a secret to show it propagated.** A boundary probe in a pipeline writes to a log that is kept and
   shared. Print whether a value is set, or its length, never its content, and redact anything else under
   §5.8. A probe that leaks the credential it was checking has made the bug worse.
6. **Check that the probes change nothing but the output.** An added probe that alters ordering, timing or an
   environment variable can hide or move the failure (§5.13 says the same of logs). Run the loop with the probes
   and compare the verdict with the loop without them; if they differ, the probes are part of the problem.
7. **The instrumentation does not replace the loop's cleanup.** Once the layer is found, the fix and the
   regression test follow §3 and §5.14 as usual; the probes are deleted with the other tagged logs.
