#!/usr/bin/env python3
"""news-image-20261117 — make.fun entry.

Writes the entry image to the output directory: a one-page front page
summing up the world news of Tuesday 17 November 2026 — the US strike
on Qeshm Island after Iran's drone attacks on the US radar in Bahrain,
Ukraine hitting the Kerch Bridge again while Russia strikes Kyiv's
bridges, Trump heading to Shenzhen for APEC talks with Xi and Putin,
and Nvidia reporting record revenue above $115 billion while refusing
to reinstate Jensen Huang, plus the day's other big stories in the
masthead strip (Gaza winter warning, Ebola in DR Congo, the US losing
its measles-free status).

Deterministic: the same bytes in, the same bytes out. No network,
no timestamps, standard library only. The copy is verified after the
write: the output must start with the PNG magic bytes and match the
source byte for byte.
"""
import hashlib
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
# sha256 of the entry image as built and verified on 2026-11-18.
EXPECTED_SHA256 = "f5608b10ef7a8026e4cd23d849b3cf68043b7f143f5bbf986879ecd0588ec24e"


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    with open(src, "rb") as f:
        want = f.read()
    with open(dst, "rb") as f:
        got = f.read()
    assert got[:8] == PNG_MAGIC, "output is not a PNG"
    assert got == want, "output differs from entry.png"
    assert hashlib.sha256(got).hexdigest() == EXPECTED_SHA256, \
        "output sha256 does not match the verified entry image"
    print("wrote", dst, len(got), "bytes",
          "sha256", hashlib.sha256(got).hexdigest()[:16])


if __name__ == "__main__":
    main()
