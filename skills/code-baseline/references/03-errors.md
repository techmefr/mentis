# code-baseline §3 — Errors

> Section 3 of `skills/code-baseline`. Read it when an exception is thrown or caught. The other sections and the guardrails stay in `SKILL.md`.

1. **Never throw a language built-in with a message string** (`Exception`, `RuntimeException`, `Error`,
   `ValueError`). Define a named class that describes the failure and throw that.
2. **The reason is catch-by-type versus catch-by-message.** `catch (UserNotFoundException)` survives a
   refactor; matching on `"user not found"` breaks the day someone improves the wording. It also gives you:
   typed context on the exception (`->userId`, `->validationErrors`, `->retryAfter`) instead of details
   stringified into a message and re-parsed; a clean mapping layer (not-found → 404, validation → 422); a log
   line that reads as a known domain outcome rather than a crash; one greppable name that finds every throw,
   catch, test and mention; and a stable assertion in tests.
3. **A hierarchy** when several failures share a category, so a caller can catch the category or the specific
   case.
4. **Four disguises that don't count.** A single mega-exception with a `code` field (enum-as-exception: it
   loses every benefit above); a catch-and-rethrow that wraps into a generic type (wrap into a *named* one);
   two throws differing only by message; and a project-wide `class AppException extends Exception` that
   everything throws — a rename, not a design.
5. An error crossing a public boundary is part of that boundary's contract, and gets the same care as a
   return type (`python-conventions` §2 for the failures-as-values form).
