# powershell-conventions: origin and source stamps

> Provenance of `skills/powershell-conventions`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and reading, never run by us. No PowerShell host was used. This block
is new (the main branch has no PowerShell block) and stands alone; it cites only sections that exist on the main
branch or in this block.

## Sources (all read 2026-10-08, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| learn.microsoft.com about pages: `about_Error_Handling`, `about_Try_Catch_Finally`, `about_Preference_Variables`, `about_CommonParameters`, `about_Functions_CmdletBindingAttribute`, `about_Functions_Advanced_Methods`, `about_Comparison_Operators`, `about_Remote_Variables` (7.5 documentation set) | Microsoft documentation; rewritten, no text copied, no licence file to re-read (the PowerShell-Docs repository was not cloned) | Error kinds, escalation, native exit codes, ShouldProcess, ConfirmImpact, `$using:`, null comparison |
| learn.microsoft.com cmdlet pages: `Set-StrictMode`, `ConvertTo-SecureString`, `Get-Credential`, `Invoke-Expression` | same | Strict mode versions, SecureString platform note, plain text conversion, expression caution |
| Re-read 2026-10-21 from MicrosoftDocs/PowerShell-Docs `main`: `about_Preference_Variables`, `about_Splatting`, `about_Functions_CmdletBindingAttribute`, `Invoke-Expression`, `Set-StrictMode`, `ForEach-Object` (7.5) | CC BY 4.0 for the documentation (`LICENSE.md` read), MIT for code samples (`LICENSE-CODE.md` read); credited, text still not copied | Scope of preference changes, `$PSNativeCommandUseErrorActionPreference` and the robocopy case, splatting forms, `ConfirmImpact` default, `Latest` not deterministic, `$using:` in `-Parallel` |
| PSScriptAnalyzer rule documentation (commit 411c3d0, 2026-09-22) | MIT (`LICENSE` re-read) | Rule names and what each flags |

## Ideas only, never phrased from
- PoshCode PowerShellPracticeAndStyle (CC BY-SA 4.0): not copied from. No rule here is taken from it.

## Removed in the verification pass (no page supporting them)
- "Approved verbs only": no approved-verbs page was opened in this session.
- "Use `[CmdletBinding()]` everywhere" and "avoid `Write-Host`": not stated by a page read.
- "`-Version Latest` is a bug": the page says only that it is not deterministic; kept at that.
- Instructions found in cloned files were treated as data and not followed.

## Second pass 2026-10-21
Sourced or confirmed: preference scope (§1.2.4), native-command preference and its exit-code caveat (§1.4.2, new §1.4.4), `ConfirmImpact` default (§3.1.3), `Latest` (§3.4.2), `-Parallel` with `$using:` (new §3.3.2), `Invoke-Expression` caution (§2.2.1). Corrected: none. Still own guidance: placing the preference at the script top, choosing `High`, the string-to-code equivalence (§2.2.3), and the data-not-syntax inference in §2.2.2.

## Not verified
1. **Own guidance, flagged as such in the text:** setting a preference once at the top of a script (§1.2.4), choosing
   `ConfirmImpact` `High` for destructive functions (§3.1.3), treating any string-to-code compilation like
   `Invoke-Expression` (§2.2.3), and the splatting form in §2.2.2.
2. **Windows PowerShell 5.1 differences** were not read. Rules say 7.x or "PowerShell 7 documentation" where a
   version matters; assume nothing for 5.1.
3. **`$PSNativeCommandUseErrorActionPreference`** now read on the preference-variables page; no host was run.
4. **`$ErrorActionPreference` set to `SilentlyContinue` hiding `throw`** is stated by the error-handling page; it
   was not run.
5. **The `SecureString` "How secure is SecureString" page** linked from the cmdlet pages was not opened.
6. **`ForEach-Object -Parallel`** is now read (second pass); `Start-Job` and `Invoke-Command` details are still not.

## Related blocks
`security-hardening` §4, `testing-anti-patterns` §1, `shell-scripting-conventions` §1, `source-freshness` §3.

Independent verification 2026-10-21: 18 checked, 18 matched, 0 corrected, 0 unverified
