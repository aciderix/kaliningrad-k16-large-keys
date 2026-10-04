#!/usr/bin/env python3
"""Extract the preregistered 979-letter K16 stream from transcription v1."""
from pathlib import Path
import re
import unicodedata

source = Path("data/transcription_v1.txt").read_text(encoding="utf-8")
letters: list[str] = []
for line in source.splitlines():
    match = re.match(r"L\d+\s+(.*)", line)
    if not match:
        continue
    body = match.group(1).split("#", 1)[0]
    ascii_body = unicodedata.normalize("NFKD", body).encode("ascii", "ignore").decode("ascii")
    letters.extend(char.lower() for char in ascii_body if char.isalpha())

stream = "".join(letters)
if len(stream) != 984 or not stream.endswith("eimat"):
    raise SystemExit(f"Expected 984 letters ending in eimat, got {len(stream)} ending {stream[-10:]!r}")

Path("data/ciphertext_979.txt").write_text(stream[:-5] + "\n", encoding="ascii")
print("Wrote 979 letters; excluded final eimat as specified by the K16 protocol.")
