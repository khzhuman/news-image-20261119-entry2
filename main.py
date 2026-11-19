"""Hand the finished front page to the scorer, byte for byte.

entry.png beside this file is the whole entry: one picture that tells
Thursday 19 November 2026 — 15 stories drawn, 18 briefs, a region strip, a
pin map and a date-check box. The scorer runs this program twice and
expects identical bytes both times, so the program does one deterministic
thing: copy the image, then verify the copy's hash against the source so a
truncated copy can never slip through quietly.
"""

import hashlib
import os
import shutil
import sys
from pathlib import Path

SOURCE = Path(__file__).with_name("entry.png")
# In the grader the writable output dir is /output; outside it the env var
# stands in for /output (same convention as the kit's starter program).
DEST_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
DEST = DEST_DIR / "entry.png"


def sha256_of(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 16), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    DEST_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE, DEST)
    if sha256_of(SOURCE) != sha256_of(DEST):
        print("ERROR: copied bytes differ from entry.png", file=sys.stderr)
        sys.exit(1)
    print(f"copied entry.png -> {DEST} ({DEST.stat().st_size} bytes, sha256 verified)")


if __name__ == "__main__":
    main()
