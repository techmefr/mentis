# react-nextjs-conventions §9 — Security, never negotiable

> Section 9 of `skills/react-nextjs-conventions`. Read it when always, on any diff. The other sections and the guardrails stay in `SKILL.md`.

1. No secret committed. If one is, it's removed **and rotated** — dropping it from the next commit leaves it
   in the history.
2. No hard-coded literal fallback on a secret env variable: fail closed, loudly, at boot.
3. `eval()`/`new Function()` on an untrusted string is forbidden: `JSON.parse` for data.
4. JWT: pin the expected algorithm (`{ algorithms: ['RS256'] }`), never accept `none`.
5. A shell command: never string interpolation, arguments as an array, a strict allowlist.
6. Never an auth token in `localStorage`/`sessionStorage`: an `HttpOnly`, `Secure`, `SameSite` cookie set
   server-side is the only sane option.
