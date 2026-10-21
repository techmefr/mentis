# computer-use-agent-pitfalls §1 — Screenshots and coordinates

> Part 1 of `skills/computer-use-agent-pitfalls`. Read it when clicks miss or the capture path is written. Sources:
> the macOS computer-use reference of anthropics/claude-quickstarts (MIT), its image-sizing module and README, read
> 2026-10-20; and, re-read the same day for the points that cite them, Anthropic's computer-use tool, vision and
> vision-coordinates pages, OpenAI's computer-use guides and Google's computer-use page (product documentation,
> facts only). Sentences marked "own guidance" are ours.

1. **The model answers in the picture it was shown.** Its click coordinates are positions in the image the service
   actually looked at, not positions on your screen. Everything below follows from this.
2. **If you send a picture the service considers too large, the service shrinks it again.** The reference notes that
   the vision input has a limit on the long edge and on the total number of tiles; an oversized screenshot is
   resized on the server, and the model then points in a frame you never observed. Anthropic's vision-coordinates
   page adds three details: the token limit can trigger a resize even when neither side exceeds the edge limit (its
   example is a page scan that fits the edge limit and is still shrunk), the service then pads the image on the
   right and bottom up to a multiple of a fixed block size, so normalise by the resized size and not the padded one,
   and the limits depend on the model's resolution tier, so a model switch can reintroduce resizing silently. The
   same page offers a per-image setting that turns an oversized image into a 400 error instead of a silent resize.
   For screenshots returned to its current computer toolset, the tool page says the API does not downscale at all and
   rejects an oversized image with a validation error. So the symptom depends on the path: drift on ordinary
   images, an error on toolset results. Symptom: clicks that are off
   by a consistent fraction, growing toward the far edges, and fine on a small laptop screen but not on a large or
   unusual-ratio display. The limits are the vendor's and change; read them from the current vision documentation
   before relying on any number (not copied here).
3. **Resize before sending, to the largest size that satisfies both limits.** The reference computes that size once
   with the same algorithm the service uses (keep the aspect ratio, fit the long edge and the tile count) and
   returns the input unchanged when it already fits; Anthropic publishes a reference implementation of the same
   computation, to be given the limits of the model tier in use. Own guidance: keep that function in one place and test it on
   a very wide, a very tall and a small image.
4. **Remember the size you sent and scale every answer back.** A point `(x, y)` in the sent image maps to the real
   screen by `x * screen_width / sent_width` and the same for y. Do it in the one place that executes actions, and
   scale zoom regions the same way. After a zoom the model still answers in the coordinates of the full screenshot,
   never in those of the zoomed image (Anthropic computer-use tool page). Symptom of scaling in two places: a double correction that only shows on
   screens that needed resizing.
5. **Check the capture is not too small.** A screenshot below a minimum useful size, or an empty one (a permission
   missing, a locked screen), must not be sent. The reference raises a named error for the too-small case; Anthropic's
   page shows the other half, answering the tool call with an error result that says the capture failed, so the model
   hears about it.
   Own guidance: an all-black capture is the usual sign of a missing screen-recording permission.
6. **Pixels are not points.** On a high-density display the capture is larger than the logical screen the mouse
   library addresses (Anthropic's click diagnosis names the doubled pixel ratio of a retina display). Check: ask for the screen size from the same library that moves the mouse, and scale from the
   capture size to that size, never to the capture's own size.
7. **Zoom is part of the loop.** Small text and small controls are better read from a zoomed region than from a
   downsized full screen; the reference's hosted tool set includes a zoom action by default. Own guidance: a loop
   that cannot zoom will guess at small targets. Anthropic's page says the zoom member is on by default and that an
   environment that cannot produce zoom images should withhold it instead of leaving it enabled and returning errors; its
   troubleshooting table names a missing zoom as a cause of clicks that land in the right area but miss the target.
   Remember point 4: the answer stays in full-screenshot coordinates.
8. **Keep the frame fixed during a run.** Window size, display scale and the browser viewport are set once; the
   reference pins a browser viewport by configuration, and OpenAI's sample fixes the viewport size in its launch
   code. Symptom of changing them mid-run: the model keeps clicking
   where a button used to be.
9. **Test with a known target.** Own guidance: draw a marker at a known position in a picture of an odd size, ask the
   model to point at it, scale back and compare with the true position. The reference ships a small page that
   shows the sent and original images side by side with the point on each, which makes the two spaces visible; build or
   borrow something like it.
10. **Encode for size, not beauty.** The reference sends compressed JPEG screenshots with a configurable quality.
    Own guidance: compression artefacts hurt small text first; raise quality before shrinking further, and look at
    a captured image once as the model sees it.
11. **Read a miss from its pattern.** Anthropic's click diagnosis separates four cases: clicks all offset the same way
    (scaling missing or applied to the wrong size), clicks in the right area but not on the target (a tiny target, detail
    lost to downscaling a very large source, or a distorted aspect ratio: zoom, crop, keep the ratio), the wrong
    element altogether (an ambiguous instruction or look-alike controls: describe the position, split the step), and
    poor accuracy everywhere (resolution too low: try a modest standard size as a baseline). Check the pattern before
    changing the prompt.
12. **Coordinate spaces differ between vendors.** Anthropic's page defines coordinates as pixels of the screenshot you
    returned; Google's computer-use page has the model answer on a normalised thousand-by-thousand grid that your code
    scales to the real viewport. A loop moved from one vendor to another keeps its scaling code and gets every click
    wrong. Check: read the coordinate definition on the vendor's page before porting.
