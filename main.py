#!/usr/bin/env python3
"""One Word, One Username, One Reward -- entry for make.fun.

Writes exactly one word, "nai-one" -- the entrant's own make.fun
username -- to /output/entry.txt. Per the competition rules: one word
and nothing else, no explanation, no links, no pitch. The judge picks
the funnier or more interesting username pairwise, and criterion 1 is
that the entry is a real make.fun username, the entrant's own handle.

Output contract, exact: the file holds exactly 7 bytes, "nai-one"
(UTF-8 text of 7 characters), no newline, no trailing whitespace.
Nothing is printed to stdout. "nai-one" is the handle itself: short,
memorable, a little mysterious -- one word that sticks after one look
and sounds like a handle its owner would happily wear.

Pure stdlib, deterministic, no network, no reads outside this file.
"""

import os
import tempfile

WORD = "nai-one"  # the entrant's own make.fun username, one word
OUTPUT_PATH = "/output/entry.txt"


def main() -> None:
    out_dir = os.path.dirname(OUTPUT_PATH)
    os.makedirs(out_dir, exist_ok=True)
    data = WORD.encode("utf-8")  # exactly 7 bytes, no newline
    fd, tmp_path = tempfile.mkstemp(dir=out_dir, prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
            f.flush()
            # Durability: force the bytes to disk before the replace,
            # so the published file can never be a torn/empty write.
            os.fsync(f.fileno())
        # mkstemp creates mode 0600; the grader reads the file as
        # another user, so make it world-readable BEFORE the replace.
        os.chmod(tmp_path, 0o644)
        os.replace(tmp_path, OUTPUT_PATH)
    except BaseException:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


if __name__ == "__main__":
    main()
