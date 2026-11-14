#!/usr/bin/env python3
"""Write the bundled JPEG image to the make.fun output directory."""

import base64
import os
from pathlib import Path


MAX_BYTES = 1_048_576
JPEG_START = b"\xff\xd8\xff"
JPEG_END = b"\xff\xd9"


def main() -> None:
    source = Path(__file__).resolve().parent / "entry.png.b64"
    encoded = source.read_text(encoding="ascii").strip()
    image = base64.b64decode(encoded, validate=True)

    if not image.startswith(JPEG_START):
        raise ValueError("Invalid image: decoded bytes do not start with a JPEG signature.")
    if len(image) > MAX_BYTES:
        raise ValueError(f"Decoded image exceeds the {MAX_BYTES}-byte limit.")
    if not image.endswith(JPEG_END):
        raise ValueError("Decoded data does not end with a JPEG end marker.")

    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    # make.fun may provide a fresh output path for each run.
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "entry.png").write_bytes(image)


if __name__ == "__main__":
    main()
