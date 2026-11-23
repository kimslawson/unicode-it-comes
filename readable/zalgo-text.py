"""Readable version of ../zalgo-text.py (255 characters).

Like ../zalgo-golfed.py, but it zalgos only the text of the spec instead of
everything in the HTML that isn't a tag, and it keeps paragraph breaks.

What each chapter page looks like:

    <!DOCTYPE html><html><head> ...inline <script> and <style>... </head>
    <body> ...site header and navigation... <main> ...chapter table of contents...
    <hgroup>Chapter 1 Introduction</hgroup> <p>The Unicode Standard is ...</p> ...

The HTML is minified, so it has almost no newlines of its own, and it contains
inline SVG pictures of glyphs, which add a lot of indentation whitespace.
"""
import os
import re

URL = "unicode.org/versions/latest/core-spec/chapter-[1-24]"

html = os.popen(f"curl -L {URL}").read()

# 1. Line breaks. Put a newline before the closing tag of each block element:
#    </div>, </figure>, </figcaption>, </h1>-</h6>, </li>, </p>, </pre>, and
#    the table tags (</td>, </th>, </tr>, ...). Only the first letter of the
#    tag name is checked; the rest of the tag is removed in step 2. Inline
#    tags (</span>, </a>, </i>, </b>, </sub>, </sup>, </code>, </svg>) don't
#    start with any of these letters, so sentences aren't split.
#
#    Side effect: "</thead>" becomes "\n<head>", which is why step 2 can't use
#    "<head>" as its starting point.
html = re.sub(r"</[dfhlpt]", "\n<", html)

# 2. Remove the page code and the tags.
#    - From each chapter's <!DOCTYPE up to (but not including) its <hgroup>
#      title, which covers the <head> with its scripts and styles, the site
#      navigation, and the chapter's table of contents. (?s) lets "." match
#      newlines.
#    - Every other tag, with nothing in its place, so inline tags inside a
#      word don't add stray spaces.
text = re.sub(r"(?s)<!D.*?(?=<hg)|<[^>]*>", "", html)

# 3. Squeeze whitespace: a newline followed by any whitespace (blank lines,
#    SVG indentation) becomes a single newline.
text = re.sub(r"\n\s*", "\n", text)

# HTML entities (&lt;, &amp;) aren't decoded: html.unescape would push the
# golfed version past 256 characters.

for c in text:
    marks = "".join(chr(0x300 + b % 112) for b in os.urandom(ord(c) % 8))
    print(c + marks, end="")
