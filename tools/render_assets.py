#!/usr/bin/env python3
"""Render assets/banner.html to assets/banner.png (README) and assets/social-preview.png
(GitHub social preview, 1280x640, under 1 MB). Needs Google Chrome or Chromium.

    python3 tools/render_assets.py
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "google-chrome",
    "chromium",
    "chromium-browser",
]


def find_chrome() -> str:
    for candidate in CANDIDATES:
        if Path(candidate).exists() or shutil.which(candidate):
            return candidate
    raise SystemExit("error: Google Chrome or Chromium not found")


def main() -> int:
    chrome = find_chrome()
    target = ASSETS / "social-preview.png"
    subprocess.run(
        [
            chrome,
            "--headless=new",
            "--disable-gpu",
            "--hide-scrollbars",
            "--force-device-scale-factor=1",
            "--window-size=1280,640",
            f"--screenshot={target}",
            (ASSETS / "banner.html").as_uri(),
        ],
        check=True,
        capture_output=True,
    )
    shutil.copyfile(target, ASSETS / "banner.png")
    size = target.stat().st_size
    print(f"wrote assets/social-preview.png and assets/banner.png ({size // 1024} KB)")
    return 0 if size < 1_000_000 else 1


if __name__ == "__main__":
    sys.exit(main())
