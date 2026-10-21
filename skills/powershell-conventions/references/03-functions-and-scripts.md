# powershell-conventions §3 — Functions and scripts

Sources: learn.microsoft.com `about_Functions_CmdletBindingAttribute`, `about_Functions_Advanced_Methods`,
`about_Preference_Variables`, `about_Comparison_Operators`, `about_Remote_Variables` and `Set-StrictMode`
(PowerShell 7.5 documentation set, read 2026-10-08), and the PSScriptAnalyzer rule documentation (tree of
2026-09-22).

## 3.1 State-changing functions
1. **A function whose verb changes state declares `[CmdletBinding(SupportsShouldProcess = $true)]`.** That adds
   `-WhatIf` (list the changes instead of making them) and `-Confirm` (prompt before acting). The analyser flags
   state-changing verbs without it (`UseShouldProcessForStateChangingFunctions`).
2. **Declaring it is not enough: the function must call `$PSCmdlet.ShouldProcess(...)`,** from its `process`
   block, before each change, and act only when it returns true. The analyser flags a declaration with no call
   and a call with no declaration (`ShouldProcess`).
3. **Set `ConfirmImpact` for the function's risk.** The prompt appears only when the function's `ConfirmImpact`
   (default `Medium`) is at or above `$ConfirmPreference` (default `High`). With the defaults a `Medium`
   function does not prompt by itself, so set `High` for destructive operations. The `about_Functions_CmdletBindingAttribute` page confirms the default and the comparison and says to set the argument only together with `SupportsShouldProcess`; choosing `High` for destructive work is our guidance.

## 3.2 Input and parameters
1. **Handle pipeline input in a `process` block.** The function body outside it executes once, while a
   `process` block executes for each object in the pipeline, so pipeline input handled in the body gives
   unexpected results (`UseProcessBlockForPipelineCommand`).
2. **Use named parameters in scripts**, at least from three positional arguments up; a later change to a
   cmdlet's parameter order breaks positional calls (`AvoidUsingPositionalParameters`). Write full cmdlet names
   rather than aliases (`AvoidUsingCmdletAliases`).
3. **Do not assign to automatic variables or name parameters after them.** They hold internal state, and the
   analyser flags it (`AvoidAssignmentToAutomaticVariable`).

## 3.3 Scope and other runspaces
1. **A script block that runs in another runspace or session cannot see the caller's variables.** Pass them with
   the `$using:` scope modifier, which expands to the caller's value, not to the variable
   (`UseUsingScopeModifierInNewRunspaces`). `$using:x = ...` does not work: the value cannot be assigned back.
2. **`ForEach-Object -Parallel` needs `$using:` too.** Its page passes outer variables into each parallel script block
   that way and says some types are not thread-safe even then.
3. **A variable defined in the local session is not defined in a remote one,** so a remote script block that
   uses it without `$using:` reads nothing.

## 3.4 Strict mode and comparisons
1. **Turn strict mode on, at the top of the script, with an explicit version** (`Set-StrictMode -Version 3.0`).
   It makes uninitialised variables, missing properties, method-call syntax for functions and out-of-range
   indexes terminating errors; with it off they quietly yield `$null` or 0. It applies to the scope it is set in
   and its children.
2. **Do not use `-Version Latest` in a script you want to behave the same tomorrow.** The page says its meaning
   changes with new releases, so an older script becomes stricter on a newer host.
3. **Put `$null` on the left of a comparison.** `$null -ne $x` tests whether `$x` is null; `$x -ne $null` with an
   array filters out its null elements and returns the rest.
