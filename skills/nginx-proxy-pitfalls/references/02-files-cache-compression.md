# nginx-proxy-pitfalls §2 — Files, caching and compression

What the proxy will serve from disk, what it lets other caches keep, and what it compresses.

## 2.1 Files that must not be served
1. **Deny hidden files and directories, except the visible content of `/.well-known/`.** Those files hold
   user preferences or the saved state of a tool and can be as sensitive as `.git` or `.svn` directories.
   `/.well-known/` is the standard (RFC 5785) path prefix for well-known locations, so it stays open
   (h5bp's file-access file).

```nginx
location ~* /\.(?!well-known\/) {
  deny all;
}
```

2. **Deny files that expose sensitive information**, by name pattern. The boilerplate blocks backup and
   source files left by editors, and the extensions `bak`, `conf`, `dist`, `fla`, `inc`, `ini`, `log`, `orig`,
   `psd`, `sh`, `sql`, `swo`, `swp`, a trailing `~`, and names wrapped in `#`.
3. **Extend the pattern to whatever can end up on your production server**: the file's own advice names
   configuration files and project metadata such as dependency lists and build scripts.
4. **Better still, keep such files out of the served tree.** Own guidance: a deny pattern is the second line;
   the first is that the deploy does not put them there.

## 2.2 `Cache-Control` and shared caches
1. **`Cache-Control` controls browsers and shared caches** such as proxies and CDNs (h5bp's cache-control
   file).
2. **`public` lets a shared cache keep a response even when a user session is active.** The file calls
   understanding `public` versus `private` highly recommended. Own reasoning from that sentence: a
   per-user response marked `public` can be served to someone else.
3. **Cache headers are preferably defined by the backend.** The boilerplate says its defaults suit static
   files and simple applications, that backend-level definition is highly preferred, and that incorrect
   directives can leak data or degrade performance.
4. **What the boilerplate's `map` does**, as a worked example: documents (HTML, markdown, calendar) get
   `private, must-revalidate`; a response with no content type gets `no-store`; JSON and XML get no value
   from the map and rely on the expiry file's `epoch`, which nginx sends as `no-cache`; SVG, manifests and
   feeds get `public` variants.
5. **Own reading of that map, a trap to avoid**: its default for any content type the map does not list is
   `public, immutable, stale-while-revalidate`. A per-user download of another type (a generated PDF, for
   example) would therefore be public. List such types explicitly or set the header in the backend.
6. **The `no-cache` directive is skipped in the `map` on purpose**, to avoid it appearing twice: nginx
   `expires epoch` already emits it (the file's footnote).

## 2.3 Expiry
1. **A far-future expiry is only safe with filename-based cache busting.** The boilerplate's default expiry
   is one year, and its comment says that without such versioning you should lower the times to something
   like one week.
2. **HTML, markdown, calendar, JSON and XML are set to `epoch`** in the expiry map so they are revalidated.

## 2.4 The open-file cache
1. **`open_file_cache` caches open file handles, "not found" results and file metadata**, so a popular file
   can be sent at once and a missing one answered with a 404 at once. The boilerplate's values: at most 1000
   entries, released after 20 seconds idle, revalidated every 30 seconds, cached only after two uses.
2. **Defaults** from the core module page: off; `inactive` 60 seconds, validity 60 seconds, a file must be
   used once, and errors are not cached unless `open_file_cache_errors on` is set.
3. **The cost is that the server does not react at once to changes on disk.** Edited files may be truncated
   until the cache refreshes (the file's warning). The file says production servers with stable file
   collections will want it. Own guidance: leave it off where files are rewritten in place.

## 2.5 Compression
1. **Set a minimum length.** The default of 20 bytes usually leads to larger files after gzipping; the
   boilerplate uses 256 (`gzip_min_length`).
2. **Set `gzip_vary on`** so proxies cache both the compressed and the plain version when the client's
   `Accept-Encoding` varies; otherwise a client that cannot decompress could be handed the compressed body
   by its proxy.
3. **`gzip_proxied any` compresses for clients behind proxies** (identified by a `Via` header); the file says
   CloudFront requires it.
4. **List the types to compress.** Only `text/html` is compressed by default (gzip module page); the boilerplate adds text,
   JSON, XML, SVG, fonts, WebAssembly and similar types. Images in compressed formats (PNG, JPEG, WebP) are
   not on its list. Own reading of that list.
6. **`gzip_min_length` is judged from the `Content-Length` header only**, so a streamed response without one is
   not held back by it. **`gzip_proxied` defaults to `off`**, so nothing is compressed for a client behind a
   proxy until you widen it. The module page says only that compressed responses over TLS may be subject to BREACH attacks; our reading of BREACH (own guidance): do not compress a response that mixes a secret token with attacker-influenced text.
5. **Level 5 is the boilerplate's compromise** between size and CPU: it quotes about 75 percent reduction for
   most text, almost identical to level 9. A figure from the file, not measured here.

## 2.6 Verify
Request `/.git/config`, a `.sql` file and a path under `/.well-known/`; the first two must be refused and
the third must follow your intent. Read the `Cache-Control` of an HTML page, an API response and a static
asset, and confirm none is `public` unless it is meant for every visitor.
