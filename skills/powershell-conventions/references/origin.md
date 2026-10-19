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
| PSScriptAnalyzer rule documentation (commit 411c3d0, 2026-09-22) | MIT (`LICENSE` re-read) | Rule names and what each flags |

## Ideas only, never phrased from
- PoshCode PowerShellPracticeAndStyle (CC BY-SA 4.0): not copied from. No rule here is taken from it.

## Removed in the verification pass (no page supporting them)
- "Approved verbs only": no approved-verbs page was opened in this session.
- "Use `[CmdletBinding()]` everywhere" and "avoid `Write-Host`": not stated by a page read.
- "`-Version Latest` is a bug": the page says only that it is not deterministic; kept at that.
- Instructions found in cloned files were treated as data and not followed.

## Not verified
1. **Own guidance, flagged as such in the text:** setting a preference once at the top of a script (§1.2.4), choosing
   `ConfirmImpact` `High` for destructive functions (§3.1.3), treating any string-to-code compilation like
   `Invoke-Expression` (§2.2.3), and the splatting form in §2.2.2.
2. **Windows PowerShell 5.1 differences** were not read. Rules say 7.x or "PowerShell 7 documentation" where a
   version matters; assume nothing for 5.1.
3. **`$PSNativeCommandUseErrorActionPreference`** was taken from the error-handling page; the dedicated page was
   not opened and no host was run.
4. **`$ErrorActionPreference` set to `SilentlyContinue` hiding `throw`** is stated by the error-handling page; it
   was not run.
5. **The `SecureString` "How secure is SecureString" page** linked from the cmdlet pages was not opened.
6. **The splatting and `$using:` rules for `ForEach-Object -Parallel`** were not read; only remote sessions.

## Related blocks
`security-hardening` §4, `testing-anti-patterns` §1, `shell-scripting-conventions` §1, `source-freshness` §3.
