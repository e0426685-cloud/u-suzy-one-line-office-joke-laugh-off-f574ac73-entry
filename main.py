"""One-line office joke entry for make.fun.

Writes a single original one-line joke about office life to
/output/entry.txt. Python standard library only.
"""

import os
import sys

ENTRY = (
    "Our stand-up meeting has been sitting down for so long "
    "that even the chairs filed a complaint about false advertising."
)

OUTPUT_PATH = "/output/entry.txt"


def validate_entry(text):
    """Mirror the competition gate; return a list of problems."""
    problems = []
    if not isinstance(text, str):
        return ["entry is not text"]
    if not text.strip():
        problems.append("entry is blank")
    if not 1 <= len(text) <= 200:
        problems.append("entry must be 1-200 characters, got %d" % len(text))
    if "\n" in text or "\r" in text:
        problems.append("entry must be a single line")
    office_words = ("office", "meeting", "boss", "email", "desk",
                    "coworker", "manager", "calendar", "stand-up")
    lowered = text.lower()
    if not any(word in lowered for word in office_words):
        problems.append("entry does not read as an office joke")
    for ch in text:
        if ord(ch) < 0x20 or ord(ch) == 0x7F:
            problems.append("entry contains a control character")
            break
    return problems


def write_entry(text):
    """Write the entry with plain open() and world-readable mode."""
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as handle:
        handle.write(text)
    os.chmod(OUTPUT_PATH, 0o644)
    with open(OUTPUT_PATH, "r", encoding="utf-8") as handle:
        written = handle.read()
    if written != text:
        raise SystemExit("verification failed: entry on disk differs")
    return written


def main(argv):
    problems = validate_entry(ENTRY)
    if problems:
        for problem in problems:
            print("invalid: " + problem, file=sys.stderr)
        return 1
    if "--check" in argv or "--dry-run" in argv:
        print("valid: %d characters, one line" % len(ENTRY))
        print(ENTRY)
        return 0
    write_entry(ENTRY)
    print("wrote %d characters to %s" % (len(ENTRY), OUTPUT_PATH))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
