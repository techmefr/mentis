# dotnet-container-runtime §1 — Image build

Applies to the official .NET 8 and later images.

## 1.1 Stages
1. **Build in the SDK image and run in the runtime image.** The final stage uses `aspnet` (or `runtime`
   for a worker) and copies only the published output; do not use the SDK image as the final stage. This is
   our own guidance following the multi-stage pattern in the official samples.
2. **Copy the project files first and restore, then copy the sources and build.** The restore layer stays
   cached until a dependency changes. This is our own guidance.
3. **Pin the base image tag on purpose** (major version and variant) and rebuild on a schedule, so patches
   still arrive. This is our own guidance.

## 1.2 User and port
1. **Run as the non-root user.** The official images expose its id in `$APP_UID`; the documented pattern is
   `USER $APP_UID` in the final stage.
2. **From .NET 8, ASP.NET Core apps in the official images listen on port 8080 by default,** not 80. Map the
   host port to 8080 (`-p 8000:8080`), and set the port through the image's `ASPNETCORE_HTTP_PORTS` rather
   than mapping 80 back in.
3. **Make the data directory writable for that user** and nothing else. This is our own guidance.

## 1.3 Architectures
**Run the SDK stage on the build machine's platform and let Docker build the final stage for the target:**
`FROM --platform=$BUILDPLATFORM ...sdk... AS build`. The SDK then runs natively on the build machine, and
the platform you pass to the build selects the final image. Do not copy a platform-specific publish into an
image of another architecture.

## 1.4 Certificates and secrets
1. **Do not create a development certificate in an image planned for redistribution.** The ASP.NET Core
   documentation says this can lead to spoofing and elevation of privilege; set
   `DOTNET_GENERATE_ASPNET_CERTIFICATE` to `false` before the CLI first runs, and supply a real
   certificate or terminate TLS in front of the container (`dotnet-aspnet-efcore-pitfalls` §2.4).
2. **Do not put a secret in `ARG`, `ENV` or a copied file.** This is our own guidance; see the equivalent
   rule in `node-container-runtime`.

## Verification
- `docker run` the image and confirm the process user is not root and the app answers on 8080.
- `docker history` shows no SDK layer in the final image and no secret.
- Change one source file and rebuild: the restore layer is reused.
