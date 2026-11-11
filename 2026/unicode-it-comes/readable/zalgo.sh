#!/bin/sh
# Readable version of ../zalgo.sh (177 characters).
#
# Same text as ../zalgo-text-golfed.py, done with curl piped into Perl.
#
# curl options:
#   -f   fail on HTTP errors: if a chapter comes back as an error page (404,
#        503, rate limit...), nothing is written for it and curl prints the
#        error to stderr, instead of the error page ending up in the book
#   -L   follow redirects ("latest" redirects to the current version)
#
# The golfed version writes the URL as chapter-\[1-24] with the first bracket
# escaped. zsh would otherwise take [1-24] as a glob and fail with "no matches
# found"; with the backslash, sh, bash and zsh all pass chapter-[1-24] to curl,
# which expands the range itself. (Quoting the URL, as here, costs 2 bytes.)
#
# Perl options:
#   -CS  read stdin and write stdout as UTF-8, so the script works on
#        characters, not bytes (otherwise marks land inside multi-byte
#        characters)
#   -0   read the whole input at once (the record separator is NUL, which
#        the HTML doesn't contain)
#   -p   print $_ when the script is done
#
# The last substitution has no /s flag, so "." doesn't match newlines and
# newlines get no marks. The Python versions put ord("\n") % 8 = 2 marks
# after each newline, so the output differs only there.

curl -fL 'unicode.org/versions/latest/core-spec/chapter-[1-24]' | perl -CS -0pe '
  # Page code (from the first <meta> to the end of <hgroup class="svelte-1obhclj">)
  # and every tag except closing tags of block elements. /s: "." matches newlines.
  s#<m.*?j">|<(?!/[dfhlpt]).*?>##gs;

  # Each run of the remaining tags, plus the whitespace after them, becomes
  # one newline.
  s/(<.*?>\s*)+/\n/g;

  # After each character ($&), add ord & 7 (= ord % 8) random marks from
  # U+0300..U+036F. pack "U*" turns code points into characters; rand 112 is
  # truncated to a whole number.
  s/./$&.pack "U*", map { 768 + rand 112 } 1 .. ord($&) & 7/ge;
'
