# react-nextjs-conventions §7 — Next.js

> Section 7 of `skills/react-nextjs-conventions`. Read it when the App Router, a server component, a route handler. The other sections and the guardrails stay in `SKILL.md`.

1. Parallelise independent fetches with `Promise.all` in Server Components: one `await` after another
   creates a network waterfall that's invisible when reading the component top to bottom.
2. `next/dynamic` for any heavy component not needed for the first paint (rich editor, chart, complex
   modal), with `ssr: false` if it depends on the DOM/window.
3. `cookies()`/`headers()`/`draftMode()`/`params`/`searchParams`: always `await` (Next 15+).
4. An error boundary is a Client Component (`'use client'`); `global-error.tsx` wraps `<html><body>`.
5. `route.ts` exports **named** handlers (`GET`, `POST`…), never `export default`.
6. `next/head` is ignored in the App Router: go through the `Metadata` API.
7. No mutable module-level state on the server side (`let`/`var` outside a function): it's shared between
   concurrent requests, i.e. between users.
8. **An exported Server Action is a public endpoint**: it is callable by an unauthenticated client and
   checks authorisation itself. Being imported by one protected page proves nothing.
9. A `GET` handler has no side effect — it gets prefetched and preloaded. A mutation is a `POST`.
