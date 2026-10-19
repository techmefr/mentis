# powershell-conventions §1 — Errors

Sources: learn.microsoft.com `about_Error_Handling`, `about_Try_Catch_Finally`, `about_Preference_Variables`
and `about_CommonParameters` (PowerShell 7.5 documentation set, read 2026-10-08), and the PSScriptAnalyzer
rule documentation (tree of 2026-09-22).

## 1.1 Three kinds of error
1. **A non-terminating error reports and carries on.** Cmdlets raise them (a missing file in a list of files);
   the pipeline continues with the next input, and `try`/`catch` and `trap` do not see them by default.
2. **A statement-terminating error stops the current statement and the script goes on with the next one.** Engine
   errors such as an unknown command, a parameter binding failure, and .NET method calls that throw are this
   kind. `try`/`catch` catches them.
3. **A script-terminating error unwinds the call stack** and ends the script unless caught. `throw` and parse
   errors produce them. The names describe scope, not severity, and `try`/`catch` catches both terminating
   kinds.
4. **A script that does not choose escalates nothing.** The default `$ErrorActionPreference` is `Continue`, so
   a failing cmdlet prints a message and the next line runs against whatever state it left.

## 1.2 Making a failure stop the script
1. **Turn a non-terminating error into a terminating one with `-ErrorAction Stop`** on the command, or set
   `$ErrorActionPreference = 'Stop'` for the scope and its child scopes. The command-level parameter wins over the
   variable for that command. A caught escalated error keeps the original in `$_.Exception.ErrorRecord`.
2. **The two are not equivalent.** `$ErrorActionPreference` also applies to statement-terminating errors and can
   silence them, and even `throw`, when set to `SilentlyContinue` or `Ignore`; the `-ErrorAction` parameter
   cannot suppress an error raised with `ThrowTerminatingError()`. A script that sets the variable to
   `SilentlyContinue` anywhere above a `try` removes that `try`'s protection for those errors.
3. **The effect of escalation depends on the scope.** In a function or script block without `[CmdletBinding()]`,
   the variable set to `Stop` produces a script-terminating error. In an advanced function (with
   `[CmdletBinding()]`) the escalated error is only statement-terminating, so execution continues after the
   call. Passing `-ErrorAction Stop` to an advanced function behaves like setting the variable inside it.
   Wrap the whole unit of work in one `try`, and treat the `catch` as the place that stops the script.
4. **Set a preference once, at the top of the script.** The documentation says a preference variable applies to
   the scope it is set in and its child scopes, so a change partway through (or in a shared module) reaches
   every later call (own guidance for where to put it).

## 1.3 Handling
1. **Put one `try` around the whole transaction**, not one per statement, and keep `catch` for recovering,
   logging with `Write-Error` or re-raising with `throw`. An empty `catch` hides the failure, and the analyser
   flags it by default (`AvoidUsingEmptyCatchBlock`).
2. **Use `finally` to release what the `try` acquired.** The documentation says `finally` runs after the `catch`,
   or when no `catch` matched.
3. **A `catch` or `finally` with no `try` is parsed as a command** and fails at run time as an unknown command
   (`MissingTryBlock`, off by default).

## 1.4 Native programs
1. **A native program is not part of the error system.** A non-zero exit code sets `$?` to false and
   `$LASTEXITCODE`, but produces no error record and does not trigger `catch` or `trap`.
2. **Check `$LASTEXITCODE` right after the call**, or set `$PSNativeCommandUseErrorActionPreference = $true`,
   which became stable in 7.4 (experimental in 7.3). A non-zero exit then raises a non-terminating error that
   follows `$ErrorActionPreference`, so with `Stop` it is catchable. The variable defaults to false.
3. **`$LASTEXITCODE` is not changed by cmdlets,** so it can hold a stale value from an earlier native call.
