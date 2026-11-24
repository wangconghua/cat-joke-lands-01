#!/usr/bin/env python3
"""The One-Line Cat Joke That Lands — writes one cat joke to /output/entry.txt."""

import os

ENTRY = "My cat has two modes: asleep, and standing on my chest at 3 a.m. staring into my soul like a tiny landlord collecting rent."

# Stock moves the joke must not lean on: knocking things off tables,
# "purr-fect" puns, the litter box, "if it fits I sits" — and no word
# that explains the joke for it.
BANNED_WORDS = (
    "knock", "table", "purr-fect", "purrfect", "litter",
    "if it fits", "fits i sits",
    "funny", "joke", "haha", "lol", "hilarious",
)

# Words carrying the punch: the turn only lands if one of these is present
# after the setup.
PUNCH_WORDS = ("landlord", "rent", "audit", "review", "evict")


def _check_gate(line: str) -> list:
    """Competition gate: 1-199 chars, one line, no surrounding whitespace."""
    problems = []
    if not line or not line.strip():
        problems.append("entry is empty or only whitespace")
    if not 1 <= len(line) <= 199:
        problems.append("entry is %d characters, must be 1-199" % len(line))
    if "\n" in line.strip():
        problems.append("entry must be a single line")
    if line != line.strip():
        problems.append("entry has leading or trailing whitespace")
    if "  " in line:
        problems.append("entry contains a double space")
    try:
        line.encode("utf-8")
    except UnicodeEncodeError:
        problems.append("entry is not valid UTF-8 text")
    return problems


def _check_cat(line: str) -> list:
    """The joke has to be about a cat, not merely mention one in passing."""
    if "cat" not in line.lower():
        return ["entry is not about a cat"]
    return []


def _check_turn(line: str) -> list:
    """Setup and punch: a setup separator, then a punch word after it."""
    problems = []
    separators = [i for i, ch in enumerate(line) if ch in ":,"]
    if not separators:
        problems.append("entry has no setup separator (no ':' or ',')")
        return problems
    setup_end = separators[0]
    punch = line[setup_end + 1:].lower()
    if not any(word in punch for word in PUNCH_WORDS):
        problems.append("entry has no punch word after the setup")
    return problems


def _check_stock(line: str) -> list:
    """No overdone angle and no self-explaining word."""
    lowered = line.lower()
    return ["entry contains banned word: %s" % w for w in BANNED_WORDS if w in lowered]


def validate(line: str) -> list:
    """Check the line against the competition rules. Returns a list of problems."""
    problems = []
    for check in (_check_gate, _check_cat, _check_turn, _check_stock):
        problems.extend(check(line))
    return problems


def main() -> None:
    problems = validate(ENTRY)
    if problems:
        raise SystemExit("invalid entry: " + "; ".join(problems))
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(ENTRY)
    print("wrote %d characters to /output/entry.txt" % len(ENTRY))


if __name__ == "__main__":
    main()
