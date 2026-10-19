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

## Rewrite notes
Rules are re-explained principle first. The "headroom" figure restates the Node documentation's own example.
The "one variable per concern" rule and the "never gate security on NODE_ENV alone" rule are the practitioner
argument adopted as our guidance, not a Node fact.

## Not verified
1. **`--max-old-space-size-percentage`**: the version it was added in was not found in the documentation read.
2. **Cgroup awareness**: the Node documentation read does not say whether the default heap limit or
   `heap_size_limit` follows a container memory limit; §1 says to measure.
3. **Exit codes** (137, 143) are common knowledge about signals and the container runtime, not from the
   sources above.
4. **The stripping version numbers** are as in the Node main-branch docs; a given release line may differ.
5. **SWC and circular-import behaviour**, and "newer Nest projects generate ESM and Vitest", are from the
   Nest 12 docs and were not run.
6. **Written by us, not sourced:** the verification lists, "pin the base image on purpose", and the
   advice not to use `staging` as a `NODE_ENV`.

## Related blocks
`devops-conventions` (CI and image policy), `security-hardening`, `nestjs-reliability` (shutdown
behaviour once the signal arrives), `node-async-performance` (heap diagnosis), `typescript-patterns`.
