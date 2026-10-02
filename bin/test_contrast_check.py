#!/usr/bin/env python3
"""Checks for bin/contrast_check.py. No network, nothing installed:

    python3 bin/test_contrast_check.py

The cases pin the two places a hand-rolled implementation goes wrong: the 0.04045 knee of the sRGB
transfer curve (a common typo is 0.03928, which shifts dark greys) and the order of the operands.
"""
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import contrast_check as cc

ok = fail = 0


def check(label, cond):
    global ok, fail
    if cond:
        ok += 1
        print(f"PASS  {label}")
    else:
        fail += 1
        print(f"FAIL  {label}")


check("black on white is 21:1", abs(cc.ratio("#000", "#fff") - 21.0) < 1e-9)
check("identical colours are 1:1", abs(cc.ratio("#777777", "#777777") - 1.0) < 1e-9)
check("operand order does not matter", cc.ratio("#123456", "#fedcba") == cc.ratio("#fedcba", "#123456"))
check("short hex expands", cc.luminance("#abc") == cc.luminance("#aabbcc"))
check("grey 767676 on white is just above 4.5", 4.5 < cc.ratio("#767676", "#ffffff") < 4.6)
check("grey 777777 on white is just below 4.5", 4.4 < cc.ratio("#777777", "#ffffff") < 4.5)
check("channel below the knee is linear", abs(cc.channel(0.04) - 0.04 / 12.92) < 1e-12)
check("channel above the knee is gamma-decoded", abs(cc.channel(0.5) - 0.21404114) < 1e-6)

try:
    cc.parse("#12")
    check("a malformed colour is refused", False)
except ValueError:
    check("a malformed colour is refused", True)

r = subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "contrast_check.py"),
                    "#000000", "#ffffff"], capture_output=True, text=True)
check("the command line prints the ratio", r.returncode == 0 and r.stdout.strip() == "21.00")

print(f"\n{ok} passed, {fail} failed")
sys.exit(1 if fail else 0)
