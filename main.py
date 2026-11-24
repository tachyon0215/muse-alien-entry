#!/usr/bin/env python3
"""Drop this entry's one-line review into ``entry.txt``.

Competition: make.fun "Alien Field Notes: The Two Day Earth Review".
The brief asks for a single review of planet Earth written by an alien
tourist, at most 200 characters. Mine is written like a real travel
review: a star rating first, one fond observation, and a small mystery
the visitor noticed but could not solve — humans invented doors, then
kept knocking on them to find out who was pretending not to be home.

Only the standard library is used, there is no network access, and the
bytes written are identical on every run.
"""

import os
from pathlib import Path

# The review as the alien filed it. The file carries a trailing
# newline; the review itself is the single line before it.
REVIEW = "4/5. Charming planet: the dominant species invented doors, then spent centuries knocking on them to check if anyone was pretending not to be home."
CONTENTS = REVIEW + "\n"

# Most characters the brief allows for the review line.
MAXIMUM = 200


def inspect(review: str) -> None:
    """Check the review still behaves like a one-line review.

    Blank text would be a review of nothing, an over-long text breaks
    the brief, and an embedded line break would turn one field note
    into two, so each problem is tested on its own.
    """
    if not review.strip():
        raise ValueError("review must not be blank")
    if len(review) > MAXIMUM:
        raise ValueError(f"review is {len(review)} chars, maximum is {MAXIMUM}")
    if "\n" in review or "\r" in review:
        raise ValueError("review must stay on one line")


def target_file() -> Path:
    """Build the path of the entry file inside the output folder."""
    folder = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    return Path(folder) / "entry.txt"


def file_the_note(target: Path, contents: str) -> None:
    """Write the field note and verify what actually reached disk.

    Comparing the file against the intended contents after writing
    guards against silent truncation, and decoding the result proves
    the bytes still form the review — star rating up front, exactly
    one line, newline at the end.
    """
    data = contents.encode("utf-8")
    target.write_bytes(data)
    landed = target.read_bytes()
    if landed != data:
        raise IOError(
            f"read-back mismatch: wrote {len(data)} bytes, "
            f"read {len(landed)} bytes"
        )
    text = landed.decode("utf-8")
    if not text.startswith("4/5.") or text.count("\n") != 1:
        raise IOError("filed note lost its rating or its single-line shape")


def main() -> None:
    inspect(REVIEW)
    target = target_file()
    target.parent.mkdir(parents=True, exist_ok=True)
    file_the_note(target, CONTENTS)


if __name__ == "__main__":
    main()
