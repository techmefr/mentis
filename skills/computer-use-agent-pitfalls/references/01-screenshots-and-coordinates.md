# computer-use-agent-pitfalls §1 — Screenshots and coordinates

> Part 1 of `skills/computer-use-agent-pitfalls`. Read it when clicks miss or the capture path is written. Source,
> read 2026-10-20: the macOS computer-use reference of anthropics/claude-quickstarts (MIT), its image-sizing module
> and README. Sentences marked "own guidance" are ours.

1. **The model answers in the picture it was shown.** Its click coordinates are positions in the image the service
   actually looked at, not positions on your screen. Everything below follows from this.
2. **If you send a picture the service considers too large, the service shrinks it again.** The reference notes that
   the vision input has a limit on the long edge and on the total number of tiles; an oversized screenshot is
   resized on the server, and the model then points in a frame you never observed. Symptom: clicks that are off
   by a consistent fraction, growing toward the far edges, and fine on a small laptop screen but not on a large or
   unusual-ratio display. The limits are the vendor's and change; read them from the current vision documentation
   before relying on any number (not copied here).
3. **Resize before sending, to the largest size that satisfies both limits.** The reference computes that size once
   with the same algorithm the service uses (keep the aspect ratio, fit the long edge and the tile count) and
   returns the input unchanged when it already fits. Own guidance: keep that function in one place and test it on
   a very wide, a very tall and a small image.
4. **Remember the size you sent and scale every answer back.** A point `(x, y)` in the sent image maps to the real
   screen by `x * screen_width / sent_width` and the same for y. Do it in the one place that executes actions, and
   scale zoom regions the same way. Symptom of scaling in two places: a double correction that only shows on
   screens that needed resizing.
5. **Check the capture is not too small.** A screenshot below a minimum useful size, or an empty one (a permission
   missing, a locked screen), must raise, not be sent. The reference raises a named error for the too-small case.
   Own guidance: an all-black capture is the usual sign of a missing screen-recording permission.
6. **Pixels are not points.** On a high-density display the capture is larger than the logical screen the mouse
   library addresses. Check: ask for the screen size from the same library that moves the mouse, and scale from the
   capture size to that size, never to the capture's own size.
7. **Zoom is part of the loop.** Small text and small controls are better read from a zoomed region than from a
   downsized full screen; the reference's hosted tool set includes a zoom action by default. Own guidance: a loop
   that cannot zoom will guess at small targets; implement zoom, and return the zoomed image at its own recorded size.
8. **Keep the frame fixed during a run.** Window size, display scale and the browser viewport are set once; the
   reference pins a browser viewport by configuration. Symptom of changing them mid-run: the model keeps clicking
   where a button used to be.
9. **Test with a known target.** Own guidance: draw a marker at a known position in a picture of an odd size, ask the
   model to point at it, scale back and compare with the true position. The reference ships a small page that
   shows the sent and original images side by side with the point on each, which makes the two spaces visible; build or
   borrow something like it.
10. **Encode for size, not beauty.** The reference sends compressed JPEG screenshots with a configurable quality.
    Own guidance: compression artefacts hurt small text first; raise quality before shrinking further, and look at
    a captured image once as the model sees it.
