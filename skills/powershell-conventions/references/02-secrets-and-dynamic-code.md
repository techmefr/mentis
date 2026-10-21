# powershell-conventions §2 — Secrets and dynamic code

Sources: learn.microsoft.com `ConvertTo-SecureString`, `Get-Credential` and `Invoke-Expression` (PowerShell 7.5
documentation set, read 2026-10-08), and the PSScriptAnalyzer rule documentation (tree of 2026-09-22).

## 2.1 Passwords and credentials
1. **A parameter named like a password takes `[SecureString]`, not `[string]`.** The analyser treats `Password`,
   `Pass`, `Passwords`, `Passphrase`, `Passphrases` and `PasswordParam` as such names
   (`AvoidUsingPlainTextForPassword`).
2. **A parameter that carries a user and a secret takes `[PSCredential]`** (`UsePSCredentialType`), obtained from
   `Get-Credential` or the caller, with the secret held as a `SecureString` inside it.
3. **Do not convert a literal or a variable to a `SecureString` with `-AsPlainText`.** The page warns that the
   plain text can end up in event logs and command history, and that the protection does not apply to input
   given this way; the analyser reports it at error severity
   (`AvoidUsingConvertToSecureStringWithPlainText`). Read the secret from a secure channel or with
   `Read-Host -AsSecureString`. Since PowerShell 7, `-Force` is not required with `-AsPlainText`; it is kept for
   older versions.
4. **A `SecureString` is not encrypted on non-Windows systems.** The `ConvertTo-SecureString` page says its contents
   are not encrypted there, while on Windows an exported string with no key is protected by DPAPI. On Linux and macOS treat it
   as an API shape that avoids accidental display, not as protection at rest; the platform rules in
   `security-hardening` §4 still apply.

## 2.2 Dynamic code
1. **Do not pass input to `Invoke-Expression`.** It evaluates a string as a command in the current scope, and the
   page's own caution says to verify anything a user enters and to prefer predefined input options over free-form
   input. A value that came from a file, a parameter or the network is user input.
2. **Call the command directly with the value as an argument**, or build a parameter hashtable and splat it
   (`& $command @arguments`), so the value is data and not syntax. The `about_Splatting` page says a hash table
   passes parameter name and value pairs and an array passes positional values; that a splatted value is never
   re-parsed as code is our inference from that, not a sentence of the page.
3. **A script block built from a string is the same hazard.** The documentation does not say so for each API;
   treat any call that compiles a string into code as `Invoke-Expression` (own guidance).
