r"""Readable version of ../zalgo-text-golfed.py (239 characters).

Like ../zalgo-text.py (255 characters), but with two re.sub calls instead of
three:

1. Remove the page code and every tag except the closing tags of block
   elements (</d.., </f.., </h.., </l.., </p.., </t..). "(?s)" lets "." match
   newlines, so "<.*?>" also removes tags that span lines.
   The page code is cut from "<m" (the first <meta>, before the <title>) to
   the first 'j">' (the end of <hgroup class="svelte-1obhclj">). This depends
   on the site's current markup: if the svelte class name changes, the page
   code shows up in the output.
2. Turn each run of the remaining tags, plus the whitespace after them, into
   one newline.

Unlike zalgo-text.py, newlines that are part of the text itself (in <pre>
code samples) aren't squeezed, so those keep their indentation and get some
blank lines.

The non-raw '\s' makes Python print a SyntaxWarning to stderr when it
compiles the file; the output isn't affected.
"""
import os
import re

URL = "unicode.org/versions/latest/core-spec/chapter-[1-24]"

html = os.popen(f"curl -L {URL}").read()
text = re.sub(r'(?s)<m.*?j">|<(?!/[dfhlpt]).*?>', "", html)
text = re.sub(r"(<.*?>\s*)+", "\n", text)

for c in text:
    marks = "".join(chr(0x300 + b % 112) for b in os.urandom(ord(c) % 8))
    print(c + marks, end="")
