#!/bin/sh
# Readable version of ../zalgoplusplus.sh (234 characters).
#
# Like ../zalgo.sh, plus:
#   - Markdown headings: "#" before chapter titles, "##" before sections,
#     "###" before subsections. The hashes get no marks, so the headings
#     still render as Markdown.
#   - &lt; and &amp; are decoded.
#   - Rising corruption ("It comes"): instead of ord % 8 marks per character,
#     each character gets a random number of marks between 0 and a ceiling
#     that grows with every character printed. Chapter 1 starts clean; by the
#     end of chapter 24 the ceiling is about 18.
#
# Run it with sh: in zsh the unquoted [1-24] in the golfed version is taken
# as a glob and fails with "no matches found".

curl -L 'unicode.org/versions/latest/core-spec/chapter-[1-24]' | perl -CS -0pe '
  # Before <h1>, <h2>, <h3>: one "#" per heading level and a space.
  s/<h(\d)/"#" x $1 . " $&"/ge;

  # Page code and every tag except closing tags of block elements
  # (see ../readable/zalgo.sh).
  s#<m.*?j">|<(?!/[dfhlpt]).*?>##gs;
  s/(<.*?>\s*)+/\n/g;

  # Entities. Done after the tags are gone, so a decoded "<" cannot start a
  # tag that the patterns above would remove.
  s/&lt;/</g;
  s/&amp;/&/g;

  # Every character except "#" and newline gets rand($i * 8e-6) marks, where
  # $i counts the characters so far ("1 .. 2.7" is 1, 2). Skipping newlines
  # keeps marks from landing at the start of a heading line.
  s/[^#\n]/$&.pack "U*", map { 768 + rand 112 } 1 .. rand($i++ * 8e-6)/ge;
'
