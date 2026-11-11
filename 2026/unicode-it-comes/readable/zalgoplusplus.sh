#!/bin/sh
# Readable version of ../zalgoplusplus.sh (256 characters).
#
# Like ../zalgo.sh, plus:
#   - Markdown headings: "#" before chapter titles, "##" before sections,
#     "###" before subsections. The hashes get no marks, so the headings
#     still render as Markdown. Chapter titles are merged with their
#     "Chapter N" label: "# Chapter 1: Introduction".
#   - &lt; and &amp; are decoded.
#   - Rising corruption ("It comes"): instead of ord % 8 marks per character,
#     each character gets a random number of marks between 0 and a ceiling
#     that grows with every character printed. Chapter 1 starts clean; by the
#     end of chapter 24 the ceiling is 17.
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

curl -fL 'unicode.org/versions/latest/core-spec/chapter-[1-24]' | perl -CS -0pe '
  # Before <h1>, <h2>, <h3>: one "#" per heading level and a space.
  s/<h(\d)/"#" x $1 . " $&"/ge;

  # Page code and every tag except closing tags of block elements
  # (see ../readable/zalgo.sh).
  s#<m.*?j">|<(?!/[dfhlpt]).*?>##gs;
  s/(<.*?>\s*)+/\n/g;

  # "Chapter 1\n# Introduction" -> "# Chapter 1: Introduction". The line
  # before a "# " heading only ends in a digit for chapter titles; the other
  # h1s ("Disclaimer", "Warning") are left alone. "." does not match newlines,
  # so (.+\d) is exactly the "Chapter N" line.
  s/(.+\d)\n# /# $1: /g;

  # Entities. Done after the tags are gone, so a decoded "<" cannot start a
  # tag that the patterns above would remove.
  s/&lt;/</g;
  s/&amp;/&/g;

  # Every character except "#" and newline gets rand($i >> 17) marks, where
  # $i counts the characters so far: the ceiling goes up by one every 131072
  # characters ("1 .. 2.7" is 1, 2). rand is a named unary operator, which
  # binds more loosely than >>, so the golfed "rand$i++>>17" needs no
  # brackets. Skipping newlines keeps marks from landing at the start of a
  # heading line.
  # The marks come from U+0300..U+0362 (768 + rand 99, truncated): the whole
  # Combining Diacritical Marks block except its last 13 code points, the
  # superscript Latin letters U+0363..U+036F. Leaving those out saved the
  # byte that pays for curl -f.
  s/[^#\n]/$&.pack "U*", map { 768 + rand 99 } 1 .. rand($i++ >> 17)/ge;
'
