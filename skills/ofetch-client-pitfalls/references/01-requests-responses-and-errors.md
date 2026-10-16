# ofetch-client-pitfalls §1 — Requests, responses and errors

> Part 1 of `skills/ofetch-client-pitfalls`. Read it when a request or a response is built or parsed. Sourced
> from the README of unjs/ofetch (commit `1dbc37f`, the README of its second major version in alpha), read
> 2026-10-16. Sentences marked "own guidance" are ours.

## 1.1 Bodies and automatic headers
1. **An object body is stringified for you.** An object, or a class with a `.toJSON()` method, passed as `body`
   goes through `JSON.stringify`. A class without `toJSON` must be converted to a string before it is passed.
2. **For POST, PUT and PATCH with a string or object body, ofetch adds `content-type: application/json` and
   `accept: application/json`.** You can override both. Own guidance: a form post, a multipart upload or a
   text body sent as a string needs the right `content-type` set by you or by the body type; check the header
   the server actually received.
3. **Binary and streamed request bodies are supported** (buffers, readable streams and the other body types of
   `fetch`), and ofetch sets `duplex: "half"` for streaming.

## 1.2 Errors
1. **A response with `response.ok` false throws.** The error is a `FetchError` with a message that names the
   method, the URL and the status, and a compact stack that hides the library's internals. The parsed error
   body is on `error.data`.
2. **Catch to read the body:** `await ofetch(url).catch((error) => error.data)` is the README's form. Own
   guidance: a handler that maps errors by status should read the status from the error, not from the message
   text, and should treat a network failure (no response, no status) as a separate branch.
3. **`ignoreResponseError: true` stops the throw** for a bad status, which then arrives as a normal result.
   Use it only for a call whose caller really branches on status; own guidance: such a call must check the
   status itself, since a 500 now looks like data.
4. **`onResponseError` is the interceptor for these** (part 2.3), called when a response arrives with `ok`
   not true.

## 1.3 Parsing the response
1. **JSON is detected and parsed.** For a binary content type ofetch returns a `Blob` instead.
2. **Force a format with `responseType`:** `blob`, `arrayBuffer`, `text` or `stream`. Or give `parseResponse` a
   function, for example one that returns the text as is.
3. **Own guidance:** when the server may send an error page with a JSON status line or an empty body on
   success, name the response type you expect and test those two shapes; automatic detection does the right
   thing for the common case only.

## 1.4 Raw response and native fetch
1. **`ofetch.raw(url)` returns the response object**, for headers and the status, with the parsed body on
   `response._data`.
2. **`ofetch.native(url)` is the platform `fetch`**, with none of the behaviour above. Own guidance: mixing
   both in one client means two error models; keep native calls to the places that need them.

## 1.5 Query and base URL
1. **`query` (alias `params`) adds search parameters** to the URL and keeps those already written in the URL
   itself: `ofetch('/movie?lang=en', { query: { id: 123 } })`.
2. **`baseURL` is prepended and slashes are normalised** (leading and trailing), also when a query is present.
3. **A `Date` or an object in a query value** is the caller's to format. The README's interceptor example sets
   `options.query.t = new Date()`; own guidance: put an explicit string in a query, since how a `Date` is
   written was not read.

## 1.6 Streams and server-sent events
1. **Ask for a stream** and read it with a reader and a `TextDecoder`: the README's SSE example awaits the call,
   gets a stream, calls `getReader()` and decodes each chunk until `done`.
2. **Own guidance:** a chunk is not necessarily one event; keep a buffer and split on the event delimiter
   before parsing, and set a timeout with care because it ends the whole call (part 2.2).

## 1.7 Types are assertions
1. **`ofetch<Article>(url)` types the result and checks nothing.** The README presents it for editor
   assistance. Own guidance: at a boundary with another team or a third party, validate the parsed value with
   a schema before using it, and treat a field that the type calls required but the server omitted as a
   runtime error.

## 1.8 Verify
Call a stub that answers 404 with a JSON body and read `error.data`; call one that answers 204 with no body
and one that returns an HTML error page, and read what the call resolves to; send a body object and read the
two headers the server received.
