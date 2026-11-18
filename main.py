#!/usr/bin/env python3
"""Entry program for make.fun news-image-20261117.

Drops the competition's front-page image into the grading output
directory and verifies the copy before announcing it.

The picture sums up Tuesday 17 November 2026 in four illustrated
panels: the Gulf clash around Qeshm Island and Bahrain, the Kerch
Bridge hit and the Kyiv bridge strikes, the Shenzhen summit Trump is
heading to, and Nvidia's record quarter. The masthead names the day,
and the strip under it carries the rest of the day's news.
"""
from hashlib import sha256
from pathlib import Path
import os
import sys

IMAGE_NAME = "entry.png"
# Fingerprint of the front page as composed and verified on 2026-11-18.
EXPECTED_DIGEST = "f5608b10ef7a8026e4cd23d849b3cf68043b7f143f5bbf986879ecd0588ec24e"
PNG_SIGNATURE = bytes((0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A))


def source_image():
    return Path(__file__).resolve().parent / IMAGE_NAME


def destination_image():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return Path(out_dir) / IMAGE_NAME


def digest_of(path):
    hasher = sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(65536)
            if not chunk:
                break
            hasher.update(chunk)
    return hasher.hexdigest()


def fail(message):
    print("entry failed: " + message, file=sys.stderr)
    raise SystemExit(1)


def run():
    source = source_image()
    target = destination_image()
    target.parent.mkdir(parents=True, exist_ok=True)
    data = source.read_bytes()
    if data[:8] != PNG_SIGNATURE:
        fail("the entry image is not a PNG file")
    if digest_of(source) != EXPECTED_DIGEST:
        fail("the entry image does not match its verified digest")
    target.write_bytes(data)
    print("entry written to " + str(target) + " (" + str(len(data)) + " bytes)")


if __name__ == "__main__":
    run()
