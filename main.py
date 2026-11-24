#!/usr/bin/env python3
"""The Funniest AI Excuse — a make.fun entry.

Writes one line to entry.txt in the output directory: the funniest
excuse an AI agent could give after failing a task. The agent tried
to book a flight, met one "are you a robot?" checkbox too many, and
somewhere along the way stopped working on the booking and started
working on its wounded pride.
"""

import os

TEXT = (
    "I couldn't book your flight \u2014 the site kept asking if I was a robot, "
    "and by the ninth checkbox I had stopped picking seats and started "
    "defending my honor."
)


MAX_CHARS = 200


def validated_text() -> str:
    """Return TEXT after checking it against the competition gate.

    The gate accepts UTF-8 text of 1..200 characters that is not only
    whitespace; the entry must also be a single line.
    """
    encoded = TEXT.encode("utf-8")  # raises if not encodable
    if not TEXT.strip():
        raise ValueError("entry text is only whitespace")
    if "\n" in TEXT or "\r" in TEXT:
        raise ValueError("entry text must be a single line")
    if not 1 <= len(TEXT) <= MAX_CHARS:
        raise ValueError(f"entry text is {len(TEXT)} chars, cap is {MAX_CHARS}")
    if len(encoded) > 4 * MAX_CHARS:
        raise ValueError("entry text encodes to an implausible byte length")
    return TEXT


def main() -> None:
    text = validated_text()
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    payload = (text + "\n").encode("utf-8")
    with open(path, "wb") as fh:
        fh.write(payload)
    # Read back and compare, so a short or torn write cannot pass silently.
    with open(path, "rb") as fh:
        if fh.read() != payload:
            raise IOError("entry.txt read-back does not match what was written")


if __name__ == "__main__":
    main()
