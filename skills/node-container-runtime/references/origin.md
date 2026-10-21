# node-container-runtime: origin and source stamps

> Provenance of `skills/node-container-runtime`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and reading, never run on a real service by us. No image was
built and no process was started while writing it.

## Sources (all read 2026-10-08, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| The Node.js Docker image repository's best-practices document | MIT, read 2026-10-08 | The environment variable, init process and PID 1, the exec-form command bypassing the package manager, the `node` user, memory limit flags, the global-prefix trick, multi-stage rule, node-gyp toolchain on Alpine |
| The Docker build documentation on build secrets | official docs, read 2026-10-08 | `ARG` and `ENV` persist in the image; secret mount default path and the build flag |
| The Node.js API documentation (main branch): CLI, process, v8, typescript and events pages | MIT, read 2026-10-08 | Heap flag units and effects, env-file and `loadEnvFile` semantics and versions, type stripping status, supported syntax and removed transform flag |
| The Nest documentation repository: the SWC recipe | MIT, read 2026-10-08 | SWC no type-check, decorator config, circular-import wrapper, plugin limits, ESM and Rspack defaults |
| The maintained tsconfig base presets repository | MIT, read 2026-10-08 | Flag sets for the Node bases, the node-ts and strictest presets |
| One Node-practices note on environment handling | MIT, read 2026-10-08 | The argument that `NODE_ENV` conflates concerns, schema validation at startup, example file |

The share-alike Node best-practice repository was used for no phrasing.

### Second pass, read 2026-10-20 (facts only, rewritten)

| Source | Licence | What it confirmed or corrected |
|---|---|---|
| Node.js API documentation, main branch (`cli`, `process`, `typescript`, `v8` pages) and the Node.js release changelogs for the 22, 24 and 25 lines | MIT (Node.js repository LICENSE read) | All stripping versions in §3.1 (default 23.6.0 and 22.18.0, no warning 24.3.0 and 22.18.0, stable 25.2.0 and 24.12.0, transform flag removed 26.0.0), erasable-syntax list, decorators parse error, `--env-file` versions and precedence, `--env-file-if-exists` 22.9.0, `loadEnvFile` and `NODE_OPTIONS`, `--max-old-space-size` 1536 example, percentage flag precedence; the changelogs date the percentage flag to 24.6.0 and 22.21.0. Corrected §2.3.2 (the `NODE_OPTIONS` caveat belongs to `loadEnvFile`, not to `--env-file`) |
| Node.js Docker image repository, `docs/BestPractices.md` (main) | MIT (LICENSE read) | PID 1 and `SIGINT`, `--init`, `node` user uid 1000, `-m 300M --memory-swap 1G`, `CMD` bypassing npm, global prefix, node-gyp on Alpine, multi-stage |
| Docker documentation, build secrets page (main) | Apache-2.0 (documentation repository LICENSE read) | Build arguments and environment variables persist in the final image, secret mount id and default path, `--secret` flag |
| tini README (master) | MIT (LICENSE read) | An init reaps zombies and makes default signal handlers apply to the process it runs |
| Nest documentation, SWC recipe (master) | MIT (LICENSE read) | `--type-check` and CLI plugins, `decorators`, Jest options, `Relation<>` wrapper, ESM and Vitest defaults, Rspack in Nest 12. Corrected §3.3.2 to §3.3.5 |
| tsconfig bases repository: `node22`, `node24`, `strictest`, `node-ts` | MIT (LICENSE.md read, Microsoft) | Flag sets quoted in §3.4 |

## Rewrite notes
Rules are re-explained principle first. The "headroom" figure restates the Node documentation's own example.
The "one variable per concern" rule and the "never gate security on NODE_ENV alone" rule are the practitioner
argument adopted as our guidance, not a Node fact.

## Not verified
1. **Resolved 2026-10-20:** the release that added `--max-old-space-size-percentage` (24.6.0 and 22.21.0, from the changelogs).
2. **Cgroup awareness:** neither the CLI page nor the `v8` page says whether the default heap limit or the percentage
   follows a container memory limit; the measure-first point of the runtime-config reference still says to measure.
3. **Exit codes** (137, 143) are common knowledge about signals and the container runtime, not from the sources above.
4. **Stripping version numbers** are as in the main-branch pages and the changelogs; a given release line may differ.
5. **Nest 12 claims:** ESM and Vitest defaults and Rspack are the recipe statements, not run; the `.js` import
   extension remark could not be confirmed on the page and was removed from §3.3.5.
6. **Written by us, not sourced:** the verification lists, "pin the base image on purpose", the advice not to use
   `staging` as a `NODE_ENV`, and the "one variable per concern" rule. The practitioner note named in the sources table
   above could not be identified again in this pass and its licence was not re-read, so that row is unconfirmed; a
   web search found no page stating the argument, and no source was opened for it.
7. **Whether `NODE_OPTIONS` inside an `--env-file` is applied before V8 starts** is read only as the page statement
   that such variables are "parsed and applied".

## Related blocks
`devops-conventions` (CI and image policy), `security-hardening`, `nestjs-reliability` (shutdown
behaviour once the signal arrives), `node-async-performance` (heap diagnosis), `typescript-patterns`.
