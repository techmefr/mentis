# go-container-runtime §1 — Image build

Applies to any supported Go version unless a rule names one.

## 1.1 Static binary on a minimal base
1. **Build with cgo off** (`CGO_ENABLED=0`). The reference build template exports it for every build and
   ships the result on a distroless static base image. Own guidance: a binary that links C libraries will
   not run on a base that lacks them, so a project that truly needs cgo chooses its base image for those
   libraries instead of copying this setup.
2. **Put only the binary and the licence files in the final image.** Compile in a build stage or build
   container, and copy the output. Own guidance, following the template, which copies a prebuilt binary
   into the final image.

## 1.2 Licences
**Ship the third-party licences of the dependencies in the image.** The template collects them with a
licence-collecting tool during the build and copies them to `/LICENSES/`. The point is that a binary
statically links its dependencies, so the licence texts travel with it or not at all.

## 1.3 User
1. **Run as a numeric user and group.** The template ends with `USER 65535:65535` and notes in a comment
   that a named user such as `nobody:nobody` would be nicer but the distroless image has no such entries.
2. **Set `HOME` deliberately.** The template sets `ENV HOME=/` next to the user, since a numeric user with
   no passwd entry has no home directory to inherit.

## 1.4 Build flags
1. **`-trimpath`** removes file system paths from the executable; recorded names start with the module path
   and version instead (`go build` flags). The template's older `-gcflags`/`-asmflags` form of the same
   option is the pre-flag spelling; use the flag.
2. **`-ldflags="-s -w"`** omits the symbol table and debug information (`-s`, which implies `-w`) and the
   DWARF table (`-w`) (`cmd/link`). The template applies them to release builds and skips them when a
   `DEBUG` switch is set. Keep an unstripped build path for debugging, not one image tag per mode.

## 1.5 Version stamp
1. **Stamp the version at link time** with `-ldflags "-X <module>/pkg/version.Version=$VERSION"`. The
   linker documents that `-X` sets a **string** variable and only works when the variable is declared
   uninitialised or initialised to a constant string expression, so a version variable assigned from a
   function call is silently left alone.
2. **Fail the build when the version is unset.** The template's build script exits with "VERSION must be
   set" before compiling, and its Makefile derives the value from `git describe --tags --always --dirty`.
3. **Do not rely on the automatic VCS stamp inside an image build.** `-buildvcs=auto` stamps the binary
   only when the main package, its module and the current directory are all in the same repository
   (`go build` flags); a build context without the repository metadata gets no stamp. `go version -m <binary>`
   prints what was embedded. This is a consequence of the documented condition, not something tested.
