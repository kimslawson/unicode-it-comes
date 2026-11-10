"""Readable version of ../zalgo-golfed.py (189 characters).

Gives the same output as ../zalgo.py (apart from the newline after each
chapter), using four tricks to save space:

1. curl URL globbing: "chapter-[1-24]" makes one curl call fetch all 24
   chapters and write them to stdout one after another, so the Python loop
   over chapters isn't needed.
2. os.urandom instead of the random module: each random byte b becomes the
   combining mark U+0300 + (b % 112). (Marks 0-31 are very slightly more
   likely, 3/256 instead of 2/256, which nobody will notice.)
3. print(end=...) for each character instead of building one big string.
4. No "http://": curl uses http by default.
"""
import os
import re

URL = "unicode.org/versions/latest/core-spec/chapter-[1-24]"

html = os.popen(f"curl -L {URL}").read()
text = re.sub(r"<[^>]+>", " ", html)  # every tag becomes a space

for c in text:
    # ord(c) % 8 random bytes, each turned into a combining mark.
    marks = "".join(chr(0x300 + b % 112) for b in os.urandom(ord(c) % 8))
    print(c + marks, end="")
