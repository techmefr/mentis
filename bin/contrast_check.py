#!/usr/bin/env python3
"""Contrast ratio of two sRGB colours, computed rather than judged by eye.

    python3 bin/contrast_check.py '#1a1a1a' '#ffffff'

Formula: relative luminance and contrast ratio as defined in WCAG 2.2 (W3C), success criterion 1.4.3
and the definitions of "relative luminance" and "contrast ratio". Prints the ratio only; the threshold
that applies comes from the standard, never from this script (skills/source-freshness).
"""
import sys


def parse(color):
    h = color.strip().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    if len(h) != 6:
        raise ValueError(f"not a hex colour: {color!r}")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def channel(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def luminance(color):
    r, g, b = (channel(c) for c in parse(color))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(foreground, background):
    hi, lo = sorted((luminance(foreground), luminance(background)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("usage: contrast_check.py FOREGROUND BACKGROUND (hex colours)")
    print(f"{ratio(sys.argv[1], sys.argv[2]):.2f}")
