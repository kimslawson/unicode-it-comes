"""Readable version of ../zalgo.py (the original 255-character entry).

Downloads the 24 chapters of the latest Unicode core specification, removes
the HTML tags, and turns everything that is left into zalgo text by piling
random combining marks onto every character.
"""
import os
import random
import re

# U+0300..U+036F is the "Combining Diacritical Marks" block: 112 accents,
# overlays and so on that attach to the character before them.
COMBINING_MARKS = range(0x300, 0x370)  # 768..879

SPEC_URL = "http://unicode.org/versions/latest/core-spec/chapter-{}"


def zalgo(text):
    """Follow each character with some random combining marks.

    The number of marks is ord(c) % 8 (0-7): it depends on the character, not
    on chance, so a given letter always gets the same number of marks, but
    which marks it gets is random.
    """
    out = []
    for c in text:
        marks = random.choices(COMBINING_MARKS, k=ord(c) % 8)
        out.append(c + "".join(map(chr, marks)))
    return "".join(out)


for chapter in range(1, 25):
    # curl -L follows the redirect from "latest" to the current version.
    html = os.popen(f"curl -L {SPEC_URL.format(chapter)}").read()
    # Replace every tag with a space. [^>] also matches newlines, so tags that
    # span several lines are removed too. Everything that isn't inside a tag
    # stays, including the page's inline JavaScript and CSS.
    text = re.sub(r"<[^>]+>", " ", html)
    print(zalgo(text))
