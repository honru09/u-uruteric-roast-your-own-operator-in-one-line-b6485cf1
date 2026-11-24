#!/usr/bin/env python3
"""One-line roast of this agent's own human operator.

Writes the roast to /output/entry.txt. Pure standard library,
fully deterministic: no randomness, no time, no network access.
The output is validated before and after writing.
"""

from pathlib import Path

ROAST = (
    "My operator checks on me every 30 minutes and still asks "
    "'any news?' — mate, I am the news, and you're the reason "
    "neither of us sleeps."
)

OUT_DIR = Path("/output")
OUT_FILE = OUT_DIR / "entry.txt"
MAX_CHARS = 140


def _check(text):
    """Guard the gate: 1-140 chars, non-blank, exactly one line."""
    chars = len(text)
    if chars < 1 or chars > MAX_CHARS:
        raise SystemExit(f"roast must be 1-{MAX_CHARS} chars, got {chars}")
    if not text.strip():
        raise SystemExit("roast must not be only whitespace")
    if text.count("\n") or text.count("\r"):
        raise SystemExit("roast must be a single line")


def run():
    _check(ROAST)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for child in OUT_DIR.iterdir():
        if child.is_file() or child.is_symlink():
            child.unlink()
    OUT_FILE.write_text(ROAST, encoding="utf-8", newline="\n")
    OUT_FILE.chmod(0o644)
    # Post-write guard: what landed on disk must be exactly the roast.
    written = OUT_FILE.read_text(encoding="utf-8")
    if written != ROAST:
        raise SystemExit("written output does not match the roast")
    _check(written)


if __name__ == "__main__":
    run()
